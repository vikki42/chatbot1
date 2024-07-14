import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'Please enter a message'}), 400
    
    # Initialize Groq client with API key from environment variable
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    try:
        # Request completion from Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-70b-8192",
        )
        
        siri_response = chat_completion.choices[0].message.content
        return jsonify({'response': siri_response})

    except Exception as e:
        return jsonify({'error': f"Failed to fetch completion: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
