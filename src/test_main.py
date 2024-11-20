from textnode import TextNode, TextType
from leafnode import LeafNode
from main import text_node_to_html_node, split_nodes_delimiter
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

    def test_split_nodes_delimiter_code_in_middle(self):
        code_node = TextNode("This has a `code block` in the middle", TextType.NORMAL)
        expected = [
                        TextNode("This has a ", TextType.NORMAL), 
                        TextNode("code block", TextType.CODE), 
                        TextNode(" in the middle", TextType.NORMAL)
                    ]
        self.assertEqual(split_nodes_delimiter([code_node], "`", TextType.CODE), expected)

    def test_split_nodes_delimiter_bold_in_middle(self):
        bold_node = TextNode("This has a **bold word** in the middle", TextType.BOLD)
        expected_bold = [
                        TextNode("This has a ", TextType.NORMAL), 
                        TextNode("bold word", TextType.BOLD), 
                        TextNode(" in the middle", TextType.NORMAL)
                    ]
        self.assertEqual(split_nodes_delimiter([bold_node], "**", TextType.BOLD), expected_bold)

    def test_split_nodes_delimiter_starts_with_tag(self):
        starts_with_tag = TextNode("**This** starts with a bold word", TextType.BOLD)
        expected_bold_2 = [
                            TextNode("This", TextType.BOLD), 
                            TextNode(" starts with a bold word", TextType.NORMAL), 
                    ]
        self.assertEqual(split_nodes_delimiter([starts_with_tag], "**", TextType.BOLD), expected_bold_2)

    def test_split_nodes_delimiter_starts_with_short_tag(self):
        starts_with_tag = TextNode("`This starts` with a code block", TextType.CODE)
        expected = [
                    TextNode("This starts", TextType.CODE), 
                    TextNode(" with a code block", TextType.NORMAL), 
                    ]
        self.assertEqual(split_nodes_delimiter([starts_with_tag], "`", TextType.CODE), expected)

    def test_split_nodes_delimiter_ends_with_tag(self):
        ends_with_tag = TextNode("This ends with a *italic block*", TextType.ITALIC)
        expected = [
                    TextNode("This ends with a ", TextType.NORMAL), 
                    TextNode("italic block", TextType.ITALIC), 
                    ]
        self.assertEqual(split_nodes_delimiter([ends_with_tag], "*", TextType.ITALIC), expected)

if __name__ == "__main__":
    unittest.main()
