"""index.py：对外的前缀索引（老工具会读 entries 属性）。"""
from __future__ import annotations


class Index:
    def __init__(self, keys=()):
        self.entries = list(dict.fromkeys(keys))
        self.entries.sort()
        self.visits = 0

    def insert(self, key: str) -> bool:
        self.visits += len(self.entries)
        if key in self.entries:
            return False
        self.entries.append(key)
        self.entries.sort()
        return True

    def find(self, key: str) -> bool:
        self.visits += len(self.entries)
        return key in self.entries

    def scan(self, low: str, high: str) -> list:
        out = []
        for key in self.entries:
            self.visits += 1
            if low <= key < high:
                out.append(key)
        return out

    def node_count(self) -> int:
        return len(self.entries)
