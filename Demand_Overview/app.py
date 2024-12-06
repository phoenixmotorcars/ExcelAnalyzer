from flask import Flask, request, render_template, jsonify, send_from_directory, url_for
from utils.file_processing import process_excel_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('output_files', filename, as_attachment=True)

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Process the file
    try:
        # Call your processing function (this should generate the output file)
        output_filename = process_excel_file(file_path)  # Replace with actual function
        # print(output_filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        template_url = url_for('static', filename='template.xlsx', _external=True)
        message = (
            "File processed successfully. If the output is not as expected, "
            "download the template file, modify your data to match its format, and try again."
        )
        # Ensure the output file exists
        if not os.path.exists(output_path):
            raise FileNotFoundError("Output file not generated")

        # Return the success response with the downloadable file path
        return jsonify({
            "message": message,
            "file_url": f"/download/{output_filename}",
           "template_link": template_url
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)