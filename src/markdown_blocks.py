from enum import Enum
from src.htmlnode import LeafNode, ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        if block != "":
            filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) >= 1 and lines[0].startswith("```") and lines[-1].endswith("```") and len(block) >= 6:
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("* ") or line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered = False
            break
    if is_ordered and len(lines) > 0:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block) or block[level] != " ":
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[3:-3]
    if text.startswith("\n"):
        text = text[1:]
    code_node = LeafNode("code", text)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        content = line[1:]
        if content.startswith(" "):
            content = content[1:]
        new_lines.append(content)
    quote_text = " ".join(new_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        item_text = line[2:]
        children = text_to_children(item_text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)


def olist_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        item_text = line.split(". ", 1)[1]
        children = text_to_children(item_text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
        else:
            raise ValueError(f"Invalid block type: {block_type}")
    return ParentNode("div", children)
