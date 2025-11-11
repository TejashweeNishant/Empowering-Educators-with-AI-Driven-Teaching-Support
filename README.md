# Agentic AI Professional Development Coach for Educators

A web application that helps teachers and educators get personalized recommendations for improving teaching methods, adopting new technologies, and increasing student engagement.

## Features

- 💬 AI-powered chat interface for educational queries
- 🎯 Personalized teaching recommendations
- 📚 Resource library with workshops, tools, and strategies
- 🎨 Modern, responsive design

## Prerequisites

- Python 3.8+
- Node.js (for frontend development, optional)
- OpenAI API key

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd educator-ai
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the `backend` directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the backend server**
   ```bash
   python app.py
   ```
   The backend will start on `http://localhost:5000`

5. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or use a local development server (e.g., `python -m http.server 8000` in the frontend directory)

## Project Structure

```
educator-ai/
├── frontend/           # Frontend files
│   ├── index.html      # Main HTML file
│   ├── style.css       # Styles
│   └── script.js       # Frontend JavaScript
└── backend/            # Backend files
    ├── app.py          # Flask application
    ├── ai_agent.py     # AI agent implementation
    └── requirements.txt # Python dependencies
```

## Usage

1. Open the website in your browser
2. Type your teaching-related question in the chat box
3. Receive AI-powered recommendations and resources
4. Click on resource links to learn more

## Example Queries

- "How can I make my online classes more engaging?"
- "Suggest digital tools for interactive learning"
- "Recommend workshops for blended learning"
- "What are some strategies for classroom management?"

## License

This project is licensed under the MIT License.
