from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 业务逻辑
def add(a, b):
    return a + b

# 路由1：渲染 HTML 页面
@app.route('/')
def index():
    return render_template('index.html')

# 路由2：提供 API 接口，方便自动化测试
@app.route('/api/add/<int:a>/<int:b>')
def api_add(a, b):
    result = add(a, b)
    return jsonify({'result': result})

if __name__ == '__main__':
    # 生产环境部署时，通常使用 gunicorn 或 uwsgi，这里仅作测试演示
    app.run(host='0.0.0.0', port=8000)