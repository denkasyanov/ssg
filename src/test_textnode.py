import pytest
from htmlnode import HTMLNode
from textnode import TextNode, TextType, split_nodes_delimiter


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
