import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "link")
        self.assertNotEqual(node, node2)

    def test_not_eq_2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_not_eq_3(self):
        node = TextNode("This is a node", TextType.PLAIN)
        node2 = TextNode("This is a plain node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a node", TextType.PLAIN, None)
        node2 = TextNode("This is a node", TextType.PLAIN)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
