from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_agent import EducatorAIAgent
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the directory containing this file
current_dir = Path(__file__).parent

# Load environment variables from .env file in the backend directory
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Initialize the AI agent
ai_agent = EducatorAIAgent()

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML file."""
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI response."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'No message provided',
                'status': 'error'
            }), 400
        
        # Get recommendations from the AI agent
        response = ai_agent.get_recommendations(user_message)
        
        return jsonify({
            'status': 'success',
            'insight': response.get('insight', 'Here are some recommendations for you.'),
            'recommendations': response.get('recommendations', [])
        })
        
    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while processing your request.'
        }), 500

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Educator AI API is running'
    })

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Check if running in production
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=debug)
