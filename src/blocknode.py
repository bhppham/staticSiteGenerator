import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CONTAINER = "container"


def block_to_block_type(block):
    if re.fullmatch(r"^---(?:\s+.*)?(?:\n.*)?$", block, flags=re.S):
        return BlockType.CONTAINER
    elif re.fullmatch(r"^\#{1,6} .*$", block, flags=re.M):
        return BlockType.HEADING
    elif re.fullmatch(r".*\x60{3}.*\x60{3}.*", block, flags=re.DOTALL):
        return BlockType.CODE
    elif re.fullmatch(r"^>.*$", block, flags=re.M | re.S):
        return BlockType.QUOTE
    elif re.fullmatch(r"^-.*$", block, flags=re.M | re.S):
        return BlockType.UNORDERED_LIST
    elif re.fullmatch(r"^\d*\..*$", block, flags=re.M | re.S):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
