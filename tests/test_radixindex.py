import json
import os
import unittest

from index import Index
from radix import RadixTree


class TestIndex(unittest.TestCase):
    def test_entries_available(self):
        self.assertEqual(Index(["ab", "ac"]).entries, ["ab", "ac"])

    def test_insert_and_find(self):
        index = Index(["ab"])
        self.assertTrue(index.find("ab"))
        self.assertFalse(index.find("zz"))

    def test_insert_duplicate(self):
        self.assertFalse(Index(["ab"]).insert("ab"))

    def test_scan_half_open(self):
        self.assertEqual(Index(["a", "b", "c"]).scan("a", "c"), ["a", "b"])

    def test_scan_sorted(self):
        index = Index(["b2", "b1", "a1"])
        self.assertEqual(index.scan("a1", "c"), ["a1", "b1", "b2"])


class TestRadixTree(unittest.TestCase):
    def test_insert_and_find(self):
        tree = RadixTree(["abc", "abd"])
        self.assertTrue(tree.find("abc"))
        self.assertTrue(tree.find("abd"))
        self.assertFalse(tree.find("ab"))
        self.assertFalse(tree.find("abcd"))
        self.assertFalse(tree.find("z"))

    def test_insert_duplicate(self):
        tree = RadixTree(["ab"])
        self.assertFalse(tree.insert("ab"))
        self.assertTrue(tree.insert("ac"))

    def test_insert_prefix_of_existing_key(self):
        tree = RadixTree(["abc"])
        self.assertTrue(tree.insert("ab"))
        self.assertTrue(tree.find("ab"))
        self.assertTrue(tree.find("abc"))

    def test_scan_half_open_and_sorted(self):
        tree = RadixTree(["user:profile:0002", "user:profile:0001", "order:0001"])
        self.assertEqual(
            tree.scan("user:profile:0001", "user:profile:0003"),
            ["user:profile:0001", "user:profile:0002"],
        )

    def test_scan_empty_range(self):
        tree = RadixTree(["a", "b"])
        self.assertEqual(tree.scan("b", "a"), [])
        self.assertEqual(tree.scan("a", "a"), [])

    def test_node_count_counts_edge_chars(self):
        # "ab"/"ac" 压缩成边 "a"、"b"、"c"，共 3 个字符节点
        self.assertEqual(RadixTree(["ab", "ac"]).node_count(), 3)

    def test_visits_count_key_chars(self):
        tree = RadixTree(["abc"])
        self.assertEqual(tree.visits, 3)
        tree.insert("abd")
        self.assertEqual(tree.visits, 6)


class TestSampleScenario(unittest.TestCase):
    """sample/keys.json 的验收数值。"""

    @classmethod
    def setUpClass(cls):
        path = os.path.join(os.path.dirname(__file__), "..", "sample", "keys.json")
        with open(path, encoding="utf-8") as handle:
            cls.spec = json.load(handle)
        cls.tree = RadixTree(cls.spec["keys"])
        for key in cls.spec["inserts"]:
            cls.tree.insert(key)

    def test_scan_results(self):
        results = [(p[0], p[1], self.tree.scan(p[0], p[1])) for p in self.spec["scans"]]
        self.assertEqual(
            results,
            [
                ("user:profile:0001", "user:profile:0004",
                 ["user:profile:0001", "user:profile:0002", "user:profile:0003"]),
                ("order:0001", "order:9999",
                 ["order:0001", "order:0002", "order:0003"]),
            ],
        )

    def test_node_count(self):
        self.assertEqual(self.tree.node_count(), 48)

    def test_visits(self):
        self.assertEqual(self.tree.visits, 183)


if __name__ == "__main__":
    unittest.main()
