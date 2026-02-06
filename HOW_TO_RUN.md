# How to Run the AI Lung Cancer Detection System

## Quick Start (Easiest Method)

### Option 1: Use the Run Script (Recommended)
From the project root directory, simply run:
```bash
run_server.bat
```

This script automatically:
- Changes to the backend directory
- Starts the server with correct settings
- Shows helpful error messages if something goes wrong

### Option 2: Manual Start
1. **Activate virtual environment** (if not already active):
   ```bash
   venv\Scripts\activate
   ```

2. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

3. **Start the server**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Important Notes

⚠️ **You MUST run the uvicorn command from the `backend` directory!**

The error `ModuleNotFoundError: No module named 'app'` occurs when you try to run from the root directory because Python can't find the `app` module.

## Verify It's Working

Once the server starts, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Then you can:
- Access API docs: http://localhost:8000/docs
- Access health check: http://localhost:8000/health
- Open frontend: `frontend/index.html` in your browser

## Troubleshooting

### Error: "No module named 'app'"
**Solution**: Make sure you're in the `backend` directory when running uvicorn.

### Error: "Module not found" for dependencies
**Solution**: 
```bash
cd backend
pip install -r requirements.txt
```

### Port already in use
**Solution**: Use a different port:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## Project Structure

```
ai_lung/
├── backend/          ← You need to be HERE when running uvicorn
│   └── app/          ← The app module is here
│       ├── main.py
│       └── ...
├── frontend/
└── run_server.bat    ← Use this script from root
```
