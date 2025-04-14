from __future__ import annotations

import re
from enum import Enum
from typing import NamedTuple

from htmlnode import HTMLNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self) -> HTMLNode:
        match self.text_type:
            case TextType.TEXT:
                return HTMLNode(self.text)
            case TextType.BOLD:
                return HTMLNode(self.text, "b")
            case TextType.ITALIC:
                return HTMLNode(self.text, "i")
            case TextType.CODE:
                return HTMLNode(self.text, "code")
            case TextType.LINK:
                return HTMLNode(self.text, "a", {"href": self.url})
            case TextType.IMAGE:
                return HTMLNode(self.text, "img", {"src": self.url})
            case _:
                raise ValueError(f"Invalid text type: {self.text_type}")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list["TextNode"]:
    next_nodes = []
    for node in old_nodes:
        if delimiter in node.text:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(
                    f"invalid markdown, formatted section not closed: {node.text}"
                )
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    next_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    next_nodes.append(TextNode(part, text_type))
        else:
            next_nodes.append(node)
    return next_nodes


class MarkdownImage(NamedTuple):
    alt_text: str
    url: str


class MarkdownLink(NamedTuple):
    text: str
    url: str


def extract_markdown_images(markdown: str) -> list[MarkdownImage]:
    matches = re.findall(r"\!\[([^\]]*)\]\(([^)]+)\)", markdown)
    return [MarkdownImage(alt_text, url) for alt_text, url in matches]


def extract_markdown_links(markdown: str) -> list[MarkdownLink]:
    matches = re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", markdown)
    return [MarkdownLink(text, url) for text, url in matches]


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        images = extract_markdown_images(remaining_text)
        for alt_text, url in images:
            image_node = TextNode(alt_text, TextType.IMAGE, url)
            image_node_str = f"![{alt_text}]({url})"
            plain_text, remaining_text = remaining_text.split(image_node_str, 1)
            new_nodes.extend([TextNode(plain_text, TextType.TEXT), image_node])
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        links = extract_markdown_links(remaining_text)
        for text, url in links:
            link_node = TextNode(text, TextType.LINK, url)
            link_node_str = f"[{text}]({url})"
            plain_text, remaining_text = remaining_text.split(link_node_str, 1)
            new_nodes.extend([TextNode(plain_text, TextType.TEXT), link_node])
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
