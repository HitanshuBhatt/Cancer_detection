from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.prediction_routes import router
from pydantic import BaseModel, EmailStr
import aiomysql
import hashlib 
import mysql.connector 

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

# Configuration for your MySQL database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Root@123", # Replace with your actual password
    "database": "LungCancer" # mysql-connector uses 'database', aiomysql uses 'db'
}

# Synchronous connection helper for standard routes
def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

# 3. Include your external routes
app.include_router(router)

# 4. Basic Root Route
@app.get("/")
def home():
    return {"message": "Lung Cancer Detection API Running"}

# --- AUTH MODELS ---
class UserSignup(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    dob: str
    address: str

# --- ASYNCHRONOUS AUTH ROUTES ---

@app.post("/signup")
async def register_doctor(user: UserSignup):
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    
    # aiomysql uses 'db' instead of 'database'
    conn = await aiomysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["database"]
    )
    async with conn.cursor() as cur:
        try:
            sql = """INSERT INTO users (full_name, email, password_hash, role, dob, address) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            await cur.execute(sql, (user.full_name, user.email, hashed_pw, "Doctor", user.dob, user.address))
            await conn.commit()
            return {"message": "Doctor registered successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")
        finally:
            conn.close()

@app.post("/login")
async def doctor_login(credentials: dict):
    email = credentials.get("email")
    password = credentials.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing email or password")
        
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    conn = await aiomysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["database"]
    )
    async with conn.cursor(aiomysql.DictCursor) as cur:
        sql = "SELECT * FROM users WHERE email = %s AND password_hash = %s AND role = 'Doctor'"
        await cur.execute(sql, (email, hashed_pw))
        user = await cur.fetchone()
        conn.close()

        if user:
            return {"status": "success", "redirect": "/dashboard.html", "name": user['full_name']}
        else:
            raise HTTPException(status_code=401, detail="Invalid Doctor Credentials")

# --- SYNCHRONOUS DATA ROUTES ---

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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-appointments")
async def get_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT a.appointment_id, p.first_name, p.last_name, a.appointment_time, a.reason, a.status
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
        raise HTTPException(status_code=500, detail=str(e))
    
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
        full_datetime = f"{appt_date} {appt_time}:00" 
        
        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_time, reason, status) VALUES (%s, %s, %s, %s, 'Confirmed')"
        values = (patient_id, doctor_id, full_datetime, reason)
        
        cursor.execute(query, values)
        conn.commit() 
        return {"message": "Success"}
    except Exception as e:
        print(f"❌ DB Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
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
        query = "INSERT INTO patients (first_name, last_name, dob, cancer_type) VALUES (%s, %s, %s, %s)"
        values = (first_name, last_name, dob, cancer_type)
        cursor.execute(query, values)
        conn.commit() 
        return {"message": "Patient registered successfully"}
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()