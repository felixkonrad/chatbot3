from flask import render_template, request, jsonify
import requests
from . import create_app

app = create_app()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Send message to Rasa server
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    try:
        rasa_response = requests.post(
            'http://localhost:5005/webhooks/rest/webhook',
            json={"sender": "user", "message": message}
        )
        response_data = rasa_response.json()
        
        # Parse the Rasa responses
        response_messages = []
        for response in response_data:
            if "text" in response:
                response_messages.append({"type": "text", "content": response["text"]})
            if "image" in response:
                response_messages.append({"type": "image", "content": response["image"]})
                
        return jsonify(response_messages)
    except Exception as e:
        return jsonify([{"type": "text", "content": "An error occurred while processing your request."}])

if __name__ == "__main__":
    app.run(debug=True)
