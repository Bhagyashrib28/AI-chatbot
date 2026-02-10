import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import database

load_dotenv()

app = Flask(__name__)

# Initialize Gemini Client (Free Tier)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# print("API KEY:", os.getenv("GEMINI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"response": "I didn't catch that. Try typing something!"}), 400

    try:
        # Generate content using Gemini 1.5 Flash
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=user_message
        )
        bot_response = response.text
        
        # Save the interaction to SQLite
        database.log_interaction(user_message, bot_response)
        
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"response": f"Sorry, I'm having trouble connecting. Error: {str(e)}"}), 500

if __name__ == "__main__":
    database.init_db()  # Initialize DB on startup
    app.run(debug=True)



