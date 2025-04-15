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

    def to_html_node(self) -> HTMLNode | str:
        match self.text_type:
            case TextType.TEXT:
                return self.text
            case TextType.BOLD:
                return HTMLNode("b", self.text)
            case TextType.ITALIC:
                return HTMLNode("i", self.text)
            case TextType.CODE:
                return HTMLNode("code", self.text)
            case TextType.LINK:
                return HTMLNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return HTMLNode("img", self.text, {"src": self.url})
            case _:
                raise ValueError(f"Invalid text type: {self.text_type}")
