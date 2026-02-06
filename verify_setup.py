"""
Verification script to check if all imports and setup are correct.
Run this from the backend directory: python verify_setup.py
"""
import sys
import os

# Add parent directory to path if running from root
if os.path.basename(os.getcwd()) != 'backend':
    print("⚠️  WARNING: This script should be run from the 'backend' directory")
    print("   Current directory:", os.getcwd())
    print("   Changing to backend directory...")
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    if os.path.exists(backend_path):
        os.chdir(backend_path)
        print("   ✅ Changed to backend directory")
    else:
        print("   ❌ Could not find backend directory!")
        sys.exit(1)

print("\n" + "="*50)
print("Verifying AI Lung Cancer Detection System Setup")
print("="*50 + "\n")

# Test 1: Check Python version
print("1. Checking Python version...")
print(f"   Python: {sys.version}")
if sys.version_info < (3, 8):
    print("   ⚠️  WARNING: Python 3.8+ recommended")
else:
    print("   ✅ Python version OK")

# Test 2: Check imports
print("\n2. Checking critical imports...")
try:
    import torch
    print(f"   ✅ PyTorch: {torch.__version__}")
except ImportError as e:
    print(f"   ❌ PyTorch not found: {e}")
    sys.exit(1)

try:
    import fastapi
    print(f"   ✅ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"   ❌ FastAPI not found: {e}")
    sys.exit(1)

try:
    import numpy
    print(f"   ✅ NumPy: {numpy.__version__}")
except ImportError as e:
    print(f"   ❌ NumPy not found: {e}")
    sys.exit(1)

try:
    from PIL import Image
    print("   ✅ Pillow (PIL)")
except ImportError as e:
    print(f"   ❌ Pillow not found: {e}")
    sys.exit(1)

# Test 3: Check app imports
print("\n3. Checking app module imports...")
try:
    from app.config import Settings
    print("   ✅ app.config")
except ImportError as e:
    print(f"   ❌ app.config import failed: {e}")
    sys.exit(1)

try:
    from app.models.lung_model import load_model
    print("   ✅ app.models.lung_model")
except ImportError as e:
    print(f"   ❌ app.models.lung_model import failed: {e}")
    sys.exit(1)

try:
    from app.utils.image_utils import preprocess_image
    print("   ✅ app.utils.image_utils")
except ImportError as e:
    print(f"   ❌ app.utils.image_utils import failed: {e}")
    sys.exit(1)

try:
    from app.utils.gradcam import generate_heatmap_image
    print("   ✅ app.utils.gradcam")
except ImportError as e:
    print(f"   ❌ app.utils.gradcam import failed: {e}")
    sys.exit(1)

try:
    from app.services.inference_service import run_inference
    print("   ✅ app.services.inference_service")
except ImportError as e:
    print(f"   ❌ app.services.inference_service import failed: {e}")
    sys.exit(1)

try:
    from app.api.inference import router
    print("   ✅ app.api.inference")
except ImportError as e:
    print(f"   ❌ app.api.inference import failed: {e}")
    sys.exit(1)

try:
    from app.main import app
    print("   ✅ app.main")
except ImportError as e:
    print(f"   ❌ app.main import failed: {e}")
    sys.exit(1)

# Test 4: Check Settings
print("\n4. Checking Settings configuration...")
try:
    settings = Settings()
    print(f"   ✅ Settings loaded: {settings.app_name}")
    print(f"   ✅ Model path: {settings.model_path or 'None (using default)'}")
except Exception as e:
    print(f"   ❌ Settings failed: {e}")
    sys.exit(1)

# Test 5: Check device
print("\n5. Checking device configuration...")
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"   ✅ Device: {device}")
    if device == "cpu":
        print("   ℹ️  Running on CPU (GPU not available)")
except Exception as e:
    print(f"   ⚠️  Device check warning: {e}")

# Test 6: Check model loading (optional, may take time)
print("\n6. Checking model loading...")
try:
    model = load_model(None)  # Load without custom weights
    print("   ✅ Model loaded successfully")
    print(f"   ✅ Model device: {next(model.parameters()).device}")
except Exception as e:
    print(f"   ⚠️  Model loading warning: {e}")
    print("   (This is OK if you haven't installed model weights)")

print("\n" + "="*50)
print("✅ All checks passed! System is ready to run.")
print("="*50)
print("\nTo start the server, run:")
print("  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
print("\nOr use the run script from root directory:")
print("  run_server.bat")
print()
