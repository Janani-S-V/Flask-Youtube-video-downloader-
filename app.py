from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        video_url = request.form['url']
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        download_path = 'downloads'
        os.makedirs(download_path, exist_ok=True)
        video.download(download_path)
        filename = video.title + '.mp4'
        return render_template('success.html', filename=filename)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/downloads/<filename>')
def uploaded_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)