from flask import Flask, render_template, request, jsonify
from japanerrorprocess import *
from kerrorp import *
from id import *
from kextract import *
from check import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/home')
def landing_page():
    return render_template('landing_page.html')

@app.route('/')
def about_page():
    return render_template('about_page.html')

@app.route('/validate', methods=['POST'])
def validate():
    # Check if the file part is in the request
    if 'fileInput[]' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('fileInput[]')  # Get all files uploaded
    print(files)
    # Check if any files were uploaded
    if not files or all(file.filename == '' for file in files):
        return jsonify({"error": "No selected files"}), 400

    # Get the selected language from the form
    selected_language = request.form.get('languageSelect')
    
    if selected_language not in ['korean', 'japanese']:
        return jsonify({"error": "Invalid language selection"}), 400
    file_paths = []
    for file in files:
        # Save each file to the uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        file_paths.append(file_path)  # Add the saved file path to the list

    try:
        # Process files based on selected language
        if selected_language == 'japanese':
            result1 = run_parser_multiple_files(file_paths)
            result2 = process_sigs(file_paths)
            result = japanep(result1, result2)  # Call Japanese processing function
        elif selected_language == 'korean':
            result1 = run_parser_multiple_files(file_paths)
            result2 = extract_combined_tables(file_paths)
            result3 = process_sigs(file_paths)
            result = koreanep(result1, result2, result3)  # Call Korean processing function

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"error": f"Error processing files: {str(e)}"}), 500
    
@app.route('/crosscheck', methods=['POST'])
def crosscheck():
    # Check if the uploaded file from the upload button is in the request
    if 'uploadedFile' not in request.files:
        return jsonify({"error": "No uploaded file part"}), 400

    uploaded_file = request.files['uploadedFile']  # This is the file from the upload button
    crosscheck_files = request.files.getlist('checkfiles[]')  # These are the files from the cross-check button

    # Validate the uploaded file (from the upload button)
    if uploaded_file.filename == '':
        return jsonify({"error": "No uploaded file selected"}), 400

    # Validate the cross-check files (from the cross-check form)
    if not crosscheck_files or all(file.filename == '' for file in crosscheck_files):
        return jsonify({"error": "No selected cross-check files"}), 400

    # Get the selected language from the form
    selected_language = request.form.get('languageSelect')

    if selected_language not in ['korean', 'japanese']:
        return jsonify({"error": "Invalid language selection"}), 400

    try:
        # Save the uploaded file to the uploads folder
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(uploaded_file_path)

        # Save the cross-check files to the uploads folder
        crosscheck_file_paths = []
        for file in crosscheck_files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            crosscheck_file_paths.append(file_path)

        # Process the uploaded file (from the upload button)
        result1 = analyze_local_id(uploaded_file_path)  # Analyze only the uploaded file
        result2 = run_parser_multiple_files(crosscheck_file_paths)

        # Process cross-check files based on selected language
        if selected_language == 'japanese':
            result = jcompare_dict_values(result1, result2)  # Compare results
        elif selected_language == 'korean':
            result = kcompare_dict_values(result1, result2)  # Compare results

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"error": f"Error processing files: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
