from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props=None)
        self.children = children

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag for ParentNode -object")

        if not self.children:
            raise ValueError("Missing children for ParentNode -object")

        html_string = f"<{self.tag}>"
        for child_node in self.children:
            html_string += f"{child_node.to_html()}"

        return f"{html_string}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.props})"
