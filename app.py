import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 必要ならアップロードフォルダを作成
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        # 画像ファイルを開く
        img = Image.open(file.stream)
        # グレースケールに変換
        grayscale_img = img.convert('L')

        # ファイルを保存するパス
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'grayscale_image.png')
        grayscale_img.save(file_path)

        return redirect(url_for('display_image', filename='grayscale_image.png'))

@app.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
