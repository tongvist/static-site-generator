import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_no_props(self):
        node_without_props = HTMLNode(tag="p", value="this is the value of the node") 
        self.assertEqual(node_without_props.props_to_html(), "")

    def test_props_start_with_space(self):
        node = HTMLNode(props={"href":"http://www.testing.url", "method":"POST"})
        self.assertTrue(" href" and " method" in node.props_to_html())

    def test_quotes_for_prop_values(self):
        node = HTMLNode(props={"href":"http://www.testing.url", "method":"POST"})
        self.assertTrue("\"http" and "url\"" and "\"POST\"" in node.props_to_html())


if __name__ == "__main__":
    unittest.main()
