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
