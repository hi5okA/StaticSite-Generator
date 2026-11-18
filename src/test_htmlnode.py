import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Boot.dev",
            props={"href": "https://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://boot.dev" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_node_to_html_p(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leaf_node_to_html_raw_text(self):
        node = LeafNode(None, "Just raw text.")
        self.assertEqual(node.to_html(), "Just raw text.")

    def test_leaf_node_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_node_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, " normal text "),
                LeafNode("i", "italic text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b> normal text <i>italic text</i></p>",
        )

    def test_parent_node_nested(self):
        inner_parent = ParentNode(
            "div",
            [
                LeafNode("h1", "Nested Title"),
                LeafNode("p", "Paragraph inside div"),
            ],
        )
        outer_parent = ParentNode("section", [inner_parent])
        self.assertEqual(
            outer_parent.to_html(),
            "<section><div><h1>Nested Title</h1><p>Paragraph inside div</p></div></section>",
        )

    def test_parent_node_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "Hello")],
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><span>Hello</span></div>',
        )

    def test_parent_node_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("p", "hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
