#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bilingual HTML Compiler for YouTube Knowledge Learner (vi-en v2.1)
Converts or assembles a bilingual Markdown knowledge file into an interactive dual-language HTML document:
- Interactive language switcher button (🇻🇳 VI | 🇬🇧 EN) in topbar
- Seamless instant toggling with zero duplicate text via scoped CSS
- Dual Table of Contents (#toc-links-vi and #toc-links-en) with accurate anchor links
- Complete Dual-Mode Visualizer (Bento Grid + Mermaid Flowchart) for both languages
- Robust safe Mermaid execution and isolated zoom controls

CLI (full pipeline: split Part 1 / Part 2 -> render Markdown -> dual TOC -> HTML):
    python3 build_bilingual_html.py note.md [--out note.html] [--title-en ...] [--date YYYY-MM-DD]
"""

import sys
import os
import re
import argparse
import datetime as dt
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_render import MarkdownRenderer, render_inline, strip_tags  # noqa: E402
from flow_viewer import inject_flow_viewer  # noqa: E402

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
    raise FileNotFoundError("template.html not found in expected locations.")


def prepare_bilingual_template(template_path: Optional[Path] = None) -> str:
    """
    Reads the base md2html template and injects:
    1. CSS for language switcher & strict bilingual visibility
    2. Root data-lang='vi'
    3. Topbar language switcher buttons (🇻🇳 VI | 🇬🇧 EN)
    4. Clean TOC attributes to prevent double-quote parsing bugs
    5. Robust JavaScript runtime with scoped Mermaid rendering and isolated zoom state
    """
    if template_path is None:
        template_file = find_template_path()
    else:
        template_file = Path(template_path).resolve()
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found at {template_file}")

    tpl = template_file.read_text(encoding="utf-8")

    # 1. CSS for Language Switcher & Robust Visibility
    lang_css = """
    /* ============================================================
       LANGUAGE SWITCHER & VISIBILITY CONTROLS (v2.0)
       ============================================================ */
    .lang-switcher {
      display: inline-flex;
      align-items: center;
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 2px;
      gap: 2px;
      margin-right: 6px;
    }
    .lang-btn {
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 600;
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: inherit;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .lang-btn:hover { color: var(--text); background: var(--surface-3); }
    .lang-btn.active {
      background: var(--surface);
      color: var(--accent);
      box-shadow: var(--shadow-sm);
      font-weight: 700;
    }

    /* Guaranteed Language Visibility: Vietnamese by default, English when data-lang='en' */
    html:not([data-lang="en"]) .en-only { display: none !important; }
    html:not([data-lang="en"]) .vi-only { display: revert !important; }
    html[data-lang="en"] .vi-only { display: none !important; }
    html[data-lang="en"] .en-only { display: revert !important; }
"""
    tpl = tpl.replace(
        "/* ============================================================\n       LAYOUT",
        lang_css + "\n    /* ============================================================\n       LAYOUT",
    )

    # 2. Set root HTML with explicit data-lang="vi"
    tpl = tpl.replace(
        '<html lang="{{LANG}}" data-theme="light" style="--rec-label: \'{{REC_LABEL}}\'">',
        '<html lang="vi" data-lang="vi" data-theme="light" style="--rec-label: \'★ Đề xuất / Recommended\'">',
    )

    # 3. Inject Language Switcher into Topbar
    topbar_switcher = """
      <div class="topbar-actions">
        <div class="lang-switcher" role="group" aria-label="Language selection">
          <button class="lang-btn active" id="btn-lang-vi" onclick="setLanguage('vi')" title="Chuyển sang Tiếng Việt" aria-pressed="true">🇻🇳 VI</button>
          <button class="lang-btn" id="btn-lang-en" onclick="setLanguage('en')" title="Switch to English" aria-pressed="false">🇬🇧 EN</button>
        </div>
"""
    tpl = tpl.replace('<div class="topbar-actions">', topbar_switcher)

    # 4. Clean TOC attributes to prevent broken double quotes
    tpl = tpl.replace(
        '<button class="icon-btn toc-mobile-trigger" id="toc-toggle" onclick="openToc()" aria-label="{{TOC_TITLE}}" title="{{TOC_TITLE}}">',
        '<button class="icon-btn toc-mobile-trigger" id="toc-toggle" onclick="openToc()" aria-label="Mục lục / Table of Contents" title="Mục lục / Table of Contents">',
    )
    tpl = tpl.replace(
        '<aside class="toc" id="toc" aria-label="{{TOC_TITLE}}">',
        '<aside class="toc" id="toc" aria-label="Mục lục / Table of Contents">',
    )
    tpl = tpl.replace(
        '<p class="toc-title">{{TOC_TITLE}}</p>',
        '<p class="toc-title"><span class="vi-only">Mục lục</span><span class="en-only">Table of Contents</span></p>',
    )

    # 5. JavaScript Runtime: Safe Mermaid + Bilingual System Map Controls
    old_mermaid_code = """    const diagramSources = new Map();
    function initMermaid() {
      const isDark = currentTheme() === "dark";
      mermaid.initialize({
        startOnLoad: false,
        theme: "base",
        themeVariables: {
          primaryColor: isDark ? "#1E293B" : "#FFFFFF",
          primaryTextColor: isDark ? "#F8FAFC" : "#0F172A",
          primaryBorderColor: isDark ? "#475569" : "#CBD5E1",
          lineColor: isDark ? "#94A3B8" : "#64748B",
          secondaryColor: isDark ? "#0F172A" : "#F8FAFC",
          tertiaryColor: isDark ? "#1E293B" : "#FFFFFF",
          clusterBkg: isDark ? "#0F172A" : "#F8FAFC",
          clusterBorder: isDark ? "#334155" : "#E2E8F0",
          edgeLabelBackground: isDark ? "#1E293B" : "#FFFFFF",
          nodeBorder: isDark ? "#475569" : "#CBD5E1",
          mainBkg: isDark ? "#1E293B" : "#FFFFFF",
          nodeTextColor: isDark ? "#F8FAFC" : "#0F172A",
          titleColor: isDark ? "#F1F5F9" : "#1E293B",
          fontFamily: "Inter, system-ui, sans-serif",
          fontSize: "12px",
        },
      });
    }
    async function renderMermaid() {
      initMermaid();
      const els = document.querySelectorAll(".mermaid");
      els.forEach(el => {
        if (!diagramSources.has(el)) diagramSources.set(el, el.textContent.trim());
        el.textContent = diagramSources.get(el);
        el.removeAttribute("data-processed");
      });
      try { await mermaid.run({ nodes: els }); } catch (e) { console.error(e); }
    }"""

    new_mermaid_code = """    const diagramSources = new Map();
    function initMermaid() {
      if (typeof mermaid === "undefined") return false;
      const isDark = currentTheme() === "dark";
      try {
        mermaid.initialize({
          startOnLoad: false,
          theme: "base",
          themeVariables: {
            primaryColor: isDark ? "#1E293B" : "#FFFFFF",
            primaryTextColor: isDark ? "#F8FAFC" : "#0F172A",
            primaryBorderColor: isDark ? "#475569" : "#CBD5E1",
            lineColor: isDark ? "#94A3B8" : "#64748B",
            secondaryColor: isDark ? "#0F172A" : "#F8FAFC",
            tertiaryColor: isDark ? "#1E293B" : "#FFFFFF",
            clusterBkg: isDark ? "#0F172A" : "#F8FAFC",
            clusterBorder: isDark ? "#334155" : "#E2E8F0",
            edgeLabelBackground: isDark ? "#1E293B" : "#FFFFFF",
            nodeBorder: isDark ? "#475569" : "#CBD5E1",
            mainBkg: isDark ? "#1E293B" : "#FFFFFF",
            nodeTextColor: isDark ? "#F8FAFC" : "#0F172A",
            titleColor: isDark ? "#F1F5F9" : "#1E293B",
            fontFamily: "Inter, system-ui, sans-serif",
            fontSize: "12px",
          },
        });
        return true;
      } catch (e) {
        console.warn("Mermaid init error:", e);
        return false;
      }
    }
    async function renderMermaid(forcedSuffix) {
      if (typeof mermaid === "undefined") return;
      if (!initMermaid()) return;
      try {
        const lang = document.documentElement.dataset.lang || "vi";
        const suffix = (forcedSuffix !== undefined) ? forcedSuffix : ((lang === "en") ? "-en" : "");
        const nodes = [];

        // 1. Visualizer flow tab (only when it is the active tab)
        const targetView = document.getElementById("view-flow" + suffix);
        if (targetView && targetView.classList.contains("active")) {
          const el = targetView.querySelector(".mermaid");
          if (el) nodes.push(el);
        }

        // 2. Standalone diagrams in the visible language body (hidden ones render on switch)
        const body = document.querySelector('[data-lang-body="' + (suffix === "-en" ? "en" : "vi") + '"]');
        if (body) {
          body.querySelectorAll(".mermaid").forEach(el => {
            if (!el.closest(".system-map-view")) nodes.push(el);
          });
        }
        if (!nodes.length) return;

        const decoder = document.createElement("textarea");
        nodes.forEach(el => {
          if (!diagramSources.has(el)) {
            // innerHTML keeps raw <br/>, <b>, <i> that textContent would drop; textarea decodes entities only
            decoder.innerHTML = el.innerHTML;
            diagramSources.set(el, decoder.value.trim());
          }
          el.textContent = diagramSources.get(el);
          el.removeAttribute("data-processed");
        });
        await mermaid.run({ nodes });
      } catch (e) {
        console.warn("Mermaid render error:", e);
      }
    }"""
    if old_mermaid_code not in tpl:
        raise RuntimeError("md2html template changed: Mermaid runtime block not found, cannot inject bilingual runtime.")
    tpl = tpl.replace(old_mermaid_code, new_mermaid_code)

    old_system_map_code = """    // ---------- System Map Dual-Mode Switcher & Controls ----------
    function switchSystemView(mode) {
      const bentoTab = document.getElementById("tab-btn-bento");
      const flowTab = document.getElementById("tab-btn-flow");
      const bentoView = document.getElementById("view-bento");
      const flowView = document.getElementById("view-flow");
      if (!bentoTab || !flowTab || !bentoView || !flowView) return;

      if (mode === "bento") {
        bentoTab.classList.add("active");
        bentoTab.setAttribute("aria-selected", "true");
        flowTab.classList.remove("active");
        flowTab.setAttribute("aria-selected", "false");
        bentoView.classList.add("active");
        flowView.classList.remove("active");
      } else {
        flowTab.classList.add("active");
        flowTab.setAttribute("aria-selected", "true");
        bentoTab.classList.remove("active");
        bentoTab.setAttribute("aria-selected", "false");
        flowView.classList.add("active");
        bentoView.classList.remove("active");
        renderMermaid();
      }
    }

    let flowZoomLevel = 1;
    function zoomFlow(delta) {
      const svg = document.querySelector("#view-flow .mermaid svg");
      if (!svg) return;
      flowZoomLevel = Math.max(0.5, Math.min(2.5, flowZoomLevel + delta));
      svg.style.transform = `scale(${flowZoomLevel})`;
      svg.style.transformOrigin = "top center";
      svg.style.transition = "transform 0.2s ease";
    }
    function resetFlowZoom() {
      const svg = document.querySelector("#view-flow .mermaid svg");
      if (!svg) return;
      flowZoomLevel = 1;
      svg.style.transform = "scale(1)";
    }
    function toggleFlowFullscreen() {
      const vp = document.getElementById("flow-viewport-box");
      if (!vp) return;
      vp.classList.toggle("is-fullscreen");
    }"""

    new_system_and_lang_code = """    // ---------- Dual-Language Runtime Switcher ----------
    const LANG_STORAGE_KEY = "youtube-learner-lang";
    function setLanguage(lang) {
      if (lang !== "en" && lang !== "vi") lang = "vi";
      document.documentElement.dataset.lang = lang;
      document.documentElement.lang = lang;
      try {
        localStorage.setItem(LANG_STORAGE_KEY, lang);
      } catch (e) {}

      const btnVi = document.getElementById("btn-lang-vi");
      const btnEn = document.getElementById("btn-lang-en");
      if (btnVi && btnEn) {
        btnVi.classList.toggle("active", lang === "vi");
        btnVi.setAttribute("aria-pressed", lang === "vi" ? "true" : "false");
        btnEn.classList.toggle("active", lang === "en");
        btnEn.setAttribute("aria-pressed", lang === "en" ? "true" : "false");
      }

      // If flowchart tab is currently active for this language, trigger render
      const suffix = (lang === "en") ? "-en" : "";
      const flowView = document.getElementById("view-flow" + suffix);
      if (flowView && flowView.classList.contains("active")) {
        renderMermaid(suffix);
      }
    }
    window.setLanguage = setLanguage;

    function restoreLanguage() {
      let saved = "vi";
      try {
        saved = localStorage.getItem(LANG_STORAGE_KEY) || "vi";
      } catch (e) {}
      setLanguage(saved);
    }

    // ---------- System Map Dual-Mode Switcher & Controls (Bilingual) ----------
    function switchSystemView(mode, lang) {
      const suffix = (lang === 'en') ? '-en' : '';
      const bentoTab = document.getElementById("tab-btn-bento" + suffix) || document.getElementById("tab-btn-bento");
      const flowTab = document.getElementById("tab-btn-flow" + suffix) || document.getElementById("tab-btn-flow");
      const bentoView = document.getElementById("view-bento" + suffix) || document.getElementById("view-bento");
      const flowView = document.getElementById("view-flow" + suffix) || document.getElementById("view-flow");
      if (!bentoTab || !flowTab || !bentoView || !flowView) return;

      if (mode === "bento") {
        bentoTab.classList.add("active");
        bentoTab.setAttribute("aria-selected", "true");
        flowTab.classList.remove("active");
        flowTab.setAttribute("aria-selected", "false");
        bentoView.classList.add("active");
        flowView.classList.remove("active");
      } else {
        flowTab.classList.add("active");
        flowTab.setAttribute("aria-selected", "true");
        bentoTab.classList.remove("active");
        bentoTab.setAttribute("aria-selected", "false");
        flowView.classList.add("active");
        bentoView.classList.remove("active");
        renderMermaid(suffix);
      }
    }
    window.switchSystemView = switchSystemView;

    // Zoom / pan / fullscreen (zoomFlow, resetFlowZoom, toggleFlowFullscreen)
    // are provided by the FLOW-VIEWER block injected before </body> (flow_viewer.py)."""
    if old_system_map_code not in tpl:
        raise RuntimeError("md2html template changed: System Map runtime block not found, cannot inject language switcher.")
    tpl = tpl.replace(old_system_map_code, new_system_and_lang_code)

    old_boot_code = """    // ---------- Boot ----------
    document.addEventListener("DOMContentLoaded", () => {
      applyThemeIcon();
      injectAnchors();
      injectCopyButtons();
      renderMermaid();
      setupTocSpy();
      setupScrollProgress();
    });"""

    new_boot_code = """    // ---------- Boot ----------
    document.addEventListener("DOMContentLoaded", () => {
      restoreLanguage();
      applyThemeIcon();
      injectAnchors();
      injectCopyButtons();
      renderMermaid();
      setupTocSpy();
      setupScrollProgress();
    });"""
    if old_boot_code not in tpl:
        raise RuntimeError("md2html template changed: Boot block not found, cannot inject restoreLanguage().")
    tpl = tpl.replace(old_boot_code, new_boot_code)

    tpl = inject_flow_viewer(tpl)

    for marker in ('data-lang="vi"', 'id="btn-lang-vi"', "function setLanguage(", "FLOW-VIEWER:START"):
        if marker not in tpl:
            raise RuntimeError(f"Bilingual template injection failed (missing {marker!r}).")

    return tpl


def assemble_bilingual_document(
    template_html: str,
    title_vi: str,
    title_en: str,
    subtitle_vi: str,
    subtitle_en: str,
    source_file: str,
    toc_vi_html: str,
    toc_en_html: str,
    body_vi_html: str,
    body_en_html: str,
    date_str: Optional[str] = None,
    read_time_vi: str = "~25 phút đọc",
    read_time_en: str = "~25 min read",
    footer_note: Optional[str] = None,
    out_path: Optional[Path] = None,
) -> str:
    """
    Injects all bilingual metadata, dual TOCs, and dual bodies into the prepared template.
    """
    html = template_html
    date_str = date_str or dt.date.today().isoformat()
    page_title = title_vi if title_vi.strip() == title_en.strip() else f"{title_vi} / {title_en}"

    # Standard placeholders
    replacements = {
        "{{REC_LABEL}}": "★ Đề xuất / Recommended",
        "{{TITLE}}": strip_tags(page_title),
        "{{DOC_TYPE}}": '<span class="vi-only">GHI CHÚ KIẾN THỨC</span><span class="en-only">KNOWLEDGE NOTES</span>',
        "{{SOURCE_FILE}}": source_file,
        "{{DATE}}": date_str,
        "{{READ_TIME}}": f'<span class="vi-only">{read_time_vi}</span><span class="en-only">{read_time_en}</span>',
        "{{BRAND_LABEL}}": '<span class="vi-only">Ghi chú kiến thức</span><span class="en-only">Knowledge Notes</span>',
        "{{PRINT_TOOLTIP}}": "In / Lưu PDF / Print",
        "{{THEME_TOOLTIP}}": "Đổi giao diện / Theme",
        "{{CLOSE_LABEL}}": "Đóng / Close",
        "{{SKIP_LINK_LABEL}}": "Chuyển đến nội dung chính / Skip to main",
        "{{FOOTER_NOTE}}": footer_note or f"Nguồn: YouTube Knowledge Learner — {source_file}",
    }
    for k, v in replacements.items():
        html = html.replace(k, v)

    # Replace Title and Subtitle in content header
    html = re.sub(
        r'<h1 class="doc-title">.*?</h1>',
        f'<h1 class="doc-title"><span class="vi-only">{title_vi}</span><span class="en-only">{title_en}</span></h1>',
        html,
    )
    html = re.sub(
        r'<p class="doc-subtitle">.*?</p>',
        f'<p class="doc-subtitle"><span class="vi-only">{subtitle_vi}</span><span class="en-only">{subtitle_en}</span></p>',
        html,
    )

    # Replace Dual TOC
    bilingual_toc = f"""<div class="vi-only" id="toc-links-vi">
{toc_vi_html.strip()}
</div>
<div class="en-only" id="toc-links-en">
{toc_en_html.strip()}
</div>"""
    html = html.replace("<!-- TOC_ENTRIES -->", bilingual_toc)

    # Replace Dual Body Content
    bilingual_body = f"""<div class="vi-only" data-lang-body="vi">
{body_vi_html.strip()}
</div>
<div class="en-only" data-lang-body="en">
{body_en_html.strip()}
</div>"""
    html = html.replace("<!-- CONTENT_START -->", bilingual_body)

    if out_path:
        out_file = Path(out_path).resolve()
        out_file.write_text(html, encoding="utf-8")
        print(f"Successfully compiled bilingual document to {out_file} ({len(html):,} bytes)")

    return html


# ---------------------------------------------------------------------------
# Markdown -> bilingual parts
# ---------------------------------------------------------------------------

PART1_RE = re.compile(r"^#\s+(?:PHẦN|PHAN|PART)\s*1\b.*$", re.IGNORECASE | re.MULTILINE)
PART2_RE = re.compile(r"^#\s+(?:PHẦN|PHAN|PART)\s*2\b.*$", re.IGNORECASE | re.MULTILINE)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|", re.MULTILINE)


LEADING_H1_RE = re.compile(r"^(?:\s*(?:---+)?\s*\n)*#\s+(.+?)\s*(?:\n|$)")


def _pop_leading_h1(part_md: str) -> Tuple[Optional[str], str]:
    """If a part starts with '# Title', return (title, rest) so it is not rendered as a section."""
    m = LEADING_H1_RE.match(part_md)
    if not m:
        return None, part_md
    return m.group(1).strip(), part_md[m.end():]


def split_bilingual_markdown(md_text: str) -> Tuple[str, str, str, Optional[str]]:
    """
    Split a bilingual note into (title, part1_vi_md, part2_en_md, part2_title).
    - title: first H1 that is not a Part marker
    - Content before '# PHẦN 1' (the boilerplate architecture note) is dropped
    - A leading H1 inside Part 2 is returned as part2_title (English title)
    - If no Part 2 marker exists, part2_en_md is "" (caller decides fallback)
    """
    md_text = md_text.replace("\r\n", "\n").replace("\r", "\n")
    title = ""
    for m in H1_RE.finditer(md_text):
        if not PART1_RE.match(m.group(0)) and not PART2_RE.match(m.group(0)):
            title = m.group(1).strip()
            break

    p1 = PART1_RE.search(md_text)
    p2 = PART2_RE.search(md_text)

    if p1:
        vi_start = p1.end()
    else:
        # Legacy single-part notes: everything after the title H1
        title_m = re.search(r"^#\s+" + re.escape(title) + r"\s*$", md_text, re.MULTILINE) if title else None
        vi_start = title_m.end() if title_m else 0

    if p2 and p2.start() >= vi_start:
        vi_md = md_text[vi_start:p2.start()]
        en_md = md_text[p2.end():]
    else:
        vi_md = md_text[vi_start:]
        en_md = ""

    # Drop a trailing horizontal rule that separates the parts
    vi_md = re.sub(r"\n\s*---\s*\n*\s*$", "\n", vi_md.rstrip() + "\n")
    _, vi_md = _pop_leading_h1(vi_md.strip("\n"))
    en_title, en_md = _pop_leading_h1(en_md.strip("\n"))
    return title, vi_md.strip("\n"), en_md.strip("\n"), en_title


def _metadata_value(md: str, key_pattern: str) -> Optional[str]:
    """Find the 2nd cell of a metadata table row whose 1st cell matches key_pattern."""
    key_re = re.compile(key_pattern, re.IGNORECASE)
    for m in TABLE_ROW_RE.finditer(md):
        if key_re.search(strip_tags(render_inline(m.group(1)))):
            value = strip_tags(render_inline(m.group(2))).strip(" `")
            if value and not set(value) <= set("-: "):
                return value
    return None


def _read_time(md: str, lang: str) -> str:
    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>|```.*?```", " ", md, flags=re.DOTALL)))
    minutes = max(1, round(words / 230))
    return f"~{minutes} phút đọc" if lang == "vi" else f"~{minutes} min read"


def _find_duplicate_ids(html_doc: str) -> List[str]:
    seen, dupes = set(), set()
    for anchor in re.findall(r'\sid="([^"]+)"', html_doc):
        if anchor in seen:
            dupes.add(anchor)
        seen.add(anchor)
    return sorted(dupes)


def compile_bilingual_html(
    md_path: str,
    html_path: Optional[str] = None,
    title_en: Optional[str] = None,
    subtitle_vi: Optional[str] = None,
    subtitle_en: Optional[str] = None,
    date_str: Optional[str] = None,
) -> str:
    """
    Full pipeline: split Part 1 / Part 2 -> render Markdown -> dual TOC -> assemble HTML.
    Returns the HTML string and writes it next to the Markdown file (or html_path).
    """
    md_file = Path(md_path).resolve()
    if not md_file.exists():
        raise FileNotFoundError(f"Markdown file does not exist: {md_file}")
    html_file = Path(html_path).resolve() if html_path else md_file.with_suffix(".html")

    md_text = md_file.read_text(encoding="utf-8")
    title_vi, vi_md, en_md, en_part_title = split_bilingual_markdown(md_text)
    title_vi = title_vi or md_file.stem
    warnings: List[str] = []

    # Vietnamese body
    vi_renderer = MarkdownRenderer(id_suffix="", lang="vi")
    body_vi_html = vi_renderer.render(vi_md)
    toc_vi_html = vi_renderer.toc_html()

    # English body (fallback notice for legacy single-language notes)
    en_renderer = MarkdownRenderer(id_suffix="-en", lang="en")
    if en_md.strip():
        body_en_html = en_renderer.render(en_md)
    else:
        warnings.append("Không tìm thấy '# PART 2' → bản EN chỉ hiển thị thông báo.")
        body_en_html = en_renderer.render(
            "## English version unavailable\n\n"
            "> [!NOTE]\n> This note has no Part 2 (Full English Reference) yet. "
            "Switch to 🇻🇳 VI to read the Vietnamese version."
        )
    toc_en_html = en_renderer.toc_html()

    # Titles & subtitles (CLI overrides > metadata table > fallback)
    title_en = (
        title_en
        or en_part_title
        or _metadata_value(en_md, r"^(video\s+)?title\b")
        or _metadata_value(vi_md, r"tiêu đề")
        or title_vi
    )
    channel_vi = _metadata_value(vi_md, r"kênh|channel|host")
    channel_en = _metadata_value(en_md, r"channel|host") or channel_vi
    subtitle_vi = subtitle_vi or (
        f"Ghi chú kiến thức song ngữ · {channel_vi}" if channel_vi else "Ghi chú kiến thức song ngữ từ YouTube"
    )
    subtitle_en = subtitle_en or (
        f"Bilingual knowledge notes · {channel_en}" if channel_en else "Bilingual knowledge notes from YouTube"
    )

    html_doc = assemble_bilingual_document(
        template_html=prepare_bilingual_template(),
        title_vi=render_inline(title_vi),
        title_en=render_inline(title_en),
        subtitle_vi=render_inline(subtitle_vi),
        subtitle_en=render_inline(subtitle_en),
        source_file=md_file.name,
        toc_vi_html=toc_vi_html,
        toc_en_html=toc_en_html,
        body_vi_html=body_vi_html,
        body_en_html=body_en_html,
        date_str=date_str,
        read_time_vi=_read_time(vi_md, "vi"),
        read_time_en=_read_time(en_md or vi_md, "en"),
        out_path=None,
    )

    # Post-build validation
    leftovers = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", html_doc)))
    if leftovers:
        warnings.append(f"Placeholder chưa thay: {', '.join(leftovers)}")
    for marker in ("<!-- TOC_ENTRIES -->", "<!-- CONTENT_START -->"):
        if marker in html_doc:
            raise RuntimeError(f"Build lỗi: marker {marker} vẫn còn trong HTML.")
    dupes = _find_duplicate_ids(html_doc)
    if dupes:
        warnings.append(
            "ID trùng (bản EN cần hậu tố -en): " + ", ".join(dupes[:10]) + (" …" if len(dupes) > 10 else "")
        )
    if 'id="system-map-root"' not in html_doc:
        warnings.append("Mục 3 chưa có Dual-Mode Visualizer (id='system-map-root') — chỉ có Mermaid thường nếu có.")

    html_file.write_text(html_doc, encoding="utf-8")

    mermaid_count = html_doc.count('class="mermaid"')
    print(f"✅ {html_file} ({len(html_doc.encode('utf-8')) / 1024:.0f} KB)")
    print(f"   VI: {len(vi_renderer.headings)} headings · EN: {len(en_renderer.headings)} headings · "
          f"mermaid: {mermaid_count}")
    for w in warnings:
        print(f"   ⚠️  {w}")
    return html_doc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile bilingual YouTube Knowledge Markdown to HTML")
    parser.add_argument("md_path", help="Path to source Markdown file")
    parser.add_argument("--out", "-o", help="Path to output HTML file (default: same name .html)")
    parser.add_argument("--title-en", help="English title (default: metadata 'Title' row or VI title)")
    parser.add_argument("--subtitle-vi", help="Vietnamese subtitle")
    parser.add_argument("--subtitle-en", help="English subtitle")
    parser.add_argument("--date", help="Date shown in header (default: today, YYYY-MM-DD)")
    args = parser.parse_args()

    try:
        compile_bilingual_html(
            args.md_path,
            args.out,
            title_en=args.title_en,
            subtitle_vi=args.subtitle_vi,
            subtitle_en=args.subtitle_en,
            date_str=args.date,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
