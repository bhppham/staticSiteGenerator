import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # def test_to_html(self):
    #     html = HTMLNode()
    #     self.assertRaises(NotImplementedError, html.to_html())

    def test_props_to_html(self):
        paragraph = HTMLNode(
            "p", "some text", None, {"class": "color-white", "background-color": "#000"}
        )
        self.assertEqual(
            'class="color-white" background-color="#000"', paragraph.props_to_html()
        )

    def test_props_to_html_2(self):
        nullNode = HTMLNode("p", "some text")
        self.assertEqual("", nullNode.props_to_html())

    def test_props_to_html_3(self):
        someNode = HTMLNode(
            "p", "some text", props={"onClick": '()=>{alert("hello");}'}
        )
        self.assertEqual('onClick="()=>{alert("hello");}"', someNode.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node(self):
        paragraph = LeafNode(
            "p", "some text", {"class": "color-white", "background-color": "#000"}
        )
        self.assertEqual(
            '<p class="color-white" background-color="#000">some text</p>',
            paragraph.to_html(),
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
