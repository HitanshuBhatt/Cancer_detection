"""
Simple test script to verify the API is working correctly.
Run this after starting the server to test the inference endpoint.
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_inference(image_path):
    """Test the inference endpoint with an image."""
    print(f"\nTesting inference endpoint with {image_path}...")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            params = {'generate_heatmap': True}
            response = requests.post(
                f"{API_URL}/inference/predict",
                files=files,
                params=params
            )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Inference successful!")
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print(f"Probability Score: {result['probability_score']:.2f}%")
            print(f"\nDetailed Probabilities:")
            for label, prob in result['probabilities'].items():
                print(f"  {label.capitalize()}: {prob:.2f}%")
            print(f"\nHeatmap generated: {'Yes' if result.get('heatmap_image') else 'No'}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except FileNotFoundError:
        print(f"❌ Image file not found: {image_path}")
        print("Please provide a valid image path.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("AI Lung Cancer Detection API Test")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("\n❌ Health check failed. Is the server running?")
        print("Start the server with: uvicorn app.main:app --reload")
        exit(1)
    
    # Test inference (requires an image file)
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_inference(image_path)
    else:
        print("\n⚠️  No image provided for inference test.")
        print("Usage: python test_api.py <path_to_image.jpg>")
        print("\nTo test inference, provide a CT scan image path.")
