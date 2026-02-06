# Quick Start Guide

Get the AI Lung Cancer Detection System up and running in minutes!

## Prerequisites Check

Make sure you have Python 3.8+ installed:
```bash
python --version
```

## Step 1: Install Dependencies

```bash
# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
cd backend
pip install -r requirements.txt
```

## Step 2: Start the Server

**Option A: Using the startup script**
```bash
# Windows
start_server.bat

# Linux/Mac
chmod +x start_server.sh
./start_server.sh
```

**Option B: Manual start**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Step 3: Access the Application

### Web Interface (Recommended)
1. Open `frontend/index.html` in your web browser
2. Upload a CT scan image
3. View results with heatmap visualization

### API Documentation
Visit: http://localhost:8000/docs

### Test the API
```bash
# Test health endpoint
python test_api.py

# Test with an image
python test_api.py path/to/your/ct_scan.jpg
```

## Step 4: Using the System

1. **Upload Image**: Use the web interface or API
2. **Get Results**: 
   - Prediction (Normal/Benign/Malignant)
   - Confidence percentage
   - Heatmap showing detected areas
3. **Review**: Check the heatmap to see where abnormalities were detected

## Troubleshooting

**Port already in use?**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

**Import errors?**
```bash
pip install -r backend/requirements.txt
```

**Model loading issues?**
- The system uses pretrained EfficientNet-B0
- No additional model files needed for basic operation
- Custom models can be added later

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check API docs at http://localhost:8000/docs
- Customize the model or interface as needed

---

**Ready to assist doctors in lung cancer detection! 🫁**
