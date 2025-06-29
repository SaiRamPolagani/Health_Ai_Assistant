from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Configure Gemini API key
api_key = os.environ.get('API_KEY')
if not api_key:
    raise ValueError("API_KEY not found in environment variables")

genai.configure(api_key=api_key)


# Gemini AI Wrapper Class
class GeminiAI:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash') 
        except Exception as e:
            print("Error initializing Gemini model:", e)

        # Prompts
        self.prediction_prompt = """You are a medical assistant. Given the symptoms, respond with:
- 3 to 5 possible conditions in bullet points
- 2 to 3 home remedies in bullet points
- Keep the response short and to the point
- Avoid long paragraphs or detailed medical explanations
- Always include a short disclaimer at the end encouraging users to consult a healthcare professional."""

        self.chat_prompt = """You are a helpful healthcare assistant. Provide clear, brief, and empathetic responses to health-related questions. Always remind users to consult healthcare professionals for serious issues."""

        self.treatment_prompt = """For the given condition, provide concise treatment steps, lifestyle tips, and precautions. Limit to 3–5 bullet points each. Always recommend seeing a doctor for personalized care."""

    def get_chat_response(self, message):
        try:
            chat = self.model.start_chat(history=[])
            response = chat.send_message(f"{self.chat_prompt}\nUser: {message}")
            return response.text
        except Exception as e:
            print("Gemini API Chat Error:", e)
            return f"Error processing request: {str(e)}"

    def predict_disease(self, symptoms):
        try:
            print(f"Sending symptoms to Gemini: {symptoms}")
            response = self.model.generate_content(
                f"{self.prediction_prompt}\nSymptoms: {symptoms}"
            )
            print("Gemini response:", response.text)
            return {
                "predicted_disease": response.text,
                "confidence": 0.85,  # Placeholder confidence
                "recommendations": "Please consult a healthcare professional for accurate diagnosis"
            }
        except Exception as e:
            print("Gemini API Prediction Error:", e)
            return {
                "error": str(e),
                "recommendations": "Error processing request. Please try again."
            }

    def generate_treatment_plan(self, condition):
        try:
            print(f"Generating treatment for: {condition}")
            response = self.model.generate_content(
                f"{self.treatment_prompt}\nCondition: {condition}"
            )
            return {
                "condition": condition,
                "treatment": response.text,
                "medications": ["Please consult a healthcare provider for medication advice"],
                "lifestyle_changes": [
                    "Follow general health guidelines",
                    "Maintain a balanced diet",
                    "Regular exercise as appropriate",
                    "Adequate rest and sleep"
                ]
            }
        except Exception as e:
            print("Gemini API Treatment Error:", e)
            return {
                "error": str(e),
                "message": "Error generating treatment plan"
            }
ai_model = GeminiAI()
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def process_chat():
    data = request.get_json()
    user_message = data.get('message')
    response = ai_model.get_chat_response(user_message)
    return jsonify({'response': response})


@app.route('/api/predict', methods=['POST'])
def process_prediction():
    data = request.get_json()
    symptoms = data.get('symptoms')
    prediction = ai_model.predict_disease(symptoms)
    return jsonify({'prediction': prediction})


@app.route('/api/treatment', methods=['POST'])
def process_treatment():
    data = request.get_json()
    condition = data.get('condition')
    treatment_plan = ai_model.generate_treatment_plan(condition)
    return jsonify({'treatment_plan': treatment_plan})


# ------------------ Start App ------------------

if __name__ == '__main__':
    app.run(debug=True)
