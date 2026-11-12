# Changelog

All notable changes to the **YouTube Knowledge Skills** project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2.3.0] - 2026-11-12

### Added
- **Claude.dev Rail TOC with Dynamic Sub-Accordions**:
  - Adopted Anthropic's `claude.dev` rail TOC architecture across all skills (`youtube-knowledge-vi-en` v2.2.0, `youtube-knowledge-vi` v1.0.2, `youtube-knowledge-en` v1.0.2).
  - Default TOC view displays top-level sections with clean branch markers (`└`).
  - H3 sub-headings are wrapped in dynamic sub-accordions (`.subs`) that automatically expand on scrollspy when entering that section, and collapse when scrolling away.
  - Smooth animation via CSS Grid (`grid-template-rows: 0fr` ↔ `1fr`) without layout jump.
  - Sticky TOC rail progress bar with ASCII block rail (`prog`) and percentage counter.
  - Streamlined TOC topbar (omitted redundant share button for local reference notes).
- **LaTeX Math Symbol Auto-Converter (`md_render.py`)**:
  - Automatically converts common LaTeX math notations in prose (outside backtick code spans) to clean Unicode characters: `$\to$` → `→`, `$\times$` → `×`, `$\ge$` → `≥`, `$\le$` → `≤`, `$\approx$` → `≈`, `$\ne$` → `≠`, `$\pm$` → `±`, `$\infty$` → `∞`, etc.
  - Prevents raw LaTeX markup from displaying unformatted when MathJax/KaTeX is not embedded.
- **Explicit English Title & Document Title Extraction**:
  - Updated `SKILL.md` to mandate `# <Full English Title / Technical Reference Title>` directly under `# PART 2: FULL ENGLISH VERSION`.
  - Added support for `Document Title` / `Doc Title` row in Part 2 metadata table.
  - Improved `build_bilingual_html.py` title regex to `r"^(video\s+|doc(ument)?\s+)?title\b"`, ensuring English view title remains strictly English.
  - Trigger `window.dispatchEvent(new Event("scroll"))` on language switch to instantly synchronize active rail TOC headings and open sub-accordions.
- **English README (`README.en.md`)**: Full English version of documentation, linked from `README.md`.
- **Pre-packaged Archives**:
  - Added `packages/youtube-knowledge-vi-en-v2.2.0.skill` and refreshed `packages/youtube-knowledge-vi-en.skill`.
  - Added `packages/youtube-knowledge-vi-v1.0.2.skill` and refreshed `packages/youtube-knowledge-vi.skill`.
  - Added `packages/youtube-knowledge-en-v1.0.2.skill` and refreshed `packages/youtube-knowledge-en.skill`.
- **Expanded Test Suite**: 27 unit tests in `skills/youtube-knowledge-vi-en/scripts/test_build_bilingual_html.py` covering inline math conversion, sub-accordion TOC generation, and bilingual assembly.

### Changed
- README: removed the "recommended" label from the Google Antigravity IDE install option, added the lite package to the `.skill` list, and made the license note in the credits neutral.

## [v2.2.0] - 2026-10-08

### Added
- **`youtube-knowledge-vi-en-lite` (v1.0.0)**: the compact Vietnamese + English mixed-language skill (renamed from `youtube-knowledge-learner-vi-en`, derived from the English skill at github.com/longmaba/youtube-knowledge-learner), brought up to the Claude skill format. It bundles its own `fetch_youtube_knowledge.py` and a self-contained `md2html.py` (sticky TOC with scroll-spy, dark mode, callouts, Mermaid, print/PDF), so it runs without any external skill.
- New archives `packages/youtube-knowledge-vi-en-lite.skill` and `packages/youtube-knowledge-vi-en-lite-v1.0.0.skill`.

### Fixed
- Frontmatter of `youtube-knowledge-vi-en-lite` was invalid YAML (unquoted `: ` in the description); it now uses a folded block scalar and a `metadata.version` field.

### Changed
- The description now points users to `youtube-knowledge-vi-en` when they need the two-part bilingual edition, to reduce overlap between the two skills.

## [v2.1.1] - 2026-10-08

### Changed
- **Claude compatibility**: moved `version` and `keywords` into the `metadata` block of every `SKILL.md` frontmatter, so the skills pass Claude's skill validation and can be uploaded to Claude.ai / Claude Desktop / Cowork or dropped into `~/.claude/skills` for Claude Code. Versions: `youtube-knowledge-vi-en` 2.1.1, `youtube-knowledge-vi` 1.0.1, `youtube-knowledge-en` 1.0.1.
- Removed machine-specific `file:///Users/...` links and the Antigravity-only `<SKILL_DIR>` path from the skill instructions; `<SKILL_DIR>` now documents Claude Code, Claude.ai and Cowork locations.
- Added guidance for sandboxed environments without Chrome cookies (`--cookies-from-browser none`, paste transcript as a fallback).
- Rebuilt every archive in `packages/` from the updated sources.
- README: added install instructions for Claude, Codex / ChatGPT, plus a references and credits section.

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
