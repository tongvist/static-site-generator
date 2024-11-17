import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_missing_value(self):
        # All leafnodes must have a value
        leaf = LeafNode("p", value="")
        self.assertRaises(ValueError, leaf.to_html)

    def test_check_output_with_tag(self):
        leaf = LeafNode(tag = "p", value = "text value for node")
        self.assertTrue(f"<{leaf.tag}>" and f"</{leaf.tag}>" in leaf.to_html())


if __name__ == "__main__":
    unittest.main()
