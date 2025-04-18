import os
import shutil
import sys
from pathlib import Path

from block_markdown import markdown_to_html_node

ROOT_DIR = Path(__file__).parent.parent
PUBLIC_DIR = ROOT_DIR / "public"
STATIC_DIR = ROOT_DIR / "static"
DOCS_DIR = ROOT_DIR / "docs"


def clean_public_dir():
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def copy_static():
    shutil.copytree(STATIC_DIR, DOCS_DIR, dirs_exist_ok=True)


def extract_title(markdown: str):
    if not markdown.startswith("# "):
        raise ValueError("Markdown must start with a title")
    return markdown.splitlines()[0].strip("# ")


def generate_page(from_path: Path, template_path: Path, to_path: Path, basepath: str):
    print(f"Generating page from {from_path} to {to_path} using {template_path}")

    with open(from_path, "r") as md_source_file:
        md_source = md_source_file.read()

    title = extract_title(md_source)

    with open(template_path, "r") as html_template_file:
        html_template = html_template_file.read()

    html = markdown_to_html_node(md_source).to_html()

    os.makedirs(to_path.parent, exist_ok=True)
    with open(to_path, "w") as f:
        f.write(
            html_template.replace("{{ Title }}", title)
            .replace("{{ Content }}", html)
            .replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
        )


def generate_pages_recursively(
    content_dir: Path, template_path: Path, public_dir: Path, basepath: str
):
    for file in content_dir.iterdir():
        if file.is_file() and file.suffix == ".md":
            generate_page(
                file,
                template_path,
                public_dir / file.name.replace(".md", ".html"),
                basepath,
            )
        elif file.is_dir():
            generate_pages_recursively(
                file, template_path, public_dir / file.name, basepath
            )


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"Using basepath: {basepath}")

    clean_public_dir()
    copy_static()

    generate_pages_recursively(
        ROOT_DIR / "content", ROOT_DIR / "template.html", DOCS_DIR, basepath
    )


if __name__ == "__main__":
    main()
