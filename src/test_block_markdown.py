from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


def test_markdown_to_blocks():
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    assert blocks == [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
    ]


def test_markdown_to_blocks_empty():
    markdown_text = ""
    blocks = markdown_to_blocks(markdown_text)
    assert blocks == []


def test_markdown_to_blocks_single():
    markdown_text = "Hello, world!"
    blocks = markdown_to_blocks(markdown_text)
    assert blocks == ["Hello, world!"]


def test_markdown_to_blocks_multiple():
    markdown_text = """Hello, world!\n\nThis is a test."""
    blocks = markdown_to_blocks(markdown_text)
    assert blocks == ["Hello, world!", "This is a test."]


def test_markdown_to_blocks_with_multiline():
    markdown_text = """Hello, world!

This is a test with real line breaks.
This should be in the same block as the previous line."""
    blocks = markdown_to_blocks(markdown_text)
    assert blocks == [
        "Hello, world!",
        "This is a test with real line breaks.\nThis should be in the same block as the previous line.",
    ]


def test_markdown_to_blocks_with_extra_3newlines():
    markdown_text = """Hello, world!\n\n\nThis is a test."""
    blocks = markdown_to_blocks(markdown_text)
    assert blocks == ["Hello, world!", "This is a test."]


def test_markdown_to_blocks_with_extra_4newlines():
    markdown_text = """Hello, world!\n\n\n\nThis is a test."""
    blocks = markdown_to_blocks(markdown_text)
    assert blocks == ["Hello, world!", "This is a test."]


def test_markdown_to_blocks_with_extra_5newlines():
    markdown_text = """Hello, world!\n\n\n\n\nThis is a test."""
    blocks = markdown_to_blocks(markdown_text)
    assert blocks == ["Hello, world!", "This is a test."]


def test_block_valid_heading():
    block = "## This is a heading"
    assert block_to_block_type(block) == BlockType.HEADING


def test_block_invalid_heading():
    block = "##This is a paragraph"
    assert block_to_block_type(block) != BlockType.HEADING


def test_block_valid_code():
    block = "```python\nprint('Hello, world!')\n```"
    assert block_to_block_type(block) == BlockType.CODE


def test_block_invalid_code():
    block = "```python\nprint('Hello, world!')\n"
    assert block_to_block_type(block) != BlockType.CODE


def test_valid_quote():
    block = "> This is a quote\n> This is another quote"
    assert block_to_block_type(block) == BlockType.QUOTE


def test_invalid_quote():
    block = "> This is a quote\nThis is not really a quote"
    assert block_to_block_type(block) != BlockType.QUOTE


def test_valid_unordered_list():
    block = "- This is a list item\n- This is another list item"
    assert block_to_block_type(block) == BlockType.UNORDERED_LIST


def test_invalid_unordered_list():
    block = "- This is a list item\nThis is not a list item"
    assert block_to_block_type(block) != BlockType.UNORDERED_LIST


def test_valid_ordered_list():
    block = "1. This is a list item\n2. This is another list item"
    assert block_to_block_type(block) == BlockType.ORDERED_LIST


def test_invalid_ordered_list():
    block = "1. This is a list item\nThis is not a list item"
    assert block_to_block_type(block) != BlockType.ORDERED_LIST


def test_valid_paragraph():
    block = "I am just lil paragraph"
    assert block_to_block_type(block) == BlockType.PARAGRAPH


def test_paragraphs():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    assert (
        html
        == "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
    )


def test_codeblock():
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    assert (
        html
        == "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
    )
