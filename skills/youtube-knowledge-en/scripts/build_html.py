#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-Language HTML Compiler for YouTube Knowledge Learner (vi / en)
Converts a Markdown knowledge note into an interactive standalone HTML document.
"""

import sys
import os
import re
import argparse
import datetime as dt
from pathlib import Path
from typing import Optional, Dict, Any, List

# Locate template
def find_template_path() -> Path:
    candidates = [
        Path(__file__).resolve().parent / "template.html",
        Path(__file__).resolve().parent.parent / "template.html",
        Path(__file__).resolve().parent.parent / "references" / "template.html",
        Path.home() / "Projects" / "md2html" / "template.html",
        Path.home() / ".gemini" / "config" / "skills" / "md2html" / "template.html",
        Path("/Users/maingocanh/Projects/md2html/template.html"),
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("template.html not found.")

def compile_single_html(
    md_path: str,
    html_path: Optional[str] = None,
    lang: str = "en",
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    date_str: Optional[str] = None,
) -> str:
    md_file = Path(md_path).resolve()
    if not md_file.exists():
        raise FileNotFoundError(f"Markdown file does not exist: {md_file}")
    html_file = Path(html_path).resolve() if html_path else md_file.with_suffix(".html")

    # Import local modules
    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))
    from md_render import MarkdownRenderer, render_inline, strip_tags
    from flow_viewer import inject_flow_viewer

    md_text = md_file.read_text(encoding="utf-8")
    
    # Extract Title if not provided
    h1_m = re.search(r"^#\s+(.+?)\s*$", md_text, re.MULTILINE)
    note_title = title or (h1_m.group(1).strip() if h1_m else md_file.stem)
    
    # Body MD: drop first H1 if it matches note_title
    body_md = md_text
    if h1_m and not title:
        body_md = md_text[h1_m.end():].lstrip("\n")

    renderer = MarkdownRenderer(id_suffix="", lang=lang)
    body_html = renderer.render(body_md)
    toc_html = renderer.toc_html()

    # Read time
    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>|```.*?```", " ", md_text, flags=re.DOTALL)))
    minutes = max(1, round(words / 230))
    read_time = f"~{minutes} phút đọc" if lang == "vi" else f"~{minutes} min read"

    date_val = date_str or dt.date.today().isoformat()
    
    # Read template
    tpl = find_template_path().read_text(encoding="utf-8")

    # Labels based on lang
    if lang == "en":
        replacements = {
            "{{LANG}}": "en",
            "{{REC_LABEL}}": "★ Recommended",
            "{{TITLE}}": render_inline(note_title),
            "{{SUBTITLE}}": render_inline(subtitle or "YouTube Knowledge Reference Notes"),
            "{{DOC_TYPE}}": "NOTES",
            "{{SOURCE_FILE}}": md_file.name,
            "{{DATE}}": date_val,
            "{{READ_TIME}}": read_time,
            "{{BRAND_LABEL}}": "Knowledge Notes",
            "{{TOC_TITLE}}": "Table of Contents",
            "{{PRINT_TOOLTIP}}": "Print / Save PDF",
            "{{THEME_TOOLTIP}}": "Toggle Theme",
            "{{CLOSE_LABEL}}": "Close",
            "{{SKIP_LINK_LABEL}}": "Skip to main content",
            "{{FOOTER_NOTE}}": f"Source: YouTube Reference Notes · {date_val}",
        }
    else:
        replacements = {
            "{{LANG}}": "vi",
            "{{REC_LABEL}}": "★ Đề xuất",
            "{{TITLE}}": render_inline(note_title),
            "{{SUBTITLE}}": render_inline(subtitle or "Ghi chú kiến thức từ YouTube"),
            "{{DOC_TYPE}}": "NOTES",
            "{{SOURCE_FILE}}": md_file.name,
            "{{DATE}}": date_val,
            "{{READ_TIME}}": read_time,
            "{{BRAND_LABEL}}": "Ghi chú kiến thức",
            "{{TOC_TITLE}}": "Mục lục",
            "{{PRINT_TOOLTIP}}": "In / Lưu PDF",
            "{{THEME_TOOLTIP}}": "Đổi giao diện",
            "{{CLOSE_LABEL}}": "Đóng",
            "{{SKIP_LINK_LABEL}}": "Chuyển đến nội dung chính",
            "{{FOOTER_NOTE}}": f"Nguồn: YouTube · {date_val}",
        }

    for k, v in replacements.items():
        tpl = tpl.replace(k, str(v))

    tpl = tpl.replace("<!-- TOC_ENTRIES -->", f'<div id="toc-links">\n{toc_html.strip()}\n</div>')
    tpl = tpl.replace("<!-- CONTENT_START -->", f'<div data-lang-body="{lang}">\n{body_html.strip()}\n</div>')

    # Inject Flow Viewer
    tpl = inject_flow_viewer(tpl)

    html_file.write_text(tpl, encoding="utf-8")
    print(f"✅ {html_file} ({len(tpl.encode('utf-8')) / 1024:.0f} KB) · {len(renderer.headings)} headings")
    return tpl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Single-Language HTML Compiler for YouTube Knowledge")
    parser.add_argument("md_path", help="Path to source Markdown file")
    parser.add_argument("--out", "-o", help="Path to output HTML file")
    parser.add_argument("--lang", choices=["vi", "en"], default="en", help="Document language (default: en)")
    parser.add_argument("--title", help="Override document title")
    parser.add_argument("--subtitle", help="Override subtitle")
    parser.add_argument("--date", help="Date string YYYY-MM-DD")
    args = parser.parse_args()

    compile_single_html(
        args.md_path,
        args.out,
        lang=args.lang,
        title=args.title,
        subtitle=args.subtitle,
        date_str=args.date,
    )
