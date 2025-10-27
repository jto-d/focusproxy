import os
from flask import Flask, jsonify, request

app = Flask(__name__)
current_activity = {"state": "idle"}

@app.route('/', methods=['GET'])
def get_root():
  return jsonify(message="Hello, World!")

@app.route('/activity', methods=['GET'])
def get_activity():
  return jsonify(current_activity)

@app.route('/activity', methods=['POST'])
def set_activity():
  data = request.get_json()
  if "state" in data:
    current_activity["state"] = data["state"]
  return jsonify(success=True)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port, debug=False)