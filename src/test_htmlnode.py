from htmlnode import HTMLNode, LeafNode, ParentNode


def test_htmlnode_props_none():
    node = HTMLNode("div", "Hello, World!", [])
    assert node.props_to_html() == ""


def test_htmlnode_props_simple():
    node = HTMLNode("div", "Hello, World!", [], {"class": "test"})
    assert node.props_to_html() == ' class="test"'


def test_htmlnode_props_multiple():
    node = HTMLNode("div", "Hello, World!", [], {"class": "test", "id": "test"})
    assert node.props_to_html() == ' class="test" id="test"'


def test_leafnode_to_html_no_tag():
    node = LeafNode(None, "Hello, World!")
    assert node.to_html() == "Hello, World!"


def test_leafnode_to_html_no_props():
    node = LeafNode("p", "Hello, World!")
    assert node.to_html() == "<p>Hello, World!</p>"


def test_leafnode_to_html():
    node = LeafNode("div", "Hello, World!", {"class": "test", "id": "test"})
    assert node.to_html() == '<div class="test" id="test">Hello, World!</div>'


def test_parentnode_to_html():
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    assert (
        node.to_html()
        == "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
    )


def test_to_html_with_children():
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    assert parent_node.to_html() == "<div><span>child</span></div>"


def test_to_html_with_grandchildren():
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    assert parent_node.to_html() == "<div><span><b>grandchild</b></span></div>"
