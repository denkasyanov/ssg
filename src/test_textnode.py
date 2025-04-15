import pytest

from htmlnode import HTMLNode
from textnode import TextNode, TextType


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
            TextNode("Bold Text", TextType.BOLD),
            HTMLNode("b", "Bold Text"),
            id="BOLD",
        ),
        pytest.param(
            TextNode("Italic Text", TextType.ITALIC),
            HTMLNode("i", "Italic Text"),
            id="ITALIC",
        ),
        pytest.param(
            TextNode("Code Text", TextType.CODE),
            HTMLNode("code", "Code Text"),
            id="CODE",
        ),
        pytest.param(
            TextNode("Link Text", TextType.LINK, "http://example.com"),
            HTMLNode("a", "Link Text", {"href": "http://example.com"}),
            id="LINK",
        ),
        pytest.param(
            TextNode("Alt Text", TextType.IMAGE, "http://example.com/image.png"),
            HTMLNode("img", "Alt Text", {"src": "http://example.com/image.png"}),
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


def text_plain_text_node_to_html():
    text_node = TextNode("Normal Text", TextType.TEXT)
    html_node = text_node.to_html_node()
    assert html_node == "Normal Text"
