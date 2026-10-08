#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for md_render.py + build_bilingual_html.py

Run:
    python3 -m unittest discover -s ~/.gemini/config/skills/youtube-knowledge-vi-en/scripts -p "test_*.py" -v
"""

import datetime as dt
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from md_render import MarkdownRenderer, render_inline, slugify  # noqa: E402
import build_bilingual_html as bb  # noqa: E402


def render(md: str, suffix: str = "", lang: str = "vi") -> str:
    return MarkdownRenderer(id_suffix=suffix, lang=lang).render(md)


class InlineTests(unittest.TestCase):
    def test_bold_italic_code(self):
        out = render_inline("**đậm** và *nghiêng* và `code <x>`")
        self.assertIn("<strong>đậm</strong>", out)
        self.assertIn("<em>nghiêng</em>", out)
        self.assertIn("<code>code &lt;x&gt;</code>", out)

    def test_stray_angle_brackets_escaped_but_inline_html_kept(self):
        out = render_inline("x < y && <br> <span class=\"a\">ok</span>")
        self.assertIn("x &lt; y &amp;&amp;", out)
        self.assertIn("<br>", out)
        self.assertIn('<span class="a">ok</span>', out)

    def test_existing_entities_not_double_escaped(self):
        self.assertIn("A &amp; B", render_inline("A &amp; B"))

    def test_link_url_not_mangled_by_emphasis(self):
        out = render_inline("[doc](https://a.com/x_y_z*1*)")
        self.assertIn('href="https://a.com/x_y_z*1*"', out)
        self.assertNotIn("<em>", out)

    def test_snake_case_not_italic(self):
        self.assertNotIn("<em>", render_inline("dùng my_var_name ở đây"))

    def test_bare_url_autolinked(self):
        out = render_inline("Xem https://youtu.be/abc.")
        self.assertIn('<a href="https://youtu.be/abc"', out)
        self.assertTrue(out.endswith("</a>."))


class BlockTests(unittest.TestCase):
    def test_standard_section_ids_and_suffix(self):
        vi = render("## 1. Metadata\n\n## 5. Phân Tích\n\n### 5.1 Khủng Hoảng")
        self.assertIn('<h2 id="quick-reference">', vi)
        self.assertIn('<h2 id="deep-dive">', vi)
        self.assertIn('<h3 id="5-1-khung-hoang">', vi)
        en = render("## 1. Metadata", suffix="-en")
        self.assertIn('<h2 id="quick-reference-en">', en)

    def test_duplicate_heading_ids_deduped(self):
        out = render("### Q&A\n\n### Q&A")
        self.assertIn('id="q-a"', out)
        self.assertIn('id="q-a-2"', out)

    def test_toc_h3_only_under_deep_dive_and_playbooks(self):
        r = MarkdownRenderer()
        r.render("## 2. Executive Summary\n### Ý 1\n## 5. Deep Dive\n### 5.1 A\n## 6. Playbooks\n### Playbook 1: B")
        toc = r.toc_html()
        self.assertNotIn("Ý 1", toc)
        self.assertIn('class="lvl-3">5.1 A', toc)
        self.assertIn('class="lvl-3">Playbook 1: B', toc)

    def test_table_alignment_and_pipe_in_code(self):
        md = "| A | B |\n| :--- | ---: |\n| `x|y` | **2** |"
        out = render(md)
        self.assertIn('<div class="table-wrap">', out)
        self.assertIn('<td style="text-align: left"><code>x|y</code></td>', out)
        self.assertIn('<td style="text-align: right"><strong>2</strong></td>', out)

    def test_table_short_row_padded(self):
        out = render("| A | B | C |\n|---|---|---|\n| 1 |")
        self.assertEqual(out.count("<td"), 3)

    def test_nested_and_task_lists(self):
        md = "- cha\n  - con\n- [x] xong\n- [ ] chưa"
        out = render(md)
        self.assertEqual(out.count("<ul>"), 2)
        self.assertIn('<input type="checkbox" disabled checked> xong', out)
        self.assertIn('<input type="checkbox" disabled> chưa', out)
        self.assertNotIn("<p>", out)  # tight list

    def test_ordered_list_start(self):
        self.assertIn('<ol start="3">', render("3. ba\n4. bốn"))

    def test_github_alert_to_callout(self):
        vi = render("> [!IMPORTANT]\n> Nội dung **quan trọng**")
        self.assertIn('class="callout callout-decision"', vi)
        self.assertIn('<use href="#i-decision"/>', vi)
        self.assertIn('<p class="callout-title">Quan trọng</p>', vi)
        self.assertIn("<strong>quan trọng</strong>", vi)
        en = render("> [!WARNING] Custom title\n> body", lang="en")
        self.assertIn('class="callout callout-warn"', en)
        self.assertIn('<p class="callout-title">Custom title</p>', en)

    def test_plain_blockquote(self):
        self.assertIn("<blockquote>", render("> trích dẫn"))

    def test_mermaid_source_escaped_for_textcontent(self):
        out = render('```mermaid\nflowchart LR\n  A["<b>X</b> &amp; Y"] --> B\n```')
        self.assertIn('<div class="mermaid">', out)
        self.assertIn("&lt;b&gt;X&lt;/b&gt; &amp;amp; Y", out)
        self.assertIn("--&gt; B", out)

    def test_code_fence_language(self):
        out = render("```python\nprint('<hi>')\n```")
        self.assertIn('<pre><code class="language-python">print(\'&lt;hi&gt;\')</code></pre>', out)

    def test_raw_html_block_with_blank_lines_passthrough(self):
        md = '<div class="bento-grid">\n\n  <div class="bento-card">**not md**</div>\n\n</div>\n\nSau đó'
        out = render(md)
        self.assertIn('<div class="bento-card">**not md**</div>', out)
        self.assertIn("<p>Sau đó</p>", out)

    def test_unbalanced_raw_html_stops_at_blank_line(self):
        out = render("<div>\nmở mà không đóng\n\nĐoạn văn")
        self.assertIn("<p>Đoạn văn</p>", out)

    def test_hr_and_hard_break(self):
        out = render("dòng 1  \ndòng 2\n\n---")
        self.assertIn("dòng 1<br>", out)
        self.assertIn("<hr>", out)

    def test_slugify_vietnamese(self):
        self.assertEqual(slugify("Đường Đi Ngắn Nhất"), "duong-di-ngan-nhat")


SAMPLE_MD = """# Tiêu Đề Tiếng Việt

> **Kiến trúc Song Ngữ**: boilerplate sẽ bị bỏ.

---

# PHẦN 1: BẢN TIẾNG VIỆT

## 1. Metadata & Quick Reference

| Trường | Chi tiết |
| :--- | :--- |
| **Kênh / Host** | Lenny's Podcast |

## 5. Phân Tích Chuyên Sâu

### 5.1 Ý Chính

```mermaid
flowchart LR
  A --> B
```

---

# PART 2: FULL ENGLISH VERSION

# English Title Here

## 1. Metadata & Quick Reference

| Field | Detail |
| :--- | :--- |
| **Channel / Host** | Lenny's Podcast |

## 5. Deep Dive

### 5.1 Main Idea
"""


class CompileTests(unittest.TestCase):
    def test_split_parts(self):
        title, vi, en, en_title = bb.split_bilingual_markdown(SAMPLE_MD)
        self.assertEqual(title, "Tiêu Đề Tiếng Việt")
        self.assertEqual(en_title, "English Title Here")
        self.assertNotIn("boilerplate", vi)
        self.assertNotIn("PART 2", vi)
        self.assertTrue(vi.startswith("## 1."))
        self.assertTrue(en.startswith("## 1."))

    def test_split_legacy_single_part(self):
        title, vi, en, en_title = bb.split_bilingual_markdown("# Cũ\n\n## 1. Metadata\nabc")
        self.assertEqual(title, "Cũ")
        self.assertIn("## 1. Metadata", vi)
        self.assertEqual(en, "")
        self.assertIsNone(en_title)

    def test_compile_end_to_end(self):
        try:
            bb.find_template_path()
        except FileNotFoundError:
            self.skipTest("md2html template.html not installed")
        with tempfile.TemporaryDirectory() as tmp:
            md = Path(tmp) / "note.md"
            md.write_text(SAMPLE_MD, encoding="utf-8")
            out = bb.compile_bilingual_html(str(md))
            written = md.with_suffix(".html").read_text(encoding="utf-8")

        self.assertEqual(out, written)
        # Regression: body + TOC were left empty before the fix
        self.assertNotIn("<!-- TOC_ENTRIES -->", out)
        self.assertNotIn("<!-- CONTENT_START -->", out)
        self.assertEqual(re.findall(r"\{\{[A-Z_]+\}\}", out), [])
        self.assertIn('<a href="#quick-reference" class="lvl-2">', out)
        self.assertIn('<a href="#quick-reference-en" class="lvl-2">', out)
        self.assertIn('<a href="#5-1-y-chinh" class="lvl-3">', out)
        self.assertIn('data-lang-body="vi"', out)
        self.assertIn('data-lang-body="en"', out)
        # Regression: date was hardcoded to 2026-10-02
        self.assertIn(dt.date.today().isoformat(), out)
        # Titles / subtitles
        self.assertIn('<span class="en-only">English Title Here</span>', out)
        self.assertIn("Bilingual knowledge notes · Lenny's Podcast", out)
        # Standalone mermaid now rendered by runtime (not only #view-flow)
        self.assertIn('body.querySelectorAll(".mermaid")', out)
        self.assertNotIn("English Title Here</h2>", out)

    def test_compile_with_explicit_date_and_title(self):
        try:
            bb.find_template_path()
        except FileNotFoundError:
            self.skipTest("md2html template.html not installed")
        with tempfile.TemporaryDirectory() as tmp:
            md = Path(tmp) / "note.md"
            md.write_text(SAMPLE_MD, encoding="utf-8")
            out = bb.compile_bilingual_html(str(md), str(Path(tmp) / "x.html"),
                                            title_en="Override", date_str="2030-01-01")
        self.assertIn("2030-01-01", out)
        self.assertIn('<span class="en-only">Override</span>', out)

    def test_missing_markdown_raises(self):
        with self.assertRaises(FileNotFoundError):
            bb.compile_bilingual_html("/nonexistent/file.md")


if __name__ == "__main__":
    unittest.main(verbosity=2)
