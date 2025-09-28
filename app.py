from flask import Flask, request, redirect, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "."

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/start', methods=['POST'])
def start_automation():
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join(UPLOAD_FOLDER, "sele.xlsx")
        file.save(filepath)

        # 🔁 Run your main script
        subprocess.run(["python", "main.py"], shell=True)

        return "✅ Automation Completed! Check console and screenshot."
    else:
        return "❌ Please upload a valid Excel (.xlsx) file."

if __name__ == '__main__':
    app.run(debug=True)
