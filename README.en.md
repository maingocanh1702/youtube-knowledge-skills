# YouTube Knowledge Skills Suite 🎓

[![Release](https://img.shields.io/badge/release-v2.3.0-blue.svg)](CHANGELOG.md)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Interactive%20HTML-success.svg)](https://maingocanh1702.github.io/youtube-knowledge-skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20Codex%20%7C%20Antigravity%20%7C%20AI%20Agents-green.svg)](#-installation)

**🇬🇧 English** · [🇻🇳 Tiếng Việt](README.md) · 🌐 **[Live Demo](https://maingocanh1702.github.io/youtube-knowledge-skills/)**

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

#### Claude Code (simplest)

**1. Install** (run in your terminal, once):

```bash
claude plugin marketplace add maingocanh1702/youtube-knowledge-skills
claude plugin install youtube-knowledge@youtube-knowledge-skills
```

**2. Use it:** open Claude Code and send a video link:

```
Learn from this video for me: https://youtu.be/BV0hy6NET-U
```

Claude picks a skill, fetches the transcript and writes the note (Markdown + HTML). To choose an edition yourself, name the skill:

| Skill | Use it when |
|---|---|
| `youtube-knowledge-vi-en-lite` | Compact edition, Vietnamese mixed with English terms |
| `youtube-knowledge-vi-en` | Two-part bilingual, HTML with a language toggle |
| `youtube-knowledge-vi` | Pure Vietnamese |
| `youtube-knowledge-en` | Pure English |

**3. Update or remove:**

```bash
claude plugin update youtube-knowledge@youtube-knowledge-skills
claude plugin uninstall youtube-knowledge@youtube-knowledge-skills
```

> You need `python3` and `yt-dlp` on your machine (see [Prerequisites](#-prerequisites)). If the skill does not run, use `/reload-plugins` or reopen Claude Code.
> To install manually without the marketplace: `cp -r skills/* ~/.claude/skills/`.

#### Claude.ai / Claude Desktop / Cowork

1. Go to **Settings → Capabilities** and turn on *Code execution and file creation*.
2. Go to **Customize → Skills → `+` → Upload a skill** and pick a file from [`packages/`](packages/) (if the extension `.skill` is rejected, rename it to `.zip`). If you only want one, pick `youtube-knowledge-vi-en-lite.skill`; you can upload all four.

If your plan shows **Customize → Plugins**, you can also add the GitHub marketplace `maingocanh1702/youtube-knowledge-skills` instead of uploading.

> Claude.ai / Cowork has no Chrome cookies, so run the script with `--cookies-from-browser none`. If YouTube still blocks the request, paste the transcript to Claude and continue from there.

### Option 2: Codex / ChatGPT (OpenAI)

**Codex: install from the repository with skill-installer**

Send this request in Codex before asking it to process a video:

```text
$skill-installer Install all four skills from https://github.com/maingocanh1702/youtube-knowledge-skills:
- skills/youtube-knowledge-vi-en-lite
- skills/youtube-knowledge-vi-en
- skills/youtube-knowledge-vi
- skills/youtube-knowledge-en
```

For manual installation from a checkout, place the selected skill folder under `~/.agents/skills/` for all projects or the current project's `.agents/skills/`. Keep its `SKILL.md`, `scripts/`, and any `references/` together. Avoid duplicate installations of the same skill name. If your installer version uses `~/.codex/skills/`, follow the actual path it reports.

Codex discovers skills automatically; restart it if they do not appear. In the CLI/IDE, select one with `/skills` or invoke its `$` name:

| Skill | Choose it for |
|---|---|
| `$youtube-knowledge-vi-en-lite` | Concise Vietnamese notes retaining English terms |
| `$youtube-knowledge-vi-en` | Two complete VI/EN versions with language-switching HTML |
| `$youtube-knowledge-vi` | Vietnamese reference notes |
| `$youtube-knowledge-en` | English reference notes |

Example:

```text
$youtube-knowledge-en Learn from this video and create Markdown + HTML notes: https://youtu.be/BV0hy6NET-U
```

**ChatGPT / ChatGPT Work**

If your environment offers `@skill-creator`, provide the selected skill folder or repository source and ask it to create the skill:

```text
@skill-creator Create a skill from skills/youtube-knowledge-en in
https://github.com/maingocanh1702/youtube-knowledge-skills.
Keep the required scripts and references; check runtime availability before execution.
```

Once the skill has been created and appears in the picker, select it with `@` and provide a URL or transcript. Skill creation/installation depends on the environment and workspace policy. Installing a local Codex folder does not automatically sync it into your ChatGPT account.

For distributing the suite to ChatGPT, use OpenAI's plugin packaging flow. Do not assume the Claude marketplace or the `.skill` archives in `packages/` are directly installable ChatGPT packages; check the format and installation flow your environment supports.

**Runtime requirements and fallback behavior**

- Transcript fetching requires Python 3.10+ and `yt-dlp` or `youtube-transcript-api`. Lite HTML export additionally requires Python's `markdown` package. Use a suitable Python environment rather than forcing system Python changes.
- Always pass `--cookies-from-browser none` without a local browser. Browser cookies require the user's explicit authorization; the original script defaults to Chrome if the flag is omitted.
- The fetch helper accepts YouTube URLs only. Read uploaded TXT/SRT/VTT transcripts directly; audio/video requires a separate transcription tool.
- If YouTube blocks retrieval or captions are unavailable, supply a transcript. Retrieval is not guaranteed for every video. In ChatGPT without shell/file creation, produce notes in chat and do not claim scripts ran or HTML was created.
- Use a fresh output directory for each run: the helper overwrites title-derived transcripts and scaffolds. HTML loads fonts and Mermaid from CDNs, so offline diagrams are not guaranteed.

Official documentation: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Package your plugin](https://developers.openai.com/plugins/build/plugins).

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

## 🔒 What the plugin runs and accesses

- **Runs locally:** the Python scripts in `skills/*/scripts/` (fetch the transcript, compile Markdown to HTML). There are no hooks, MCP servers or other executables.
- **Network:** only YouTube, to fetch subtitles and metadata for the video you give it, through `yt-dlp` and `youtube-transcript-api`.
- **Browser cookies:** by default `--cookies-from-browser chrome` lets `yt-dlp` read your YouTube cookies from Chrome on your machine to avoid HTTP 429. The cookies are used only for requests to YouTube. To turn this off, run with `--cookies-from-browser none`.
- **Files written:** only to the `--out` folder (default `knowledge/youtube`).
- **Generated HTML:** when opened, it loads fonts from Google Fonts and Mermaid from `cdn.jsdelivr.net`. None of your data is sent anywhere.

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
│   ├── youtube-knowledge-vi-en-v2.2.0.skill
│   ├── youtube-knowledge-vi.skill
│   ├── youtube-knowledge-vi-v1.0.2.skill
│   ├── youtube-knowledge-en.skill
│   ├── youtube-knowledge-en-v1.0.2.skill
│   ├── youtube-knowledge-vi-en-lite.skill
│   └── youtube-knowledge-vi-en-lite-v1.0.0.skill
├── skills/                               # Source of each skill
│   ├── youtube-knowledge-vi-en/          # Interactive bilingual (v2.2.0)
│   ├── youtube-knowledge-vi/             # Pure Vietnamese (v1.0.2)
│   ├── youtube-knowledge-en/             # Pure English (v1.0.2)
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
