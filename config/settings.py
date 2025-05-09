from pathlib import Path
from datetime import datetime, UTC

# 项目基础配置
PROJECT_ROOT = Path(__file__).parent.parent
STORAGE_DIR = PROJECT_ROOT / "storage"
BLOCKCHAIN_DATA_DIR = STORAGE_DIR / "blockchain_data"

# 区块链配置
MINING_DIFFICULTY = 2
BLOCK_SIZE_LIMIT = 1024 * 1024  # 1MB

# 用户和时间配置
DEFAULT_USER_ID = "202400130071"
CURRENT_TIME = "2025-04-24 11:17:09"
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_current_timestamp() -> str:
    """获取当前时间戳"""
    return CURRENT_TIME

def get_user_id() -> str:
    """获取当前用户ID"""
    return DEFAULT_USER_ID

# 确保存储目录存在
STORAGE_DIR.mkdir(exist_ok=True)
BLOCKCHAIN_DATA_DIR.mkdir(exist_ok=True)

# 版权配置
COPYRIGHT_SETTINGS = {
    "default_license": "All rights reserved",
    "supported_licenses": [
        "All rights reserved",
        "MIT",
        "Creative Commons BY-SA 4.0",
        "Apache 2.0"
    ],
    "supported_content_types": [
        "text",
        "image",
        "audio",
        "video",
        "code"
    ]
}

# AI模型配置
AI_MODEL_SETTINGS = {
    "supported_models": [
        "GPT-4",
        "GPT-3.5",
        "DALL-E 3",
        "Claude 2",
        "Gemini Pro"
    ],
    "default_parameters": {
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.95
    }
}