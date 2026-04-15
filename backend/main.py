from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.prediction_routes import router
from pydantic import BaseModel, EmailStr
import aiomysql
import hashlib 
import mysql.connector 
from typing import Optional

# 1. Initialize the app
app = FastAPI()

# 2. Setup CORS Middleware - Use wildcard to prevent Chrome blocking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Root@123", 
    "database": "LungCancer" 
}

def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Lung Cancer Detection API Running"}

# --- AUTH MODELS & ROUTES ---
class UserSignup(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    dob: str
    address: str

@app.post("/signup")
async def register_doctor(user: UserSignup):
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    conn = await aiomysql.connect(**DB_CONFIG, db=DB_CONFIG["database"])
    async with conn.cursor() as cur:
        try:
            sql = "INSERT INTO users (full_name, email, password_hash, role, dob, address) VALUES (%s, %s, %s, 'Doctor', %s, %s)"
            await cur.execute(sql, (user.full_name, user.email, hashed_pw, user.dob, user.address))
            await conn.commit()
            return {"message": "Doctor registered successfully"}
        finally:
            conn.close()

# --- BOOKING LOGIC WITH AVAILABILITY CHECK ---
from typing import Optional

class PublicBooking(BaseModel):
    email: str
    appointment_time: str
    reason: Optional[str] = None

from datetime import datetime

@app.post("/public-book-appointment")
async def public_book_appointment(data: PublicBooking):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        appointment_time = datetime.fromisoformat(data.appointment_time)

        # 1. Check patient exists
        cursor.execute("SELECT patient_id FROM patients WHERE email = %s", (data.email,))
        patient = cursor.fetchone()

        if not patient:
            raise HTTPException(
                status_code=400,
                detail="Patient does not exist. Please sign up first."
            )

        patient_id = patient["patient_id"]

        # 2. Get doctor
        cursor.execute("SELECT user_id FROM users WHERE role = 'Doctor' LIMIT 1")
        doctor = cursor.fetchone()

        if not doctor:
            raise HTTPException(status_code=500, detail="No doctor found")

        doctor_id = doctor["user_id"]

        # 3. Check availability (clean version)
        cursor.execute("""
            SELECT appointment_id 
            FROM appointments 
            WHERE appointment_time = %s AND doctor_id = %s
        """, (appointment_time, doctor_id))

        existing = cursor.fetchone()

        if existing:
            raise HTTPException(status_code=400, detail="Time slot already booked")

        # 4. Insert appointment
        cursor.execute("""
            INSERT INTO appointments 
            (patient_id, doctor_id, appointment_time, reason, status)
            VALUES (%s, %s, %s, %s, 'Pending')
        """, (
            patient_id,
            doctor_id,
            appointment_time,
            data.reason
        ))

        conn.commit()

        return {"message": "Appointment booked successfully"}

    except mysql.connector.Error as db_error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"MySQL Error: {str(db_error)}")

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    dob: str
    email: str
    phone: str

@app.post("/create-patient")
async def create_patient(data: PatientCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM patients WHERE email = %s", (data.email,))
        if cursor.fetchone():
            return {"message": "Patient already exists"}

        cursor.execute("""
            INSERT INTO patients (first_name, last_name, dob, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """, (data.first_name, data.last_name, data.dob, data.email, data.phone))

        conn.commit()
        return {"message": "Patient created successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

        # --- DATA RETRIEVAL ROUTES ---
@app.get("/get-appointments")
async def get_appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT a.*, p.first_name, p.last_name FROM appointments a JOIN patients p ON a.patient_id = p.patient_id")
    res = cursor.fetchall()
    conn.close()
    return res