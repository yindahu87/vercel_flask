from flask import Flask, jsonify, request
from werkzeug.utils import url_quote

app = Flask(__name__)

# 我们这里用一个字典模拟一个简单的数据库
qa_db = {
    "What is Flask?": "Flask is a micro web framework written in Python.",
    "Who developed Flask?": "Flask was developed by Armin Ronacher."
}

@app.route('/qa/<question>', methods=['GET'])
def get_answer(question):
    # 用户可以通过 GET 请求得到某个问题的答案
    answer = qa_db.get(question)
    if answer is None:
        return jsonify({"error": "question not found"}), 404
    else:
        return jsonify({"question": question, "answer": answer})

@app.route('/qa', methods=['POST'])
def add_qa():
    # 使用 try/except 进行错误处理
    try:
        if not request.json or 'question' not in request.json or 'answer' not in request.json:
            return jsonify({"error": "request needs json 'question' and 'answer' parameters"}), 400
        qa_db[request.json['question']] = request.json['answer']
        return jsonify({"success": True, "qa": request.json}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
