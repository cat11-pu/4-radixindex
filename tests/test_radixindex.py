import unittest

from index import Index


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


if __name__ == "__main__":
    unittest.main()
