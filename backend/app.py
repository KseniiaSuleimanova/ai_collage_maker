# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
from process_files import get_dominant_colors
import json
from find_similar import fetch_filenames
from make_collage import collage_creation

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
    color_count = int(request.form.get('colorCount', 1))
    image_count = int(request.form.get('imageCount', 1))
    for key in request.files:
        if key == 'colorCount' or key == 'imageCount':
            continue
        file = request.files[key]
        if file.filename == '':
            return jsonify({"error": f"One of the files is empty"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        sql_query = "INSERT INTO properties (file_name, colors) VALUES (%s, %s)"
        colors = get_dominant_colors(file_path, k=color_count)
        values = (str(file.filename), colors)
        cur.execute(sql_query, values)

        uploaded_files.append(file.filename)
    db.commit()
    cur.close()
    db.close()

    return jsonify({"message": "Files uploaded successfully", "files": uploaded_files})

@app.route('/create', methods=['POST'])
def create_collage():
    image_count = int(request.form.get('imageCount', 1))
    colors = request.form.get('colors', 1).split(',')
    img_paths = fetch_filenames(target_colors=colors, n=image_count)
    filename = collage_creation(img_paths)
    return jsonify({"filename": filename})



if __name__ == '__main__':
    app.run(port=5000, debug=True)
