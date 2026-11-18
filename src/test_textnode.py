import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Link text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link text", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Text A", TextType.TEXT)
        node2 = TextNode("Text B", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("Node without url", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("Test text", TextType.CODE, "https://boot.dev")
        self.assertEqual(repr(node), "TextNode('Test text', code, 'https://boot.dev')")

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is raw text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is raw text")
        self.assertEqual(html_node.to_html(), "This is raw text")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_to_html_node_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>print('hi')</code>")

    def test_text_node_to_html_node_link(self):
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})
        self.assertEqual(html_node.to_html(), '<a href="https://boot.dev">Click here</a>')

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt description", TextType.IMAGE, "https://boot.dev/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://boot.dev/img.png", "alt": "Alt description"},
        )
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://boot.dev/img.png" alt="Alt description"></img>',
        )


if __name__ == "__main__":
    unittest.main()
