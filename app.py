from flask import Flask, render_template, request, send_file
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['video']
        start = float(request.form['start'])
        end = float(request.form['end'])

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        clip = VideoFileClip(filepath).subclip(start, end)
        export_path = os.path.join(EXPORT_FOLDER, f"cut_{file.filename}")
        clip.write_videofile(export_path, codec='libx264')

        return send_file(export_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
