from flask import Flask, request, jsonify
import os
import tempfile
from classify import analyze

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Create a temporary file with .jpg extension
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', dir='./temp_uploads')
        try:
            # Save the file content to the temporary file
            file.save(temp_file.name)
            print(temp_file)
            
            
            return analyze(temp_file.name) 

        except Exception as e:
            # Ensure cleanup in case of an error
            os.unlink(temp_file.name)
            return jsonify({"error": f"Failed to upload file: {str(e)}"}), 500

        finally:
            # Close the file to ensure resources are released
            temp_file.close()
            os.unlink(temp_file.name)

    return jsonify({"error": "Unexpected error occurred"}), 500

if __name__ == '__main__':
    # Ensure the temporary directory exists
    if not os.path.exists('./temp_uploads'):
        os.makedirs('./temp_uploads')
    app.run(debug=True, port=5000)