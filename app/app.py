from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    rasa_response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})
    response_data = rasa_response.json()
    
    response_messages = []
    for response in response_data:
        if "text" in response:
            response_messages.append({"type": "text", "content": response["text"]})
        if "image" in response:
            response_messages.append({"type": "image", "content": response["image"]})
    
    return jsonify(response_messages)

if __name__ == '__main__':
    app.run(debug=True)

