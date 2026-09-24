"""radix.py：压缩前缀树（radix tree）。

边存一段公共前缀（字符串片段），insert / find / scan 都沿着边逐字符比较。
节点数远小于键数：十万个同前缀的键只共享一段前缀边和少量分叉边。

visits 记录在 insert / find 中访问（比较或写入）的字符数；
node_count() 返回按字符展开的节点数，即每条边上的每个字符计一个节点。
"""
from __future__ import annotations


class _Node:
    __slots__ = ("label", "children", "terminal")

    def __init__(self, label: str):
        self.label = label          # 父节点到本节点的边上的公共前缀片段
        self.children = {}          # 子边的首字符 -> _Node
        self.terminal = False       # 是否有键恰好结束在本节点


def _match_length(label: str, key: str, i: int) -> int:
    """label 与 key[i:] 的公共前缀长度。"""
    matched = 0
    limit = min(len(label), len(key) - i)
    while matched < limit and label[matched] == key[i + matched]:
        matched += 1
    return matched


class RadixTree:
    def __init__(self, keys=()):
        self._root = _Node("")
        self.visits = 0
        for key in keys:
            self.insert(key)

    def insert(self, key: str) -> bool:
        """插入键；已存在返回 False。每个字符要么沿边比较一次，要么写进新边。"""
        node = self._root
        i = 0
        n = len(key)
        while i < n:
            first = key[i]
            child = node.children.get(first)
            if child is None:
                leaf = _Node(key[i:])
                leaf.terminal = True
                node.children[first] = leaf
                self.visits += n - i
                return True
            label = child.label
            matched = _match_length(label, key, i)
            self.visits += matched
            if matched == len(label):
                i += matched
                node = child
                continue
            # 在 matched 处把边劈成两段：公共前缀下沉为新节点
            mid = _Node(label[:matched])
            mid.children[label[matched]] = child
            child.label = label[matched:]
            node.children[first] = mid
            rest = key[i + matched:]
            if rest:
                leaf = _Node(rest)
                leaf.terminal = True
                mid.children[rest[0]] = leaf
                self.visits += len(rest)
            else:
                mid.terminal = True
            return True
        if node.terminal:
            return False
        node.terminal = True
        return True

    def find(self, key: str) -> bool:
        """沿边逐字符比较；键恰好落在终端节点上返回 True。"""
        node = self._root
        i = 0
        n = len(key)
        while i < n:
            child = node.children.get(key[i])
            if child is None:
                return False
            label = child.label
            matched = _match_length(label, key, i)
            self.visits += matched
            if matched < len(label):
                return False
            i += matched
            node = child
        return node.terminal

    def scan(self, low: str, high: str) -> list:
        """返回 [low, high) 区间内的键，升序；空区间返回空列表。"""
        if low >= high:
            return []
        out = []

        def walk(node: _Node, prefix: str) -> None:
            if prefix >= high:
                return  # 子树里所有的键都以 prefix 开头，必然都 >= high
            if node.terminal and low <= prefix:
                out.append(prefix)
            for first in sorted(node.children):
                child = node.children[first]
                walk(child, prefix + child.label)

        walk(self._root, "")
        return out

    def node_count(self) -> int:
        """按字符展开的节点数：每条边上的每个字符计一个节点。"""
        total = 0
        stack = [self._root]
        while stack:
            node = stack.pop()
            total += len(node.label)
            stack.extend(node.children.values())
        return total
