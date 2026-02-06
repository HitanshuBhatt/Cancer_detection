# AI Lung Cancer Detection System

An AI-powered system to assist doctors in detecting lung cancer from CT scan images. The system provides:

- **Automated Detection**: Classifies CT scans as Normal, Benign, or Malignant
- **Heatmap Visualization**: Shows exactly where the AI detected potential abnormalities
- **Probability Scores**: Provides confidence percentages for all predictions
- **Doctor-Friendly Interface**: Clean, intuitive web interface for medical professionals

## Features

### 🎯 Core Capabilities
- **Deep Learning Model**: Uses EfficientNet-B0 for accurate lung cancer detection
- **Grad-CAM Heatmaps**: Visual attention maps showing where the model focuses
- **Confidence Scoring**: Percentage-based probability scores (0-100%)
- **Multi-Class Classification**: Distinguishes between Normal, Benign, and Malignant cases
- **RESTful API**: FastAPI backend for easy integration
- **Modern Web Interface**: Responsive frontend for easy image upload and result visualization

### 📊 Output Information
- **Prediction**: Normal / Benign / Malignant classification
- **Confidence Score**: Overall model confidence (0-100%)
- **Class Probabilities**: Detailed breakdown for all three classes
- **Heatmap Image**: Visual representation of detected abnormalities

## Project Structure

```
ai_lung/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── health.py          # Health check endpoint
│   │   │   └── inference.py       # Main prediction endpoint
│   │   ├── models/
│   │   │   └── lung_model.py      # Deep learning model definition
│   │   ├── services/
│   │   │   └── inference_service.py  # Inference logic
│   │   ├── utils/
│   │   │   ├── image_utils.py     # Image preprocessing
│   │   │   └── gradcam.py         # Heatmap generation (Grad-CAM)
│   │   ├── schemas/
│   │   │   └── inference.py       # API response schemas
│   │   ├── config.py              # Configuration
│   │   ├── main.py                # FastAPI application
│   │   └── logging_config.py      # Logging setup
│   └── requirements.txt
├── frontend/
│   └── index.html                 # Web interface for doctors
└── README.md
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd ai_lung
   ```

2. **Create and activate virtual environment** (if not already created)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
   ```

## Running the Application

### Start the Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Access the Frontend

1. Open `frontend/index.html` in a web browser
2. Or serve it using a simple HTTP server:
   ```bash
   # Python 3
   cd frontend
   python -m http.server 8080
   ```
   Then open http://localhost:8080 in your browser

## Usage

### Using the Web Interface

1. **Open the frontend** (`frontend/index.html`)
2. **Upload a CT scan image**:
   - Click "Choose File" or drag and drop an image
   - Supported formats: PNG, JPEG, JPG
3. **View Results**:
   - Prediction (Normal/Benign/Malignant)
   - Confidence percentage score
   - Detailed probability breakdown
   - Heatmap visualization showing detected areas

### Using the API Directly

#### Example: Python Request

```python
import requests

url = "http://localhost:8000/inference/predict"
files = {"file": open("ct_scan.jpg", "rb")}
params = {"generate_heatmap": True}

response = requests.post(url, files=files, params=params)
result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['probability_score']:.2f}%")
print(f"Probabilities: {result['probabilities']}")
```

#### Example: cURL Request

```bash
curl -X POST "http://localhost:8000/inference/predict?generate_heatmap=true" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@ct_scan.jpg"
```

### API Response Format

```json
{
  "prediction": "malignant",
  "confidence": 0.95,
  "probability_score": 95.0,
  "probabilities": {
    "normal": 2.5,
    "benign": 2.5,
    "malignant": 95.0
  },
  "heatmap_image": "base64_encoded_image_string",
  "message": "lung-cancer-detection-v1"
}
```

## Model Details

### Architecture
- **Base Model**: EfficientNet-B0 (pretrained on ImageNet)
- **Task**: 3-class classification (Normal, Benign, Malignant)
- **Input Size**: 224x224 pixels
- **Output**: Softmax probabilities for each class

### Heatmap Generation
- **Method**: Grad-CAM (Gradient-weighted Class Activation Mapping)
- **Purpose**: Visualize which regions of the CT scan the model focuses on
- **Output**: Overlaid heatmap showing attention regions in red/yellow

## Important Notes

### Medical Disclaimer
⚠️ **This system is for research and assistance purposes only.**
- The AI model provides predictions, not definitive diagnoses
- Always consult with qualified medical professionals
- This tool is designed to assist, not replace, medical judgment
- Results should be verified through proper medical procedures

### Model Training
- The current model uses pretrained EfficientNet-B0 weights
- For production use, the model should be fine-tuned on a medical dataset
- To use a custom trained model, place the weights file and update `model_path` in `config.py`

## Development

### Adding Custom Model Weights

1. Train or obtain a model checkpoint file (`.pth` format)
2. Place it in a `models/` directory
3. Update `backend/app/config.py`:
   ```python
   model_path: str = "models/your_model.pth"
   ```

### Extending Functionality

- **New endpoints**: Add to `backend/app/api/`
- **Model improvements**: Modify `backend/app/models/lung_model.py`
- **UI enhancements**: Edit `frontend/index.html`

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **CORS errors**: The backend is configured to allow all origins. For production, update CORS settings in `main.py`

3. **Model loading errors**: If using custom weights, ensure the model architecture matches

4. **Heatmap generation fails**: Check that OpenCV and matplotlib are properly installed

## Technology Stack

- **Backend**: FastAPI, PyTorch, Torchvision
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **ML Framework**: PyTorch
- **Image Processing**: PIL/Pillow, OpenCV, NumPy
- **Visualization**: Matplotlib, Grad-CAM

## License

This project is for educational and research purposes. Please ensure compliance with medical software regulations in your jurisdiction.

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Medical accuracy is maintained
- Proper testing is performed
- Documentation is updated

## Support

For issues or questions, please check:
- API documentation: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health

---

**Built with ❤️ to assist medical professionals in early lung cancer detection**
"# Cancer_detection" 
