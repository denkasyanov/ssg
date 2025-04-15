import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    elif re.match(r"^`{3,}.*`{3,}$", block, re.DOTALL):
        return BlockType.CODE

    elif all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE

    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST

    elif all(re.match(r"^\d+\. ", line) for line in block.splitlines()):
        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown_text: str) -> list[str]:
    if not markdown_text:
        return []
    raw_blocks = markdown_text.split("\n\n")
    blocks = []
    for raw_block in raw_blocks:
        if not raw_block:
            continue
        if "\n" in raw_block:
            raw_block = raw_block.strip()
        blocks.append(raw_block)
    return blocks


# def text_to_children(text: str) -> list[HTMLNode]:


def paragraph_md_to_html_node(paragraph: str) -> list[LeafNode]:
    # splitting down to leaf nodes should be done here
    paragraph = paragraph.replace("\n", " ")
    text_nodes = text_to_textnodes(paragraph)

    html_nodes = []
    for text_node in text_nodes:
        if text_node.text_type == TextType.TEXT:
            html_nodes.append(LeafNode(tag=None, value=text_node.text))
        elif text_node.text_type == TextType.BOLD:
            html_nodes.append(LeafNode(tag="b", value=text_node.text))
        elif text_node.text_type == TextType.ITALIC:
            html_nodes.append(LeafNode(tag="i", value=text_node.text))
        elif text_node.text_type == TextType.CODE:
            html_nodes.append(LeafNode(tag="code", value=text_node.text))
        elif text_node.text_type == TextType.IMAGE:
            html_nodes.append(
                LeafNode(
                    tag="img",
                    value=" ",
                    props={"src": text_node.url, "alt": text_node.text},
                )
            )
        elif text_node.text_type == TextType.LINK:
            html_nodes.append(
                LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
            )
        else:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

    return html_nodes


def heading_md_to_html_node(heading: str) -> LeafNode:
    heading_level = heading.count("#")

    content = heading.strip("#").strip()

    return LeafNode(
        tag=f"h{heading_level}",
        value=content,
    )


def code_md_to_html_node(code: str) -> ParentNode:
    code = code.strip("`").lstrip()

    return ParentNode(
        tag="pre",
        children=[LeafNode(tag="code", value=code)],
    )


def quote_md_to_html_node(quote: str) -> ParentNode:
    lines = quote.splitlines()
    stripped_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(stripped_lines)
    return LeafNode(
        tag="blockquote",
        value=content,
    )


def unordered_list_md_to_html_nodes(unordered_list: str) -> list[LeafNode]:
    lines = unordered_list.splitlines()

    list_item_nodes = []

    for line in lines:
        processed_line = paragraph_md_to_html_node(line.strip("- ").strip())
        list_item_nodes.append(
            ParentNode(
                tag="li",
                children=processed_line,
            )
        )

    return ParentNode(
        tag="ul",
        children=list_item_nodes,
    )


def ordered_list_md_to_html_nodes(ordered_list: str) -> list[LeafNode]:
    lines = ordered_list.splitlines()

    list_item_nodes = []

    for line in lines:
        processed_line = paragraph_md_to_html_node(line.split(".", 1)[1].strip())
        list_item_nodes.append(
            ParentNode(
                tag="li",
                children=processed_line,
            )
        )

    return ParentNode(
        tag="ol",
        children=list_item_nodes,
    )


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                children = paragraph_md_to_html_node(block)
                html_node = ParentNode(tag="p", children=children)
            case BlockType.HEADING:
                html_node = heading_md_to_html_node(block)
            case BlockType.CODE:
                html_node = code_md_to_html_node(block)
            case BlockType.QUOTE:
                html_node = quote_md_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                html_node = unordered_list_md_to_html_nodes(block)
            case BlockType.ORDERED_LIST:
                html_node = ordered_list_md_to_html_nodes(block)

        html_nodes.append(html_node)

    return ParentNode(
        tag="div",
        children=html_nodes,
    )
