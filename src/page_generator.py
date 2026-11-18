import os
from src.markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    if basepath != "/":
        if not basepath.endswith("/"):
            basepath = f"{basepath}/"
        template_content = template_content.replace('href="/', f'href="{basepath}')
        template_content = template_content.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(from_path):
            if item.endswith(".md"):
                dest_html_path = os.path.splitext(dest_path)[0] + ".html"
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
