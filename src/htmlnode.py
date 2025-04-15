from __future__ import annotations


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self) -> str:
        return (
            "".join(f' {k}="{v}"' for k, v in self.props.items()) if self.props else ""
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict | None = None,
    ):
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")

        if not self.tag:
            return self.value

        if self.tag.lower() == "img":
            return f"<{self.tag}{self.props_to_html()}>"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
