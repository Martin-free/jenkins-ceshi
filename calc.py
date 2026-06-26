import http.server
import socketserver

def add(a, b):
    return a + b

# 一个简单的 Web 服务，用于测试部署后能否正常访问
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"服务已启动，端口: {PORT}")
        httpd.serve_forever()