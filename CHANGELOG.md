# Changelog

All notable changes to the **YouTube Knowledge Skills** project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2.1.0] - 2026-10-08

### Added
- **Triad Skill Suite**: Full release of all 3 variants:
  - `youtube-knowledge-vi-en` (v2.1.0): Bilingual Interactive (🇻🇳 VI ⇋ 🇬🇧 EN) with instantaneous topbar switcher and dual independent TOCs.
  - `youtube-knowledge-vi` (v1.0.0): Pure Vietnamese edition, translating 100% of industry terms with first-mention English glossaries.
  - `youtube-knowledge-en` (v1.0.0): Full English Technical Reference, designed for international researchers and AI Agent system prompts.
- **Embedded Zero-Dependency Template Engine**: Bundled `template.html` directly inside each skill so HTML compilation works out of the box without external `md2html` dependencies.
- **Single-Language HTML Compiler (`scripts/build_html.py`)**: Lightweight, self-contained compiler for `vi` and `en` editions.
- **Bilingual HTML Compiler (`scripts/build_bilingual_html.py`)**: Full dual-part parser, Markdown renderer, and scoped CSS switcher.
- **Interactive Flow Viewer (`scripts/flow_viewer.py`)**: Real width-based Mermaid zoom, pan, and fullscreen viewport controls.
- **Pre-packaged `.skill` Archives**: Added `packages/` directory containing ready-to-import `.skill` files for instant deployment.

### Changed
- **Rate-Limit Resilience**: Enhanced `fetch_youtube_knowledge.py` with multi-client rotation (`android,web`), Chrome session cookies auth, and automated fallback to `youtube-transcript-api`.
- **Molly Graham Benchmark**: Standardized all skills onto the 10-Section In-Depth Reference Architecture (~8,000–12,000 words).

---

## [v2.0.0] - 2026-10-02

### Added
- **Bilingual Dual-Part Architecture**: Separated documents into Part 1 (Vietnamese with preserved English terms) and Part 2 (Full English Technical Reference).
- **Dual-Mode Visualizer**: Executive Bento Grid + Technical Mermaid LR Pipeline in Section 3.

---

## [v1.0.0] - 2026-06-02

### Added
- Initial standalone YouTube Knowledge Learner skills.
- Direct transcript extraction using `yt-dlp` and `youtube-transcript-api`.
- Markdown scaffolding generator with timestamp navigation.
