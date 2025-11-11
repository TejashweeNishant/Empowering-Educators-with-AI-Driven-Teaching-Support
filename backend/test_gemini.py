import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure the API
genai.configure(api_key=API_KEY)

def list_available_models():
    """List all available models."""
    try:
        models = genai.list_models()
        print("\nAvailable models:")
        for m in models:
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {str(e)}")

def test_gemini():
    try:
        # List available models first
        list_available_models()
        
        # Try with gemini-2.5-flash, if not available, use the default model
        model_name = 'gemini-2.5-flash'
        
        # Initialize the model
        print(f"\nAttempting to use model: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        # Generate content
        print("\nGenerating response...")
        response = model.generate_content("Explain how AI works in a few words")
        
        # Print the response
        print("\nResponse:")
        print(response.text)
        
    except Exception as e:
        print(f"\nError with model {model_name}: {str(e)}")
        print("\nTrying with default model...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Explain how AI works in a few words")
            print("\nResponse from default model (gemini-pro):")
            print(response.text)
        except Exception as e2:
            print(f"\nError with default model: {str(e2)}")

if __name__ == "__main__":
    test_gemini()
