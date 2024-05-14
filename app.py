from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)


@app.route('/')
def main():
    files = os.listdir('./files')
    filenames = [f for f in files]

    return render_template("index.html", files=filenames)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'./files/{f.filename}')
        return render_template("upload.html")


@app.route('/download', methods=['GET'])
def download_file():
    if request.method == 'GET':
        args = request.args
        return send_from_directory('./files', args['filename'], as_attachment=True)


if __name__ == '__main__':
    app.run()
