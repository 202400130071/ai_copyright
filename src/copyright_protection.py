from typing import Dict, Any, List, Optional
from .content_registry import ContentRegistry
from .utils.helpers import (
    calculate_hash,
    validate_content,
    ValidationError
)
from config.settings import (
    COPYRIGHT_SETTINGS,
    AI_MODEL_SETTINGS,
    get_current_timestamp,
    get_user_id
)


class CopyrightProtection:
    def __init__(self) -> None:
        """初始化版权保护系统"""
        self.registry = ContentRegistry()

    def protect_ai_content(
            self,
            content: str,
            title: str,
            description: str,
            ai_model: str,
            ai_params: Optional[Dict[str, Any]] = None,
            license_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """保护AI生成的内容"""
        try:
            # 验证AI模型
            if ai_model not in AI_MODEL_SETTINGS["supported_models"]:
                raise ValidationError(f"Unsupported AI model: {ai_model}")

            # 验证许可证类型
            if license_type and license_type not in COPYRIGHT_SETTINGS["supported_licenses"]:
                raise ValidationError(f"Unsupported license type: {license_type}")

            # 准备元数据
            metadata = {
                "title": title,
                "description": description,
                "content_type": "text",
                "ai_info": {
                    "model": ai_model,
                    "parameters": ai_params or AI_MODEL_SETTINGS["default_parameters"]
                },
                "license": license_type or COPYRIGHT_SETTINGS["default_license"],
                "creation_time": get_current_timestamp(),
                "creator_id": get_user_id()
            }

            # 注册内容
            result = self.registry.register_content(content, metadata)

            if result["status"] != "success":
                raise ValidationError(result["message"])

            return result

        except ValidationError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Protection failed: {str(e)}"
            }

    def verify_ownership(self, content: str) -> Dict[str, Any]:
        """验证内容所有权"""
        return self.registry.verify_content(content)

    def get_content_history(self, content: str) -> Dict[str, Any]:
        """获取内容的历史记录"""
        try:
            content_hash = calculate_hash(content)
            history = []

            for block in self.registry.blockchain.chain:
                if block.data.get("content_hash") == content_hash:
                    history.append({
                        "block_number": block.index,
                        "timestamp": block.timestamp,
                        "action": block.data.get("type", "unknown"),
                        "metadata": block.data.get("metadata", {})
                    })

            return {
                "status": "success",
                "history": history,
                "count": len(history),
                "query_time": get_current_timestamp()
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get content history: {str(e)}"
            }

    def update_license(self, content: str, new_license: str) -> Dict[str, Any]:
        """更新内容的许可证类型"""
        try:
            # 验证许可证类型
            if new_license not in COPYRIGHT_SETTINGS["supported_licenses"]:
                raise ValidationError(f"Unsupported license type: {new_license}")

            # 验证所有权
            verify_result = self.verify_ownership(content)
            if not verify_result.get("verified"):
                raise ValidationError("Content not found or not owned by current user")

            if verify_result["user_id"] != get_user_id():
                raise ValidationError("Not authorized to update license")

            # 准备更新数据
            content_hash = calculate_hash(content)
            update_data = {
                "type": "license_update",
                "content_hash": content_hash,
                "previous_license": verify_result["metadata"]["license"],
                "new_license": new_license,
                "timestamp": get_current_timestamp(),
                "user_id": get_user_id()
            }

            # 添加到区块链
            new_block = self.registry.blockchain.add_block(update_data)

            return {
                "status": "success",
                "message": "License updated successfully",
                "block_number": new_block.index,
                "block_hash": new_block.hash,
                "new_license": new_license,
                "update_time": get_current_timestamp()
            }

        except ValidationError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"License update failed: {str(e)}"
            }

    def get_statistics(self) -> Dict[str, Any]:
        """获取版权保护系统的统计信息"""
        try:
            total_blocks = len(self.registry.blockchain.chain)
            registrations = 0
            updates = 0
            models_usage = {}
            licenses_usage = {}

            for block in self.registry.blockchain.chain:
                if block.data.get("type") == "content_registration":
                    registrations += 1
                    metadata = block.data.get("metadata", {})

                    # 统计AI模型使用情况
                    ai_model = metadata.get("ai_info", {}).get("model")
                    if ai_model:
                        models_usage[ai_model] = models_usage.get(ai_model, 0) + 1

                    # 统计许可证使用情况
                    license_type = metadata.get("license")
                    if license_type:
                        licenses_usage[license_type] = licenses_usage.get(license_type, 0) + 1

                elif block.data.get("type") == "license_update":
                    updates += 1

            return {
                "status": "success",
                "total_blocks": total_blocks,
                "total_registrations": registrations,
                "total_updates": updates,
                "models_usage": models_usage,
                "licenses_usage": licenses_usage,
                "query_time": get_current_timestamp()
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get statistics: {str(e)}"
            }