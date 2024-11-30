from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Ensure an upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def uploader():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('success.html', filename=filename)

if __name__ == '__main__':
    print("Running manage.py")
    app.run(debug=True)
