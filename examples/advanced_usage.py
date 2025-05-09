from src.copyright_protection import CopyrightProtection
from src.utils.helpers import calculate_hash
from typing import Dict, Any
import json
from config.settings import (
    AI_MODEL_SETTINGS,
    COPYRIGHT_SETTINGS,
    get_current_timestamp,
    get_user_id
)

class AdvancedDemo:
    def __init__(self):
        """高级功能演示初始化"""
        self.protection = CopyrightProtection()
        self.content_database = {}

    def register_batch_content(self, contents: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """批量注册内容"""
        results = {}
        for content_id, content_info in contents.items():
            result = self.protection.protect_ai_content(
                content=content_info["content"],
                title=content_info["title"],
                description=content_info["description"],
                ai_model=content_info["ai_model"],
                license_type=content_info["license_type"]
            )
            results[content_id] = result
            if result["status"] == "success":
                self.content_database[content_id] = {
                    "content": content_info["content"],
                    "registration": result
                }
        return results

    def verify_batch_content(self) -> Dict[str, Any]:
        """批量验证内容"""
        results = {}
        for content_id, content_info in self.content_database.items():
            result = self.protection.verify_ownership(
                content_info["content"]
            )
            results[content_id] = result
        return results

    def demo_run(self):
        """运行演示"""
        print(f"高级演示开始时间: {get_current_timestamp()}")
        print(f"用户ID: {get_user_id()}\n")

        # 1. 准备测试内容
        test_contents = {
            "content1": {
                "content": "这是第一段AI生成的测试内容。",
                "title": "测试内容1",
                "description": "第一个测试用例",
                "ai_model": "GPT-4",
                "license_type": "MIT"
            },
            "content2": {
                "content": "这是第二段AI生成的测试内容。",
                "title": "测试内容2",
                "description": "第二个测试用例",
                "ai_model": "Claude 2",
                "license_type": "Apache 2.0"
            }
        }

        # 2. 批量注册
        print("1. 批量注册内容...")
        register_results = self.register_batch_content(test_contents)
        print(json.dumps(register_results, indent=2, ensure_ascii=False))

        # 3. 批量验证
        print("\n2. 批量验证内容...")
        verify_results = self.verify_batch_content()
        print(json.dumps(verify_results, indent=2, ensure_ascii=False))

        # 4. 更新许可证
        print("\n3. 更新许可证...")
        for content_id, content_info in self.content_database.items():
            update_result = self.protection.update_license(
                content_info["content"],
                "Creative Commons BY-SA 4.0"
            )
            print(f"内容 {content_id} 许可证更新结果:")
            print(json.dumps(update_result, indent=2, ensure_ascii=False))

        # 5. 获取统计信息
        print("\n4. 系统统计...")
        stats = self.protection.get_statistics()
        print(json.dumps(stats, indent=2, ensure_ascii=False))

def run_advanced_demo():
    """运行高级演示"""
    demo = AdvancedDemo()
    demo.demo_run()

if __name__ == "__main__":
    run_advanced_demo()