import unittest
import json
from app import app, add

class TestWebApp(unittest.TestCase):
    def setUp(self):
        # 创建测试客户端
        self.client = app.test_client()
        self.app = app

    def test_add_logic(self):
        # 测试纯业务逻辑
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)

    def test_api_add(self):
        # 测试 Web API 接口是否正常返回 JSON
        response = self.client.get('/api/add/5/10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 15)

    def test_index_page(self):
        # 测试首页 HTML 是否能正常渲染
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jenkins 部署测试', response.data)

if __name__ == '__main__':
    unittest.main()