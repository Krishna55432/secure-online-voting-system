import hashlib
import datetime
import json


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = str(timestamp)
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = str(self.index) + self.timestamp + str(self.data) + self.previous_hash + str(self.nonce)
        return hashlib.sha256(value.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_latest_block()

        new_block = Block(
            prev_block.index + 1,
            datetime.datetime.now(),
            data,
            prev_block.hash
        )

        difficulty = 3
        new_block.mine_block(difficulty)

        print("⛏️ Block mined:", new_block.hash)

        self.chain.append(new_block)
        self.save_chain()

    # 🔥 FULL VALIDATION WITH HASH DIFFERENCE
    def is_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            recalculated_hash = curr.calculate_hash()

            # Case 1: Data tampered
            if curr.hash != recalculated_hash:
                return False, i, curr.hash, recalculated_hash

            # Case 2: Chain broken
            if curr.previous_hash != prev.hash:
                return False, i, curr.previous_hash, prev.hash

        return True, -1, None, None

    def save_chain(self):
        with open("chain.json", "w") as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    def load_chain(self):
        try:
            with open("chain.json", "r") as f:
                data = json.load(f)
                self.chain = []

                for b in data:
                    block = Block(
                        b["index"],
                        b["timestamp"],
                        b["data"],
                        b["previous_hash"]
                    )
                    block.nonce = b.get("nonce", 0)
                    block.hash = b["hash"]
                    self.chain.append(block)

        except:
            self.chain = [self.create_genesis_block()]