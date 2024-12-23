import os
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import openai
from pdfminer.high_level import extract_text

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = extract_text(file_path)
    return text

# Function to summarize text with OpenAI
def summarize_text(text):
    prompt = f"Summarize the following research paper in simple terms:\n\n{text[:4000]}"  # Limit text for token size
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace with "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful research paper summarizer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Handle file upload
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            # Save uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Extract text and summarize
            text = extract_text_from_pdf(file_path)
            summary = summarize_text(text)

            return render_template("index.html", summary=summary)

    return render_template("index.html", summary=None)

if __name__ == "__main__":
    app.run(debug=True)
