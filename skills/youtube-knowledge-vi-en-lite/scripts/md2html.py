#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2html.py — chuyển một file Markdown sang HTML self-contained theo template
"Notes" (phong cách Anthropic): TOC sticky + scroll-spy, dark-mode toggle,
scroll progress, callout, timeline (qua list), mermaid, collapsible, in/PDF.

Đây là bản md2html ĐƯỢC ĐÓNG GÓI KÈM skill youtube-knowledge-vi-en-lite để
bước "chain sang HTML" chạy tự động, KHÔNG phụ thuộc một skill md2html riêng.

Cách dùng:
    python3 md2html.py "<duong-dan>.md" [--out "<duong-dan>.html"] \
        [--title "..."] [--subtitle "..."] [--brand "Notes"] [--eyebrow "NOTES"]

Nếu không truyền --out, file .html được ghi cạnh file .md (cùng slug).

Cú pháp Markdown mở rộng được hỗ trợ:
  - Tiêu đề H1 đầu tiên  -> doc-title (tự tách khỏi nội dung).
  - Khối "Key: value" ngay sau H1 -> hộp metadata (callout-info).
  - ```mermaid ...```      -> sơ đồ mermaid trong khung .diagram.
  - Blockquote admonition: "> [!INFO] Tiêu đề" / [!WARN] / [!DANGER] /
    [!TIP] / [!SUCCESS] / [!DECISION] -> callout tương ứng.
  - Bảng Markdown          -> bọc .table-wrap để scroll ngang.
  - TOC sidebar tự sinh từ H2/H3.

Phụ thuộc: thư viện `markdown` (pip install markdown). Nếu thiếu, script in
hướng dẫn cài và thoát với mã != 0.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html as _html
import re
import sys
from pathlib import Path

try:
    import markdown  # type: ignore
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "Thiếu thư viện 'markdown'. Cài bằng:\n"
        "    python3 -m pip install --user --break-system-packages markdown\n"
    )
    sys.exit(2)

# --------------------------------------------------------------------------- #
# Template — CSS + chrome + JS lấy nguyên từ md2html "Notes" template.
# Dùng placeholder %%...%% và .replace() (KHÔNG dùng str.format vì CSS có {}).
# --------------------------------------------------------------------------- #
TEMPLATE = r"""<!DOCTYPE html>
<html lang="vi" data-theme="light" style="--rec-label: '★ Recommended'">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <title>%%TITLE%%</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #FAFAF7; --surface: #FFFFFF; --surface-2: #F5F5F0; --surface-3: #EFEEE8;
      --text: #1A1A1A; --text-muted: #4A4A45; --text-subtle: #6B6B66;
      --accent: #D97757; --accent-hover: #C56843; --accent-soft: #FBEEE6; --accent-border: #F0D5C4; --accent-strong: #A85533;
      --border: #E5E4DC; --border-strong: #CDCDC4; --code-bg: #F5F2EC; --code-text: #2A2A2A;
      --info: #2563EB; --info-soft: #EFF6FF; --info-border: #BFDBFE;
      --warn: #B45309; --warn-soft: #FFFBEB; --warn-border: #FDE68A;
      --danger: #B91C1C; --danger-soft: #FEF2F2; --danger-border: #FECACA;
      --success: #047857; --success-soft: #ECFDF5; --success-border: #A7F3D0;
      --decision: #6D28D9; --decision-soft: #F5F3FF; --decision-border: #DDD6FE;
      --shadow-sm: 0 1px 2px rgba(20, 14, 8, 0.04);
      --shadow: 0 1px 2px rgba(20, 14, 8, 0.04), 0 4px 12px rgba(20, 14, 8, 0.06);
      --shadow-lg: 0 8px 24px rgba(20, 14, 8, 0.10);
      --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace;
      --z-progress: 200; --z-topbar: 100; --z-drawer: 300; --z-backdrop: 250;
    }
    [data-theme="dark"] {
      --bg: #1A1714; --surface: #221E1A; --surface-2: #2A2520; --surface-3: #322C26;
      --text: #F5F0E8; --text-muted: #C8C0B6; --text-subtle: #9A938A;
      --accent: #E89572; --accent-hover: #F2A87F; --accent-soft: #3A2A22; --accent-border: #5A3D2E; --accent-strong: #F5B493;
      --border: #2E2924; --border-strong: #463F38; --code-bg: #1E1B17; --code-text: #E8E2D8;
      --info: #93C5FD; --info-soft: #1E2A3D; --info-border: #2A4365;
      --warn: #FBBF24; --warn-soft: #332817; --warn-border: #5C4520;
      --danger: #FCA5A5; --danger-soft: #3A1F1F; --danger-border: #5C2A2A;
      --success: #6EE7B7; --success-soft: #1A3329; --success-border: #1F5C45;
      --decision: #C4B5FD; --decision-soft: #2A1F40; --decision-border: #4A3870;
      --shadow-sm: 0 1px 2px rgba(0,0,0,0.25);
      --shadow: 0 1px 2px rgba(0,0,0,0.25), 0 4px 12px rgba(0,0,0,0.35);
      --shadow-lg: 0 8px 24px rgba(0,0,0,0.45);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 80px; }
    body { margin: 0; font-family: var(--font-sans); background: var(--bg); color: var(--text); line-height: 1.65; font-size: 16px; -webkit-font-smoothing: antialiased; transition: background-color 0.2s, color 0.2s; }
    ::selection { background: var(--accent-soft); color: var(--accent-strong); }
    .skip-link { position: absolute; top: -100px; left: 8px; padding: 10px 16px; background: var(--accent); color: #fff; text-decoration: none; border-radius: var(--radius-sm); font-weight: 500; z-index: 1000; transition: top 0.15s; }
    .skip-link:focus { top: 8px; }
    .icon-sprite { position: absolute; width: 0; height: 0; overflow: hidden; }
    .icon { display: inline-block; flex-shrink: 0; vertical-align: middle; stroke: currentColor; fill: none; }
    .scroll-progress { position: fixed; top: 0; left: 0; height: 2px; width: 0; background: var(--accent); z-index: var(--z-progress); transition: width 0.05s linear; }
    .topbar { position: sticky; top: 0; z-index: var(--z-topbar); background: rgba(250,250,247,0.85); backdrop-filter: saturate(180%) blur(12px); -webkit-backdrop-filter: saturate(180%) blur(12px); border-bottom: 1px solid var(--border); }
    [data-theme="dark"] .topbar { background: rgba(26,23,20,0.85); }
    .topbar-inner { max-width: 1280px; margin: 0 auto; padding: 10px 20px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    .brand { display: flex; align-items: center; gap: 10px; font-weight: 600; color: var(--text); font-size: 14px; }
    .brand-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 0 4px var(--accent-soft); animation: brand-pulse 2.8s ease-in-out infinite; }
    @keyframes brand-pulse { 0%,100% { box-shadow: 0 0 0 4px var(--accent-soft); } 50% { box-shadow: 0 0 0 7px transparent; } }
    .topbar-actions { display: flex; gap: 6px; align-items: center; }
    .icon-btn { width: 40px; height: 40px; display: inline-flex; align-items: center; justify-content: center; border: 1px solid var(--border); background: var(--surface); color: var(--text-muted); border-radius: var(--radius-sm); cursor: pointer; transition: color 0.15s, border-color 0.15s, background-color 0.15s; padding: 0; }
    .icon-btn .icon { width: 18px; height: 18px; stroke-width: 2; }
    .layout { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 260px 1fr; gap: 48px; padding: 32px 24px 96px; }
    .content { min-width: 0; }
    .toc { position: sticky; top: 80px; align-self: start; max-height: calc(100vh - 100px); overflow-y: auto; padding-right: 8px; }
    .toc::-webkit-scrollbar { width: 6px; }
    .toc::-webkit-scrollbar-track { background: transparent; }
    .toc::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }
    .toc-head { display: flex; align-items: center; justify-content: space-between; padding: 0 12px 12px; }
    .toc-title { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-subtle); margin: 0; }
    .toc-close { display: none; }
    .toc-nav { display: flex; flex-direction: column; gap: 2px; }
    .toc-nav a { display: flex; align-items: center; min-height: 36px; padding: 8px 14px; color: var(--text-muted); text-decoration: none; font-size: 13.5px; border-left: 2px solid transparent; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; transition: color 0.15s, background-color 0.15s, border-color 0.15s; line-height: 1.4; }
    .toc-nav a.active { color: var(--accent); border-left-color: var(--accent); background: var(--accent-soft); font-weight: 500; }
    .toc-nav a.lvl-3 { padding-left: 26px; font-size: 12.5px; }
    .toc-backdrop { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.45); z-index: var(--z-backdrop); opacity: 0; transition: opacity 0.2s; }
    .doc-header { margin-bottom: 40px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
    .doc-eyebrow { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; background: var(--accent-soft); color: var(--accent-strong); border: 1px solid var(--accent-border); border-radius: 999px; font-size: 12px; font-weight: 500; letter-spacing: 0.04em; margin-bottom: 16px; }
    .doc-title { font-size: clamp(28px,3vw + 16px,40px); font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; margin: 0 0 12px; color: var(--text); text-wrap: balance; }
    .doc-subtitle { font-size: clamp(15px,0.6vw + 13px,18px); color: var(--text-muted); line-height: 1.55; margin: 0 0 20px; max-width: 75ch; text-wrap: pretty; }
    .doc-meta { display: flex; flex-wrap: wrap; gap: 16px; font-size: 13px; color: var(--text-subtle); }
    .doc-meta-item { display: inline-flex; align-items: center; gap: 6px; }
    .doc-meta .icon { width: 14px; height: 14px; stroke-width: 2; }
    .content h1,.content h2,.content h3,.content h4 { color: var(--text); line-height: 1.3; letter-spacing: -0.01em; scroll-margin-top: 80px; text-wrap: balance; }
    .content h2 { font-size: 26px; font-weight: 600; margin: 56px 0 16px; padding-top: 8px; position: relative; }
    .content h3 { font-size: 19px; font-weight: 600; margin: 36px 0 12px; position: relative; }
    .content h4 { font-size: 13px; font-weight: 600; margin: 24px 0 8px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; }
    .content > p,.content > ul,.content > ol,.content > blockquote { max-width: 75ch; }
    .content p { margin: 0 0 16px; text-wrap: pretty; overflow-wrap: anywhere; }
    .content a { color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-border); }
    .content ul,.content ol { padding-left: 24px; margin: 0 0 16px; }
    .content li { margin: 4px 0; }
    .content strong { color: var(--text); font-weight: 600; }
    .content em { color: var(--text-muted); }
    .content hr { border: none; border-top: 1px solid var(--border); margin: 40px 0; }
    .anchor { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; margin-left: 6px; color: var(--text-subtle); opacity: 0; transform: translateY(-1px); transition: opacity 0.15s, color 0.15s; border-bottom: none !important; border-radius: var(--radius-sm); }
    .anchor .icon { width: 14px; height: 14px; stroke-width: 2; }
    .content img { max-width: 100%; height: auto; border-radius: var(--radius); border: 1px solid var(--border); margin: 20px 0; display: block; }
    .content code { font-family: var(--font-mono); background: var(--code-bg); padding: 2px 6px; border-radius: 4px; font-size: 0.88em; color: var(--code-text); border: 1px solid var(--border); overflow-wrap: anywhere; }
    .content pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px 20px; overflow-x: auto; font-size: 13.5px; line-height: 1.6; margin: 16px 0; position: relative; }
    .content pre code { background: none; padding: 0; border: none; color: var(--code-text); font-size: inherit; }
    .copy-btn { position: absolute; top: 8px; right: 8px; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); cursor: pointer; color: var(--text-subtle); opacity: 0; transition: opacity 0.15s, color 0.15s, border-color 0.15s; padding: 0; }
    .copy-btn .icon { width: 14px; height: 14px; stroke-width: 2; }
    .copy-btn.copied { color: var(--success); border-color: var(--success-border); opacity: 1; }
    .callout { display: grid; grid-template-columns: 24px 1fr; gap: 14px; padding: 14px 18px; border-radius: var(--radius); border: 1px solid; margin: 20px 0; font-size: 14.5px; line-height: 1.6; max-width: 75ch; }
    .callout-icon { width: 20px; height: 20px; margin-top: 2px; stroke-width: 2; }
    .callout-body { min-width: 0; }
    .callout-title { font-weight: 600; margin: 0 0 4px; font-size: 14px; }
    .callout-body p:last-child { margin-bottom: 0; }
    .callout-info { background: var(--info-soft); border-color: var(--info-border); color: var(--text); }
    .callout-info .callout-title,.callout-info .callout-icon { color: var(--info); }
    .callout-warn { background: var(--warn-soft); border-color: var(--warn-border); color: var(--text); }
    .callout-warn .callout-title,.callout-warn .callout-icon { color: var(--warn); }
    .callout-danger { background: var(--danger-soft); border-color: var(--danger-border); color: var(--text); }
    .callout-danger .callout-title,.callout-danger .callout-icon { color: var(--danger); }
    .callout-success { background: var(--success-soft); border-color: var(--success-border); color: var(--text); }
    .callout-success .callout-title,.callout-success .callout-icon { color: var(--success); }
    .callout-decision { background: var(--decision-soft); border-color: var(--decision-border); color: var(--text); }
    .callout-decision .callout-title,.callout-decision .callout-icon { color: var(--decision); }
    .callout-tip { background: var(--accent-soft); border-color: var(--accent-border); color: var(--text); }
    .callout-tip .callout-title,.callout-tip .callout-icon { color: var(--accent-strong); }
    .highlight { background: linear-gradient(135deg,var(--accent-soft),var(--surface-2)); border-left: 4px solid var(--accent); padding: 18px 22px; border-radius: 0 var(--radius) var(--radius) 0; margin: 24px 0; font-size: 16px; line-height: 1.65; max-width: 75ch; }
    .highlight-label { display: inline-block; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent-strong); margin-bottom: 6px; }
    .diagram { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; margin: 24px 0; box-shadow: var(--shadow-sm); overflow-x: auto; }
    .diagram-caption { margin-top: 12px; padding-top: 12px; border-top: 1px dashed var(--border); font-size: 13px; color: var(--text-subtle); text-align: center; }
    .mermaid { text-align: center; min-height: 80px; }
    .mermaid svg { max-width: 100%; height: auto; }
    .mermaid:not([data-processed]) { opacity: 0.4; font-family: var(--font-mono); font-size: 12px; color: var(--text-subtle); white-space: pre-wrap; text-align: left; }
    details.collapsible { border: 1px solid var(--border); border-radius: var(--radius); margin: 16px 0; background: var(--surface); overflow: hidden; }
    details.collapsible[open] { box-shadow: var(--shadow-sm); }
    details.collapsible > summary { cursor: pointer; padding: 14px 18px; font-weight: 500; color: var(--text); list-style: none; display: flex; align-items: center; gap: 10px; user-select: none; transition: background 0.15s; min-height: 44px; }
    details.collapsible > summary::-webkit-details-marker { display: none; }
    details.collapsible > summary::before { content: "›"; display: inline-block; transition: transform 0.18s; color: var(--accent); font-size: 18px; font-weight: 700; }
    details.collapsible[open] > summary::before { transform: rotate(90deg); }
    .collapsible-body { padding: 4px 18px 18px; border-top: 1px solid var(--border); }
    .table-wrap { overflow-x: auto; margin: 20px 0; border-radius: var(--radius); border: 1px solid var(--border); max-width: 100%; }
    .content table { width: 100%; border-collapse: collapse; font-size: 14px; background: var(--surface); margin: 0; }
    .content th { background: var(--surface-2); color: var(--text); font-weight: 600; text-align: left; padding: 12px 14px; border-bottom: 1px solid var(--border); font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em; white-space: nowrap; }
    .content td { padding: 12px 14px; border-bottom: 1px solid var(--border); color: var(--text-muted); vertical-align: top; }
    .content tr:last-child td { border-bottom: none; }
    .content blockquote { margin: 20px 0; padding: 4px 20px; border-left: 3px solid var(--accent-border); color: var(--text-muted); font-style: italic; }
    .doc-footer { margin-top: 80px; padding-top: 24px; border-top: 1px solid var(--border); font-size: 13px; color: var(--text-subtle); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
    .doc-footer a { color: var(--accent); text-decoration: none; }
    *:focus { outline: none; }
    *:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: var(--radius-sm); }
    @media (hover: hover) {
      .icon-btn:hover { color: var(--accent); border-color: var(--accent-border); background: var(--accent-soft); }
      .toc-nav a:hover { color: var(--accent); background: var(--accent-soft); }
      .content a:hover { color: var(--accent-hover); border-bottom-color: var(--accent); }
      .content tr:hover td { background: var(--surface-2); }
      details.collapsible > summary:hover { background: var(--surface-2); }
      .anchor:hover { color: var(--accent); }
      .content h2:hover .anchor,.content h3:hover .anchor { opacity: 1; }
      .copy-btn:hover { color: var(--accent); border-color: var(--accent-border); }
      .content pre:hover .copy-btn { opacity: 1; }
    }
    @media (hover: none) { .copy-btn { opacity: 0.6; } .anchor { opacity: 0.4; } }
    @media (max-width: 900px) {
      .layout { grid-template-columns: 1fr; gap: 16px; padding: 20px 16px 80px; }
      .topbar-inner { padding: 8px 12px; }
      .doc-header { margin-bottom: 28px; padding-bottom: 20px; }
      .toc-mobile-trigger { display: inline-flex !important; }
      .toc { position: fixed; top: 0; left: 0; width: min(300px,82vw); height: 100dvh; max-height: 100dvh; background: var(--surface); z-index: var(--z-drawer); padding: 16px 8px 24px 16px; box-shadow: var(--shadow-lg); transform: translateX(-105%); transition: transform 0.25s ease; }
      .toc-head { padding: 4px 4px 12px 8px; }
      .toc-close { display: inline-flex !important; width: 36px; height: 36px; align-items: center; justify-content: center; background: transparent; border: 1px solid transparent; border-radius: var(--radius-sm); color: var(--text-muted); cursor: pointer; padding: 0; }
      .toc-close .icon { width: 18px; height: 18px; stroke-width: 2; }
      body.toc-open .toc { transform: translateX(0); }
      body.toc-open .toc-backdrop { display: block; opacity: 1; }
      .toc-backdrop { display: block; opacity: 0; pointer-events: none; }
      body.toc-open .toc-backdrop { pointer-events: auto; }
      body.toc-open { overflow: hidden; }
    }
    @media (min-width: 901px) { .toc-mobile-trigger { display: none !important; } }
    @media (prefers-reduced-motion: reduce) {
      *,*::before,*::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
      html { scroll-behavior: auto; }
      .brand-dot { animation: none; box-shadow: 0 0 0 4px var(--accent-soft); }
    }
    @media print {
      .topbar,.toc,.toc-backdrop,.icon-btn,.copy-btn,.anchor,.scroll-progress { display: none !important; }
      .layout { grid-template-columns: 1fr; padding: 0; max-width: 100%; }
      body { background: #fff; color: #000; }
      a { color: #000; }
      .content pre,.callout,.diagram { break-inside: avoid; }
      .doc-footer { break-before: avoid; }
    }
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>
  <div class="scroll-progress" id="scroll-progress" aria-hidden="true"></div>

  <svg class="icon-sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <symbol id="i-info" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></symbol>
    <symbol id="i-warn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></symbol>
    <symbol id="i-danger" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></symbol>
    <symbol id="i-success" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></symbol>
    <symbol id="i-decision" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></symbol>
    <symbol id="i-tip" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14a5 5 0 1 0-6.18 0 4 4 0 0 1 1.59 2h2.99a4 4 0 0 1 1.6-2Z"/></symbol>
    <symbol id="i-printer" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></symbol>
    <symbol id="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></symbol>
    <symbol id="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/></symbol>
    <symbol id="i-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></symbol>
    <symbol id="i-file" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></symbol>
    <symbol id="i-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></symbol>
    <symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></symbol>
    <symbol id="i-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></symbol>
    <symbol id="i-link" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></symbol>
  </svg>

  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand">
        <button class="icon-btn toc-mobile-trigger" id="toc-toggle" onclick="openToc()" aria-label="Mục lục" title="Mục lục">
          <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-menu"/></svg>
        </button>
        <span class="brand-dot" aria-hidden="true"></span>
        <span>%%BRAND%%</span>
      </div>
      <div class="topbar-actions">
        <button class="icon-btn" onclick="window.print()" title="Print / Save PDF" aria-label="Print / Save PDF">
          <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-printer"/></svg>
        </button>
        <button class="icon-btn" id="theme-toggle" onclick="toggleTheme()" title="Đổi theme" aria-label="Đổi theme">
          <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use id="theme-icon-use" href="#i-moon"/></svg>
        </button>
      </div>
    </div>
  </header>

  <div class="toc-backdrop" onclick="closeToc()" aria-hidden="true"></div>

  <div class="layout">
    <aside class="toc" id="toc" aria-label="Mục lục">
      <div class="toc-head">
        <p class="toc-title">Mục lục</p>
        <button class="toc-close" onclick="closeToc()" aria-label="Đóng">
          <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-x"/></svg>
        </button>
      </div>
      <nav class="toc-nav" id="toc-nav">
%%TOC_NAV%%
      </nav>
    </aside>

    <main class="content" id="main">
      <header class="doc-header">
        <span class="doc-eyebrow">%%EYEBROW%%</span>
        <h1 class="doc-title">%%TITLE%%</h1>
%%SUBTITLE_BLOCK%%
        <div class="doc-meta">
          <span class="doc-meta-item">
            <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-file"/></svg>
            %%FILENAME%%
          </span>
          <span class="doc-meta-item">
            <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-calendar"/></svg>
            %%DATE%%
          </span>
          <span class="doc-meta-item">
            <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-clock"/></svg>
            %%READTIME%%
          </span>
        </div>
      </header>

%%METADATA_BLOCK%%
%%CONTENT%%

      <footer class="doc-footer">
        <span>Generated by <a href="#">md2html</a></span>
        <span>Source: %%FILENAME%%</span>
      </footer>
    </main>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
  <script>
    const STORAGE_KEY = "md2html-theme";
    function currentTheme() { return document.documentElement.dataset.theme || "light"; }
    function applyThemeIcon() {
      const use = document.getElementById("theme-icon-use");
      if (use) use.setAttribute("href", currentTheme() === "dark" ? "#i-sun" : "#i-moon");
    }
    (function restoreTheme() {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) document.documentElement.dataset.theme = saved;
    })();
    const diagramSources = new Map();
    function initMermaid() {
      if (typeof mermaid === "undefined") return;
      const isDark = currentTheme() === "dark";
      mermaid.initialize({
        startOnLoad: false, theme: isDark ? "dark" : "default",
        themeVariables: {
          primaryColor: isDark ? "#3A2A22" : "#FBEEE6",
          primaryTextColor: isDark ? "#F5F0E8" : "#1A1A1A",
          primaryBorderColor: isDark ? "#E89572" : "#D97757",
          lineColor: isDark ? "#9A938A" : "#6B6B66",
          secondaryColor: isDark ? "#2A2520" : "#F5F5F0",
          tertiaryColor: isDark ? "#221E1A" : "#FFFFFF",
          fontFamily: "Inter, system-ui, sans-serif",
        },
      });
    }
    async function renderMermaid() {
      if (typeof mermaid === "undefined") return;
      initMermaid();
      const els = document.querySelectorAll(".mermaid");
      els.forEach(el => {
        if (!diagramSources.has(el)) diagramSources.set(el, el.textContent.trim());
        el.textContent = diagramSources.get(el);
        el.removeAttribute("data-processed");
      });
      try { await mermaid.run({ nodes: els }); } catch (e) { console.error(e); }
    }
    function toggleTheme() {
      const next = currentTheme() === "light" ? "dark" : "light";
      document.documentElement.dataset.theme = next;
      localStorage.setItem(STORAGE_KEY, next);
      applyThemeIcon(); renderMermaid();
    }
    function openToc() { document.body.classList.add("toc-open"); }
    function closeToc() { document.body.classList.remove("toc-open"); }
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && document.body.classList.contains("toc-open")) closeToc();
    });
    function setupTocSpy() {
      const links = document.querySelectorAll("#toc-nav a[href^='#']");
      if (!links.length) { const toc = document.getElementById("toc"); if (toc) toc.style.display = "none"; return; }
      const map = new Map();
      links.forEach(a => {
        const id = a.getAttribute("href").slice(1);
        const el = document.getElementById(id);
        if (el) map.set(el, a);
        a.addEventListener("click", () => { if (window.matchMedia("(max-width: 900px)").matches) closeToc(); });
      });
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          const link = map.get(en.target);
          if (!link) return;
          if (en.isIntersecting) { links.forEach(l => l.classList.remove("active")); link.classList.add("active"); }
        });
      }, { rootMargin: "-80px 0px -70% 0px", threshold: 0 });
      map.forEach((_, el) => obs.observe(el));
    }
    function injectAnchors() {
      document.querySelectorAll(".content h2[id], .content h3[id]").forEach(h => {
        if (h.querySelector(".anchor")) return;
        const a = document.createElement("a");
        a.className = "anchor"; a.href = "#" + h.id; a.setAttribute("aria-label", "Permalink");
        a.innerHTML = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-link"/></svg>';
        h.appendChild(a);
      });
    }
    function injectCopyButtons() {
      document.querySelectorAll(".content pre").forEach(pre => {
        if (pre.classList.contains("mermaid")) return;
        if (pre.querySelector(".copy-btn")) return;
        const btn = document.createElement("button");
        btn.type = "button"; btn.className = "copy-btn"; btn.setAttribute("aria-label", "Copy code");
        btn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-copy"/></svg>';
        btn.addEventListener("click", async () => {
          const code = pre.querySelector("code")?.textContent ?? pre.textContent;
          try {
            await navigator.clipboard.writeText(code);
            btn.classList.add("copied");
            btn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-check"/></svg>';
            setTimeout(() => { btn.classList.remove("copied"); btn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-copy"/></svg>'; }, 1500);
          } catch (e) { console.error(e); }
        });
        pre.appendChild(btn);
      });
    }
    function setupScrollProgress() {
      const bar = document.getElementById("scroll-progress");
      if (!bar) return;
      const onScroll = () => {
        const h = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const p = h > 0 ? (document.documentElement.scrollTop / h * 100) : 0;
        bar.style.width = p + "%";
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
    document.addEventListener("DOMContentLoaded", () => {
      applyThemeIcon(); injectAnchors(); injectCopyButtons(); renderMermaid(); setupTocSpy(); setupScrollProgress();
    });
  </script>
</body>
</html>
"""

CALLOUT_MAP = {
    "INFO": ("info", "i-info", "Lưu ý"),
    "NOTE": ("info", "i-info", "Lưu ý"),
    "WARN": ("warn", "i-warn", "Cảnh báo"),
    "WARNING": ("warn", "i-warn", "Cảnh báo"),
    "DANGER": ("danger", "i-danger", "Nguy hiểm"),
    "CAUTION": ("danger", "i-danger", "Nguy hiểm"),
    "TIP": ("tip", "i-tip", "Tip"),
    "SUCCESS": ("success", "i-success", "Tốt"),
    "DECISION": ("decision", "i-decision", "Quyết định"),
}

META_ICON = {
    "nguồn": "i-link", "source": "i-link", "url": "i-link",
    "kênh": "i-file", "tác giả": "i-file", "channel": "i-file",
    "ngày": "i-calendar", "date": "i-calendar",
    "thời lượng": "i-clock", "length": "i-clock",
}


def _slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text or "section"


def _extract_title_and_meta(md_text: str):
    """Tách H1 đầu tiên (title) và khối metadata 'Key: value' ngay sau nó."""
    lines = md_text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    title = None
    if i < len(lines) and lines[i].startswith("# "):
        title = lines[i][2:].strip()
        i += 1
    # bỏ qua dòng trống giữa H1 và khối metadata (nếu có)
    while i < len(lines) and not lines[i].strip():
        i += 1
    meta = []
    meta_re = re.compile(r"^([^#>*\-\d][^:]{0,40}):\s+(.*\S)\s*$")
    while i < len(lines) and lines[i].strip():
        m = meta_re.match(lines[i])
        if not m:
            break
        meta.append((m.group(1).strip(), m.group(2).strip()))
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    rest = "\n".join(lines[i:])
    return title, meta, rest


def _build_meta_block(meta):
    if not meta:
        return ""
    rows = []
    for key, val in meta:
        val_html = _html.escape(val)
        val_html = re.sub(
            r"(https?://[^\s]+)",
            r'<a href="\1">\1</a>',
            val_html,
        )
        rows.append(
            f'<p style="margin:2px 0"><strong>{_html.escape(key)}:</strong> {val_html}</p>'
        )
    body = "\n".join(rows)
    return (
        '      <aside class="callout callout-info">\n'
        '        <svg class="callout-icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-info"/></svg>\n'
        '        <div class="callout-body">\n'
        '          <p class="callout-title">Thông tin nguồn</p>\n'
        f"          {body}\n"
        "        </div>\n"
        "      </aside>\n"
    )


def _transform_mermaid(html_str: str) -> str:
    pattern = re.compile(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>', re.S
    )
    return pattern.sub(
        lambda m: '<figure class="diagram"><pre class="mermaid">\n'
        + m.group(1).strip()
        + "\n</pre></figure>",
        html_str,
    )


def _transform_callouts(html_str: str) -> str:
    def repl(m):
        inner = m.group(1)
        am = re.match(r"\s*<p>\s*\[!(\w+)\]\s*(.*?)</p>(.*)", inner, re.S)
        if not am:
            return m.group(0)
        kind = am.group(1).upper()
        if kind not in CALLOUT_MAP:
            return m.group(0)
        cls, icon, default_title = CALLOUT_MAP[kind]
        title = am.group(2).strip() or default_title
        body = am.group(3).strip()
        if not body:
            body = f"<p>{title}</p>"
            title = default_title
        return (
            f'<aside class="callout callout-{cls}">\n'
            f'  <svg class="callout-icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#{icon}"/></svg>\n'
            f'  <div class="callout-body">\n'
            f'    <p class="callout-title">{title}</p>\n'
            f"    {body}\n"
            f"  </div>\n"
            f"</aside>"
        )

    return re.sub(r"<blockquote>(.*?)</blockquote>", repl, html_str, flags=re.S)


def _wrap_tables(html_str: str) -> str:
    return html_str.replace("<table>", '<div class="table-wrap"><table>').replace(
        "</table>", "</table></div>"
    )


def _toc_name(name: str) -> str:
    # toc_tokens name có thể đã chứa entity (vd '&amp;'); chuẩn hoá để không
    # bị double-escape thành '&amp;amp;'.
    return _html.escape(_html.unescape(name))


def _build_toc(toc_tokens) -> str:
    out = []
    for tok in toc_tokens:
        if tok["level"] == 2:
            out.append(
                f'        <a href="#{tok["id"]}" class="lvl-2">{_toc_name(tok["name"])}</a>'
            )
            for child in tok.get("children", []):
                if child["level"] == 3:
                    out.append(
                        f'        <a href="#{child["id"]}" class="lvl-3">{_toc_name(child["name"])}</a>'
                    )
    return "\n".join(out)


def convert(md_text: str, *, title=None, subtitle=None, filename="",
            date=None, brand="Notes", eyebrow="NOTES") -> str:
    parsed_title, meta, rest = _extract_title_and_meta(md_text)
    title = title or parsed_title or "Document"

    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "nl2br", "toc", "attr_list"],
        extension_configs={"toc": {"slugify": lambda v, s: _slugify(v)}},
    )
    body = md.convert(rest)
    body = _transform_mermaid(body)
    body = _transform_callouts(body)
    body = _wrap_tables(body)

    toc_nav = _build_toc(getattr(md, "toc_tokens", []))
    meta_block = _build_meta_block(meta)

    words = len(re.findall(r"\w+", rest))
    read_min = max(1, round(words / 200))
    read_time = f"~{read_min} phút đọc"

    if subtitle:
        subtitle_block = (
            f'        <p class="doc-subtitle">{_html.escape(subtitle)}</p>'
        )
    else:
        subtitle_block = ""

    if date is None:
        date = _dt.date.today().isoformat()

    # indent body để khớp template
    content = "\n".join("      " + ln if ln else ln for ln in body.splitlines())

    html_out = TEMPLATE
    replacements = {
        "%%TITLE%%": _html.escape(title),
        "%%SUBTITLE_BLOCK%%": subtitle_block,
        "%%FILENAME%%": _html.escape(filename),
        "%%DATE%%": _html.escape(date),
        "%%READTIME%%": read_time,
        "%%BRAND%%": _html.escape(brand),
        "%%EYEBROW%%": _html.escape(eyebrow),
        "%%TOC_NAV%%": toc_nav,
        "%%METADATA_BLOCK%%": meta_block,
        "%%CONTENT%%": content,
    }
    for k, v in replacements.items():
        html_out = html_out.replace(k, v)
    return html_out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Convert Markdown -> Notes-style HTML.")
    ap.add_argument("input", help="Đường dẫn file .md")
    ap.add_argument("--out", default=None, help="Đường dẫn .html (mặc định: cạnh .md)")
    ap.add_argument("--title", default=None)
    ap.add_argument("--subtitle", default=None)
    ap.add_argument("--brand", default="Notes")
    ap.add_argument("--eyebrow", default="NOTES")
    args = ap.parse_args(argv)

    src = Path(args.input)
    if not src.is_file():
        sys.stderr.write(f"Không tìm thấy file: {src}\n")
        return 1
    md_text = src.read_text(encoding="utf-8")
    out = Path(args.out) if args.out else src.with_suffix(".html")

    html_out = convert(
        md_text,
        title=args.title,
        subtitle=args.subtitle,
        filename=src.name,
        brand=args.brand,
        eyebrow=args.eyebrow,
    )
    out.write_text(html_out, encoding="utf-8")
    print(f"OK -> {out} ({len(html_out)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
