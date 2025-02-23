# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
from process_files import get_dominant_colors

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if not request.files:
        return jsonify({"error": "No files in the request"}), 400

    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Innuendo-1991',
        database='file_properties'
    )
    cur = db.cursor()

    uploaded_files = []
    for key in request.files:
        file = request.files[key]
        if file.filename == '':
            return jsonify({"error": f"One of the files is empty"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        sql_query = "INSERT INTO properties (file_name, colors) VALUES (%s, %s)"
        colors = get_dominant_colors(file_path, k=3) #TODO: make k not constant
        values = (str(file.filename), colors)
        cur.execute(sql_query, values)
        file.save(file_path)
        uploaded_files.append(file.filename)
    db.commit()
    cur.close()

    return jsonify({"message": "Files uploaded successfully", "files": uploaded_files})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
