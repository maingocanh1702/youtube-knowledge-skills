#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flow Viewer (v1) — zoom / pan / fullscreen runtime for Mermaid flowcharts
in youtube-knowledge bilingual HTML notes.

Features
- Width-based zoom (not CSS transform) so the scroll area grows → you can pan to every corner
- Fullscreen mode with its own floating toolbar (− % + · Fit · 1:1 · ✕), backdrop, body scroll lock
- ⌘/Ctrl + wheel and trackpad pinch zoom anchored at the cursor (also Safari gesture events)
- Drag to pan (mouse) · one-finger pan + two-finger pinch (touch, fullscreen only)
- Keyboard in fullscreen: + / − / 0 (fit) / 1 (actual size) / Esc (exit)
- Keeps the public API used by existing markup: zoomFlow(delta, suffix),
  resetFlowZoom(suffix), toggleFlowFullscreen(suffix)

Usage
    from flow_viewer import inject_flow_viewer
    html = inject_flow_viewer(html)            # idempotent: replaces an existing block

CLI (upgrade already-generated HTML files in place):
    python3 flow_viewer.py knowledge/youtube/*.html
"""

import re
import sys
from pathlib import Path

START_MARK = "<!-- FLOW-VIEWER:START v1 -->"
END_MARK = "<!-- FLOW-VIEWER:END -->"
BLOCK_RE = re.compile(r"<!-- FLOW-VIEWER:START[^>]*-->.*?<!-- FLOW-VIEWER:END -->\s*", re.S)

FLOW_VIEWER_CSS = """
    /* ============================================================
       FLOW VIEWER — zoom / pan / fullscreen (v1)
       ============================================================ */
    :root {
      --flow-fs-backdrop: rgba(15, 23, 42, 0.55); /* dim layer behind the fullscreen diagram */
      --flow-fs-shadow: 0 12px 32px rgba(15, 23, 42, 0.28); /* floating toolbar / hint elevation */
      --flow-fs-btn-size: 38px; /* desktop toolbar button size */
      --flow-fs-gap: 20px; /* fullscreen inset from the window edges */
    }
    @media (pointer: coarse) { :root { --flow-fs-btn-size: 44px; } }

    .flow-viewport .mermaid:has(svg[data-flow-zoom]) { overflow: visible; width: max-content; min-width: 100%; }
    .flow-viewport .mermaid svg[data-flow-zoom] { display: block; margin: 0 auto; }
    .flow-viewport:has(svg[data-flow-zoom]) { cursor: grab; user-select: none; -webkit-user-select: none; }
    .flow-viewport.is-panning { cursor: grabbing !important; }

    body.flow-fs-open { overflow: hidden; }
    .flow-viewport.is-fullscreen {
      position: fixed;
      inset: var(--flow-fs-gap);
      z-index: 1000;
      max-height: none;
      padding: 80px 24px 24px;
      overflow: auto;
      overscroll-behavior: contain;
      touch-action: none;
      cursor: grab;
      user-select: none;
      -webkit-user-select: none;
      animation: flowFsZoomIn 0.2s ease;
    }
    .flow-fs-backdrop {
      position: fixed;
      inset: 0;
      z-index: 999;
      background: var(--flow-fs-backdrop);
      backdrop-filter: blur(3px);
      -webkit-backdrop-filter: blur(3px);
      animation: flowFsFade 0.18s ease;
    }
    .flow-fs-bar {
      position: fixed;
      top: calc(var(--flow-fs-gap) + 16px);
      left: 50%;
      transform: translateX(-50%);
      z-index: 1002;
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 6px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 999px;
      box-shadow: var(--flow-fs-shadow);
      animation: flowFsDrop 0.22s ease;
    }
    .flow-fs-btn {
      min-width: var(--flow-fs-btn-size);
      height: var(--flow-fs-btn-size);
      padding: 0 10px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid transparent;
      border-radius: 999px;
      background: transparent;
      color: var(--text);
      font: 600 14px/1 var(--font-sans);
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease, transform 0.1s ease;
    }
    .flow-fs-btn:hover { background: var(--surface-3); color: var(--accent-strong); }
    .flow-fs-btn:active { transform: scale(0.92); }
    .flow-fs-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
    .flow-fs-btn[data-flow-act="close"]:hover { background: var(--accent); color: var(--surface); }
    .flow-fs-zoom {
      min-width: 54px;
      text-align: center;
      font: 600 12px/1 var(--font-sans);
      font-variant-numeric: tabular-nums;
      color: var(--text-muted);
    }
    .flow-fs-sep { width: 1px; height: 20px; background: var(--border); margin: 0 4px; }
    .flow-fs-hint {
      position: fixed;
      bottom: calc(var(--flow-fs-gap) + 16px);
      left: 50%;
      transform: translateX(-50%);
      z-index: 1002;
      padding: 8px 14px;
      border-radius: 999px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 12px;
      white-space: nowrap;
      box-shadow: var(--flow-fs-shadow);
      pointer-events: none;
      animation: flowFsHint 5s ease forwards;
    }
    @keyframes flowFsFade { from { opacity: 0; } }
    @keyframes flowFsZoomIn { from { opacity: 0; transform: scale(0.98); } }
    @keyframes flowFsDrop { from { opacity: 0; transform: translate(-50%, -8px); } }
    @keyframes flowFsHint { 0%, 80% { opacity: 1; } 100% { opacity: 0; } }
    @media (max-width: 768px) {
      :root { --flow-fs-gap: 0px; }
      .flow-viewport.is-fullscreen { border-radius: 0; padding: 16px 12px 96px; }
      .flow-fs-bar { top: auto; bottom: 20px; }
      .flow-fs-hint { display: none; }
    }
    @media (prefers-reduced-motion: reduce) {
      .flow-viewport.is-fullscreen, .flow-fs-backdrop, .flow-fs-bar, .flow-fs-hint { animation: none; }
    }
"""

FLOW_VIEWER_JS = r"""
  (function () {
    "use strict";
    var MIN_SCALE = 0.2, MAX_SCALE = 4, MAX_FIT = 2, BTN_FACTOR = 1.2;
    var activeFs = null;
    var T = {
      vi: { zoomIn: "Phóng to (+)", zoomOut: "Thu nhỏ (−)", fit: "Vừa màn hình (0)", actual: "Kích thước gốc (1)",
            close: "Thoát toàn màn hình (Esc)", hint: "⌘/Ctrl + cuộn hoặc pinch để zoom · kéo để di chuyển · Esc để thoát" },
      en: { zoomIn: "Zoom in (+)", zoomOut: "Zoom out (−)", fit: "Fit to screen (0)", actual: "Actual size (1)",
            close: "Exit fullscreen (Esc)", hint: "⌘/Ctrl + scroll or pinch to zoom · drag to pan · Esc to exit" }
    };

    function lang() { return document.documentElement.dataset.lang === "en" ? "en" : "vi"; }
    function clamp(v) { return Math.max(MIN_SCALE, Math.min(MAX_SCALE, v)); }
    function getViewport(suffix) {
      return document.getElementById("flow-viewport-box" + (suffix || "")) || document.getElementById("flow-viewport-box");
    }
    function getSvg(vp) { return vp ? vp.querySelector(".mermaid svg") : null; }
    function closestViewport(target) {
      return target && target.closest ? target.closest(".flow-viewport") : null;
    }
    function naturalSize(svg) {
      var vb = svg.viewBox && svg.viewBox.baseVal;
      if (vb && vb.width && vb.height) return { w: vb.width, h: vb.height };
      var r = svg.getBoundingClientRect();
      return { w: r.width || 1, h: r.height || 1 };
    }
    function currentScale(svg) {
      var z = parseFloat(svg.dataset.flowZoom);
      if (z) return z;
      return (svg.getBoundingClientRect().width / naturalSize(svg).w) || 1;
    }
    function isInteractive(vp) {
      var svg = getSvg(vp);
      return !!vp && (vp.classList.contains("is-fullscreen") || !!(svg && svg.dataset.flowZoom));
    }
    function updateLabel(scale) {
      if (!activeFs) return;
      var el = activeFs.bar.querySelector(".flow-fs-zoom");
      if (el) el.textContent = Math.round(scale * 100) + "%";
    }

    // Zoom by resizing the SVG (keeps scrollable area in sync), anchored at a client point
    function setScale(vp, scale, clientX, clientY) {
      var svg = getSvg(vp);
      if (!svg) return;
      scale = clamp(scale);
      var vr = vp.getBoundingClientRect();
      var ax = (clientX == null) ? vr.left + vp.clientWidth / 2 : clientX;
      var ay = (clientY == null) ? vr.top + vp.clientHeight / 2 : clientY;
      var sr = svg.getBoundingClientRect();
      var fx = sr.width ? (ax - sr.left) / sr.width : 0.5;
      var fy = sr.height ? (ay - sr.top) / sr.height : 0.5;

      if (svg.dataset.flowOrigStyle === undefined) svg.dataset.flowOrigStyle = svg.getAttribute("style") || "";
      var n = naturalSize(svg);
      svg.dataset.flowZoom = String(scale);
      svg.style.transform = "none";
      svg.style.maxWidth = "none";
      svg.style.width = (n.w * scale) + "px";
      svg.style.height = (n.h * scale) + "px";

      var sr2 = svg.getBoundingClientRect();
      vp.scrollLeft += (sr2.left + fx * sr2.width) - ax;
      vp.scrollTop += (sr2.top + fy * sr2.height) - ay;
      updateLabel(scale);
    }
    function resetScale(vp) {
      var svg = getSvg(vp);
      if (!vp || !svg) return;
      if (svg.dataset.flowOrigStyle !== undefined) {
        svg.setAttribute("style", svg.dataset.flowOrigStyle);
        delete svg.dataset.flowOrigStyle;
      } else {
        svg.style.transform = "";
      }
      delete svg.dataset.flowZoom;
      vp.scrollLeft = 0;
      vp.scrollTop = 0;
    }
    function fitScale(vp) {
      var svg = getSvg(vp);
      if (!svg) return;
      var n = naturalSize(svg);
      var cs = getComputedStyle(vp);
      var w = vp.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      var h = vp.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
      setScale(vp, Math.min(MAX_FIT, w / n.w, h / n.h));
      vp.scrollLeft = (vp.scrollWidth - vp.clientWidth) / 2;
      vp.scrollTop = (vp.scrollHeight - vp.clientHeight) / 2;
    }

    // ---------- Fullscreen ----------
    function btn(act, label, title) {
      return '<button type="button" class="flow-fs-btn" data-flow-act="' + act + '" title="' + title +
        '" aria-label="' + title + '">' + label + "</button>";
    }
    function enterFs(vp) {
      var t = T[lang()];
      var backdrop = document.createElement("div");
      backdrop.className = "flow-fs-backdrop";
      backdrop.addEventListener("click", exitFs);

      var bar = document.createElement("div");
      bar.className = "flow-fs-bar";
      bar.setAttribute("role", "toolbar");
      bar.setAttribute("aria-label", "Diagram zoom");
      bar.innerHTML = btn("out", "−", t.zoomOut) +
        '<span class="flow-fs-zoom" aria-live="polite">100%</span>' + btn("in", "+", t.zoomIn) +
        '<span class="flow-fs-sep"></span>' + btn("fit", "⤢", t.fit) + btn("actual", "1:1", t.actual) +
        '<span class="flow-fs-sep"></span>' + btn("close", "✕", t.close);
      bar.addEventListener("click", function (e) {
        var b = e.target.closest("[data-flow-act]");
        if (!b) return;
        var act = b.dataset.flowAct, svg = getSvg(vp);
        if (act === "close") { exitFs(); return; }
        if (!svg) return;
        if (act === "in") setScale(vp, currentScale(svg) * BTN_FACTOR);
        else if (act === "out") setScale(vp, currentScale(svg) / BTN_FACTOR);
        else if (act === "fit") fitScale(vp);
        else if (act === "actual") setScale(vp, 1);
      });

      var hint = document.createElement("div");
      hint.className = "flow-fs-hint";
      hint.textContent = t.hint;

      document.body.appendChild(backdrop);
      document.body.appendChild(bar);
      document.body.appendChild(hint);
      vp.classList.add("is-fullscreen");
      document.body.classList.add("flow-fs-open");
      activeFs = { vp: vp, bar: bar, hint: hint, backdrop: backdrop, prevFocus: document.activeElement };
      if (!vp.hasAttribute("tabindex")) vp.setAttribute("tabindex", "-1");
      try { vp.focus({ preventScroll: true }); } catch (e) {}
      requestAnimationFrame(function () { fitScale(vp); });
    }
    function exitFs() {
      if (!activeFs) return;
      var s = activeFs;
      activeFs = null;
      s.vp.classList.remove("is-fullscreen", "is-panning");
      document.body.classList.remove("flow-fs-open");
      [s.bar, s.hint, s.backdrop].forEach(function (el) { if (el && el.parentNode) el.parentNode.removeChild(el); });
      resetScale(s.vp);
      if (s.prevFocus && s.prevFocus.focus) { try { s.prevFocus.focus({ preventScroll: true }); } catch (e) {} }
    }

    // ---------- Public API (used by toolbar markup) ----------
    function targetViewport(suffix) { return (activeFs && activeFs.vp) || getViewport(suffix); }
    window.zoomFlow = function (delta, suffix) {
      var vp = targetViewport(suffix), svg = getSvg(vp);
      if (!svg) return;
      setScale(vp, currentScale(svg) * (delta >= 0 ? BTN_FACTOR : 1 / BTN_FACTOR));
    };
    window.resetFlowZoom = function (suffix) {
      var vp = targetViewport(suffix);
      if (!vp) return;
      if (activeFs && activeFs.vp === vp) fitScale(vp); else resetScale(vp);
    };
    window.toggleFlowFullscreen = function (suffix) {
      if (activeFs) { exitFs(); return; }
      var vp = getViewport(suffix);
      if (vp && getSvg(vp)) enterFs(vp);
    };

    // ---------- Keyboard (fullscreen only) ----------
    document.addEventListener("keydown", function (e) {
      if (!activeFs) return;
      var vp = activeFs.vp, svg = getSvg(vp), k = e.key;
      if (k === "Escape") { e.preventDefault(); exitFs(); return; }
      if (!svg || e.altKey) return;
      if (k === "+" || k === "=") { e.preventDefault(); setScale(vp, currentScale(svg) * BTN_FACTOR); }
      else if (k === "-" || k === "_") { e.preventDefault(); setScale(vp, currentScale(svg) / BTN_FACTOR); }
      else if (k === "0") { e.preventDefault(); fitScale(vp); }
      else if (k === "1" && !e.metaKey && !e.ctrlKey) { e.preventDefault(); setScale(vp, 1); }
    });

    // ---------- ⌘/Ctrl + wheel & trackpad pinch (Chrome/Firefox send ctrlKey wheel) ----------
    var gesture = null;
    document.addEventListener("wheel", function (e) {
      if (gesture || !(e.ctrlKey || e.metaKey)) return;
      var vp = closestViewport(e.target), svg = getSvg(vp);
      if (!svg) return;
      e.preventDefault();
      var unit = e.deltaMode === 1 ? 0.05 : 0.002;
      setScale(vp, currentScale(svg) * Math.exp(-e.deltaY * unit), e.clientX, e.clientY);
    }, { passive: false });

    // Safari trackpad pinch
    document.addEventListener("gesturestart", function (e) {
      var vp = closestViewport(e.target), svg = getSvg(vp);
      if (!svg) return;
      e.preventDefault();
      gesture = { vp: vp, scale: currentScale(svg) };
    });
    document.addEventListener("gesturechange", function (e) {
      if (!gesture) return;
      e.preventDefault();
      setScale(gesture.vp, gesture.scale * e.scale, e.clientX, e.clientY);
    });
    document.addEventListener("gestureend", function () { gesture = null; });

    // ---------- Drag to pan + touch pinch ----------
    var pointers = new Map(), pan = null, pinch = null;
    function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y) || 1; }
    document.addEventListener("pointerdown", function (e) {
      var vp = closestViewport(e.target);
      if (!isInteractive(vp)) return;
      if (e.pointerType === "mouse" && e.button !== 0) return;
      if (e.pointerType === "touch" && !vp.classList.contains("is-fullscreen")) return; // keep native page scroll
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pointers.size === 1) {
        pan = { vp: vp, x: e.clientX, y: e.clientY, sl: vp.scrollLeft, st: vp.scrollTop, moved: false };
      } else if (pointers.size === 2) {
        var p = Array.from(pointers.values()), svg = getSvg(vp);
        pinch = { vp: vp, d: dist(p[0], p[1]), scale: svg ? currentScale(svg) : 1 };
        pan = null;
      }
    });
    document.addEventListener("pointermove", function (e) {
      if (!pointers.has(e.pointerId)) return;
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pinch && pointers.size >= 2) {
        var p = Array.from(pointers.values());
        setScale(pinch.vp, pinch.scale * dist(p[0], p[1]) / pinch.d, (p[0].x + p[1].x) / 2, (p[0].y + p[1].y) / 2);
        e.preventDefault();
        return;
      }
      if (!pan) return;
      var dx = e.clientX - pan.x, dy = e.clientY - pan.y;
      if (!pan.moved && Math.abs(dx) + Math.abs(dy) < 4) return;
      pan.moved = true;
      pan.vp.classList.add("is-panning");
      pan.vp.scrollLeft = pan.sl - dx;
      pan.vp.scrollTop = pan.st - dy;
      e.preventDefault();
    });
    function endPointer(e) {
      pointers.delete(e.pointerId);
      if (pointers.size < 2) pinch = null;
      if (pointers.size === 0 && pan) { pan.vp.classList.remove("is-panning"); pan = null; }
    }
    document.addEventListener("pointerup", endPointer);
    document.addEventListener("pointercancel", endPointer);
  })();
"""


def build_block() -> str:
    return (
        f"{START_MARK}\n<style>{FLOW_VIEWER_CSS}  </style>\n"
        f"<script>{FLOW_VIEWER_JS}</script>\n{END_MARK}\n"
    )


def inject_flow_viewer(html: str) -> str:
    """Insert (or replace) the Flow Viewer block right before the last </body>. Idempotent."""
    html = BLOCK_RE.sub("", html)
    idx = html.rfind("</body>")
    if idx == -1:
        raise ValueError("No </body> found — cannot inject Flow Viewer.")
    return html[:idx] + build_block() + html[idx:]


def upgrade_files(paths) -> int:
    changed = 0
    for p in map(Path, paths):
        text = p.read_text(encoding="utf-8")
        if "flow-viewport" not in text:
            print(f"   skip (no flowchart): {p.name}")
            continue
        new = inject_flow_viewer(text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            changed += 1
            print(f"✅ upgraded: {p.name}")
        else:
            print(f"   up-to-date: {p.name}")
    return changed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    n = upgrade_files(sys.argv[1:])
    print(f"Done — {n} file(s) upgraded.")
