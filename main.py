from flask import Flask, render_template, request, url_for, send_from_directory, abort
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

@app.route('/view')
def view_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('view.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view_text/<filename>')
def view_text_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template('view_text.html', filename=filename, content=content)
    except:
        abort(404)

if __name__ == '__main__':
    print("Running manage.py")
    app.run(debug=True)
