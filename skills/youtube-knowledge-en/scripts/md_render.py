#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zero-dependency Markdown -> HTML renderer for YouTube Knowledge notes.

Covers the GitHub-Flavored Markdown subset that knowledge notes actually use:
- Headings with stable anchor ids (10 standard sections get fixed ids)
- Paragraphs, hard breaks, emphasis, strikethrough, inline code, links, images
- Fenced code (```mermaid -> <figure class="diagram"><div class="mermaid">)
- Tables (wrapped in .table-wrap, column alignment, `|` inside code spans)
- Nested / ordered / task lists
- Blockquotes + GitHub alerts (> [!NOTE] -> md2html callouts)
- Horizontal rules
- Raw HTML blocks passed through untouched (e.g. Dual-Mode Visualizer markup)
"""

from __future__ import annotations

import html
import re
import unicodedata
from typing import Dict, List, Set, Tuple

# Fixed anchor ids for the 10 standard sections (matches existing TOC convention).
SECTION_IDS: Dict[int, str] = {
    1: "quick-reference",
    2: "executive-summary",
    3: "mental-model",
    4: "terminology",
    5: "deep-dive",
    6: "playbooks",
    7: "counter-intuitive",
    8: "trade-offs",
    9: "faqs",
    10: "prompts-checklist",
}

# H3 headings appear in the TOC only under these standard sections (or under non-standard H2s).
TOC_H3_PARENTS: Set[str] = {"deep-dive", "playbooks"}

# GitHub alert -> (md2html callout variant, default VI title, default EN title)
ALERT_TYPES: Dict[str, Tuple[str, str, str]] = {
    "NOTE": ("info", "Ghi chú", "Note"),
    "TIP": ("tip", "Mẹo", "Tip"),
    "IMPORTANT": ("decision", "Quan trọng", "Important"),
    "WARNING": ("warn", "Cảnh báo", "Warning"),
    "CAUTION": ("danger", "Thận trọng", "Caution"),
}

RAW_BLOCK_TAGS: Set[str] = {
    "address", "article", "aside", "blockquote", "br", "canvas", "details",
    "dialog", "div", "dl", "fieldset", "figcaption", "figure", "footer", "form",
    "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "iframe", "img", "main",
    "nav", "ol", "p", "picture", "pre", "script", "section", "style", "svg",
    "table", "ul", "video",
}
VOID_TAGS: Set[str] = {"br", "hr", "img"}

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s{0,3}([-*_])(?:\s*\1){2,}\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])(\s+|$)")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$")
BLOCKQUOTE_RE = re.compile(r"^\s{0,3}>")
RAW_START_RE = re.compile(r"^\s{0,3}<(!--|/?([A-Za-z][A-Za-z0-9-]*)(?=[\s/>]|$))")
ALERT_RE = re.compile(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", re.IGNORECASE)
TASK_RE = re.compile(r"^\[([ xX])\]\s+")
SECTION_NUM_RE = re.compile(r"^(\d{1,2})\.\s")
PLACEHOLDER_RE = re.compile(r"\x00(\d+)\x00")
TAG_STRIP_RE = re.compile(r"<[^>]+>")


def slugify(text: str, max_len: int = 60) -> str:
    """ASCII slug for anchor ids (Vietnamese diacritics removed)."""
    text = text.replace("đ", "d").replace("Đ", "D")
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only.lower()).strip("-")
    return slug[:max_len].strip("-") or "section"


def strip_tags(fragment: str) -> str:
    """Plain text from an inline HTML fragment (for TOC labels)."""
    return html.unescape(TAG_STRIP_RE.sub("", fragment)).strip()


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


# ---------------------------------------------------------------------------
# Inline rendering
# ---------------------------------------------------------------------------

def render_inline(text: str) -> str:
    """Render inline Markdown. Inline HTML tags are preserved, stray < > & escaped."""
    stash: List[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    # 1. Code spans (content is literal)
    text = re.sub(
        r"(`+)(.+?)\1",
        lambda m: keep("<code>" + html.escape(m.group(2).strip(), quote=False) + "</code>"),
        text,
    )
    # 2. Backslash escapes
    text = re.sub(
        r"\\([\\`*_{}\[\]()#+\-.!|~<>])",
        lambda m: keep(html.escape(m.group(1), quote=False)),
        text,
    )
    # 3. Autolinks <https://...>
    text = re.sub(
        r"<(https?://[^\s<>]+)>",
        lambda m: keep(
            f'<a href="{html.escape(m.group(1))}" target="_blank" rel="noopener">'
            f"{html.escape(m.group(1), quote=False)}</a>"
        ),
        text,
    )
    # 4. Raw inline HTML tags / comments
    text = re.sub(
        r"<!--.*?-->|</?[A-Za-z][A-Za-z0-9-]*(?:\s+[^<>]*?)?\s*/?>",
        lambda m: keep(m.group(0)),
        text,
    )
    # 5. Escape whatever is left (keep existing entities)
    text = re.sub(r"&(?!#?[A-Za-z0-9]+;)", "&amp;", text)
    text = text.replace("<", "&lt;").replace(">", "&gt;")

    # 6. Images & links (tags stashed so URLs are never touched by emphasis rules)
    def image(m: re.Match) -> str:
        alt = m.group(1).replace('"', "&quot;")
        src = m.group(2).replace('"', "%22")
        title = f' title="{m.group(3).replace(chr(34), "&quot;")}"' if m.group(3) else ""
        return keep(f'<img src="{src}" alt="{alt}"{title} loading="lazy">')

    text = re.sub(r'!\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+"([^"]*)")?\s*\)', image, text)

    def link(m: re.Match) -> str:
        href = m.group(2).replace('"', "%22")
        attrs = f' href="{href}"'
        if m.group(3):
            attrs += f' title="{m.group(3).replace(chr(34), "&quot;")}"'
        if href.startswith(("http://", "https://")):
            attrs += ' target="_blank" rel="noopener"'
        return keep(f"<a{attrs}>") + m.group(1) + keep("</a>")

    text = re.sub(r'\[([^\]]+)\]\(\s*([^)\s]+)(?:\s+"([^"]*)")?\s*\)', link, text)

    # 7. Bare URLs
    text = re.sub(
        r"(?<![\w/\"=])(https?://[^\s<>()\[\]\x00]*[^\s<>()\[\].,;:!?'\"\x00])",
        lambda m: keep(f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>'),
        text,
    )

    # 8. Emphasis
    text = re.sub(r"\*\*\*(?=\S)(.+?)(?<=\S)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)__(?=\S)(.+?)(?<=\S)__(?!\w)", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![*\w])", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)_(?=[^\s_])(.+?)(?<=[^\s_])_(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"<del>\1</del>", text)

    # 9. Restore stashed fragments
    for _ in range(5):
        restored = PLACEHOLDER_RE.sub(lambda m: stash[int(m.group(1))], text)
        if restored == text:
            break
        text = restored
    return text


# ---------------------------------------------------------------------------
# Block rendering
# ---------------------------------------------------------------------------

class MarkdownRenderer:
    """Stateful renderer: collects headings (for TOC) and keeps anchor ids unique."""

    def __init__(self, id_suffix: str = "", lang: str = "vi") -> None:
        self.id_suffix = id_suffix
        self.lang = lang
        self.headings: List[Tuple[int, str, str, bool]] = []  # (level, id, plain text, in_toc)
        self._used_ids: Set[str] = set()
        self._parent_h2: str = ""  # base id of the current H2 section

    # ---- public -----------------------------------------------------------

    def render(self, markdown_text: str) -> str:
        text = markdown_text.replace("\r\n", "\n").replace("\r", "\n").expandtabs(4)
        return self._blocks(text.split("\n"))

    def toc_html(self) -> str:
        links = []
        for level, anchor, label, in_toc in self.headings:
            if not in_toc:
                continue
            links.append(
                f'<a href="#{anchor}" class="lvl-{level}">{html.escape(label, quote=False)}</a>'
            )
        return "\n".join(links)

    # ---- block dispatcher ---------------------------------------------------

    def _blocks(self, lines: List[str], tight: bool = False) -> str:
        out: List[str] = []
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            fence = FENCE_RE.match(line)
            if fence:
                i, block = self._fence(lines, i, fence)
            elif self._is_raw_start(line):
                i, block = self._raw_html(lines, i)
            elif HEADING_RE.match(line):
                m = HEADING_RE.match(line)
                block = self._heading(len(m.group(1)), m.group(2))
                i += 1
            elif HR_RE.match(line):
                block = "<hr>"
                i += 1
            elif self._is_table_start(lines, i):
                i, block = self._table(lines, i)
            elif BLOCKQUOTE_RE.match(line):
                i, block = self._blockquote(lines, i)
            elif LIST_RE.match(line):
                i, block = self._list(lines, i)
            else:
                i, block = self._paragraph(lines, i, tight)
            out.append(block)
        return "\n".join(out)

    def _is_block_start(self, lines: List[str], i: int) -> bool:
        line = lines[i]
        return bool(
            FENCE_RE.match(line)
            or HEADING_RE.match(line)
            or HR_RE.match(line)
            or BLOCKQUOTE_RE.match(line)
            or LIST_RE.match(line)
            or self._is_raw_start(line)
            or self._is_table_start(lines, i)
        )

    # ---- fenced code ------------------------------------------------------

    def _fence(self, lines: List[str], i: int, m: re.Match) -> Tuple[int, str]:
        indent, marker, info = len(m.group(1)), m.group(2), m.group(3).strip()
        lang = info.split()[0] if info else ""
        close_re = re.compile(r"^\s*" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}\s*$")
        body: List[str] = []
        i += 1
        while i < len(lines) and not close_re.match(lines[i]):
            raw = lines[i]
            body.append(raw[min(indent, _indent(raw)):])
            i += 1
        i += 1  # skip closing fence (or EOF)
        src = "\n".join(body)
        if lang.lower() == "mermaid":
            # Escaped so mermaid reads the original source via textContent.
            return i, (
                '<figure class="diagram">\n<div class="mermaid">\n'
                f"{html.escape(src, quote=False)}\n</div>\n</figure>"
            )
        cls = f' class="language-{html.escape(lang)}"' if lang else ""
        return i, f"<pre><code{cls}>{html.escape(src, quote=False)}</code></pre>"

    # ---- raw HTML ---------------------------------------------------------

    @staticmethod
    def _is_raw_start(line: str) -> bool:
        m = RAW_START_RE.match(line)
        if not m:
            return False
        if m.group(1) == "!--":
            return True
        return (m.group(2) or "").lower() in RAW_BLOCK_TAGS

    def _raw_html(self, lines: List[str], i: int) -> Tuple[int, str]:
        start = i
        m = RAW_START_RE.match(lines[i])
        if m.group(1) == "!--":
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            return i + 1, "\n".join(lines[start:i + 1])

        tag = m.group(2).lower()
        if tag in VOID_TAGS:
            return i + 1, lines[i]

        open_re = re.compile(r"<" + tag + r"(?=[\s/>])(?![^>]*/>)", re.IGNORECASE)
        close_re = re.compile(r"</" + tag + r"\s*>", re.IGNORECASE)
        depth = 0
        while i < len(lines):
            depth += len(open_re.findall(lines[i])) - len(close_re.findall(lines[i]))
            i += 1
            if depth <= 0:
                return i, "\n".join(lines[start:i])

        # Unbalanced markup: fall back to CommonMark rule (block ends at blank line).
        i = start
        while i < len(lines) and lines[i].strip():
            i += 1
        return i, "\n".join(lines[start:i])

    # ---- headings ---------------------------------------------------------

    def _heading(self, level: int, raw_text: str) -> str:
        inner = render_inline(raw_text)
        label = strip_tags(inner)
        tag_level = max(level, 2)  # H1 is reserved for the document title

        base = ""
        standard = False
        if tag_level == 2:
            num = SECTION_NUM_RE.match(label)
            if num and int(num.group(1)) in SECTION_IDS:
                base = SECTION_IDS[int(num.group(1))]
                standard = True
        if not base:
            base = slugify(label)

        if tag_level == 2:
            in_toc = True
            self._parent_h2 = base if standard else ""
        elif tag_level == 3:
            in_toc = (not self._parent_h2) or self._parent_h2 in TOC_H3_PARENTS
        else:
            in_toc = False

        anchor, n = base, 2
        while anchor in self._used_ids:
            anchor = f"{base}-{n}"
            n += 1
        self._used_ids.add(anchor)
        anchor += self.id_suffix

        self.headings.append((tag_level, anchor, label, in_toc))
        return f'<h{tag_level} id="{anchor}">{inner}</h{tag_level}>'

    # ---- tables -----------------------------------------------------------

    @staticmethod
    def _is_table_start(lines: List[str], i: int) -> bool:
        return (
            "|" in lines[i]
            and i + 1 < len(lines)
            and "-" in lines[i + 1]
            and bool(TABLE_SEP_RE.match(lines[i + 1]))
        )

    @staticmethod
    def _split_row(line: str) -> List[str]:
        s = line.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|") and not s.endswith("\\|"):
            s = s[:-1]
        cells: List[str] = []
        buf, in_code, j = "", False, 0
        while j < len(s):
            c = s[j]
            if c == "\\" and j + 1 < len(s) and s[j + 1] == "|":
                buf += "|"
                j += 2
                continue
            if c == "`":
                in_code = not in_code
            if c == "|" and not in_code:
                cells.append(buf.strip())
                buf = ""
            else:
                buf += c
            j += 1
        cells.append(buf.strip())
        return cells

    def _table(self, lines: List[str], i: int) -> Tuple[int, str]:
        header = self._split_row(lines[i])
        aligns: List[str] = []
        for spec in self._split_row(lines[i + 1]):
            spec = spec.strip()
            if spec.startswith(":") and spec.endswith(":"):
                aligns.append("center")
            elif spec.endswith(":"):
                aligns.append("right")
            elif spec.startswith(":"):
                aligns.append("left")
            else:
                aligns.append("")
        i += 2
        rows: List[List[str]] = []
        while i < len(lines) and lines[i].strip() and "|" in lines[i]:
            rows.append(self._split_row(lines[i]))
            i += 1

        cols = len(header)

        def cell(tag: str, content: str, idx: int) -> str:
            align = aligns[idx] if idx < len(aligns) else ""
            style = f' style="text-align: {align}"' if align else ""
            return f"<{tag}{style}>{render_inline(content)}</{tag}>"

        parts = ['<div class="table-wrap">', "<table>", "<thead>", "<tr>"]
        parts += [cell("th", h, k) for k, h in enumerate(header)]
        parts += ["</tr>", "</thead>", "<tbody>"]
        for row in rows:
            row = (row + [""] * cols)[:cols]
            parts.append("<tr>" + "".join(cell("td", c, k) for k, c in enumerate(row)) + "</tr>")
        parts += ["</tbody>", "</table>", "</div>"]
        return i, "\n".join(parts)

    # ---- blockquotes & alerts --------------------------------------------

    def _blockquote(self, lines: List[str], i: int) -> Tuple[int, str]:
        inner: List[str] = []
        while i < len(lines) and BLOCKQUOTE_RE.match(lines[i]):
            inner.append(re.sub(r"^\s{0,3}> ?", "", lines[i]))
            i += 1

        first = inner[0].strip() if inner else ""
        alert = ALERT_RE.match(first)
        if alert:
            kind = alert.group(1).upper()
            variant, title_vi, title_en = ALERT_TYPES[kind]
            title = alert.group(2).strip() or (title_en if self.lang == "en" else title_vi)
            body = self._blocks(inner[1:])
            return i, (
                f'<aside class="callout callout-{variant}">\n'
                f'  <svg class="callout-icon" viewBox="0 0 24 24" aria-hidden="true">'
                f'<use href="#i-{variant}"/></svg>\n'
                f'  <div class="callout-body">\n'
                f'    <p class="callout-title">{render_inline(title)}</p>\n'
                f"{body}\n"
                f"  </div>\n"
                f"</aside>"
            )
        return i, f"<blockquote>\n{self._blocks(inner)}\n</blockquote>"

    # ---- lists ------------------------------------------------------------

    def _list(self, lines: List[str], i: int) -> Tuple[int, str]:
        first = LIST_RE.match(lines[i])
        base_indent = len(first.group(1))
        ordered = first.group(2)[0].isdigit()
        start_num = int(first.group(2)[:-1]) if ordered else 1
        items: List[List[str]] = []
        loose = False
        n = len(lines)

        while i < n:
            m = LIST_RE.match(lines[i])
            if not m or len(m.group(1)) != base_indent or m.group(2)[0].isdigit() != ordered:
                break
            content_indent = len(m.group(0)) if m.group(3) else len(m.group(0)) + 1
            item_lines = [lines[i][len(m.group(0)):]]
            i += 1
            while i < n:
                cur = lines[i]
                if not cur.strip():
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and _indent(lines[j]) > base_indent and not (
                        LIST_RE.match(lines[j]) and _indent(lines[j]) == base_indent
                    ):
                        item_lines.extend([""] * (j - i))
                        loose = loose or not LIST_RE.match(lines[j])
                        i = j
                        continue
                    break
                ind = _indent(cur)
                if ind > base_indent:
                    item_lines.append(cur[min(ind, content_indent):])
                    i += 1
                    continue
                if self._is_block_start(lines, i):
                    break
                item_lines.append(cur.strip())  # lazy continuation
                i += 1
            items.append(item_lines)

            # Blank line(s) between sibling items -> loose list
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j > i and j < n:
                nxt = LIST_RE.match(lines[j])
                if nxt and len(nxt.group(1)) == base_indent and nxt.group(2)[0].isdigit() == ordered:
                    loose = True
                    i = j

        rendered: List[str] = []
        for item_lines in items:
            head = item_lines[0] if item_lines else ""
            checkbox, li_cls = "", ""
            task = TASK_RE.match(head)
            if task:
                checked = " checked" if task.group(1).lower() == "x" else ""
                checkbox = f'<input type="checkbox" disabled{checked}> '
                li_cls = ' class="task-item"'
                item_lines = [head[task.end():]] + item_lines[1:]
            body = self._blocks(item_lines, tight=not loose)
            rendered.append(f"<li{li_cls}>{checkbox}{body}</li>")

        tag = "ol" if ordered else "ul"
        start_attr = f' start="{start_num}"' if ordered and start_num != 1 else ""
        return i, f"<{tag}{start_attr}>\n" + "\n".join(rendered) + f"\n</{tag}>"

    # ---- paragraphs -------------------------------------------------------

    def _paragraph(self, lines: List[str], i: int, tight: bool) -> Tuple[int, str]:
        buf: List[str] = []
        while i < len(lines) and lines[i].strip():
            if buf and self._is_block_start(lines, i):
                break
            raw = lines[i]
            if raw.endswith("  ") or raw.rstrip().endswith("\\") and not raw.rstrip().endswith("\\\\"):
                raw = raw.rstrip().rstrip("\\").rstrip() + "<br>"
            buf.append(raw.strip())
            i += 1
        text = render_inline("\n".join(buf))
        return i, text if tight else f"<p>{text}</p>"
