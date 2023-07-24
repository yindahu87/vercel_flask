from flask import Flask, request, render_template, send_file
from PIL import Image, ImageFilter
import os
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'image' not in request.files:
            return render_template('index.html', error='No file selected')

        image_file = request.files['image']

        # 检查文件是否符合要求
        if image_file.filename == '':
            return render_template('index.html', error='No file selected')

        if not allowed_file(image_file.filename):
            return render_template('index.html', error='Invalid file type')

        # 保存上传的图片
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)

        # 打开图片
        image = Image.open(image_path)

        # 图片处理
        if 'operation' in request.form:
            operation = request.form['operation']
            if operation == 'noise':
                image = add_noise(image)
            elif operation == 'grayscale':
                image = grayscale(image)
            elif operation == 'blur':
                image = blur(image)

        # 保存处理后的图片
        processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + image_file.filename)
        image.save(processed_image_path)

        # 返回处理后的图片给用户
        return render_template('result.html', image_path=processed_image_path)

    return render_template('index.html')

def add_noise(image):
    return image

def grayscale(image):
    return image.convert('L')

def blur(image):
    return image.filter(ImageFilter.BLUR)

@app.route('/download', methods=['GET'])
def download_image():
    image_path = request.args.get('image_path')

    if image_path:
        # 读取文件
        file = io.BytesIO()
        with open(image_path, 'rb') as f:
            file.write(f.read())
        file.seek(0)

        # 删除处理后的图片
        os.remove(image_path)

        # 返回文件给用户下载
        return send_file(file, attachment_filename='processed_image.jpg', as_attachment=True)

    return 'Invalid image path'

if __name__ == '__main__':
    app.run(debug=True)
