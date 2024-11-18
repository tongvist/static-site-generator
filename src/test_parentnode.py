import unittest
from parentnode import ParentNode
from leafnode import LeafNode
from htmlnode import HTMLNode

class TestParentNode(unittest.TestCase):
    def test_only_leaf_nodes(self):
        node1 = LeafNode("b", "Bold Text")
        node2 = LeafNode(None, "Normal text")
        node3 = LeafNode("i", "Italic text")

        node = ParentNode(tag = "p", children = [node1, node2, node3])

        expected = "<p><b>Bold Text</b>Normal text<i>Italic text</i></p>"
        self.assertTrue(node.to_html() == expected)

    def test_with_nested_children(self):
        node1 = LeafNode("b", "Bold Text")
        node2 = LeafNode(None, "Normal text")
        node3 = LeafNode("p", "Paragraph Node")
        node4 = LeafNode("p", "Second paragraph")

        node5 = ParentNode("div", [node3, node4])

        node = ParentNode(tag = "div", children = [node1, node2, node5])

        expected = "<div><b>Bold Text</b>Normal text<div><p>Paragraph Node</p><p>Second paragraph</p></div></div>"
        self.assertTrue(node.to_html() == expected)

    def test_missing_tag(self):
        node1 = LeafNode("b", "Bold Text")
        node2 = LeafNode(None, "Normal text")
        node = ParentNode(tag="", children=[node1, node2])

        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertTrue("missing tag" in str(e.exception).lower())

    def test_missing_children(self):
        node1 = LeafNode("b", "Bold Text")
        node2 = LeafNode(None, "Normal text")
        node = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertTrue("missing children" in str(e.exception).lower())

if __name__ == "__main__":
    unittest.main()
