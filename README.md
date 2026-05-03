# MediCare — AI-Powered Lung Cancer Detection & Clinic Management System

A full-stack medical AI application that classifies lung CT scan images into four diagnostic categories using a fine-tuned EfficientNet-B0 deep learning model. The system exposes a FastAPI backend with a patient management portal, appointment booking workflow, and a doctor-facing dashboard built in plain HTML/CSS/JavaScript.

---

## Description

MediCare is a clinical decision-support tool designed to assist doctors in preliminary lung cancer screening. Radiologists and pulmonologists upload CT scan images through a web interface; the system runs inference through a trained PyTorch model and returns a predicted diagnosis with a confidence score in real time.

Beyond AI inference, the application functions as a lightweight clinic management system: patients can self-register and book appointments online, while authenticated doctors access a dashboard showing today's schedule, total patient load, and an appointment frequency chart by weekday.

The project solves a realistic problem in under-resourced healthcare settings: providing fast, automated image analysis without requiring specialized radiology software.

---

## Features

**AI Inference**
- EfficientNet-B0 model fine-tuned on a 4-class lung CT dataset (adenocarcinoma, large cell carcinoma, squamous cell carcinoma, normal)
- Returns predicted class label and softmax confidence percentage per request
- Model loaded once at server startup; inference runs on CPU by default with GPU support when available

**Patient Portal (Public)**
- Patient self-registration (first name, last name, date of birth, email, phone)
- Appointment booking by email — validates that the patient exists before inserting a record
- Conflict detection: rejects double-booking the same doctor at the same time slot

**Doctor Dashboard (Authenticated)**
- Secure login with SHA-256 password hashing
- Stat cards: today's appointments, total appointments, upcoming appointments
- Expandable table showing scheduled patients for the current day with reschedule/cancel actions
- Weekday bar chart built from live appointment data
- Doctor schedule panel and quick-access navigation

**Appointments Management**
- Full CRUD interface for appointments (create via form, read as cards)
- Patient dropdown populated dynamically from the database
- Status tags (Confirmed, Pending) on each appointment card

**Patient Records**
- Patient registration form with medical conditions, gender, and address fields
- Live search/filter on the patient table (client-side)
- Age calculation from date of birth on render
- Clickable rows for future patient detail views

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Framework | PyTorch 2.5.1, TorchVision 0.20.1 |
| Model Architecture | EfficientNet-B0 (pretrained ImageNet, fine-tuned) |
| Image Processing | Pillow 11.0, OpenCV 4.10 |
| Backend API | FastAPI 0.115, Uvicorn 0.32 |
| Database | MySQL (via `mysql-connector-python`, `aiomysql`) |
| Data Validation | Pydantic v2 |
| Frontend | HTML5, CSS3, Vanilla JavaScript (Fetch API) |
| Training Utilities | NumPy, SciPy, scikit-image, Matplotlib |

---

## Architecture

```
Cancer_detection/
├── backend/
│   ├── main.py                        # FastAPI app, CORS, all HTTP routes
│   ├── database.py                    # MySQL connection helper
│   └── app/
│       ├── api/
│       │   └── prediction_routes.py   # POST /predict-lung-cancer
│       ├── ml/
│       │   └── model_loader.py        # EfficientNet-B0 loader
│       └── services/
│           └── lung_prediction_service.py  # Inference logic
├── frontend/
│   ├── index.html / index.css         # Public landing page
│   ├── book_appointments.html/css     # Patient signup + booking
│   ├── login.html/css/js              # Doctor authentication
│   ├── home.html / home.js            # Doctor dashboard
│   ├── patients.html / patients.js    # Patient records + registration
│   ├── appointments.html/js           # Appointment management
│   ├── detection.html/css/js          # AI scan upload + result
│   └── style.css / appointment.css    # Shared component styles
└── training/
    ├── train.py                       # Full training pipeline
    └── lung_model.py                  # Prototype training script
```

**Request flow for AI inference:**

1. User uploads a CT image via `detection.html`
2. JavaScript POSTs the file as `multipart/form-data` to `/predict-lung-cancer`
3. `prediction_routes.py` delegates to `lung_prediction_service.py`
4. The service opens the image with Pillow, applies the ImageNet normalization transform, runs a forward pass through the frozen EfficientNet-B0 model, and applies `torch.softmax`
5. The predicted class index and confidence are returned as JSON
6. The frontend renders the label and confidence inline

**Database schema (inferred from queries):**
- `users` — doctor accounts (user_id, full_name, email, password_hash, role, dob, address)
- `patients` — patient records (patient_id, first_name, last_name, dob, email, phone, gender, address, medical_conditions)
- `appointments` — bookings (appointment_id, patient_id, doctor_id, appointment_time, reason, status)

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Node.js not required (frontend is plain HTML/JS)

### 1. Clone the repository

```bash
git clone https://github.com/HitanshuBhatt/Cancer_detection.git
cd Cancer_detection
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure the database

Create a MySQL database named `LungCancer` and run your schema migrations. Update the credentials in `backend/main.py` and `backend/database.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "your_user",
    "password": "your_password",
    "database": "LungCancer"
}
```

### 5. Add the trained model

Place the trained weights file at:

```
backend/models/lung_cancer_model.pth
```

To train from scratch using your own dataset:

```bash
# Expects: Datasets/train/<class_folder>/ and Datasets/validation/<class_folder>/
python training/train.py
```

### 6. Start the backend server

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 7. Open the frontend

Open `frontend/index.html` directly in a browser, or serve with any static file server:

```bash
cd frontend
python -m http.server 5500
```

---

## Usage

**Patient workflow:**
1. Navigate to `book_appointments.html`
2. Complete the Patient Signup form to register in the system
3. Use the Book Appointment form with your registered email to schedule a visit

**Doctor workflow:**
1. Navigate to `login.html` and sign in with doctor credentials
2. The dashboard (`home.html`) loads appointment statistics automatically
3. Click the Today's Appointments card to expand the schedule table
4. Navigate to `appointments.html` to add or review all appointments
5. Navigate to `patients.html` to register new patients or search records
6. Navigate to `detection.html` to upload a lung CT scan and run AI inference

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/signup` | Register a new doctor account |
| POST | `/login` | Authenticate a doctor (returns name) |
| POST | `/create-patient` | Register a new patient (public) |
| POST | `/register-patient` | Register a patient with full details (doctor portal) |
| POST | `/public-book-appointment` | Book an appointment by patient email |
| POST | `/add-appointment` | Add an appointment via doctor portal |
| GET | `/get-appointments` | Retrieve all appointments with patient names |
| GET | `/patients` | Retrieve all patient records |
| POST | `/predict-lung-cancer` | Upload CT scan image, returns prediction + confidence |

**Example inference response:**

```json
{
  "prediction": "adenocarcinoma",
  "confidence": 94.37
}
```

---

## Model Training

The training pipeline in `training/train.py` uses transfer learning:

- Base model: EfficientNet-B0 with pretrained ImageNet weights
- Final classifier layer replaced with `nn.Linear(in_features, 4)`
- Optimizer: Adam, learning rate 0.001
- Augmentation: random horizontal flip, random 10-degree rotation
- Normalization: ImageNet mean/std (`[0.485, 0.456, 0.406]`, `[0.229, 0.224, 0.225]`)
- Training epochs: 20
- Batch size: 16
- Device: CUDA if available, CPU fallback

The four output classes map to dataset folders loaded via `torchvision.datasets.ImageFolder`:
`adenocarcinoma`, `large_cell_carcinoma`, `normal`, `squamous_cell_carcinoma`

---

## Learning Outcomes

- Implementing transfer learning with EfficientNet-B0 for a multi-class medical imaging task
- Structuring a FastAPI application with a service layer, separated route handlers, and a singleton model loader pattern
- Handling multipart file uploads asynchronously in FastAPI
- Building a full patient management system with role-based access (doctor vs. patient) backed by MySQL
- Connecting a vanilla JavaScript frontend to a Python REST API using the Fetch API and FormData
- Managing CORS configuration for local development
- Applying ImageNet normalization to custom domain images for inference consistency

---

## Future Improvements

- **Security:** Replace SHA-256 password hashing with bcrypt; implement JWT-based authentication with token expiration; move database credentials to environment variables or a secrets manager
- **Deployment:** Containerize with Docker and add a docker-compose file for the API and MySQL service; add Nginx as a reverse proxy
- **Model improvements:** Add Grad-CAM visualization to highlight regions influencing the prediction; evaluate model on a held-out test set and report precision/recall per class
- **Database:** Migrate to PostgreSQL; add SQLAlchemy ORM with Alembic migrations to replace raw SQL queries
- **Frontend:** Migrate to a React or Vue frontend for component reusability and state management; add loading skeletons and toast notifications
- **Testing:** Add pytest unit tests for service functions and FastAPI integration tests using `httpx.AsyncClient`
- **CI/CD:** Add GitHub Actions workflow for linting, testing, and Docker image builds on push
- **Appointment system:** Add email notification on booking confirmation; implement calendar view for doctor schedule

---

## License

MediCare was developed as a capstone project. Not licensed for clinical or production medical use.
