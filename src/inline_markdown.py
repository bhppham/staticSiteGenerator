import re

from blocknode import BlockType, block_to_block_type
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


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


def markdown_to_blocks(markdown):
    blocks = list(markdown.split("\n\n"))
    filter(lambda x: x != "", blocks)
    blocks = list(map(lambda x: x.strip(), blocks))
    return blocks


def text_to_children(text):
    tNodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, tNodes))


def text_to_list_children(text, isOrdered):
    children_list = []
    delimiter = r"\d*\.." if isOrdered else r"-."
    items = re.split(delimiter, text)
    for item in items:
        item = item.strip()
        if item:
            children = text_to_children(item)
            children_list.append(ParentNode(tag="li", children=children))
    return children_list


def text_to_code_child(text):
    result = []
    children = text.split("```")
    for child in children:
        child = child.lstrip()
        if child:
            tNode = TextNode(text=child, text_type=TextType.CODE)
            result.append(text_node_to_html_node(tNode))
    return result


def html_node_from_block_type(blockType, value):
    if blockType == BlockType.CODE:
        return ParentNode(tag="pre", children=text_to_code_child(value))
    else:
        children = text_to_children(value)
        if blockType == BlockType.PARAGRAPH:
            no_new_line = value.replace("\n", " ")
            return ParentNode(tag="p", children=text_to_children(no_new_line))
        elif blockType == BlockType.HEADING:
            tag = f"h{value.count("#")}"
            return ParentNode(tag=tag, children=children)
        elif blockType == BlockType.QUOTE:
            return ParentNode(tag="blockquote", children=children)
        elif blockType == BlockType.UNORDERED_LIST:
            return ParentNode(tag="ul", children=text_to_list_children(block, False))
        elif blockType == BlockType.ORDERED_LIST:
            return ParentNode(tag="li", children=text_to_list_children(block, True))
        else:
            return ParentNode(tag="div", children=children)


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)

    all_children = []
    for block in md_blocks:
        bt = block_to_block_type(block)
        all_children.append(html_node_from_block_type(bt, block))
    return ParentNode(tag="div", children=all_children)
