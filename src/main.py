import shutil

from htmlnode import LeafNode
from inline_markdown import markdown_to_html_node
from textnode import TextNode, TextType

if __name__ == "__main__":
    tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(tn)

    markdown = """
- First Item
- Second Item
- Third Item
    """

    markdown_to_html_node(markdown)

    shutil.rmtree("../public/")
