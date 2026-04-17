class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        return ""

    def __repr__(self):
        return f"tag={self.tag} value={self.value} children={self.children} props={self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode has to have a value")
        if not self.tag:
            return str(self.value)
        return f"<{self.tag}{" " if self.props else ""}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"tag={self.tag} value={self.value} props={self.props}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode has to have a tag")
        if not self.children:
            raise ValueError("ParentNode has to have children")
        html = f"<{self.tag}{" " if self.props else ""}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
