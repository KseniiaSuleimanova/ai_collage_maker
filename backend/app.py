from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows cross-origin requests, which are necessary for connecting to the frontend.

counter = 0  # This is a simple in-memory counter.

@app.route('/increment', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    return jsonify({'counter': counter})

if __name__ == '__main__':
    app.run(port=5000)  # Run the server on port 5000
