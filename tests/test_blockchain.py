import unittest
from datetime import datetime, UTC
from src.blockchain import Blockchain, Block
from src.utils.helpers import calculate_hash
from config.settings import get_current_timestamp, get_user_id


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        """测试创世区块"""
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.previous_hash, "0")
        self.assertEqual(genesis.data["message"], "Genesis Block")

    def test_add_block(self):
        """测试添加区块"""
        data = {
            "message": "Test Block",
            "timestamp": get_current_timestamp(),
            "user_id": get_user_id()
        }
        new_block = self.blockchain.add_block(data)

        self.assertEqual(new_block.index, 1)
        self.assertEqual(new_block.data, data)
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_chain_validity(self):
        """测试区块链有效性"""
        self.assertTrue(self.blockchain.is_chain_valid())

        # 添加新区块
        self.blockchain.add_block({"message": "Test Block"})
        self.assertTrue(self.blockchain.is_chain_valid())

        # 篡改数据
        self.blockchain.chain[1].data["message"] = "Modified"
        self.assertFalse(self.blockchain.is_chain_valid())

    def test_mining(self):
        """测试挖矿"""
        block = Block(
            1,
            get_current_timestamp(),
            {"message": "Test Mining"},
            "0"
        )

        block.mine_block(2)
        self.assertTrue(block.hash.startswith("00"))


if __name__ == '__main__':
    unittest.main()