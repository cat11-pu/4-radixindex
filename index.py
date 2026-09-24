"""index.py：对外的前缀索引（老工具会读 entries 属性）。

内部走 radix.py 的压缩前缀树；entries 仍然是有序列表，公开方法签名不变。
LegacyIndex 是改造前的旧实现（每个键一条记录），保留作对照。
"""
from __future__ import annotations

from bisect import insort

from radix import RadixTree


class Index:
    def __init__(self, keys=()):
        self._tree = RadixTree(keys)
        self.entries = sorted(dict.fromkeys(keys))

    @property
    def visits(self) -> int:
        return self._tree.visits

    @visits.setter
    def visits(self, value: int) -> None:
        self._tree.visits = value

    def insert(self, key: str) -> bool:
        inserted = self._tree.insert(key)
        if inserted:
            insort(self.entries, key)
        return inserted

    def find(self, key: str) -> bool:
        return self._tree.find(key)

    def scan(self, low: str, high: str) -> list:
        return self._tree.scan(low, high)

    def node_count(self) -> int:
        return self._tree.node_count()


class LegacyIndex:
    """旧实现：每个键一条记录，查找和扫描都遍历全表。保留作对照。"""

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
