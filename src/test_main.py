from textnode import TextNode, TextType
from leafnode import LeafNode
from main import text_node_to_html_node
import unittest

class TestMain(unittest.TestCase):
    def test_text_node_to_html_node_plain_text(self):
        node = TextNode("This is the text value", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is the text value")
        self.assertEqual(html_node.tag, None)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is the text value", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is the text value")
        self.assertEqual(html_node.tag, "b")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is the text value", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is the text value")
        self.assertEqual(html_node.tag, "i")

    def test_text_node_to_html_node_link(self):
        node = TextNode("This is the text value", TextType.LINK, "http://testing.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is the text value")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], node.url)

    def test_text_node_to_html_node_link_missing_url(self):
        node = TextNode("This is the text value", TextType.LINK)
        with self.assertRaises(Exception) as e:
            text_node_to_html_node(node)
        self.assertTrue("missing url" and "link" in str(e.exception).lower())

    def test_text_node_to_html_node_image_missing_url(self):
        node = TextNode("This is the text value", TextType.IMAGE)
        with self.assertRaises(Exception) as e:
            text_node_to_html_node(node)
        self.assertTrue("missing url" and "image" in str(e.exception).lower())

    def test_text_node_to_html_node_invalid_type(self):
        node = TextNode("This is the text value", "http://testing.dev")
        with self.assertRaises(AttributeError) as e:
            text_node_to_html_node(node)
        self.assertTrue("invalid text type" in str(e.exception).lower())

if __name__ == "__main__":
    unittest.main()
