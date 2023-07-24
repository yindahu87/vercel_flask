from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1 style='color: red; text-align: center;'>欢迎来到我的网站!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
