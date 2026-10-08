# YouTube Knowledge Skills Suite 🎓

[![Release](https://img.shields.io/badge/release-v2.2.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20Codex%20%7C%20Antigravity%20%7C%20AI%20Agents-green.svg)](#-installation)

**🇬🇧 English** · [🇻🇳 Tiếng Việt](README.md)

> **A set of AI agent skills that turn YouTube videos into deep technical and strategy knowledge notes, held to a fixed quality bar (the "Molly Graham Benchmark").**

Give your agent a YouTube link. It fetches the transcript, writes a long, structured note (about 8,000–12,000 words across 10 sections), and compiles it into an interactive HTML page with dark/light themes, print/PDF export and zoomable Mermaid diagrams.

---

## 🌟 Overview: 4 Skills

Three main language editions plus one lightweight edition cover research, study and day-to-day use:

| Skill | Purpose | Language | Bundled HTML compiler |
| :--- | :--- | :--- | :--- |
| **`youtube-knowledge-vi-en`** | **The full interactive bilingual edition.** Two independent parts: Part 1 in Vietnamese (all English technical terms kept as-is) and Part 2 as a complete English technical reference. | 🇻🇳 VI ⇋ 🇬🇧 EN | ✅ Instant language toggle, dual table of contents, Bento + Mermaid visualizer in both languages |
| **`youtube-knowledge-vi`** | **Pure Vietnamese edition.** Translates business and management terms into Vietnamese (*career growth* → thăng tiến sự nghiệp, *talent bar* → chuẩn nhân sự). | 🇻🇳 Vietnamese | ✅ Standalone single-language HTML compiler |
| **`youtube-knowledge-en`** | **Full English technical reference.** Everything in English, suited to international readers and usable as a system prompt for other AI agents. | 🇬🇧 English | ✅ Standalone single-language HTML compiler |
| **`youtube-knowledge-vi-en-lite`** | **Lite edition (Vietnamese mixed with English).** Keeps English terms, fetches the transcript and converts to HTML with the bundled `md2html.py`. Use it for quick notes when you don't need the two-part bilingual document. | 🇻🇳🇬🇧 Mixed | ✅ Bundled `md2html.py` (TOC, dark mode, Mermaid) |

---

## ✨ Highlights

### 1. A fixed quality bar (the Molly Graham Benchmark)

No thin, generic summaries. Each Markdown note is distilled into **10 in-depth sections**, roughly **8,000–12,000 words**:

1. **Metadata & Quick Reference**: guest bio, metadata table, and 15–25 timestamp markers across the whole video.
2. **Executive Summary**: 5–6 macro-level takeaways with context, figures and practical lessons.
3. **Systems Mental Model (dual-mode visualizer)**:
   - **Tab 1, Executive Bento Grid**: grasp the system in 30 seconds.
   - **Tab 2, Technical Mermaid Flowchart**: a left-to-right pipeline diagram.
4. **Conceptual Lexicon**: a glossary with working definitions and usage context.
5. **Deep Dive**: 4–6 multi-layered topics.
6. **Practical Frameworks & Playbooks**: step-by-step processes, decision diagrams, implementation checklists.
7. **Contrarian Insights**: conventional wisdom versus battle-tested reality.
8. **Trade-offs Matrix**: hidden costs, risks, constraints and mitigations.
9. **The "Fail Corner" & Anti-Patterns**: common fatal mistakes and how to handle a crisis.
10. **High-Signal Quotes & Verbatim Excerpts**: decisive quotes with timestamps.

### 2. Self-contained HTML compiler (zero dependencies)

- Compiles Markdown into a rich interactive HTML page (about 70–110 KB).
- **Embedded template engine**: `template.html` ships inside each skill, so there is no external tool to install.
- Dark/light theme, print / export to PDF, responsive on phone, tablet and desktop.
- **Interactive flow viewer**: zoom in (`＋`), zoom out (`－`), reset (`⟲`), fullscreen (`⛶`) and drag to pan Mermaid diagrams.

### 3. Handling YouTube rate limits (HTTP 429)

- Prefers `yt-dlp` with `--cookies-from-browser chrome`, authenticating through your own YouTube session.
- Rotates client identifiers (`android,web`) and retries with backoff.
- Falls back to `youtube-transcript-api` (an independent endpoint) on captcha or bot challenges.

---

## 🚀 Installation

Every platform below uses the same open format: **a skill folder with `SKILL.md` at its root**, plus the `scripts/` and `references/` next to it. Only the place you put the folder changes.

### Option 1: Claude

The skills use a Claude-compatible frontmatter (`name`, `description`, `metadata`).

**Claude.ai / Claude Desktop / Cowork**

1. Go to **Settings → Capabilities** and turn on *Code execution and file creation*.
2. Go to **Customize → Skills → `+` → Upload a skill**.
3. Pick a file from [`packages/`](packages/), one skill at a time. If the dialog rejects the `.skill` extension, rename it to `.zip`.

**Claude Code (terminal)**

```bash
# Global
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/

# Or for one project only
mkdir -p .claude/skills
cp -r skills/* .claude/skills/
```

> **Running inside Claude.ai / Cowork:** the sandbox has no browser, so there are no Chrome cookies. Run the script with `--cookies-from-browser none`. If YouTube still blocks the request, paste the transcript to Claude and continue from there.

### Option 2: Codex / ChatGPT (OpenAI)

Codex reads the same `SKILL.md` format:

```bash
mkdir -p ~/.agents/skills        # available in every project
cp -r skills/* ~/.agents/skills/

# or only for the current repo
mkdir -p .agents/skills
cp -r skills/* .agents/skills/
```

Codex picks up new skills automatically (restart it if a skill does not show up). Invoke with `$` or `/skills`. For the ChatGPT app, OpenAI's docs currently describe creating skills with `@skill-creator` or packaging them as a plugin; there is no direct folder or ZIP upload step.

### Option 3: Google Antigravity IDE

```bash
# Global (macOS / Linux)
mkdir -p ~/.gemini/config/skills
cp -r skills/* ~/.gemini/config/skills/

# Or per project
mkdir -p .agents/skills
cp -r skills/* .agents/skills/
```

The Antigravity CLI may read global skills from `~/.gemini/antigravity-cli/skills/`; check which path your version uses.

### Option 4: Import a packaged `.skill` file

Ready-made archives are in [`packages/`](packages/):

- 📦 [`packages/youtube-knowledge-vi-en.skill`](packages/youtube-knowledge-vi-en.skill): bilingual edition
- 📦 [`packages/youtube-knowledge-vi.skill`](packages/youtube-knowledge-vi.skill): pure Vietnamese edition
- 📦 [`packages/youtube-knowledge-en.skill`](packages/youtube-knowledge-en.skill): pure English edition
- 📦 [`packages/youtube-knowledge-vi-en-lite.skill`](packages/youtube-knowledge-vi-en-lite.skill): lite edition

Unzip, or drop them into the skills folder of the assistant you use.

### Check that it works

Open your agent and send:

```
Learn from this video for me: https://youtu.be/BV0hy6NET-U
```

The agent should pick the right skill, run the transcript script and start writing the note. If nothing happens, check the folder location and restart the agent.

---

## 🛠️ Standalone CLI usage

You can run the scripts from a terminal without any agent.

### 1. Fetch subtitles and create a note scaffold

```bash
# Vietnamese subtitles (or English if the video only has English)
python3 skills/youtube-knowledge-vi-en/scripts/fetch_youtube_knowledge.py "https://youtu.be/BV0hy6NET-U" \
  --out "output" \
  --cookies-from-browser chrome
```

### 2. Compile Markdown to HTML

```bash
# Bilingual edition (vi-en)
python3 skills/youtube-knowledge-vi-en/scripts/build_bilingual_html.py "output/note.md" --out "output/note.html"

# Single-language editions (vi or en)
python3 skills/youtube-knowledge-vi/scripts/build_html.py "output/note.md" --lang vi --out "output/note.html"
python3 skills/youtube-knowledge-en/scripts/build_html.py "output/note.md" --lang en --out "output/note.html"
```

---

## 📁 Repository layout

```text
youtube-knowledge-skills/
├── packages/                             # Ready-to-import .skill archives
│   ├── youtube-knowledge-vi-en.skill
│   ├── youtube-knowledge-vi-en-v2.1.1.skill
│   ├── youtube-knowledge-vi.skill
│   ├── youtube-knowledge-vi-v1.0.1.skill
│   ├── youtube-knowledge-en.skill
│   ├── youtube-knowledge-en-v1.0.1.skill
│   ├── youtube-knowledge-vi-en-lite.skill
│   └── youtube-knowledge-vi-en-lite-v1.0.0.skill
├── skills/                               # Source of each skill
│   ├── youtube-knowledge-vi-en/          # Interactive bilingual (v2.1.1)
│   ├── youtube-knowledge-vi/             # Pure Vietnamese (v1.0.1)
│   ├── youtube-knowledge-en/             # Pure English (v1.0.1)
│   └── youtube-knowledge-vi-en-lite/     # Lite, Vietnamese + English (v1.0.0)
├── CHANGELOG.md
├── LICENSE
├── README.md                             # Vietnamese
└── README.en.md                          # English
```

Each skill folder contains `SKILL.md`, `scripts/` (fetch script, HTML compiler, bundled template) and, for the three main editions, `references/system-map-template.md`.

---

## 📋 Prerequisites

- **Python** 3.9+
- **yt-dlp** (recommended):
  ```bash
  # macOS
  brew install yt-dlp
  # Windows / Linux
  pip install --user yt-dlp
  ```
- **youtube-transcript-api** (fallback):
  ```bash
  pip install --user youtube-transcript-api
  ```
- The lite edition's `md2html.py` also needs the `markdown` package (the script prints the install command if it is missing).

---

## 🙏 References & credits

- **Molly Graham Benchmark**: the project's own quality bar, taken from three sample notes written from interviews with Molly Graham, Peter Deng and Ian Silber.
- [`longmaba/youtube-knowledge-learner`](https://github.com/longmaba/youtube-knowledge-learner): the original English skill that the lite edition (`youtube-knowledge-vi-en-lite`) was split out from and developed. No license file was visible in that repository, so check its terms before wide redistribution.
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp): subtitle and video metadata download.
- [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api): fallback transcript fetching.
- [Mermaid](https://mermaid.js.org/): flow diagrams in the System Map section.
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html): conventions for `CHANGELOG.md` and version numbers.

---

## 📄 License

Released under the **[MIT License](LICENSE)**. Free to use, modify and integrate into any personal or commercial AI agent setup.
