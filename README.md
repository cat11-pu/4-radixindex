# radixindex

纯 Python 标准库的 radixindex（无第三方依赖，没有 pip 也能跑）。

## 用法

```python
from radix import RadixTree
from index import Index

tree = RadixTree(["user:profile:0001", "user:profile:0002"])
tree.insert("order:0001")
tree.find("user:profile:0001")          # True
tree.scan("user:profile:0001", "user:profile:0003")  # 左闭右开，升序
tree.node_count()                       # 按字符展开的节点数
tree.visits                             # insert / find 访问的字符数

index = Index(["b", "a"])               # 对外索引，内部走 RadixTree
index.entries                           # 有序列表，老工具可以直接遍历
```

## 测试

    python3 -m unittest discover -s tests -v

## 场景自检

    python3 check_sample.py
