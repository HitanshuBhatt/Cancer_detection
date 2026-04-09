from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from app.api.prediction_routes import router
from database import get_db_connection

# 1. Initialize the app ONLY ONCE
app = FastAPI()

# 2. Setup CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# 3. Include your external routes
app.include_router(router)

# 4. Basic Root Route
@app.get("/")
def home():
    return {"message": "Lung Cancer Detection API Running"}

@app.get("/patients")
async def get_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        cursor.close()
        conn.close()
        return patients
    except Exception as e:
        return {"error": str(e)}, 500

# NEW: Route to fetch data specifically from the appointments table
@app.get("/get-appointments")
async def get_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # This query joins the tables to get the actual names
        query = """
        SELECT 
            a.appointment_id, 
            p.first_name, 
            p.last_name, 
            a.appointment_time, 
            a.reason, 
            a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        ORDER BY a.appointment_time DESC
        """
        
        cursor.execute(query)
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        return appointments
    except Exception as e:
        print(f"❌ Fetch Error: {e}")
        return {"error": str(e)}, 500
    
@app.post("/add-appointment")
async def add_appointment(
    patient_id: int = Form(...), 
    doctor_id: int = Form(...),  
    appt_date: str = Form(...),
    appt_time: str = Form(...),
    reason: str = Form(...)
):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ensure format is YYYY-MM-DD HH:MM:SS for MySQL DATETIME
        full_datetime = f"{appt_date} {appt_time}:00" 
        
        query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_time, reason, status)
        VALUES (%s, %s, %s, %s, 'Confirmed')
        """
        values = (patient_id, doctor_id, full_datetime, reason)
        
        cursor.execute(query, values)
        
        # CRITICAL: Force MySQL to save the changes
        conn.commit() 
        
        # Verify if a row was actually affected
        if cursor.rowcount == 0:
            raise Exception("No rows were inserted into the database.")

        return {"message": "Success"}
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return {"error": str(e)}, 500
    finally:
        if conn:
            cursor.close()
            conn.close()


@app.post("/add-patient")
async def add_patient(
    first_name: str = Form(...),
    last_name: str = Form(...),
    dob: str = Form(...),
    cancer_type: str = Form(...)
):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # We OMIT patient_id here because MySQL handles it automatically
        query = """
        INSERT INTO patients (first_name, last_name, dob, cancer_type)
        VALUES (%s, %s, %s, %s)
        """
        values = (first_name, last_name, dob, cancer_type)
        
        cursor.execute(query, values)
        conn.commit()  # Saves the new patient to the database
        
        return {"message": "Patient registered successfully"}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}, 500
    finally:
        if conn:
            cursor.close()
            conn.close()