import unittest
from src.content_registry import ContentRegistry
from src.utils.helpers import calculate_hash
from config.settings import get_current_timestamp, get_user_id


class TestContentRegistry(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.registry = ContentRegistry()
        self.test_content = "This is test content"
        self.test_metadata = {
            "title": "Test Content",
            "description": "Content for testing",
            "content_type": "text"
        }

    def test_register_content(self):
        """测试内容注册"""
        result = self.registry.register_content(
            self.test_content,
            self.test_metadata
        )

        self.assertEqual(result["status"], "success")
        self.assertIn("content_hash", result)
        self.assertIn("block_hash", result)
        self.assertEqual(result["metadata"]["title"], "Test Content")

    def test_verify_content(self):
        """测试内容验证"""
        # 先注册内容
        register_result = self.registry.register_content(
            self.test_content,
            self.test_metadata
        )

        # 验证已注册的内容
        verify_result = self.registry.verify_content(self.test_content)

        self.assertEqual(verify_result["status"], "success")
        self.assertTrue(verify_result["verified"])
        self.assertEqual(
            verify_result["content_hash"],
            register_result["content_hash"]
        )

    def test_empty_content(self):
        """测试空内容"""
        result = self.registry.register_content("")
        self.assertEqual(result["status"], "error")
        self.assertIn("Content cannot be empty", result["message"])

    def test_invalid_metadata(self):
        """测试无效元数据"""
        invalid_metadata = {
            "title": "Test"
            # 缺少必需的字段
        }
        result = self.registry.register_content(
            self.test_content,
            invalid_metadata
        )
        self.assertEqual(result["status"], "error")

    def test_search_content(self):
        """测试内容搜索"""
        # 注册测试内容
        self.registry.register_content(
            self.test_content,
            self.test_metadata
        )

        # 搜索内容
        search_result = self.registry.search_content({
            "title": "Test Content"
        })

        self.assertEqual(search_result["status"], "success")
        self.assertEqual(len(search_result["results"]), 1)
        self.assertEqual(
            search_result["results"][0]["metadata"]["title"],
            "Test Content"
        )

    def test_chain_status(self):
        """测试链状态"""
        status = self.registry.get_chain_status()

        self.assertEqual(status["status"], "success")
        self.assertTrue(status["is_valid"])
        self.assertGreaterEqual(status["length"], 1)  # 至少有创世区块


if __name__ == '__main__':
    unittest.main()