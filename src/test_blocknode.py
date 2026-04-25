import unittest

from blocknode import BlockType, block_to_block_type


class TestBlockNode(unittest.TestCase):
    def test_heading_type(self):
        block = "### Heading 3"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.HEADING)

    def test_code_type(self):
        block = "```\nsome code\n```"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.CODE)

    def test_quote_type(self):
        block = "> first line quote\n>second\n>third"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.QUOTE)

    def test_unordered_list_type(self):
        block = "- first\n- second\n- third"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.UNORDERED_LIST)

    def test_ordered_list_type(self):
        block = "1. first\n2. second\n3. third"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.ORDERED_LIST)

    def test_paragraph_type(self):
        block = " first\n second\n third"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.PARAGRAPH)

    def test_heading_without_space_is_paragraph(self):
        block = "#Heading"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.PARAGRAPH)

    def test_ordered_list_non_sequential_still_ordered_type(self):
        block = "1. first\n4. second\n10. third"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.ORDERED_LIST)

    def test_code_block_with_surrounding_text_is_code_type(self):
        block = "before\n```\ncode\n```\nafter"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.CODE)

    def test_container_type_without_class(self):
        block = "---\nSome content"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.CONTAINER)

    def test_container_type_with_class(self):
        block = "--- hero\nSome content"
        t = block_to_block_type(block)
        self.assertEqual(t, BlockType.CONTAINER)
