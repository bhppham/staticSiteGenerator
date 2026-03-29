import re

from textnode import TextNode, TextType


def split_nodes_delimiter(nodes, delimiter, textType):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        sp = node.text.split(delimiter)
        num_delimiter = len(sp)
        if num_delimiter % 2 == 0:
            raise ValueError(
                f"Syntax error {node.text} has wrong number of delimiters {delimiter}"
            )
        for i in range(num_delimiter):
            if sp[i] == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(sp[i], TextType.TEXT))
            else:
                result.append(TextNode(sp[i], textType))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        txt = node.text
        while txt != "":
            images = extract_markdown_images(txt)
            if not images:
                result.append(TextNode(txt, TextType.TEXT))
                txt = ""
            else:
                sp = txt.split(f"![{"](".join(images[0])})")
                if sp[0] != "":
                    result.append(TextNode(sp[0], TextType.TEXT))
                result.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
                txt = sp[1]
    return result


def split_nodes_link(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        txt = node.text
        while txt != "":
            links = extract_markdown_links(txt)
            if not links:
                result.append(TextNode(txt, TextType.TEXT))
                txt = ""
            else:
                sp = txt.split(f"[{"](".join(links[0])})")
                if sp[0] != "":
                    result.append(TextNode(sp[0], TextType.TEXT))
                result.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
                txt = sp[1]
    return result


def text_to_textnodes(text):
    result = [TextNode(text, TextType.TEXT)]
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result
