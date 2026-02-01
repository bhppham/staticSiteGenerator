import unittest

from htmlnode import HTMLNode


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
