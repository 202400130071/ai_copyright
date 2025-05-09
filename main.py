from src.copyright_protection import CopyrightProtection
from datetime import datetime, UTC
import json
from typing import Dict, Any
from config.settings import AI_MODEL_SETTINGS, COPYRIGHT_SETTINGS, get_current_timestamp, get_user_id

def print_header() -> None:
    """打印程序头部信息"""
    print(f"\n当前时间: {get_current_timestamp()}")
    print(f"用户ID: {get_user_id()}")
    print("=" * 50)

def print_menu() -> None:
    """打印菜单选项"""
    print("\n可用操作:")
    print("1. 注册AI生成内容")
    print("2. 验证内容")
    print("3. 查看区块链状态")
    print("4. 更新许可证")
    print("5. 查看内容历史")
    print("6. 查看系统统计")
    print("7. 退出")


def get_ai_model_choice() -> str:
    """获取AI模型选择"""
    print("\n可用的AI模型:")
    for i, model in enumerate(AI_MODEL_SETTINGS["supported_models"], 1):
        print(f"{i}. {model}")

    while True:
        try:
            choice = int(input("\n请选择AI模型 (1-5): ")) - 1
            if 0 <= choice < len(AI_MODEL_SETTINGS["supported_models"]):
                return AI_MODEL_SETTINGS["supported_models"][choice]
        except ValueError:
            pass
        print("无效选择，请重试")


def get_license_choice() -> str:
    """获取许可证类型选择"""
    print("\n可用的许可证类型:")
    for i, license_type in enumerate(COPYRIGHT_SETTINGS["supported_licenses"], 1):
        print(f"{i}. {license_type}")

    while True:
        try:
            choice = int(input("\n请选择许可证类型 (1-4): ")) - 1
            if 0 <= choice < len(COPYRIGHT_SETTINGS["supported_licenses"]):
                return COPYRIGHT_SETTINGS["supported_licenses"][choice]
        except ValueError:
            pass
        print("无效选择，请重试")


def format_result(result: Dict[str, Any]) -> None:
    """格式化并打印结果"""
    if result["status"] == "success":
        print("\n✓ 操作成功!")
        for key, value in result.items():
            if key != "status":
                if isinstance(value, (dict, list)):
                    print(f"{key}:")
                    print(json.dumps(value, indent=2, ensure_ascii=False))
                else:
                    print(f"{key}: {value}")
    else:
        print(f"\n✗ 操作失败: {result['message']}")


def main() -> None:
    """主程序入口"""
    protection = CopyrightProtection()

    while True:
        try:
            print_header()
            print_menu()

            choice = input("\n请选择操作 (1-7): ").strip()

            if choice == "1":
                print("\n注册AI生成内容")
                content = input("请输入内容: ").strip()
                if not content:
                    print("错误: 内容不能为空")
                    continue

                title = input("请输入标题: ").strip()
                description = input("请输入描述: ").strip()

                # 选择AI模型
                ai_model = get_ai_model_choice()

                # 选择许可证类型
                license_type = get_license_choice()

                # 注册内容
                result = protection.protect_ai_content(
                    content=content,
                    title=title or "无标题",
                    description=description or "无描述",
                    ai_model=ai_model,
                    license_type=license_type
                )
                format_result(result)

            elif choice == "2":
                print("\n验证内容")
                content = input("请输入要验证的内容: ").strip()
                if not content:
                    print("错误: 内容不能为空")
                    continue

                result = protection.verify_ownership(content)
                format_result(result)

            elif choice == "3":
                print("\n区块链状态")
                result = protection.registry.get_chain_status()
                format_result(result)

            elif choice == "4":
                print("\n更新许可证")
                content = input("请输入内容: ").strip()
                if not content:
                    print("错误: 内容不能为空")
                    continue

                # 选择新的许可证类型
                new_license = get_license_choice()

                result = protection.update_license(content, new_license)
                format_result(result)

            elif choice == "5":
                print("\n查看内容历史")
                content = input("请输入内容: ").strip()
                if not content:
                    print("错误: 内容不能为空")
                    continue

                result = protection.get_content_history(content)
                format_result(result)

            elif choice == "6":
                print("\n系统统计信息")
                result = protection.get_statistics()
                format_result(result)

            elif choice == "7":
                print("\n感谢使用!")
                break

            else:
                print("\n无效的选择，请重试")

        except KeyboardInterrupt:
            print("\n\n程序已终止")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            continue


if __name__ == "__main__":
    main()