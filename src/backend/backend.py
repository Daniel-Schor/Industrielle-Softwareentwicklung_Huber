from flask import Flask, jsonify
from database import get_data_from_db

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = get_data_from_db()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)