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
  app.run(debug=True, port=8080)