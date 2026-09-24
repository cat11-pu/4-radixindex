"""legacy.py：重构前的旧实现（每个键一条记录），保留作对照。

旧实现的 insert/find/scan 都要扫一遍已有的全部记录，
十万个同前缀键就是十万条记录、插入成本随键数线性增长。
"""
from __future__ import annotations


class LegacyIndex:
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
