import unittest
from src.markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item
* This is a second list item
* This is a third list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item\n* This is a second list item\n* This is a third list item",
            ],
        )

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
# Heading


Paragraph 1



Paragraph 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Paragraph 1", "Paragraph 2"])

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Not a heading (missing space)
        self.assertEqual(block_to_block_type("#NotHeading"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        code_block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        quote_block = ">Line one\n>Line two\n> Line three"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        ul_star = "* Item 1\n* Item 2\n* Item 3"
        ul_dash = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(ul_star), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ul_dash), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        ol_block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST)
        # Invalid sequence (not starting at 1 or skipping numbers)
        invalid_ol = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(invalid_ol), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        p_block = "Just a standard paragraph with no special markdown prefix."
        self.assertEqual(block_to_block_type(p_block), BlockType.PARAGRAPH)

    def test_markdown_to_html_node_heading(self):
        md = "# Main Header\n\n### Sub Header"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Main Header</h1><h3>Sub Header</h3></div>",
        )

    def test_markdown_to_html_node_paragraph_with_inline(self):
        md = "This is **bold** and *italic* with `code`."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bold</b> and <i>italic</i> with <code>code</code>.</p></div>",
        )

    def test_markdown_to_html_node_code_block(self):
        md = "```\ndef hello():\n    return 'world'\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>def hello():\n    return 'world'\n</code></pre></div>",
        )

    def test_markdown_to_html_node_quote(self):
        md = "> Not all those who wander are lost.\n> — J.R.R. Tolkien"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>Not all those who wander are lost. — J.R.R. Tolkien</blockquote></div>",
        )

    def test_markdown_to_html_node_lists(self):
        md = "* Item A\n* Item B\n\n1. First item\n2. Second item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item A</li><li>Item B</li></ul><ol><li>First item</li><li>Second item</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
