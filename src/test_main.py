from textnode import TextNode, TextType
from leafnode import LeafNode
from main import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images
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
        bold_node = TextNode("This has a **bold word** in the middle", TextType.NORMAL)
        expected_bold = [
                        TextNode("This has a ", TextType.NORMAL), 
                        TextNode("bold word", TextType.BOLD), 
                        TextNode(" in the middle", TextType.NORMAL)
                    ]
        self.assertEqual(split_nodes_delimiter([bold_node], "**", TextType.BOLD), expected_bold)

    def test_split_nodes_delimiter_starts_with_tag(self):
        starts_with_tag = TextNode("**This** starts with a bold word", TextType.NORMAL)
        expected_bold_2 = [
                            TextNode("This", TextType.BOLD), 
                            TextNode(" starts with a bold word", TextType.NORMAL), 
                    ]
        self.assertEqual(split_nodes_delimiter([starts_with_tag], "**", TextType.BOLD), expected_bold_2)

    def test_split_nodes_delimiter_starts_with_short_tag(self):
        starts_with_tag = TextNode("`This starts` with a code block", TextType.NORMAL)
        expected = [
                    TextNode("This starts", TextType.CODE), 
                    TextNode(" with a code block", TextType.NORMAL), 
                    ]
        self.assertEqual(split_nodes_delimiter([starts_with_tag], "`", TextType.CODE), expected)

    def test_split_nodes_delimiter_ends_with_tag(self):
        ends_with_tag = TextNode("This ends with a *italic block*", TextType.NORMAL)
        expected = [
                    TextNode("This ends with a ", TextType.NORMAL), 
                    TextNode("italic block", TextType.ITALIC), 
                    ]
        self.assertEqual(split_nodes_delimiter([ends_with_tag], "*", TextType.ITALIC), expected)

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("This ends with a **bold block**", TextType.NORMAL)
        node2 = TextNode("This has a **bold block** in the middle", TextType.NORMAL)
        expected = [
                    TextNode("This ends with a ", TextType.NORMAL), 
                    TextNode("bold block", TextType.BOLD), 
                    TextNode("This has a ", TextType.NORMAL),
                    TextNode("bold block", TextType.BOLD),
                    TextNode(" in the middle", TextType.NORMAL)
                    ]
        self.assertEqual(split_nodes_delimiter([node1, node2], "**", TextType.BOLD), expected)

    def test_split_nodes_delimiter_no_delimiter_in_text(self):
        without_delimiter = TextNode("This has no delimiters", TextType.NORMAL)
        expected = [
                    TextNode("This has no delimiters", TextType.NORMAL) 
                    ]
        self.assertEqual(split_nodes_delimiter([without_delimiter], "*", TextType.NORMAL), expected)

    def test_split_nodes_delimiter_text_type_other_than_normal(self):
        node = TextNode("This is all italic", TextType.ITALIC)
        node2 = TextNode("**This should be bold**", TextType.NORMAL)
        expected = [
                    TextNode("This is all italic", TextType.ITALIC),
                    TextNode("This should be bold", TextType.BOLD)
                    ]
        self.assertEqual(split_nodes_delimiter([node, node2], "**", TextType.BOLD), expected)

    def test_split_nodes_delimiter_missing_closing_delimiter(self):
        missing_closing_tag = TextNode("This **bold was not closed", TextType.NORMAL)
        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([missing_closing_tag], "**", TextType.BOLD)
        self.assertTrue("invalid markdown" in str(e.exception).lower())

    def test_split_nodes_delimiter_many_tags_in_text(self):
        node = TextNode("**This** has many **tags**", TextType.NORMAL)
        node2 = TextNode("**This should be bold**", TextType.NORMAL)
        expected = [
                    TextNode("This", TextType.BOLD),
                    TextNode(" has many ", TextType.NORMAL),
                    TextNode("tags", TextType.BOLD),
                    TextNode("This should be bold", TextType.BOLD),
                    ]
        self.assertEqual(split_nodes_delimiter([node, node2], "**", TextType.BOLD), expected)

    def test_extract_markdown_images_normal_cases(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

        text2 = "This is text with a link ![to boot dev](https://www.boot.dev)"

        expected2 = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_images(text2), expected2)

if __name__ == "__main__":
    unittest.main()
