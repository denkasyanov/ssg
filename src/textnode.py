from __future__ import annotations

from enum import Enum

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
