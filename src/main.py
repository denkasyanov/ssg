import shutil
from block_markdown import markdown_to_html_node
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
PUBLIC_DIR = ROOT_DIR / "public"
STATIC_DIR = ROOT_DIR / "static"


def clean_public_dir():
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)


def copy_static():
    shutil.copytree(STATIC_DIR, PUBLIC_DIR, dirs_exist_ok=True)


def extract_title(markdown: str):
    if not markdown.startswith("# "):
        raise ValueError("Markdown must start with a title")
    return markdown.splitlines()[0].strip("# ")


def generate_page(from_path: Path, template_path: Path, to_path: Path):
    print(f"Generating page from {from_path} to {to_path} using {template_path}")

    with open(from_path, "r") as md_source_file:
        md_source = md_source_file.read()

    title = extract_title(md_source)

    with open(template_path, "r") as html_template_file:
        html_template = html_template_file.read()

    html = markdown_to_html_node(md_source).to_html()

    with open(to_path, "w") as f:
        f.write(
            html_template.replace("{{ Title }}", title).replace("{{ Content }}", html)
        )


def main():
    clean_public_dir()
    copy_static()

    generate_page(
        ROOT_DIR / "content" / "index.md",
        ROOT_DIR / "template.html",
        PUBLIC_DIR / "index.html",
    )


if __name__ == "__main__":
    main()
