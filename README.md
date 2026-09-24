# radixindex

纯 Python 标准库的 radixindex（无第三方依赖，没有 pip 也能跑）。

## 结构

- `radix.py`：`RadixTree`，压缩前缀树。每个节点携带一段公共前缀，
  同前缀的键共享路径，节点数 ≈ 不同公共前缀片段数（远小于逐键记录）。
  `insert` / `find` 沿前缀逐层比较并累计 `visits`；`scan(low, high)`
  左闭右开、结果升序；`node_count()` 返回节点数。
- `index.py`：对外的 `Index`，内部走 `RadixTree`。`entries` 仍是有序
  列表（老工具在遍历），公开方法签名不变。
- `legacy.py`：`LegacyIndex`，重构前的旧实现（每键一条记录），仅作对照。

## 用法

    from radix import RadixTree
    from index import Index

    tree = RadixTree(["user:profile:0001", "user:profile:0002"])
    tree.insert("user:profile:0003")
    tree.find("user:profile:0002")          # True
    tree.scan("user:profile:0001", "user:profile:0003")  # 左闭右开，升序
    tree.node_count(), tree.visits

    index = Index(["b2", "b1", "a1"])
    index.entries                           # 有序列表：['a1', 'b1', 'b2']
    index.scan("a1", "c")                   # ['a1', 'b1', 'b2']

## 测试

    python3 -m unittest discover -s tests -v

## 场景自检

    python3 check_sample.py
