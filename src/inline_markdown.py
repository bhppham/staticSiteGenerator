from textnode import TextNode, TextType


def split_nodes_delimiter(nodes, delimiter, textType):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        if delimiter not in node.text:
            raise ValueError(f"delimiter {delimiter} not found in text: {node.text}")
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
