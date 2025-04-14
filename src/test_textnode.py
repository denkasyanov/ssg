import pytest

from htmlnode import HTMLNode
from textnode import (
    MarkdownImage,
    MarkdownLink,
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def test_eq():
    text_node = TextNode("Hello, World!", TextType.TEXT)
    other_text_node = TextNode("Hello, World!", TextType.TEXT)
    assert text_node == other_text_node


def test_different_text():
    text_node = TextNode("Hello, World!", TextType.TEXT)
    other_text_node = TextNode("Hello, World!", TextType.BOLD)
    assert text_node != other_text_node


def test_default_url():
    text_node = TextNode("Hello, World!", TextType.TEXT)
    assert text_node.url is None


@pytest.mark.parametrize(
    "input_text_node, expected_html_node",
    [
        pytest.param(
            TextNode("Normal Text", TextType.TEXT),
            HTMLNode("Normal Text"),
            id="TEXT",
        ),
        pytest.param(
            TextNode("Bold Text", TextType.BOLD),
            HTMLNode("Bold Text", "b"),
            id="BOLD",
        ),
        pytest.param(
            TextNode("Italic Text", TextType.ITALIC),
            HTMLNode("Italic Text", "i"),
            id="ITALIC",
        ),
        pytest.param(
            TextNode("Code Text", TextType.CODE),
            HTMLNode("Code Text", "code"),
            id="CODE",
        ),
        pytest.param(
            TextNode("Link Text", TextType.LINK, "http://example.com"),
            HTMLNode("Link Text", "a", {"href": "http://example.com"}),
            id="LINK",
        ),
        pytest.param(
            TextNode("Alt Text", TextType.IMAGE, "http://example.com/image.png"),
            HTMLNode("Alt Text", "img", {"src": "http://example.com/image.png"}),
            id="IMAGE",
        ),
    ],
)
def test_text_node_to_html_node(input_text_node, expected_html_node):
    converted_node = input_text_node.to_html_node()

    # Compare relevant attributes as HTMLNode might not have __eq__ implemented
    assert converted_node.tag == expected_html_node.tag
    assert converted_node.value == expected_html_node.value
    assert converted_node.children == expected_html_node.children
    assert converted_node.props == expected_html_node.props


def test_split_nodes_delimiter_noop():
    node = TextNode("This is `text` with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter(
        [node],
        "**",
        TextType.BOLD,
    )
    assert new_nodes == [node]


def test_split_nodes_delimiter_code_single():
    text = "This is text with a `code block` word"
    nodes = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)],
        "`",
        TextType.CODE,
    )
    assert nodes == [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]


def test_split_nodes_delimiter_code_multiple():
    node = TextNode("This is `text` with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter(
        [node],
        "`",
        TextType.CODE,
    )

    assert new_nodes == [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.CODE),
        TextNode(" with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]


def test_split_nodes_delimiter_bold():
    node = TextNode("This is **bold** text", TextType.TEXT)
    new_nodes = split_nodes_delimiter(
        [node],
        "**",
        TextType.BOLD,
    )
    assert new_nodes == [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.TEXT),
    ]


def test_split_nodes_delimiter_multiple_nodes():
    nodes = [
        TextNode("This is **bold** text", TextType.TEXT),
        TextNode("This is also **bold** text", TextType.TEXT),
    ]
    new_nodes = split_nodes_delimiter(
        nodes,
        "**",
        TextType.BOLD,
    )
    assert new_nodes == [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.TEXT),
        TextNode("This is also ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.TEXT),
    ]


def test_split_nodes_delimiter_odd_number_of_delimiters():
    with pytest.raises(ValueError):
        split_nodes_delimiter(
            [TextNode("This **is **bold** text", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )


def test_extract_markdown_images_single():
    markdown = "This is an image ![alt text](https://example.com/image.png)"
    images = extract_markdown_images(markdown)
    assert images == [MarkdownImage("alt text", "https://example.com/image.png")]


def test_extract_markdown_images_empty_alt_text():
    markdown = "This is an image ![](https://example.com/image.png)"
    images = extract_markdown_images(markdown)
    assert images == [MarkdownImage("", "https://example.com/image.png")]


def test_extract_markdown_images_multiple():
    markdown = "This is an image ![alt text](https://example.com/image.png) and another image ![alt text 2](https://example.com/image2.png)"
    images = extract_markdown_images(markdown)
    assert images == [
        MarkdownImage("alt text", "https://example.com/image.png"),
        MarkdownImage("alt text 2", "https://example.com/image2.png"),
    ]


def test_extract_markdown_links_single():
    markdown = "This is a link [link text](https://example.com)"
    links = extract_markdown_links(markdown)
    assert links == [MarkdownLink("link text", "https://example.com")]


def test_extract_markdown_links_multiple():
    markdown = "This is a link [link text](https://example.com) and another link [link text 2](https://example.com/2)"
    links = extract_markdown_links(markdown)
    assert links == [
        MarkdownLink("link text", "https://example.com"),
        MarkdownLink("link text 2", "https://example.com/2"),
    ]


def test_split_images_without_trailing_text():
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert new_nodes == [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
    ]


def test_split_images_with_trailing_text():
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some trailing text",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert new_nodes == [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        TextNode(" and some trailing text", TextType.TEXT),
    ]


def test_split_nodes_link_without_trailing_text():
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    assert new_nodes == [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
    ]


def test_split_nodes_link_with_trailing_text():
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some trailing text",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    assert new_nodes == [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        TextNode(" and some trailing text", TextType.TEXT),
    ]
