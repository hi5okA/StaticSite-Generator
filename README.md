# Custom Python Static Site Generator (SSG)

A complete, standard-library-only **Static Site Generator** built in Python, following the full curriculum and architectural design of **[Boot.dev's Build a Static Site Generator in Python](https://www.boot.dev/lessons/7d4f1f5a-215d-4dc2-ad7a-2728c23fb695)**.

It compiles raw Markdown files into an Abstract Syntax Tree (AST) of structured HTML nodes, applies HTML templates with dynamic metadata injection, handles recursive directory trees, and supports custom deployment base paths (e.g., for GitHub Pages).

---

## 🌟 Architecture & Design Patterns

The static site generator is built using three foundational software engineering patterns:

### 1. Composite Design Pattern (`HTMLNode`, `LeafNode`, `ParentNode`)
- **`HTMLNode`**: Abstract base class representing any node in the DOM tree. Tracks `tag`, `value`, `children`, and `props`.
- **`LeafNode`**: Terminal node without children (e.g. `<b>`, `<code>`, `<img>`, or raw text). Generates its own HTML string directly.
- **`ParentNode`**: Container node with nested children (e.g. `<div>`, `<p>`, `<ul>`, `<ol>`, `<blockquote>`). Recursively renders opening tags, all children via `child.to_html()`, and closing tags.

### 2. Strategy Pattern (`block_to_block_type` & Block Processors)
- Markdown is first partitioned into isolated blocks using `markdown_to_blocks`.
- Each block is classified via `block_to_block_type` into `BlockType` (`HEADING`, `CODE`, `QUOTE`, `UNORDERED_LIST`, `ORDERED_LIST`, or `PARAGRAPH`).
- A specialized handler function transforms each block into its corresponding `HTMLNode` structure.

### 3. Pipeline Pattern (Inline Markdown Parsing)
- Text blocks are sequentially transformed through a tokenization pipeline:
  1. `split_nodes_image`: Extracts `![alt](url)` tokens into `TextType.IMAGE`.
  2. `split_nodes_link`: Extracts `[anchor](url)` tokens into `TextType.LINK`.
  3. `split_nodes_delimiter` for `**`: Converts bold segments to `TextType.BOLD`.
  4. `split_nodes_delimiter` for `*`: Converts italic segments to `TextType.ITALIC`.
  5. `split_nodes_delimiter` for `` ` ``: Converts code segments to `TextType.CODE`.
  6. `text_node_to_html_node`: Converts all resulting `TextNode` objects into `LeafNode` instances.

---

## 📁 Project Structure

```text
static_site_generator/
├── src/
│   ├── __init__.py
│   ├── textnode.py                # TextNode class & TextType Enum
│   ├── htmlnode.py                # HTMLNode, LeafNode, ParentNode definitions
│   ├── leafnode.py                # LeafNode export wrapper
│   ├── parentnode.py              # ParentNode export wrapper
│   ├── inline_markdown.py         # Inline delimiter, link & image tokenizers
│   ├── markdown_blocks.py         # Block splitting, classification & HTML node conversion
│   ├── markdown_to_html_node.py   # Root markdown-to-HTML parser wrapper
│   ├── page_generator.py          # extract_title, generate_page, generate_pages_recursive
│   ├── generate_page.py           # generate_page wrapper
│   ├── generate_pages_recursive.py# generate_pages_recursive wrapper
│   ├── copystatic.py              # Recursive file copy utility
│   ├── main.py                    # Build CLI entry point
│   ├── test_textnode.py           # Unit tests for TextNode & LeafNode conversions
│   ├── test_htmlnode.py           # Unit tests for HTMLNode, LeafNode, ParentNode
│   ├── test_inline_markdown.py    # Unit tests for delimiters, images & links
│   ├── test_markdown_blocks.py    # Unit tests for block types & AST conversion
│   └── test_page_generator.py     # Unit tests for page generation & basepath
├── static/
│   ├── index.css                  # Modern fantasy styling (dark mode, typography, responsiveness)
│   └── images/
│       └── ring.svg               # Vector graphic asset
├── content/
│   ├── index.md                   # Tolkien Fan Club homepage
│   ├── contact.md                 # Fellowship contact page
│   ├── majesty/
│   │   └── index.md               # Nested page: The Majesty of Middle-Earth
│   └── tolkien/
│       └── index.md               # Nested page: Biography of J.R.R. Tolkien
├── public/                        # Build output (generated on build)
├── template.html                  # Master HTML template (contains {{ Title }} & {{ Content }})
├── main.sh / main.bat             # Run local generator
├── test.sh / test.bat             # Run test suite
├── build.sh / build.bat           # Run generator with custom basepath
├── serve.py                       # Local preview server (http://localhost:8888)
└── README.md
```

---

## 🚀 Quickstart & Usage

### 1. Run All Automated Unit Tests (52 Tests)
Using Bash:
```bash
./test.sh
```
Or on Windows:
```cmd
test.bat
# or directly:
python -m unittest discover -s src
```

### 2. Generate the Website
Using Bash:
```bash
./main.sh
```
Or on Windows:
```cmd
main.bat
# or directly:
python src/main.py
```
This will:
1. Delete and clean the `public/` directory.
2. Recursively copy all assets from `static/` into `public/`.
3. Recursively crawl `content/` and compile every `.md` file into `.html` in `public/`.

### 3. Preview the Live Website Locally
Run the built-in HTTP server:
```bash
python serve.py
```
Open **[http://localhost:8888](http://localhost:8888)** in your web browser.

### 4. Deploying to GitHub Pages (Custom Basepath)
When hosting on GitHub Pages at `https://<username>.github.io/<repo>/`, pass your repository name as the basepath:
```bash
./build.sh "/<repo-name>/"
# or on Windows:
build.bat "/<repo-name>/"
```
All asset links (`/index.css`, `/images/...`) and page links (`/majesty/`, etc.) will automatically be prefixed with your repository base path.

---

## 🧪 Verified Test Suite

All 52 unit tests cover:
- Equality, representation, and edge cases for `TextNode` and `TextType`.
- LeafNode rendering, missing value validation, raw text conversion.
- ParentNode recursive HTML generation, multi-tier nesting, missing tag/child checks.
- Image and link extraction using regex patterns (`r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"` and `r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"`).
- Splitting text nodes with single/multiple images and links.
- Markdown block separation with variable whitespace and blank lines.
- Classification of H1-H6 headings, fenced code blocks, multi-line quotes, ordered lists, and unordered lists.
- Full document AST compilation to HTML.
- H1 title extraction with validation and error raising.
- Recursive page generation and basepath link transformations.
