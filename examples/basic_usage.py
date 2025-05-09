from src.copyright_protection import CopyrightProtection
from config.settings import (
    AI_MODEL_SETTINGS,
    COPYRIGHT_SETTINGS,
    get_current_timestamp,
    get_user_id
)


def basic_demo():
    """基础功能演示"""
    print(f"演示开始时间: {get_current_timestamp()}")
    print(f"用户ID: {get_user_id()}\n")

    # 初始化版权保护系统
    protection = CopyrightProtection()

    # 示例内容
    content = """这是一段由AI生成的测试内容。
    用于演示AI版权保护系统的基本功能。
    生成时间: 2025-04-24 11:25:42
    """

    # 1. 注册AI生成内容
    print("1. 注册AI生成内容...")
    result = protection.protect_ai_content(
        content=content,
        title="基础演示内容",
        description="用于演示的AI生成内容",
        ai_model="GPT-4",
        license_type="MIT"
    )
    print("注册结果:", result)

    # 2. 验证内容
    print("\n2. 验证内容...")
    verify_result = protection.verify_ownership(content)
    print("验证结果:", verify_result)

    # 3. 查看内容历史
    print("\n3. 查看内容历史...")
    history_result = protection.get_content_history(content)
    print("历史记录:", history_result)

    # 4. 更新许可证
    print("\n4. 更新许可证...")
    update_result = protection.update_license(
        content,
        "Creative Commons BY-SA 4.0"
    )
    print("更新结果:", update_result)

    # 5. 查看系统统计
    print("\n5. 系统统计...")
    stats_result = protection.get_statistics()
    print("统计信息:", stats_result)


if __name__ == "__main__":
    basic_demo()