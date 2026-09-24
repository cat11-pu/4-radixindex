"""radix.py：压缩前缀树。

每个节点携带「从根到该节点的一段公共前缀」，同前缀的键共享路径，
不再像旧实现那样每个键占一条独立记录。节点数 ≈ 所有键的不同
公共前缀片段数，而不是键数。

- insert / find：沿前缀逐层比较，visits 记录访问的节点/字符数；
- scan(low, high)：左闭右开，结果升序，空区间返回空列表；
- node_count()：返回节点数（不含根）。
"""
from __future__ import annotations


class _Node:
    __slots__ = ("prefix", "children", "terminal")

    def __init__(self, prefix: str):
        self.prefix = prefix       # 从根到该节点的公共前缀片段
        self.children = {}         # 下一个字符 -> 子节点
        self.terminal = False      # 是否有键恰好落在该前缀上


class RadixTree:
    def __init__(self, keys=()):
        self._root = _Node("")
        self._nodes = 0
        self._size = 0
        self.visits = 0
        for key in keys:
            self.insert(key)

    def insert(self, key: str) -> bool:
        node = self._root
        for ch in key:
            self.visits += 1
            child = node.children.get(ch)
            if child is None:
                child = _Node(node.prefix + ch)
                node.children[ch] = child
                self._nodes += 1
            node = child
        if node.terminal:
            return False
        node.terminal = True
        self._size += 1
        return True

    def find(self, key: str) -> bool:
        node = self._root
        for ch in key:
            self.visits += 1
            node = node.children.get(ch)
            if node is None:
                return False
        return node.terminal

    def scan(self, low: str, high: str) -> list:
        out = []
        if low >= high:
            return out

        def walk(node: _Node) -> None:
            if node.terminal and low <= node.prefix < high:
                out.append(node.prefix)
            for ch in sorted(node.children):
                walk(node.children[ch])

        walk(self._root)
        return out

    def node_count(self) -> int:
        return self._nodes

    def __len__(self) -> int:
        return self._size
