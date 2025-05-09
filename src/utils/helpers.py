from datetime import datetime, UTC
import hashlib
import json
from typing import Any, Dict
from pathlib import Path
from config.settings import get_current_timestamp, get_user_id

def get_current_info() -> Dict[str, str]:
    """获取当前用户和时间信息"""
    return {
        "user_id": get_user_id(),
        "timestamp": get_current_timestamp()
    }

def calculate_hash(data: Any) -> str:
    """计算数据的SHA256哈希值"""
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True)
    elif not isinstance(data, str):
        data = str(data)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def validate_metadata(metadata: Dict[str, Any]) -> bool:
    """验证元数据格式"""
    required_fields = ["title", "description", "content_type"]
    return all(field in metadata for field in required_fields)

def load_json_file(file_path: Path) -> Dict[str, Any]:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_file(data: Dict[str, Any], file_path: Path) -> bool:
    """保存JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def generate_content_id(content: str) -> str:
    """生成内容ID"""
    data = f"{content}{get_user_id()}{get_current_timestamp()}"
    return calculate_hash(data)

class ValidationError(Exception):
    """验证错误"""
    pass

def validate_content(content: str) -> None:
    """验证内容有效性"""
    if not content or not content.strip():
        raise ValidationError("Content cannot be empty")
    if len(content) > 1024 * 1024:  # 1MB
        raise ValidationError("Content size exceeds limit")