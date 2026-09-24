"""index.py：对外的前缀索引。

内部走 radix.RadixTree（共享公共前缀，节点数远小于逐键记录）；
兼容约束：entries 仍是有序列表（老工具在遍历），公开方法签名不变。
"""
from __future__ import annotations

from bisect import insort

from radix import RadixTree


class Index:
    def __init__(self, keys=()):
        self._tree = RadixTree()
        self.entries = []
        for key in keys:
            self.insert(key)

    @property
    def visits(self) -> int:
        return self._tree.visits

    def insert(self, key: str) -> bool:
        if not self._tree.insert(key):
            return False
        insort(self.entries, key)
        return True

    def find(self, key: str) -> bool:
        return self._tree.find(key)

    def scan(self, low: str, high: str) -> list:
        return self._tree.scan(low, high)

    def node_count(self) -> int:
        return self._tree.node_count()
