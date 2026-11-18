import os
import shutil
import sys
from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Resolve paths relative to project root
    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(src_dir, ".."))

    dir_path_static = os.path.join(project_root, "static")
    dir_path_public = os.path.join(project_root, "public")
    dir_path_content = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    print(f"Basepath: {basepath}")
    print(f"Project root: {project_root}")
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    if os.path.exists(dir_path_static):
        copy_files_recursive(dir_path_static, dir_path_public)
    else:
        print(f"Warning: static directory '{dir_path_static}' does not exist.")

    print("Generating content...")
    if os.path.exists(dir_path_content) and os.path.exists(template_path):
        generate_pages_recursive(
            dir_path_content, template_path, dir_path_public, basepath
        )
        print("Static site generation completed successfully!")
    else:
        print(f"Error: Content directory '{dir_path_content}' or template '{template_path}' missing.")


if __name__ == "__main__":
    main()
