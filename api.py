from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os
import uuid

app = Flask(__name__)

# Pasta para armazenar downloads temporários
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({
        "message": "API de download do YouTube está rodando!",
        "usage": {
            "download_mp4": "/download?url=LINK_DO_VIDEO",
            "download_mp3": "/download?url=LINK_DO_VIDEO&format=mp3",
            "baixar_baixa_qualidade": "/download?url=LINK_DO_VIDEO&quality=lowest"
        }
    })

@app.route("/download", methods=["GET"])
def download_video():
    try:
        url = request.args.get("url")
        format_type = request.args.get("format", "mp4")  # mp4 ou mp3
        quality = request.args.get("quality", "highest") # highest ou lowest

        if not url:
            return jsonify({"error": "URL do vídeo é obrigatória"}), 400

        yt = YouTube(url)

        # Escolhe stream dependendo do formato
        if format_type == "mp3":
            stream = yt.streams.filter(only_audio=True).first()
        else:  # mp4
            if quality == "lowest":
                stream = yt.streams.get_lowest_resolution()
            else:
                stream = yt.streams.get_highest_resolution()

        if not stream:
            return jsonify({"error": "Não foi possível encontrar stream compatível"}), 404

        # Nome de arquivo único para evitar conflito
        file_ext = "mp3" if format_type == "mp3" else "mp4"
        filename = f"{uuid.uuid4().hex}.{file_ext}"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        # Baixa o arquivo
        stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Localmente → http://127.0.0.1:5000
    # Online (Render/Railway/Heroku) → usa a porta definida pela plataforma
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)