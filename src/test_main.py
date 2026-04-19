import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from main import (
    copy_static_to_public,
    extract_title,
    generate_page,
    generate_pages_recursive,
)


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_from_h1(self):
        markdown = "# My Portfolio\n\n## Projects\n\nSome text"
        self.assertEqual(extract_title(markdown), "My Portfolio")

    def test_extract_title_raises_without_h1(self):
        markdown = "## Projects\n\nSome text"
        with self.assertRaises(ValueError):
            extract_title(markdown)


class TestGeneratePage(unittest.TestCase):
    def test_generate_page_renders_html_and_creates_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            markdown_path = temp_path / "content" / "index.md"
            template_path = temp_path / "template.html"
            dest_path = temp_path / "public" / "nested" / "index.html"

            markdown_path.parent.mkdir(parents=True, exist_ok=True)
            markdown_path.write_text(
                "# Home Page\n\nThis is a **bold** line.", encoding="utf-8"
            )
            template_path.write_text(
                "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>",
                encoding="utf-8",
            )

            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                generate_page(
                    str(markdown_path),
                    str(template_path),
                    str(dest_path),
                )

            self.assertTrue(dest_path.exists())
            generated_html = dest_path.read_text(encoding="utf-8")
            self.assertIn("<title>Home Page</title>", generated_html)
            self.assertIn(
                "<div><h1>Home Page</h1><p>This is a <b>bold</b> line.</p></div>",
                generated_html,
            )
            self.assertIn("Generating from", output_buffer.getvalue())


class TestGeneratePagesRecursive(unittest.TestCase):
    def test_generate_pages_recursive_mirrors_directory_structure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            content_dir = temp_path / "content"
            template_path = temp_path / "template.html"
            output_dir = temp_path / "public"

            (content_dir / "blog").mkdir(parents=True, exist_ok=True)
            (content_dir / "index.md").write_text("# Home\n\nWelcome.", encoding="utf-8")
            (content_dir / "blog" / "post.md").write_text(
                "# Post\n\nNested page.", encoding="utf-8"
            )
            (content_dir / "notes.txt").write_text("ignore me", encoding="utf-8")
            template_path.write_text(
                "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>",
                encoding="utf-8",
            )

            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                generate_pages_recursive(
                    str(content_dir), str(template_path), str(output_dir)
                )

            self.assertTrue((output_dir / "index.html").exists())
            self.assertTrue((output_dir / "blog" / "post.html").exists())
            self.assertFalse((output_dir / "notes.html").exists())

            index_html = (output_dir / "index.html").read_text(encoding="utf-8")
            post_html = (output_dir / "blog" / "post.html").read_text(encoding="utf-8")
            self.assertIn("<title>Home</title>", index_html)
            self.assertIn("<title>Post</title>", post_html)
            self.assertIn("Generating from", output_buffer.getvalue())

    def test_generate_pages_recursive_raises_when_content_dir_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            template_path = temp_path / "template.html"
            output_dir = temp_path / "public"
            template_path.write_text(
                "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>",
                encoding="utf-8",
            )

            with self.assertRaises(FileNotFoundError):
                generate_pages_recursive(
                    str(temp_path / "missing_content"),
                    str(template_path),
                    str(output_dir),
                )


class TestCopyStaticToPublic(unittest.TestCase):
    def test_copy_static_to_public_cleans_and_copies_nested_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            static_dir = temp_path / "static"
            public_dir = temp_path / "public"

            (static_dir / "images").mkdir(parents=True, exist_ok=True)
            (static_dir / "css").mkdir(parents=True, exist_ok=True)
            (static_dir / "images" / "photo.png").write_text("img", encoding="utf-8")
            (static_dir / "css" / "index.css").write_text("body{}", encoding="utf-8")

            (public_dir / "old_dir").mkdir(parents=True, exist_ok=True)
            (public_dir / "old_dir" / "old.txt").write_text("old", encoding="utf-8")
            (public_dir / "stale.txt").write_text("stale", encoding="utf-8")

            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                copy_static_to_public(str(static_dir), str(public_dir))

            self.assertFalse((public_dir / "stale.txt").exists())
            self.assertFalse((public_dir / "old_dir").exists())
            self.assertTrue((public_dir / "images" / "photo.png").exists())
            self.assertTrue((public_dir / "css" / "index.css").exists())

            logs = output_buffer.getvalue()
            self.assertIn("static/images/photo.png -> public/images/photo.png", logs)
            self.assertIn("static/css/index.css -> public/css/index.css", logs)

    def test_copy_static_to_public_raises_when_static_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with self.assertRaises(FileNotFoundError):
                copy_static_to_public(
                    str(temp_path / "missing_static"),
                    str(temp_path / "public"),
                )


if __name__ == "__main__":
    unittest.main()
