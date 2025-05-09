from typing import Dict, Any, Optional, List
import json
from pathlib import Path
from .blockchain import Blockchain
from .utils.helpers import (
    calculate_hash,
    validate_metadata,
    validate_content,
    ValidationError,
    get_current_info
)
from config.settings import COPYRIGHT_SETTINGS, AI_MODEL_SETTINGS, get_current_timestamp, get_user_id


class ContentRegistry:
    def __init__(self) -> None:
        """初始化内容注册管理器"""
        self.blockchain = Blockchain()

    def register_content(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """注册AI生成内容"""
        try:
            # 验证内容
            validate_content(content)

            # 处理元数据
            if metadata is None:
                metadata = {}

            # 添加基本元数据
            metadata.update({
                "registration_time": get_current_timestamp(),
                "user_id": get_user_id(),
                "license": metadata.get("license", COPYRIGHT_SETTINGS["default_license"])
            })

            # 验证元数据
            if not validate_metadata(metadata):
                raise ValidationError("Invalid metadata format")

            # 计算内容哈希
            content_hash = calculate_hash(content)

            # 准备交易数据
            transaction_data = {
                "type": "content_registration",
                "content_hash": content_hash,
                "timestamp": get_current_timestamp(),
                "user_id": get_user_id(),
                "metadata": metadata
            }

            # 添加到区块链
            new_block = self.blockchain.add_block(transaction_data)

            return {
                "status": "success",
                "content_hash": content_hash,
                "block_hash": new_block.hash,
                "block_number": new_block.index,
                "timestamp": new_block.timestamp,
                "metadata": metadata
            }

        except ValidationError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Registration failed: {str(e)}"
            }

    def verify_content(self, content: str) -> Dict[str, Any]:
        """验证内容在区块链上的注册状态"""
        try:
            # 验证内容
            validate_content(content)

            # 计算内容哈希
            content_hash = calculate_hash(content)

            # 搜索区块链
            for block in self.blockchain.chain:
                if (block.data.get("type") == "content_registration" and
                        block.data.get("content_hash") == content_hash):
                    return {
                        "status": "success",
                        "verified": True,
                        "block_number": block.index,
                        "block_hash": block.hash,
                        "timestamp": block.data["timestamp"],
                        "user_id": block.data["user_id"],
                        "metadata": block.data["metadata"]
                    }

            return {
                "status": "success",
                "verified": False,
                "message": "Content not found in blockchain"
            }

        except ValidationError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Verification failed: {str(e)}"
            }

    def get_chain_status(self) -> Dict[str, Any]:
        """获取区块链状态"""
        try:
            return {
                "status": "success",
                "length": len(self.blockchain.chain),
                "latest_block": self.blockchain.get_latest_block().to_dict(),
                "is_valid": self.blockchain.is_chain_valid(),
                "difficulty": self.blockchain.difficulty
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get chain status: {str(e)}"
            }

    def search_content(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """搜索内容"""
        results = []
        try:
            for block in self.blockchain.chain:
                if block.data.get("type") != "content_registration":
                    continue

                metadata = block.data.get("metadata", {})

                # 按条件过滤
                matches = True
                for key, value in query.items():
                    if key in metadata and metadata[key] != value:
                        matches = False
                        break

                if matches:
                    results.append({
                        "block_number": block.index,
                        "content_hash": block.data["content_hash"],
                        "timestamp": block.data["timestamp"],
                        "metadata": metadata
                    })

            return {
                "status": "success",
                "results": results,
                "count": len(results),
                "query_time": get_current_timestamp()
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Search failed: {str(e)}"
            }