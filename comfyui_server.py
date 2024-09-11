import os
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)

WORKFLOW_PATH = "C:\\Users\\Manh Me~\\source\\repos\\Tryon V2.1\\Tryon.json"

@app.route('/process', methods=['POST'])
def process_images():
    if 'clothing_image' not in request.files or 'model_image' not in request.files:
        return 'No file uploaded!', 400

    clothing_image = request.files['clothing_image']
    model_image = request.files['model_image']

    clothing_path = os.path.join('uploads', clothing_image.filename)
    model_path = os.path.join('uploads', model_image.filename)

    clothing_image.save(clothing_path)
    model_image.save(model_path)

    output_path = os.path.join('results', 'output_image.jpg')

    try:
        subprocess.run(
            [
                "python",
                "X:\\ComfyUI_windows_portable\\ComfyUI\\main.py",
                "--input", model_path,
                "--clothing", clothing_path,
                "--workflow", WORKFLOW_PATH,
                "--output", output_path
            ],
            check=True
        )

        return send_file(output_path, mimetype='image/jpeg')
    except subprocess.CalledProcessError as e:
        return f"Error running ComfyUI workflow: {e}", 500

@app.route('/')
def home():
    return "This is the home page for the ComfyUI server."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
