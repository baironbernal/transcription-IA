from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/upload-audio', methods=["POST"])
def uploadAudio():
    data = request.get_json()

    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)