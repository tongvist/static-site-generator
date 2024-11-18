from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=None)
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("Missing value for node")

        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

