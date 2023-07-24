from flask import Flask, request, render_template, send_file


app = Flask(__name__)


@app.route('/')
def welcome():
    return "欢迎来到我的 Flask 网页！"

if __name__ == '__main__':
    app.run(debug=True)
