import os
import tempfile
import unittest
from page_generator import extract_title, generate_page


class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello World\n\nThis is a paragraph."
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_with_leading_whitespace(self):
        md = "\n\n# Tolkien Fan Club\n\nWelcome to Middle Earth."
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_extract_title_raises_if_no_h1(self):
        md = "## Subtitle Only\n\nNo main h1 header here."
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_generate_page(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from_path = os.path.join(tmpdir, "index.md")
            template_path = os.path.join(tmpdir, "template.html")
            dest_path = os.path.join(tmpdir, "output", "index.html")

            with open(from_path, "w", encoding="utf-8") as f:
                f.write("# Page Title\n\nWelcome to the [site](https://boot.dev).")

            with open(template_path, "w", encoding="utf-8") as f:
                f.write(
                    "<html><head><title>{{ Title }}</title></head><body><article>{{ Content }}</article></body></html>"
                )

            generate_page(from_path, template_path, dest_path, basepath="/")

            self.assertTrue(os.path.exists(dest_path))
            with open(dest_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("<title>Page Title</title>", content)
            self.assertIn("<h1>Page Title</h1>", content)
            self.assertIn('<a href="https://boot.dev">site</a>', content)

    def test_generate_page_custom_basepath(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from_path = os.path.join(tmpdir, "index.md")
            template_path = os.path.join(tmpdir, "template.html")
            dest_path = os.path.join(tmpdir, "output", "index.html")

            with open(from_path, "w", encoding="utf-8") as f:
                f.write("# Subpath Page\n\nHere is an image: ![logo](/images/logo.png)")

            with open(template_path, "w", encoding="utf-8") as f:
                f.write(
                    '<html><head><link rel="stylesheet" href="/index.css" /></head><body>{{ Content }}</body></html>'
                )

            generate_page(from_path, template_path, dest_path, basepath="/my-repo/")

            with open(dest_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn('href="/my-repo/index.css"', content)
            self.assertIn('src="/my-repo/images/logo.png"', content)


if __name__ == "__main__":
    unittest.main()
