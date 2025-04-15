import shutil
from textnode import TextNode, TextType
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


def main():
    clean_public_dir()
    copy_static()


if __name__ == "__main__":
    main()
