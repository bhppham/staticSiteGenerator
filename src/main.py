import re
import shutil
from pathlib import Path

from inline_markdown import markdown_to_html_node


def copy_static_to_public(static_dir: str, public_dir: str) -> None:
    static_path = Path(static_dir).resolve()
    public_path = Path(public_dir).resolve()
    project_root = static_path.parent

    if not static_path.exists() or not static_path.is_dir():
        raise FileNotFoundError(f"Required static directory missing: {static_path}")

    public_path.mkdir(parents=True, exist_ok=True)

    for item in public_path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    def copy_recursive(src: Path, dst: Path) -> None:
        dst.mkdir(parents=True, exist_ok=True)
        for entry in src.iterdir():
            destination = dst / entry.name
            if entry.is_dir():
                copy_recursive(entry, destination)
            else:
                shutil.copy2(entry, destination)
                src_log = entry.relative_to(project_root).as_posix()
                dst_log = destination.relative_to(project_root).as_posix()
                print(f"{src_log} -> {dst_log}")

    copy_recursive(static_path, public_path)


def extract_title(markdown: str) -> str:
    title_match = re.search(r"^#\s+(.+)$", markdown, flags=re.MULTILINE)
    if not title_match:
        raise ValueError("Markdown document is missing an h1 title")
    return title_match.group(1).strip()


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating from {from_path} to {dest_path} using {template_path}")

    markdown = Path(from_path).read_text(encoding="utf-8")
    template = Path(template_path).read_text(encoding="utf-8")

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    rendered_page = template
    rendered_page = rendered_page.replace("{{ Title }}", title)
    rendered_page = rendered_page.replace("{{ Content }}", html_content)

    destination = Path(dest_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(rendered_page, encoding="utf-8")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    content_root = Path(dir_path_content).resolve()
    destination_root = Path(dest_dir_path).resolve()

    if not content_root.exists() or not content_root.is_dir():
        raise FileNotFoundError(f"Required content directory missing: {content_root}")

    for entry in sorted(content_root.rglob("*")):
        if entry.is_file() and entry.suffix == ".md":
            relative_html_path = entry.relative_to(content_root).with_suffix(".html")
            destination_path = destination_root / relative_html_path
            generate_page(str(entry), template_path, str(destination_path))


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    copy_static_to_public(str(root / "static"), str(root / "public"))
    generate_pages_recursive(
        str(root / "content"),
        str(root / "template.html"),
        str(root / "public"),
    )
