from typing import Dict, List, Any, Optional
import json
from pathlib import Path
from .utils.helpers import calculate_hash, get_current_info, load_json_file, save_json_file
from config.settings import BLOCKCHAIN_DATA_DIR, MINING_DIFFICULTY, get_current_timestamp, get_user_id


class Block:
    def __init__(self, index: int, timestamp: str, data: Dict[str, Any], previous_hash: str) -> None:
        """初始化区块"""
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """计算区块哈希值"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return calculate_hash(block_string)

    def mine_block(self, difficulty: int) -> str:
        """挖掘区块"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self) -> None:
        """初始化区块链"""
        self.chain: List[Block] = []
        self.difficulty = MINING_DIFFICULTY
        self.chain_file = BLOCKCHAIN_DATA_DIR / "chain.json"

        if self.chain_file.exists():
            self.load_chain()
        else:
            self.create_genesis_block()
            self.save_chain()

    def create_genesis_block(self) -> None:
        """创建创世区块"""
        genesis_block = Block(
            0,
            get_current_timestamp(),
            {
                "message": "Genesis Block",
                "user_id": get_user_id()
            },
            "0"
        )
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """获取最新区块"""
        return self.chain[-1]

    def add_block(self, data: Dict[str, Any]) -> Block:
        """添加新区块"""
        previous_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            get_current_timestamp(),
            data,
            previous_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain()
        return new_block

    def is_chain_valid(self) -> bool:
        """验证区块链的完整性"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def save_chain(self) -> None:
        """保存区块链到文件"""
        chain_data = {
            "chain": [block.to_dict() for block in self.chain],
            "metadata": {
                "last_updated": get_current_timestamp(),
                "user_id": get_user_id(),
                "difficulty": self.difficulty
            }
        }
        save_json_file(chain_data, self.chain_file)

    def load_chain(self) -> None:
        """从文件加载区块链"""
        chain_data = load_json_file(self.chain_file)

        self.chain = []
        for block_data in chain_data.get("chain", []):
            block = Block(
                block_data["index"],
                block_data["timestamp"],
                block_data["data"],
                block_data["previous_hash"]
            )
            block.nonce = block_data["nonce"]
            block.hash = block_data["hash"]
            self.chain.append(block)

        self.difficulty = chain_data.get("metadata", {}).get("difficulty", MINING_DIFFICULTY)