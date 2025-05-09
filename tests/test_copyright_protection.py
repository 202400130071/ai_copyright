import unittest
from src.copyright_protection import CopyrightProtection
from config.settings import (
    AI_MODEL_SETTINGS,
    COPYRIGHT_SETTINGS,
    get_current_timestamp,
    get_user_id
)


class TestCopyrightProtection(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.protection = CopyrightProtection()
        self.test_content = "This is AI generated test content"
        self.test_title = "Test Title"
        self.test_description = "Test Description"
        self.test_ai_model = AI_MODEL_SETTINGS["supported_models"][0]
        self.test_license = COPYRIGHT_SETTINGS["supported_licenses"][0]

    def test_protect_ai_content(self):
        """测试AI内容保护"""
        result = self.protection.protect_ai_content(
            content=self.test_content,
            title=self.test_title,
            description=self.test_description,
            ai_model=self.test_ai_model,
            license_type=self.test_license
        )

        self.assertEqual(result["status"], "success")
        self.assertIn("content_hash", result)
        self.assertIn("block_hash", result)
        self.assertEqual(
            result["metadata"]["title"],
            self.test_title
        )

    def test_invalid_ai_model(self):
        """测试无效的AI模型"""
        result = self.protection.protect_ai_content(
            content=self.test_content,
            title=self.test_title,
            description=self.test_description,
            ai_model="InvalidModel",
            license_type=self.test_license
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("Unsupported AI model", result["message"])

    def test_invalid_license(self):
        """测试无效的许可证类型"""
        result = self.protection.protect_ai_content(
            content=self.test_content,
            title=self.test_title,
            description=self.test_description,
            ai_model=self.test_ai_model,
            license_type="InvalidLicense"
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("Unsupported license type", result["message"])

    def test_verify_ownership(self):
        """测试所有权验证"""
        # 先注册内容
        protect_result = self.protection.protect_ai_content(
            content=self.test_content,
            title=self.test_title,
            description=self.test_description,
            ai_model=self.test_ai_model,
            license_type=self.test_license
        )

        # 验证所有权
        verify_result = self.protection.verify_ownership(self.test_content)

        self.assertEqual(verify_result["status"], "success")
        self.assertTrue(verify_result["verified"])
        self.assertEqual(verify_result["user_id"], get_user_id())

    def test_content_history(self):
        """测试内容历史"""
        # 先注册内容
        self.protection.protect_ai_content(
            content=self.test_content,
            title=self.test_title,
            description=self.test_description,
            ai_model=self.test_ai_model,
            license_type=self.test_license
        )

        # 获取历史记录
        history_result = self.protection.get_content_history(
            self.test_content
        )

        self.assertEqual(history_result["status"], "success")
        self.assertGreaterEqual(len(history_result["history"]), 1)

    def test_update_license(self):
        """测试更新许可证"""
        # 先注册内容
        self.protection.protect_ai_content(
            content=self.test_content,
            title=self.test_title,
            description=self.test_description,
            ai_model=self.test_ai_model,
            license_type=self.test_license
        )

        # 更新许可证
        new_license = COPYRIGHT_SETTINGS["supported_licenses"][1]
        update_result = self.protection.update_license(
            self.test_content,
            new_license
        )

        self.assertEqual(update_result["status"], "success")
        self.assertEqual(update_result["new_license"], new_license)


if __name__ == '__main__':
    unittest.main()