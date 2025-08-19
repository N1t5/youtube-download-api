from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({
        "message": "API de download do YouTube está rodando!",
        "usage": {
            "download_mp4": "/download?url=<link_do_video>"
        }
    })

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL do vídeo não fornecida"}), 400

    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)