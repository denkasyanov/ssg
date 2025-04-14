import re
from typing import NamedTuple

from textnode import TextNode, TextType


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
