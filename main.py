from flask import Flask, request, jsonify
import whisper
import ffmpeg
import os

app = Flask(__name__)

# Initialize Whisper model
model = whisper.load_model("base")

# Create directory for temporary files
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Endpoint to upload an audio file
@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        # Convert the audio file to WAV format using ffmpeg
        wav_filepath = filepath.rsplit(".", 1)[0] + ".wav"
        ffmpeg.input(filepath).output(wav_filepath).run()

        # Use Whisper AI to transcribe the audio
        result = model.transcribe(wav_filepath)
        transcription = result["text"]

        # Clean up temporary files
        os.remove(filepath)
        os.remove(wav_filepath)

        return jsonify({"transcription": transcription})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
