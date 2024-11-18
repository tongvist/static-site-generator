from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=None)
        self.children = children

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid HTML: Missing tag for ParentNode -object")

        if not self.children:
            raise ValueError("Invalid HTML: Missing children for ParentNode -object")

        html_string = f"<{self.tag}>"

        for child_node in self.children:
            html_string += child_node.to_html()

        return f"{html_string}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.props})"
