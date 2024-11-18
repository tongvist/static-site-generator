from textnode import TextNode, TextType
from leafnode import LeafNode

def main():
    link_node = TextNode("This is a link node", TextType.LINK, "http://www.testing.dev")
    print(text_node_to_html_node(link_node).to_html())

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise AttributeError("Invalid text type")

    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise Exception("Missing url for a link node")

        return LeafNode("a", text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise Exception("Missing url for a image node")
        return LeafNode("img", "", props={"src": text_node.url, "alt":text_node.text})

if __name__ == "__main__":
    main()
