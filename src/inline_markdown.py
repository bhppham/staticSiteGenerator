import re

from blocknode import BlockType, block_to_block_type
from htmlnode import ParentNode
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


def extract_container_blocks(markdown):
    lines = markdown.split("\n")
    containers = []
    outside_lines = []
    in_container = False
    container_header = ""
    container_lines = []

    for line in lines:
        if in_container:
            if line.startswith("---"):
                container_content = "\n".join(container_lines).strip()
                if container_content:
                    containers.append(f"{container_header}\n{container_content}")
                else:
                    containers.append(container_header)
                placeholder = f"__CONTAINER_BLOCK_{len(containers) - 1}__"
                if outside_lines and outside_lines[-1] != "":
                    outside_lines.append("")
                outside_lines.append(placeholder)
                outside_lines.append("")
                in_container = False
                container_header = ""
                container_lines = []
            else:
                container_lines.append(line)
        else:
            if line.startswith("---"):
                in_container = True
                container_header = line.strip()
                container_lines = []
            else:
                outside_lines.append(line)

    if in_container:
        container_content = "\n".join(container_lines).strip()
        if container_content:
            containers.append(f"{container_header}\n{container_content}")
        else:
            containers.append(container_header)
        placeholder = f"__CONTAINER_BLOCK_{len(containers) - 1}__"
        if outside_lines and outside_lines[-1] != "":
            outside_lines.append("")
        outside_lines.append(placeholder)
        outside_lines.append("")

    outside_markdown = "\n".join(outside_lines)
    return outside_markdown, containers


def markdown_to_blocks(markdown):
    outside_markdown, containers = extract_container_blocks(markdown)
    blocks = list(outside_markdown.split("\n\n"))
    blocks = list(map(lambda x: x.strip(), blocks))
    blocks = [block for block in blocks if block != ""]

    result = []
    for block in blocks:
        match = re.fullmatch(r"__CONTAINER_BLOCK_(\d+)__", block)
        if match:
            result.append(containers[int(match.group(1))])
        else:
            result.append(block)
    return result


def text_to_children(text):
    tNodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, tNodes))


def text_to_list_children(text, isOrdered):
    children_list = []
    items = text.split("\n")
    for item in items:
        item = item.strip()
        if not item:
            continue
        if isOrdered:
            item = re.sub(r"^\d+\.\s*", "", item, count=1)
        else:
            item = re.sub(r"^-\s*", "", item, count=1)
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
            match = re.match(r"^(#{1,6})\s+(.*)$", value.strip())
            if not match:
                return ParentNode(tag="p", children=text_to_children(value.strip()))
            tag = f"h{len(match.group(1))}"
            heading_text = match.group(2).strip()
            return ParentNode(tag=tag, children=text_to_children(heading_text))
        elif blockType == BlockType.QUOTE:
            quote_text = "\n".join(
                [re.sub(r"^>\s?", "", line) for line in value.split("\n")]
            )
            return ParentNode(tag="blockquote", children=text_to_children(quote_text))
        elif blockType == BlockType.UNORDERED_LIST:
            return ParentNode(tag="ul", children=text_to_list_children(value, False))
        elif blockType == BlockType.ORDERED_LIST:
            return ParentNode(tag="ol", children=text_to_list_children(value, True))
        elif blockType == BlockType.CONTAINER:
            header, content = (value.split("\n", 1) + [""])[:2]
            class_name = header[3:].strip()
            content = content.strip()
            if not content:
                raise ValueError("Container block must have content")
            nested_root = markdown_to_html_node(content)
            props = {"class": class_name} if class_name else None
            return ParentNode(tag="div", children=nested_root.children, props=props)
        else:
            return ParentNode(tag="div", children=children)


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)

    all_children = []
    for block in md_blocks:
        bt = block_to_block_type(block)
        all_children.append(html_node_from_block_type(bt, block))
    return ParentNode(tag="div", children=all_children)
