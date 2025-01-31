import os
from flask import Flask, request, render_template, send_file
import whisper

# Initialize Flask app
app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("medium")  # Use "medium" or "large" for better accuracy

# Configure upload folder
UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]

        # Check if the file is a .wav file
        if file.filename == "" or not file.filename.endswith(".wav"):
            return "Invalid file. Please upload a .wav file.", 400

        # Save the uploaded file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Transcribe the audio file
        result = model.transcribe(file_path, language="tr")
        transcription = result["text"]

        # Save the transcription as a .txt file
        txt_file_path = file_path.replace(".wav", ".txt")
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(transcription)

        # Return the transcription file for download
        return send_file(txt_file_path, as_attachment=True)

    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable
    app.run(host="0.0.0.0", port=port)
