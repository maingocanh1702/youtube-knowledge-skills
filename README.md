# YouTube Knowledge Skills Suite 🎓

[![Release](https://img.shields.io/badge/release-v2.2.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20Codex%20%7C%20Antigravity%20%7C%20AI%20Agents-green.svg)](#-cài-đặt-installation)

> **Bộ AI Agent Skills cao cấp biến video YouTube thành kho tri thức kỹ thuật & chiến lược chuyên sâu theo Tiêu Chuẩn Vàng (Molly Graham Benchmark).**

[🇬🇧 English](README.en.md) · **🇻🇳 Tiếng Việt**

---

## 🌟 Tổng Quan 4 Phiên Bản (Triad Suite + Lite)

Bộ kỹ năng gồm 3 phân hệ ngôn ngữ chính cùng 1 bản lite gọn nhẹ để đáp ứng mọi nhu cầu nghiên cứu, học tập và triển khai thực chiến:

| Skill | Mục đích & Đặc thù | Ngôn ngữ | HTML Compiler Đi Kèm |
| :--- | :--- | :--- | :--- |
| **`youtube-knowledge-vi-en`** | **Bản Song Ngữ Tương Tác cao cấp nhất**. Cấu trúc 2 Part độc lập: Part 1 (Tiếng Việt giữ nguyên 100% thuật ngữ tiếng Anh) và Part 2 (Full English Technical Reference). | 🇻🇳 VI ⇋ 🇬🇧 EN | ✅ Nút đổi ngôn ngữ tức thì, Dual TOC, Bento + Mermaid cả 2 ngôn ngữ |
| **`youtube-knowledge-vi`** | **Bản Thuần Tiếng Việt**. Dịch 100% tất cả thuật ngữ kinh doanh/quản trị sang tiếng Việt (*career growth* → thăng tiến sự nghiệp, *talent bar* → chuẩn nhân sự). | 🇻🇳 Tiếng Việt thuần | ✅ Standalone Single-Lang HTML Compiler |
| **`youtube-knowledge-en`** | **Bản Full English Technical Reference**. Chưng cất 100% tiếng Anh chuẩn kỹ thuật toàn diện, phục vụ tra cứu quốc tế và làm system prompt cho AI Agents. | 🇬🇧 English | ✅ Standalone Single-Lang HTML Compiler |
| **`youtube-knowledge-vi-en-lite`** | **Bản Lite (Việt trộn Anh)**. Giữ nguyên thuật ngữ tiếng Anh, tự lấy transcript và chuyển sang HTML bằng `md2html.py` đi kèm. Dùng khi chỉ cần ghi chú nhanh, không cần 2 phần song ngữ. | 🇻🇳🇬🇧 Trộn Việt + Anh | ✅ `md2html.py` đi kèm (TOC, dark mode, Mermaid) |

---

## ✨ Điểm Nổi Bật Vượt Trội

### 1. Tiêu Chuẩn Vàng (Molly Graham Benchmark)
Không tạo bản tóm tắt sơ sài, chung chung. Mỗi tài liệu Markdown được chưng cất thành **10 Phân Hệ Chuyên Sâu** với độ dài từ **8.000 – 12.000 từ** (~35–45 KB Markdown):
1. **Metadata & Quick Reference**: Tiểu sử khách mời, bảng metadata và chỉ mục timestamp chi tiết từ đầu đến cuối video (15–25 mốc).
2. **Executive Summary**: 5–6 luận điểm vĩ mô cốt tử, phân tích sâu về bối cảnh, số liệu và bài học thực tiễn.
3. **Systems Mental Model (Dual-Mode Visualizer)**:
   - **Tab 1: ✨ Executive Bento Grid** — Nắm bắt bản chất hệ thống trong 30 giây.
   - **Tab 2: 🔍 Technical Mermaid Flowchart** — Sơ đồ dòng chảy LR Pipeline (tỷ lệ 16:9, classDef 4 phân miền pastel, node mini-card 2 tầng).
4. **Thuật Ngữ Cốt Lõi / Conceptual Lexicon**: Bảng từ điển thuật ngữ kèm định nghĩa vận hành và bối cảnh áp dụng.
5. **Phân Tích Chuyên Sâu (Deep Dive)**: 4–6 chủ đề vi mô bóc tách đa tầng.
6. **Frameworks & Playbooks Thực Chiến**: Quy trình từng bước, sơ đồ quyết định, checklist triển khai.
7. **Góc Nhìn Phản Trực Giác / Contrarian Insights**: Thách thức quan niệm thông thường (Conventional Wisdom vs. Battle-Tested Reality).
8. **Ma Trận So Sánh & Đánh Đổi (Trade-offs Matrix)**: Chi phí ẩn, rủi ro, ràng buộc và giải pháp giảm thiểu.
9. **The "Fail Corner" & Anti-Patterns**: Cảnh báo sai lầm chết người và quy trình xử lý khủng hoảng.
10. **High-Signal Quotes & Verbatim Excerpts**: Trích dẫn nguyên văn mang tính quyết định kèm timestamp.

### 2. Trình Biên Dịch HTML Tự Chứa (Zero-Dependency)
- Tự động biên dịch từ Markdown sang file HTML tương tác cao cấp (dung lượng 70–110 KB).
- **Embedded Template Engine**: Tích hợp sẵn `template.html` bên trong mỗi skill, không phụ thuộc công cụ ngoài.
- Hỗ trợ đầy đủ **Dark/Light Theme**, In/Xuất PDF, Responsive trên Mobile/Tablet/Desktop.
- **Interactive Flow Viewer**: Hỗ trợ phóng to (`＋`), thu nhỏ (`－`), đặt lại kích thước (`⟲`), toàn màn hình (`⛶`) và kéo thả chuột (pan) cho sơ đồ Mermaid.

### 3. Cơ Chế Chống Rate-Limit YouTube 429
- Ưu tiên gọi `yt-dlp` kết hợp `--cookies-from-browser chrome` để xác thực qua session YouTube của người dùng.
- Tự động luân chuyển client identifiers (`android,web`) và áp dụng retry thuật toán backoff.
- Tự động fallback sang `youtube-transcript-api` (endpoint độc lập) nếu `yt-dlp` gặp captcha/bot challenge.

---

## 🚀 Cài Đặt (Installation)

### Cách 1: Dùng cho Google Antigravity IDE

Copy các thư mục skill từ `skills/` vào thư mục cấu hình toàn cục:

```bash
# macOS / Linux
mkdir -p ~/.gemini/config/skills
cp -r skills/* ~/.gemini/config/skills/
```

*Hoặc copy vào từng dự án cụ thể:*
```bash
mkdir -p .agents/skills
cp -r skills/* .agents/skills/
```

### Cách 2: Dùng cho Claude

Các skill đã được chuẩn hóa frontmatter (`name`, `description`, `metadata`) để vượt qua bộ kiểm tra của Claude.

**Claude.ai / Claude Desktop / Cowork**

1. Vào **Settings → Capabilities** và bật *Code execution and file creation*.
2. Vào **Customize → Skills → `+` → Upload a skill**.
3. Chọn file trong [`packages/`](packages/), mỗi lần một skill (nếu giao diện không nhận đuôi `.skill`, đổi đuôi thành `.zip`).

**Claude Code (terminal)**

```bash
# Toàn cục
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/

# Hoặc cho riêng một dự án
mkdir -p .claude/skills
cp -r skills/* .claude/skills/
```

> **Lưu ý khi chạy trong Claude.ai / Cowork:** môi trường này không có trình duyệt nên không có cookie Chrome. Hãy chạy script với `--cookies-from-browser none`; nếu YouTube vẫn chặn, hãy dán transcript cho Claude để làm tiếp.

### Cách 3: Dùng cho Codex / ChatGPT (OpenAI)

Codex đọc cùng định dạng `SKILL.md`:

```bash
mkdir -p ~/.agents/skills        # dùng cho mọi dự án
cp -r skills/* ~/.agents/skills/

# hoặc riêng cho repo hiện tại
mkdir -p .agents/skills
cp -r skills/* .agents/skills/
```

Codex tự phát hiện skill mới (khởi động lại nếu chưa thấy), gọi bằng `$` hoặc `/skills`. Với ứng dụng ChatGPT, OpenAI hiện hướng dẫn tạo skill bằng `@skill-creator` hoặc đóng gói thành plugin; chưa có bước tải lên thư mục/ZIP trực tiếp.

### Cách 4: Nhập Bằng File Đóng Gói `.skill`

Các file đóng gói sẵn nằm trong thư mục [`packages/`](packages/):
* 📦 [`packages/youtube-knowledge-vi-en.skill`](packages/youtube-knowledge-vi-en.skill) *(Bản song ngữ)*
* 📦 [`packages/youtube-knowledge-vi.skill`](packages/youtube-knowledge-vi.skill) *(Bản thuần Việt)*
* 📦 [`packages/youtube-knowledge-en.skill`](packages/youtube-knowledge-en.skill) *(Bản thuần Anh)*
* 📦 [`packages/youtube-knowledge-vi-en-lite.skill`](packages/youtube-knowledge-vi-en-lite.skill) *(Bản Lite, Việt trộn Anh)*

Giải nén hoặc kéo thả vào thư mục `skills` của trợ lý AI bạn đang sử dụng.

---

## 🛠️ Hướng Dẫn Sử Dụng Bằng CLI (Standalone)

Bạn hoàn toàn có thể chạy độc lập các script từ Terminal mà không cần thông qua Agent:

### 1. Trích xuất phụ đề và tạo scaffold ghi chú
```bash
# Lấy phụ đề tiếng Việt (hoặc tiếng Anh nếu video chỉ có tiếng Anh)
python3 skills/youtube-knowledge-vi-en/scripts/fetch_youtube_knowledge.py "https://youtu.be/BV0hy6NET-U" \
  --out "output" \
  --cookies-from-browser chrome
```

### 2. Biên dịch file Markdown sang HTML
```bash
# Đối với bản song ngữ (vi-en):
python3 skills/youtube-knowledge-vi-en/scripts/build_bilingual_html.py "output/note.md" --out "output/note.html"

# Đối với bản đơn ngữ (vi hoặc en):
python3 skills/youtube-knowledge-vi/scripts/build_html.py "output/note.md" --lang vi --out "output/note.html"
python3 skills/youtube-knowledge-en/scripts/build_html.py "output/note.md" --lang en --out "output/note.html"
```

---

## 📁 Cấu Trúc Thư Mục

```text
youtube-knowledge-skills/
├── packages/                             # File nén .skill sẵn sàng import/cài đặt
│   ├── youtube-knowledge-vi-en.skill
│   ├── youtube-knowledge-vi-en-v2.1.1.skill
│   ├── youtube-knowledge-vi.skill
│   ├── youtube-knowledge-vi-v1.0.1.skill
│   ├── youtube-knowledge-en.skill
│   ├── youtube-knowledge-en-v1.0.1.skill
│   ├── youtube-knowledge-vi-en-lite.skill
│   └── youtube-knowledge-vi-en-lite-v1.0.0.skill
├── skills/                               # Mã nguồn chi tiết từng skill
│   ├── youtube-knowledge-vi-en/          # Skill Song ngữ tương tác (v2.1.1)
│   │   ├── SKILL.md
│   │   ├── references/system-map-template.md
│   │   └── scripts/
│   │       ├── fetch_youtube_knowledge.py
│   │       ├── build_bilingual_html.py
│   │       ├── flow_viewer.py
│   │       ├── md_render.py
│   │       └── template.html
│   ├── youtube-knowledge-vi/             # Skill Thuần tiếng Việt (v1.0.1)
│   │   ├── SKILL.md
│   │   ├── references/system-map-template.md
│   │   └── scripts/
│   │       ├── fetch_youtube_knowledge.py
│   │       ├── build_html.py
│   │       ├── flow_viewer.py
│   │       ├── md_render.py
│   │       └── template.html
│   ├── youtube-knowledge-en/             # Skill Thuần tiếng Anh (v1.0.1)
│   │   ├── SKILL.md
│   │   ├── references/system-map-template.md
│   │   └── scripts/
│   │       ├── fetch_youtube_knowledge.py
│   │       ├── build_html.py
│   │       ├── flow_viewer.py
│   │       ├── md_render.py
│   │       └── template.html
│   └── youtube-knowledge-vi-en-lite/  # Skill Lite Việt + Anh (v1.0.0)
│       ├── SKILL.md
│       └── scripts/
│           ├── fetch_youtube_knowledge.py
│           └── md2html.py
├── CHANGELOG.md                          # Lịch sử cập nhật phiên bản
├── LICENSE                               # Giấy phép MIT
├── README.md                             # Hướng dẫn chi tiết (tiếng Việt)
├── README.en.md                          # English version
└── .gitignore                            # Quy tắc bỏ qua file rác
```

---

## 📋 Yêu Cầu Môi Trường (Prerequisites)

- **Python**: 3.9+
- **yt-dlp** (khuyên dùng):
  ```bash
  # macOS
  brew install yt-dlp
  # Windows / Linux
  pip install --user yt-dlp
  ```
- **youtube-transcript-api** (dự phòng):
  ```bash
  pip install --user youtube-transcript-api
  ```

---

## 🙏 Nguồn Tham Khảo & Ghi Nhận

- **Molly Graham Benchmark**: chuẩn chất lượng tự đặt của dự án, lấy từ ba ghi chú mẫu viết từ các cuộc phỏng vấn với Molly Graham, Peter Deng và Ian Silber.
- [`longmaba/youtube-knowledge-learner`](https://github.com/longmaba/youtube-knowledge-learner): skill gốc bằng tiếng Anh mà bản Lite (`youtube-knowledge-vi-en-lite`) được tách ra và phát triển từ đó. Repo này chưa hiển thị file giấy phép, nên hãy kiểm tra lại điều khoản trước khi phát hành rộng.
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp): tải phụ đề và metadata video.
- [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api): lấy transcript dự phòng.
- [Mermaid](https://mermaid.js.org/): vẽ sơ đồ luồng trong phần System Map.
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) và [Semantic Versioning](https://semver.org/spec/v2.0.0.html): quy ước cho `CHANGELOG.md` và đánh số phiên bản.

---

## 📄 License

Dự án được phân phối dưới giấy phép **[MIT License](LICENSE)**. Tự do sử dụng, tùy biến và tích hợp vào bất kỳ hệ thống AI Agent cá nhân hoặc thương mại nào.
