"""把 sample/keys.json 跑一遍，打印验收面（树、对外索引、旧实现对照）。"""
import json
import os
import sys

from index import Index
from legacy import LegacyIndex
from radix import RadixTree


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "keys.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)

    tree = RadixTree(spec["keys"])
    for key in spec["inserts"]:
        tree.insert(key)
    results = [(pair[0], pair[1], tree.scan(pair[0], pair[1])) for pair in spec["scans"]]
    print("树上的扫描结果 =", results)
    print("树节点数 =", tree.node_count())
    print("树访问计数 =", tree.visits)

    index = Index(spec["keys"])
    for key in spec["inserts"]:
        index.insert(key)
    print("对外索引的扫描结果 =", index.scan(spec["scans"][0][0], spec["scans"][0][1]))
    print("entries 属性仍在且有序 =", index.entries == sorted(index.entries))

    legacy = LegacyIndex()
    for key in spec["keys"]:
        legacy.insert(key)
    print("旧实现的 visit 计数 =", legacy.visits)

    print("键数 =", len(index.entries))
    common = spec.get("common_prefix", "")
    print("共享公共前缀的键数 =", sum(1 for key in index.entries if key.startswith(common)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
