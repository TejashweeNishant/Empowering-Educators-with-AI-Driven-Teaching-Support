import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import json

# Get the directory containing this file
current_dir = Path(__file__).parent

# Load environment variables from .env file in the backend directory
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

# Configure the API
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(api_key=API_KEY)

# Sample educational resources database
EDUCATION_RESOURCES = [
    {
        "title": "Workshop: Digital Pedagogy for Modern Classrooms",
        "type": "Workshop",
        "description": "Learn how to effectively integrate technology into your teaching practice with hands-on activities and real-world examples.",
        "link": "https://example.com/digital-pedagogy"
    },
    {
        "title": "Tool: Nearpod",
        "type": "EdTech Tool",
        "description": "Interactive lessons, videos, and activities to engage students in any learning environment.",
        "link": "https://nearpod.com"
    },
    {
        "title": "Strategy: Think-Pair-Share",
        "type": "Teaching Strategy",
        "description": "A collaborative learning strategy that encourages student participation through structured discussion.",
        "link": "https://example.com/think-pair-share"
    },
    {
        "title": "Workshop: Flipped Classroom Techniques",
        "type": "Workshop",
        "description": "Learn how to implement flipped classroom strategies to make the most of in-class time.",
        "link": "https://example.com/flipped-classroom"
    },
    {
        "title": "Tool: Kahoot!",
        "type": "EdTech Tool",
        "description": "Game-based learning platform that makes it easy to create, share and play learning games or trivia quizzes.",
        "link": "https://kahoot.com"
    }
]

class EducatorAIAgent:
    def __init__(self):
        # Initialize the model - using gemini-2.5-flash which is available
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Define the prompt template
        self.prompt_template = """
        You are an AI teaching assistant helping educators improve their teaching methods and find resources.
        
        User's question: {user_input}
        
        Based on the user's question, provide:
        1. A brief, helpful insight or advice (2-3 sentences)
        2. 3-5 specific resource recommendations from the available resources
        
        Format your response as a JSON object with the following structure:
        {{
            "insight": "Your teaching insight here...",
            "recommendations": [
                {{
                    "title": "Resource Title",
                    "type": "Resource Type",
                    "description": "Brief description of the resource",
                    "link": "URL or reference to the resource"
                }}
            ]
        }}
        
        Available resources:
        {resources}
        
        Response:
        """
    
    def get_recommendations(self, user_input):
        try:
            # Format the resources as a string for the prompt
            resources_str = "\n".join([
                f"- {r['title']} ({r['type']}): {r['description']}"
                for r in EDUCATION_RESOURCES
            ])
            
            # Format the prompt
            prompt = self.prompt_template.format(
                user_input=user_input,
                resources=resources_str
            )
            
            # Get response from the model
            response = self.model.generate_content(prompt)
            
            # Parse the response
            try:
                # Extract text from response
                response_text = response.text.strip()
                
                # Clean the response to ensure it's valid JSON
                if '```json' in response_text:
                    # Extract JSON from markdown code block
                    json_str = response_text.split('```json')[1].split('```')[0].strip()
                else:
                    # Try to find JSON in the response
                    json_str = response_text[response_text.find('{'):response_text.rfind('}')+1]
                
                result = json.loads(json_str)
                return result
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Response was: {response}")
                # Return a fallback response
                return {
                    "insight": "I've analyzed your request and have some recommendations for you.",
                    "recommendations": [
                        {
                            "title": "Workshop: Digital Pedagogy for Modern Classrooms",
                            "type": "Workshop",
                            "description": "Learn how to effectively integrate technology into your teaching practice.",
                            "link": "https://example.com/digital-pedagogy"
                        },
                        {
                            "title": "Tool: Nearpod",
                            "type": "EdTech Tool",
                            "description": "Interactive lessons, videos, and activities to engage students in any setting.",
                            "link": "https://nearpod.com"
                        }
                    ]
                }
                
        except Exception as e:
            print(f"Error getting recommendations: {str(e)}")
            return {
                "insight": "I'm having trouble processing your request right now. Please try again later.",
                "recommendations": []
            }

# Example usage
if __name__ == "__main__":
    agent = EducatorAIAgent()
    test_query = "How can I make my online classes more engaging?"
    result = agent.get_recommendations(test_query)
    print("Insight:", result["insight"])
    print("\nRecommendations:")
    for rec in result["recommendations"]:
        print(f"- {rec['title']} ({rec['type']}): {rec['description']}")
