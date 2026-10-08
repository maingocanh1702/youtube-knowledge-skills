---
name: youtube-knowledge-vi-en
description: >-
  Bản SONG NGỮ TƯƠNG TÁC (🇻🇳 VI ⇋ 🇬🇧 EN) cao cấp nhất cho YouTube. Gồm 2 phần độc lập theo Tiêu Chuẩn Vàng (Molly Graham Benchmark):
  Part 1 (Tiếng Việt chuyên sâu, giữ nguyên 100% thuật ngữ chuyên ngành tiếng Anh) và Part 2 (Full English Technical Reference).
  Tự động xuất file HTML tương tác có nút chuyển đổi ngôn ngữ tức thì, 2 mục lục (TOC) độc lập, và Dual-Mode Visualizer (Bento + Mermaid)
  chuẩn mực cho cả 2 ngôn ngữ. Kích hoạt khi người dùng cung cấp URL YouTube hoặc yêu cầu học từ video.
metadata:
  version: "2.1.1"
  keywords: [youtube, tiếng việt, english, song ngữ, bilingual, mixed, vi-en, transcript, ghi chú, markdown, interactive html, bento, mermaid, knowledge]
---

# YouTube Knowledge Learner — Bản Song Ngữ Tương Tác Cao Cấp (vi-en v2.1)

Sử dụng skill này để biến một video YouTube thành một kho tri thức tham khảo chuẩn mực hàng đầu **song ngữ hoàn chỉnh (Bilingual Dual-Language Architecture)**:

1. **Lấy transcript/phụ đề** (ưu tiên tiếng Việt; nếu không có thì lấy tiếng Anh/ngôn ngữ gốc và trích xuất timestamp đầy đủ).
2. **Bảo tồn metadata gốc** và các tham chiếu theo timestamp chi tiết từ đầu đến cuối video.
3. **Chưng cất video thành tài liệu Markdown Song Ngữ (2 Parts Độc Lập)**:
   - **Part 1 (Bản Tiếng Việt)**: Phân tích chuyên sâu đa tầng, giữ nguyên 100% thuật ngữ chuyên ngành tiếng Anh (`career growth`, `talent bar`, `clock speed`, `feedback`, `trade-off`...).
   - **Part 2 (Full English Technical Reference)**: Bản tiếng Anh chuẩn kỹ thuật toàn diện, phục vụ tra cứu quốc tế và làm system prompt cho các AI Agents tương lai.
4. **Tự động chain sang trình biên dịch HTML Song Ngữ (`scripts/build_bilingual_html.py`)**:
   - Tích hợp nút chuyển đổi ngôn ngữ tức thì (`🇻🇳 VI` ⇋ `🇬🇧 EN`) trên Topbar.
   - Dual Table of Contents (`#toc-links-vi` và `#toc-links-en`) với liên kết neo chính xác 100%, không bị trùng lặp chữ hay nhảy giao diện.
   - Cung cấp **Dual-Mode Visualizer (Executive Bento Grid + Technical Mermaid Flowchart)** hoàn chỉnh cho cả hai ngôn ngữ.
5. **Áp dụng kiến thức học được** vào tác vụ kỹ thuật/sản phẩm hiện tại của người dùng.

> Nếu muốn dịch thuần Việt (dịch cả các cụm như "career growth" → "thăng tiến sự nghiệp", "talent bar" → "chuẩn nhân sự"...), dùng skill **`youtube-knowledge-vi`** thay thế.

---

## 1. Quy tắc ngôn ngữ — Bản SONG NGỮ CHUẨN MỰC

### Quy tắc Part 1: Tiếng Việt Giữ Nguyên Thuật Ngữ Tiếng Anh

1. **GIỮ NGUYÊN TẤT CẢ thuật ngữ chuyên ngành tiếng Anh.** Tuyệt đối không dịch sang tiếng Việt:
   - **Kỹ thuật / AI / Data**: `API`, `framework`, `deploy`, `CI/CD`, `Docker`, `Kubernetes`, `machine learning`, `embedding`, `transformer`, `prompt`, `LLM`, `context window`, `token`, `fine-tuning`, `agent`, `MCP`, `RAG`, `evals`, `capability overhang`...
   - **Product / Management / Strategy**: `career growth`, `fast pace`, `talent bar`, `zone of genius`, `kind vs nice`, `brilliant jerk`, `clock speed`, `personal SLA`, `T-shaped leadership`, `cross-functional`, `OKR`, `KPI`, `MVP`, `PRD`, `roadmap`, `backlog`, `sprint`, `retro`, `stand-up`, `imposter syndrome`, `growth hack`, `ecosystem`, `feedback`, `team`, `leader`, `stakeholder`, `pipeline`, `funnel`, `trade-off`, `taste`, `craft`...
   - **Marketing / GTM**: `product-led`, `sales-led`, `bottom-up`, `top-down`, `PLG`, `ICP`, `pricing`, `unit economics`, `TAM`, `SAM`, `SOM`, `churn`, `retention`, `activation`, `acquisition`...
   - **Design / UX**: `UX`, `UI`, `design system`, `canvas`, `modal`, `blank box`, `spatial UI`, `latency`, `affordance`, `mental model`...
   - **Tên riêng**: tên người, công ty, sản phẩm, địa danh, công cụ, thư viện code.
   - **Quotes nguyên văn** của diễn giả.

2. **CHỈ DỊCH KHUNG NỘI DUNG CHÍNH** sang tiếng Việt: cấu trúc câu, từ nối ("và", "nhưng", "bởi vì", "do đó"), phân tích nguyên lý, ngữ cảnh, case study và narrative tổng quát.

3. **Bảng đối chiếu — TUYỆT ĐỐI KHÔNG dịch trong Part 1**:
   | Tiếng Anh (Bắt buộc giữ nguyên) | TUYỆT ĐỐI KHÔNG dịch thành |
   |---|---|
   | career growth | ~~thăng tiến sự nghiệp~~ |
   | fast pace | ~~tốc độ nhanh / nhịp độ nhanh~~ |
   | talent bar | ~~chuẩn nhân sự~~ |
   | brilliant jerk | ~~thiên tài đểu~~ |
   | zone of genius | ~~vùng thiên tài~~ |
   | feedback | ~~phản hồi~~ |
   | team / leader | ~~đội / lãnh đạo~~ |
   | scrappy / scrappiness | ~~lì lợm / sự lì lợm~~ |
   | ecosystem | ~~hệ sinh thái~~ |
   | trade-off | ~~đánh đổi~~ |
   | stakeholder | ~~bên liên quan~~ |
   | cross-functional | ~~đa chức năng~~ |
   | imposter syndrome | ~~hội chứng kẻ mạo danh~~ |
   | clock speed | ~~tốc độ đồng hồ~~ |

### Quy tắc Part 2: Full English Technical Reference

1. **100% Native Technical English**: Văn phong kỹ thuật/quản trị sản phẩm chuẩn Thung lũng Silicon, mật độ thông tin cao, chặt chẽ, chính xác.
2. **Đồng bộ 1:1 về chiều sâu với Part 1**: Không tóm tắt sơ sài. Part 2 phải có đủ 10 phân hệ tương ứng, tái hiện đầy đủ mọi số liệu, trích dẫn, sơ đồ và playbook.
3. **Phục vụ đa mục đích**: Dành cho kỹ sư quốc tế tra cứu trực tiếp hoặc cung cấp ngữ cảnh hoàn hảo (system context) cho các mô hình LLM tiên tiến nhất.

---

## 2. Đầu vào & Cách lấy transcript

Skill chấp nhận URL YouTube, file audio/video cục bộ, hoặc file transcript.

### Chạy helper script tự động:

```bash
python3 "<SKILL_DIR>/scripts/fetch_youtube_knowledge.py" "<YOUTUBE_URL>" \
  --out "<OUTPUT_DIR>" \
  --lang vi \
  --cookies-from-browser chrome \
  --task "<mô tả tác vụ nếu có>"
```

- `<SKILL_DIR>` = thư mục chứa skill này (Claude Code: `~/.claude/skills/youtube-knowledge-vi-en` hoặc `.claude/skills/youtube-knowledge-vi-en`; Claude.ai / Cowork: thư mục skill được mount cho phiên, dùng đường dẫn thực tế của skill).
- **Khi chạy trong Claude.ai / Cowork** (sandbox không có trình duyệt, không có cookie Chrome): đổi thành `--cookies-from-browser none`. Nếu YouTube chặn, script tự fallback sang `youtube-transcript-api`; nếu vẫn thất bại, nhờ người dùng dán transcript hoặc đính kèm file transcript rồi truyền đường dẫn file đó vào thay cho URL.
- Mặc định dùng `yt-dlp` với cookie từ Chrome để tránh rate-limit HTTP 429.
- Tự động fallback sang `youtube-transcript-api` nếu `yt-dlp` gặp trở ngại.
- Script tạo scaffold tài liệu song ngữ 10 phân hệ tại `knowledge/youtube/<slug>.md`.

---

## 3. Cấu trúc đầu ra chuẩn mực — TIÊU CHUẨN VÀNG (Molly Graham Benchmark)

> **QUY TẮC BẮT BUỘC**: Mọi tài liệu tạo bởi skill này PHẢI áp dụng **Tiêu Chuẩn Vàng (Gold Standard Benchmark)** tương đương các tài liệu mẫu Molly Graham, Peter Deng, và Ian Silber.
> Tổng dung lượng Markdown đạt từ **70–100 KB** (khoảng **8.000 – 12.000 từ** cho cả 2 phần), HTML hoàn thiện đạt từ **130–170 KB**.

Tài liệu Markdown được tổ chức thành 2 phần rõ rệt:

```markdown
# <Tiêu đề Video Đầy Đủ & Sâu Sắc>

> **Kiến trúc Song Ngữ (Bilingual Standard v2.0)**: Tài liệu gồm 2 phần độc lập theo Tiêu Chuẩn Vàng (Molly Graham Benchmark):
> - **Phần 1 (Bản Tiếng Việt + Thuật Ngữ EN)**: Giữ nguyên toàn bộ thuật ngữ chuyên ngành tiếng Anh (`career growth`, `talent bar`, `feedback`, `trade-off`, `clock speed`...), phân tích chuyên sâu đa chiều bằng tiếng Việt.
> - **Part 2 (Full English Technical Reference)**: Bản tiếng Anh chuẩn kỹ thuật toàn diện, phục vụ tra cứu quốc tế và làm ngữ cảnh cho AI Agents.

---

# PHẦN 1: BẢN TIẾNG VIỆT (GIỮ THUẬT NGỮ CHUYÊN NGÀNH TIẾNG ANH)

## 1. Metadata & Quick Reference
- **Bảng Metadata**: Nguồn URL, Kênh/Host, Khách mời (Bio chi tiết, vai trò, thành tựu), Thời lượng, Lĩnh vực, Đối tượng mục tiêu.
- **Chỉ Mục Timestamp (Timestamp Navigation)**: Tối thiểu 15–25 mốc thời gian kèm tóm tắt chủ đề chi tiết từ đầu đến cuối video.

## 2. Executive Summary
- Tối thiểu 5–6 luận điểm vĩ mô cốt tử, phân tích sâu về bối cảnh, số liệu, tâm lý học tổ chức và kết luận thực tiễn.

## 3. Bản Đồ Tư Duy Hệ Thống (Dual-Mode Visualizer BẮT BUỘC)
- BẮT BUỘC áp dụng cấu trúc **Dual-Mode Visualizer** theo chuẩn [references/system-map-template.md](references/system-map-template.md):
  * **Tab 1: ✨ Executive Bento Grid** — 3–4 thẻ kiến trúc Bento (step-pill 1-4, badge, flow steps với icon sinh động, highlight bar axiom vàng). Nắm bắt 100% bản chất hệ thống trong 30 giây không cần cuộn chuột.
  * **Tab 2: 🔍 Technical Mermaid Flowchart LR Pipeline** — Sơ đồ Mermaid `flowchart LR` chuẩn tỷ lệ 16:9, chia 3–4 phân miền màu pastel via `classDef`, node mini-card 2 tầng (Icon + Title đậm + Subtitle nhỏ), vòng lặp feedback dạng nét đứt `-.->`, kèm toolbar zoom/fullscreen tương tác.

## 4. Thuật Ngữ Cốt Lõi
- Bảng từ điển 8–12 thuật ngữ chuyên môn tiếng Anh xuất hiện trong video, kèm giải thích ngữ nghĩa, bối cảnh thực tế và cách ứng dụng.

## 5. Phân Tích Chuyên Sâu (Deep Dive)
- BẮT BUỘC chia thành **tối thiểu 4–5 tiểu mục H3 riêng biệt** (`### 5.1`, `### 5.2`, `### 5.3`, `### 5.4`, `### 5.5`).
- Mỗi tiểu mục là một bài phân tích chuyên sâu về cơ chế, nguyên lý nền tảng, case study thực tế, và trích dẫn trực tiếp của diễn giả.

## 6. Frameworks & Playbooks Thực Chiến
- BẮT BUỘC đóng gói thành **tối thiểu 2–3 Playbooks thực thi từng bước** (`### Playbook 1: ...`, `### Playbook 2: ...`, `### Playbook 3: ...`).
- Mỗi Playbook có bảng các bước tuần tự (Bước 1, Bước 2, Bước 3...), kịch bản thực hiện, và template mẫu.

## 7. Góc Nhìn Ngược Số Đông (Contrarian Perspectives)
- Liệt kê 3–5 góc nhìn phản trực giác, đi ngược lại các quan niệm thông thường của số đông trong ngành, kèm bảng so sánh "Quan niệm phổ biến" vs "Sự thật thực chiến".

## 8. Ma Trận So Sánh & Đánh Đổi (Trade-offs & Comparison Matrix)
- Các bảng so sánh đa chiều: Phân tích ưu/nhược điểm, chi phí ẩn, rủi ro và giải pháp giảm thiểu cho từng lựa chọn kỹ thuật hoặc chiến lược.

## 9. Giải Đáp Thắc Mắc Thực Chiến (Q&A Scenarios)
- 4–5 câu hỏi tiến thoái lưỡng nan hóc búa nhất mà kỹ sư, PM hay lãnh đạo đối mặt khi triển khai, kèm lời giải đáp thực tế.

## 10. Prompts & Action Checklist
- **Action Checklist**: Bảng checklist 5 bước hành động ngay.
- **Reusable Prompt Block**: Prompt mẫu chất lượng cao đóng gói làm system prompt cho AI Agents.

---

# PART 2: FULL ENGLISH VERSION (TECHNICAL & PRODUCT REFERENCE)

## 1. Metadata & Quick Reference
- Standard metadata table & granular timestamp index (15–25 timestamps).

## 2. Executive Summary
- 5–6 high-level architectural & strategic takeaways.

## 3. System Architecture & Workflow Map (Dual-Mode Visualizer -en)
- Full English Dual-Mode Visualizer using `-en` suffix for all container IDs, tabs, and interactive handlers.

## 4. Core Terminology & Technical Taxonomy
- Comprehensive 8–12 term glossary defined with precision.

## 5. In-Depth Strategic & Technical Deep Dive
- Minimum 4–5 detailed H3 sections (`### 5.1` to `### 5.5`).

## 6. Implementation Frameworks & Step-by-Step Playbooks
- Minimum 2–3 actionable operational playbooks (`### Playbook 1` to `### Playbook 3`).

## 7. Contrarian Insights & Non-Obvious Truths
- 3–5 counter-intuitive paradigms with comparison tables.

## 8. Trade-off Matrix & Engineering Evaluation
- Detailed evaluation matrix analyzing trade-offs, hidden costs, and failure modes.

## 9. Pragmatic Engineering & Product Management Q&A
- 4–5 high-stakes technical dilemmas and solutions.

## 10. AI System Prompts & Execution Checklist
- Immediate action checklist + structured production prompt block for LLM agents.
```

---

## 4. Kiến Trúc HTML Song Ngữ Tương Tác (Bilingual Interactive Architecture)

Để đảm bảo tài liệu hiển thị mượt mà, chuyên nghiệp và không bị lỗi, toàn bộ file HTML BẮT BUỘC tuân thủ các quy chuẩn kỹ thuật sau:

### 1. Nút chuyển đổi ngôn ngữ trên Topbar

Nút chuyển đổi nằm cạnh công cụ theme trong `.topbar-actions`:

```html
<div class="lang-switcher" role="group" aria-label="Language selection">
  <button class="lang-btn active" id="btn-lang-vi" onclick="setLanguage('vi')" title="Chuyển sang Tiếng Việt" aria-pressed="true">🇻🇳 VI</button>
  <button class="lang-btn" id="btn-lang-en" onclick="setLanguage('en')" title="Switch to English" aria-pressed="false">🇬🇧 EN</button>
</div>
```

### 2. Quy tắc CSS hiển thị không giật lag, không trùng lặp

Áp dụng quy tắc kiểm soát hiển thị dựa trên thuộc tính `data-lang` tại thẻ `<html>`:

```css
/* Guaranteed Language Visibility: Vietnamese by default, English when data-lang='en' */
html:not([data-lang="en"]) .en-only { display: none !important; }
html:not([data-lang="en"]) .vi-only { display: revert !important; }
html[data-lang="en"] .vi-only { display: none !important; }
html[data-lang="en"] .en-only { display: revert !important; }
```

> **LƯU Ý QUAN TRỌNG**: Thẻ `<html>` phải luôn có sẵn thuộc tính `lang="vi" data-lang="vi"` ngay từ khi tải trang để tránh tình trạng flash hai thứ tiếng cùng lúc trước khi JavaScript khởi chạy.

### 3. Mục lục kép độc lập (Dual TOC)

Phần mục lục bên trái (`#toc-nav`) chứa 2 khối danh sách neo riêng biệt:

```html
<nav class="toc-nav" id="toc-nav">
  <div class="vi-only" id="toc-links-vi">
    <a href="#quick-reference" class="lvl-2">1. Metadata &amp; Quick Reference</a>
    <a href="#executive-summary" class="lvl-2">2. Executive Summary</a>
    <a href="#mental-model" class="lvl-2">3. Bản Đồ Tư Duy Hệ Thống</a>
    ...
  </div>
  <div class="en-only" id="toc-links-en">
    <a href="#quick-reference-en" class="lvl-2">1. Metadata &amp; Quick Reference</a>
    <a href="#executive-summary-en" class="lvl-2">2. Executive Summary</a>
    <a href="#mental-model-en" class="lvl-2">3. Systems Architecture Map</a>
    ...
  </div>
</nav>
```

> **LƯU Ý VỀ PARSING**: Các thuộc tính `aria-label` và `title` của nút TOC hoặc aside PHẢI là chuỗi thuần túy (ví dụ: `aria-label="Mục lục / Table of Contents"`), TUYỆT ĐỐI KHÔNG chứa thẻ `<span class="...">` bên trong attribute vì sẽ gây vỡ chuỗi đóng ngoặc kép HTML.

### 4. Dual-Mode Visualizer cho cả 2 Ngôn Ngữ

- Bản Tiếng Việt: Sử dụng các ID gốc `id="system-map-root"`, `tab-btn-bento`, `tab-btn-flow`, `view-bento`, `view-flow`.
- Bản Tiếng Anh: BẮT BUỘC thêm hậu tố `-en` cho mọi ID: `id="system-map-root-en"`, `tab-btn-bento-en`, `tab-btn-flow-en`, `view-bento-en`, `view-flow-en`, `flow-viewport-box-en`.

### 5. JavaScript Runtime An Toàn (Safe Runtime)

BẮT BUỘC tuân thủ các nguyên tắc lập trình JavaScript sau:
1. **Tránh trùng lặp biến**: Khai báo biến zoom theo dạng bảng phân nhóm:
   ```javascript
   let flowZoomLevels = { '': 1, '-en': 1 };
   ```
   Tuyệt đối không khai báo lại `let flowZoomLevel = 1;` nhiều lần vì sẽ gây lỗi `SyntaxError: Identifier 'flowZoomLevel' has already been declared`.
2. **Mermaid Rendering an toàn và đúng mục tiêu**:
   - Hàm `renderMermaid(forcedSuffix)` chỉ nhắm chính xác vào `#view-flow` hoặc `#view-flow-en`.
   - Lưu trữ mã nguồn Mermaid gốc trong `diagramSources = new Map()` trước khi chạy `mermaid.run()`.
3. **Phản hồi khi chuyển đổi ngôn ngữ**: Khi bấm chuyển sang ngôn ngữ khác, hàm `setLanguage(lang)` tự động kiểm tra xem tab sơ đồ Mermaid ở ngôn ngữ đó có đang mở hay không để kích hoạt `renderMermaid(suffix)` ngay lập tức.
4. **Ghi nhớ tùy chọn**: Sử dụng `localStorage.setItem("youtube-learner-lang", lang)` và tự động phục hồi khi `DOMContentLoaded`.

---

## 5. Quy Trình Auto-Chain Sang HTML Compiler

Sau khi hoàn tất nội dung Markdown song ngữ, chạy **1 lệnh duy nhất** để biên dịch ra HTML hoàn chỉnh (KHÔNG cần viết script build riêng cho từng video):

```bash
python3 "<SKILL_DIR>/scripts/build_bilingual_html.py" "<PATH_TO_MD>" \
  [--out <PATH_TO_HTML>] [--title-en "..."] [--subtitle-vi "..."] [--subtitle-en "..."] [--date YYYY-MM-DD]
```

Pipeline tự động (renderer `scripts/md_render.py`, zero-dependency):
1. Tách `# PHẦN 1` / `# PART 2` → body VI / body EN (phần boilerplate trước PHẦN 1 bị bỏ).
2. Render Markdown → HTML: bảng (`.table-wrap`), list lồng/task list, `> [!NOTE|TIP|IMPORTANT|WARNING|CAUTION]` → callout md2html, ```` ```mermaid ```` → `<figure class="diagram"><div class="mermaid">`, **raw HTML block được giữ nguyên** (dùng cho Bento Grid / Dual-Mode Visualizer).
3. Gắn ID cố định cho 10 mục chuẩn (`quick-reference`, `executive-summary`, `mental-model`, `terminology`, `deep-dive`, `playbooks`, `counter-intuitive`, `trade-offs`, `faqs`, `prompts-checklist`), bản EN tự thêm hậu tố `-en`.
4. Sinh Dual TOC (H2 + H3 thuộc mục 5 & 6).
5. Tiêu đề EN: `--title-en` → H1 đầu tiên trong PART 2 → dòng `Title`/`Tiêu đề` trong bảng metadata → tiêu đề VI. Ngày mặc định = hôm nay. Thời gian đọc tính theo số từ.
6. Validate sau build và in cảnh báo: thiếu PART 2, placeholder `{{...}}` còn sót, **ID trùng** (raw HTML bản EN quên hậu tố `-en`), thiếu `system-map-root`.

> **Quy ước Markdown để build đúng**: Part markers phải là H1 (`# PHẦN 1: ...`, `# PART 2: ...`). Mục chuẩn là H2 bắt đầu bằng số (`## 5. ...`). Dual-Mode Visualizer viết dưới dạng raw HTML trong mục 3 (bản EN dùng ID có hậu tố `-en`). Mermaid ngoài Visualizer vẫn được render cho ngôn ngữ đang hiển thị.

Hoặc dùng module Python khi cần tự kiểm soát HTML từng phần:

```python
from build_bilingual_html import prepare_bilingual_template, assemble_bilingual_document

# 1. Khởi tạo template với đầy đủ CSS/JS song ngữ
tpl = prepare_bilingual_template()

# 2. Đóng gói tài liệu hoàn chỉnh (date_str mặc định = hôm nay)
assemble_bilingual_document(
    template_html=tpl,
    title_vi=title_vi,
    title_en=title_en,
    subtitle_vi=subtitle_vi,
    subtitle_en=subtitle_en,
    source_file=source_file,
    toc_vi_html=toc_vi_html,
    toc_en_html=toc_en_html,
    body_vi_html=body_vi_html,
    body_en_html=body_en_html,
    out_path=out_html_path,
)
```

Test của compiler: `python3 -m unittest discover -s "<SKILL_DIR>/scripts" -p "test_*.py"`

---

## 6. Danh Mục Kiểm Tra Chất Lượng (Pre-Flight Audit Checklist)

Trước khi bàn giao tài liệu cho người dùng, hãy kiểm tra các tiêu chí sau:

- [ ] Tài liệu có đầy đủ **Part 1 (Bản Tiếng Việt)** và **Part 2 (Full English Reference)**?
- [ ] Cả 2 phần đều có đủ **10 Phân Hệ Chuyên Sâu** với độ dài từ 8.000 – 12.000 từ?
- [ ] Part 1 giữ nguyên 100% thuật ngữ chuyên ngành tiếng Anh (`career growth`, `talent bar`, `feedback`...)?
- [ ] Part 2 được viết bằng tiếng Anh kỹ thuật tự nhiên, chính xác, không dùng từ ngữ dịch máy gượng gạo?
- [ ] Mục 3 áp dụng **Dual-Mode Visualizer** cho cả hai ngôn ngữ (Bento Grid + Mermaid Flowchart)?
- [ ] Sơ đồ Mermaid tuân thủ chuẩn tỷ lệ 16:9, chia 4 phân miền màu pastel via `classDef`, có mini-cards 2 tầng?
- [ ] Nút chuyển đổi `🇻🇳 VI` ⇋ `🇬🇧 EN` hoạt động tức thì, không bị nhảy giao diện, không hiện trùng chữ?
- [ ] Mục lục (TOC) hiển thị đúng theo ngôn ngữ được chọn và neo đúng ID heading?
- [ ] Các công cụ Zoom (`＋`, `－`, `⟲`, `⛶`) hoạt động độc lập và trơn tru cho cả 2 ngôn ngữ?
- [ ] Dung lượng file HTML đạt chuẩn từ **130 KB – 170 KB**?
