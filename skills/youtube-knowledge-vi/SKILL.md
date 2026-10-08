---
name: youtube-knowledge-vi
description: >-
  Phiên bản THUẦN TIẾNG VIỆT. Dịch HẾT các thuật ngữ chuyên ngành sang tiếng Việt
  (career growth → thăng tiến sự nghiệp, talent bar → chuẩn nhân sự, feedback → phản hồi).
  Chỉ giữ nguyên thuật ngữ kỹ thuật cứng (API, Docker, Kubernetes...) và tên riêng.
  Kích hoạt khi người dùng cung cấp URL YouTube và muốn ghi chú kiến thức thuần Việt.
  Nếu cần giữ thuật ngữ chuyên ngành tiếng Anh, dùng skill youtube-knowledge-vi-en.
metadata:
  version: "1.0.1"
  keywords: [youtube, tiếng việt, vietnamese, pure, vi, transcript, ghi chú, markdown, knowledge]
---

# YouTube Knowledge Learner — Bản Thuần Tiếng Việt

Sử dụng skill này để biến một video YouTube thành kiến thức sẵn sàng dùng **hoàn toàn bằng tiếng Việt** — dịch tất cả các thuật ngữ chuyên ngành, chỉ giữ nguyên thuật ngữ kỹ thuật cứng và tên riêng:

1. Lấy transcript/phụ đề (ưu tiên tiếng Việt; nếu không có thì lấy tiếng Anh và DỊCH sang tiếng Việt).
2. Bảo toàn metadata gốc và các tham chiếu theo timestamp.
3. Chưng cất video thành một tài liệu tham khảo Markdown **tiếng Việt thuần** có thể tái sử dụng.
4. Áp dụng kiến thức học được vào tác vụ hiện tại của người dùng nếu có.

Mục tiêu không phải là bản tóm tắt chung chung. Đầu ra phải giúp một agent trong tương lai tái sử dụng nhanh chóng nội dung video làm ngữ cảnh đáng tin cậy mà không cần xem lại.

> Nếu muốn **giữ nguyên tất cả thuật ngữ chuyên ngành tiếng Anh** (career growth, talent bar, feedback, trade-off...), dùng skill **`youtube-knowledge-vi-en`** thay thế.

## Quy tắc ngôn ngữ — Bản THUẦN VIỆT (dịch hết thuật ngữ)

**Nguyên tắc cốt lõi:**

1. **DỊCH TẤT CẢ thuật ngữ chuyên ngành sang tiếng Việt**, bao gồm business, management, marketing, design. Đây là điểm khác biệt chính với skill `youtube-knowledge-vi-en`.

2. **CHỈ GIỮ NGUYÊN** những thứ sau bằng tiếng Anh:
   - Thuật ngữ kỹ thuật cứng không có bản dịch phổ biến: `API`, `framework`, `deploy`, `CI/CD`, `Docker`, `Kubernetes`, `machine learning`, `LLM`, `RAG`, `MCP`...
   - Tên riêng: tên người, công ty, sản phẩm, địa danh, công cụ, hàm/lệnh shell.
   - Quotes nguyên văn của diễn giả (kèm bản dịch tiếng Việt bên cạnh).

3. **Khi dịch thuật ngữ**, lần đầu xuất hiện dùng template `bản dịch tiếng Việt (english term)` để người đọc biết gốc tiếng Anh.
   - Ví dụ: `thăng tiến sự nghiệp (career growth)`, `chuẩn nhân sự (talent bar)`, `phản hồi (feedback)`.
   - Lần sau chỉ dùng bản dịch tiếng Việt.

### Bảng đối chiếu — PHẢI dịch sang tiếng Việt

| Tiếng Anh | Dịch thành tiếng Việt |
|---|---|
| career growth | thăng tiến sự nghiệp |
| fast pace | tốc độ nhanh / nhịp độ nhanh |
| talent bar | chuẩn nhân sự |
| brilliant jerk | thiên tài đểu |
| zone of genius | vùng thiên tài |
| feedback | phản hồi |
| team / leader | đội / lãnh đạo |
| scrappy / scrappiness | lì lợm / sự lì lợm |
| ecosystem | hệ sinh thái |
| feature | tính năng |
| customer / user | khách hàng / người dùng |
| short-term / long-term | ngắn hạn / dài hạn |
| imposter syndrome | hội chứng kẻ mạo danh |
| trade-off | đánh đổi |
| stakeholder | bên liên quan |
| cross-functional | đa chức năng |
| ladder / level | bậc / cấp |
| onboarding | đào tạo gia nhập |
| pipeline / funnel | đường ống / phễu |
| roadmap | lộ trình |
| sprint | lượt chạy nước rút |
| backlog | danh sách tồn đọng |
| retention | giữ chân (người dùng) |
| churn | rời bỏ (người dùng) |
| activation | kích hoạt |

### Self-check trước khi finalize

Trước khi coi ghi chú là hoàn chỉnh, đọc lại file `.md` và tự hỏi:

- [ ] Tất cả thuật ngữ business/management/marketing/design đã được dịch sang tiếng Việt?
- [ ] Lần đầu xuất hiện thuật ngữ dịch có kèm gốc tiếng Anh trong ngoặc?
- [ ] Chỉ giữ nguyên thuật ngữ kỹ thuật cứng (API, Docker, ML...) và tên riêng?
- [ ] Văn phong tổng thể: hoàn toàn bằng tiếng Việt, dễ đọc cho người Việt?

Nếu trả lời "không" cho bất kỳ checkbox nào → sửa trước khi hoàn tất.

## Đầu vào

Chấp nhận bất kỳ dạng nào sau đây:

- URL YouTube.
- File audio/video cục bộ.
- File transcript do người dùng cung cấp.
- URL YouTube kèm yêu cầu tác vụ, ví dụ "xem video này và triển khai cách tiếp cận đó".

Nếu người dùng đưa cả video và tác vụ, hãy tạo ghi chú tham khảo trước, sau đó dùng ghi chú đó làm ngữ cảnh cho tác vụ.

## Cách lấy transcript — thứ tự ưu tiên

### 1. Chạy helper script trực tiếp (tốt nhất — tự động hoàn toàn)

Skill này đi kèm script Python tại `scripts/fetch_youtube_knowledge.py`. Chạy script bằng `run_command`:

```bash
python3 "<SKILL_DIR>/scripts/fetch_youtube_knowledge.py" "<YOUTUBE_URL>" \
  --out "<OUTPUT_DIR>" \
  --lang vi \
  --cookies-from-browser chrome \
  --task "<mô tả tác vụ nếu có>"
```

Trong đó:
- `<SKILL_DIR>` = thư mục chứa skill này (Claude Code: `~/.claude/skills/youtube-knowledge-vi` hoặc `.claude/skills/youtube-knowledge-vi`; Claude.ai / Cowork: thư mục skill được mount cho phiên, hãy dùng đường dẫn thực tế của skill)
- **Khi chạy trong Claude.ai / Cowork** (không có cookie Chrome): dùng `--cookies-from-browser none`; nếu bị chặn thì nhờ người dùng dán transcript.
- `<OUTPUT_DIR>` = thư mục xuất, mặc định `knowledge/youtube` relative to project root
- `--cookies-from-browser chrome` = dùng cookies Chrome để auth (giảm rate-limit)
- `--task` = mô tả tác vụ, tuỳ chọn

Script có chiến lược chống rate-limit:

- Mặc định dùng `yt-dlp` với `--cookies-from-browser chrome` → request được auth bằng cookie YouTube của người dùng → quota cao hơn rất nhiều.
- Nếu `yt-dlp` vẫn fail (vd: 429 hoặc bot challenge), tự fallback sang `youtube-transcript-api` (endpoint khác, không chia sẻ rate-limit window).
- Khi cả hai fail vì rate-limit, script trả về error rõ ràng.

Script ưu tiên phụ đề tiếng Việt trước (`vi`), nếu không có thì tự fallback sang `en`. Kết quả trả về là JSON gồm `note`, `transcript`, `title`, `source`, `language`, `segments`, `path_used`. Sau đó:

1. Đọc file `transcript` từ đĩa.
2. **Nếu `language` không phải `vi`**, dịch nội dung transcript sang tiếng Việt khi viết ghi chú (dịch HẾT thuật ngữ sang tiếng Việt).
3. Viết ghi chú thực sự đè lên scaffold tại đường dẫn `note`.

### Quy tắc xử lý lỗi — RẤT QUAN TRỌNG

- Nếu error chứa `RATE-LIMITED` hoặc `HTTP 429`: **KHÔNG CHẠY LẠI script**. Báo cho người dùng: YouTube đang rate-limit IP, đợi 30-60 phút rồi thử lại. Nhắc người dùng đảm bảo đã đăng nhập YouTube trên Chrome. Việc retry liên tục chỉ kéo dài thời gian rate-limit.
- Nếu error đề cập `yt-dlp is not installed`: hướng dẫn người dùng cài (`brew install yt-dlp` trên macOS, `pip install --user yt-dlp` cross-platform).
- Nếu error đề cập `youtube-transcript-api chưa được cài`: hướng dẫn cài (`pip install --user youtube-transcript-api`). Đây là fallback nên không bắt buộc, nhưng có sẽ giúp tránh fail toàn bộ.
- Nếu error đề cập cookies (vd: keyring locked, browser not found): có thể thử lại với `--cookies-from-browser none` hoặc browser khác.

### 2. Clipboard + Terminal (giải pháp cuối cùng)

Chỉ dùng khi script không chạy được (vd: sandbox chặn network). Ghi lệnh script ra chat và bảo người dùng chạy trong Terminal. Chờ họ paste kết quả JSON vào chat.

## Cấu trúc đầu ra chuẩn mực — TIÊU CHUẨN VÀNG (Molly Graham Benchmark)

> **QUY TẮC BẮT BUỘC**: Mọi bản tóm tắt tạo bởi skill này PHẢI áp dụng **Tiêu Chuẩn Vàng (Gold Standard Benchmark)** tương đương bản tham chiếu mẫu Molly Graham. Không được phép tạo bản tóm tắt sơ sài, chung chung hoặc chỉ có H2 phẳng.

Mỗi tài liệu Markdown PHẢI có cấu trúc tối thiểu **10 Phân Hệ Chuyên Sâu** với độ dài từ **8.000 – 12.000 từ** (khoảng 35–45 KB Markdown), bao gồm:

```markdown
# <Tiêu đề video — dịch sang tiếng Việt nếu video tiếng Anh>

Nguồn: <URL hoặc đường dẫn file>
Kênh/tác giả: <tên nếu biết>
Ngày ghi nhận: <YYYY-MM-DD>
Nguồn transcript: <phụ đề chính thức | phụ đề tự động | bản chép cục bộ | do người dùng cung cấp>
Ngôn ngữ gốc: <vi | en | ...>
Ngữ cảnh tác vụ: <điều người dùng muốn làm với video, hoặc "chỉ tham khảo">

## 1. Metadata & Quick Reference
- **Bảng Metadata**: Tiêu đề, Kênh/Host, Khách mời (Kèm tiểu sử chi tiết, sự nghiệp, vai trò), Thời lượng, URL, Lĩnh vực, Đối tượng mục tiêu.
- **Quick Index (Timestamp Navigation)**: Mục lục timestamp chi tiết từ đầu đến cuối video (tối thiểu 15-25 mốc thời gian kèm tóm tắt chủ đề).

## 2. Tóm Tắt Điều Hành (Executive Summary)
- Tối thiểu 5–6 luận điểm vĩ mô cốt tử, phân tích sâu về bối cảnh, số liệu, tâm lý học tổ chức và kết luận thực tiễn.

## 3. Bản Đồ Tư Duy Hệ Thống (Dual-Mode Visualizer BẮT BUỘC)
- BẮT BUỘC áp dụng cấu trúc **Dual-Mode Visualizer** theo chuẩn [references/system-map-template.md](references/system-map-template.md):
  * **Tab 1: ✨ Bản Đồ Trực Quan (Executive Bento Grid)** — 3–4 thẻ kiến trúc Bento (step pill 1-4, badge, flow steps với biểu tượng trực quan, highlight bar nguyên tắc sống còn). Giúp nắm bắt 100% bản chất hệ thống trong 30 giây không cần cuộn chuột dài.
  * **Tab 2: 🔍 Sơ Đồ Kỹ Thuật (Technical Mermaid Flowchart LR Pipeline)** — Sơ đồ Mermaid `flowchart LR` chuẩn tỷ lệ 16:9, chia 3–4 phân miền màu pastel qua `classDef`, node mini-card 2 tầng (Biểu tượng + Tiêu đề đậm + Chú thích nhỏ), vòng lặp phản hồi nét đứt `-.->`, kèm thanh công cụ phóng to/thu nhỏ/toàn màn hình tương tác.

## 4. Thuật Ngữ Cốt Lõi
- Bảng từ điển thuật ngữ gồm 8–12 thuật ngữ chuyên môn, dịch nghĩa thuần Việt và kèm thuật ngữ gốc tiếng Anh trong ngoặc ở lần đầu.

## 5. Phân Tích Chuyên Sâu (Deep Dive Analysis)
- BẮT BUỘC chẻ nhỏ thành **tối thiểu 4–5 tiểu mục H3 riêng biệt** (`### 5.1`, `### 5.2`, `### 5.3`, `### 5.4`, `### 5.5`).
- Mỗi tiểu mục là một bài phân tích chuyên sâu về cơ chế, nguyên lý nền tảng, case study thực tế, và trích dẫn trực tiếp của diễn giả.

## 6. Khung Hành Động & Cẩm Nang (Frameworks & Playbooks)
- BẮT BUỘC đóng gói thành **tối thiểu 2–3 Playbooks thực thi từng bước** (`### Cẩm nang 1: ...`, `### Cẩm nang 2: ...`, `### Cẩm nang 3: ...`).
- Mỗi Playbook có bảng các bước tuần tự (Bước 1, Bước 2, Bước 3...), kịch bản thực hiện, và template mẫu.

## 7. Góc Nhìn Ngược Số Đông (Contrarian Perspectives)
- Liệt kê 3–5 góc nhìn phản trực giác, đi ngược lại các quan niệm thông thường của số đông trong ngành, kèm bảng so sánh "Quan niệm phổ biến" vs "Sự thật thực chiến".

## 8. Ma Trận So Sánh & Đánh Đổi (Trade-offs & Comparison Matrix)
- Các bảng so sánh đa chiều: Phân tích ưu/nhược điểm, chi phí ẩn, rủi ro và giải pháp giảm thiểu cho từng lựa chọn kỹ thuật hoặc chiến lược.

## 9. Giải Đáp Thắc Mắc (Q&A Thực Chiến)
- 4–5 câu hỏi tiến thoái lưỡng nan hóc búa nhất mà kỹ sư, PM, hay lãnh đạo sẽ gặp phải khi áp dụng kiến thức trong video, kèm lời giải đáp thực tế.

## 10. Gợi Ý Lệnh Prompt & Danh Mục Hành Động (Prompts & Action Checklist)
- **Action Checklist**: Bảng checklist 5 bước hành động ngay.
- **Reusable Prompt Block**: Prompt mẫu chất lượng cao trong block code để các AI agents tương lai sử dụng làm system prompt.
```

## Quy trình học

1. Xác định mục tiêu của người dùng:
   - Chỉ cần ghi chú tham khảo.
   - Áp dụng video vào tác vụ code/design/research.
   - Cần cả transcript và ghi chú kiến thức.
2. Lấy transcript và metadata (xem mục "Cách lấy transcript" ở trên).
3. Phân đoạn transcript theo timestamp và sự chuyển chủ đề.
4. Trích kiến thức có giá trị lâu dài:
   - Định nghĩa và thuật ngữ (**dịch sang tiếng Việt**, kèm gốc EN lần đầu).
   - Tuyên bố và bằng chứng.
   - Quy trình, lệnh, công thức, code pattern, cấu hình.
   - Ràng buộc, prerequisite, cảnh báo, failure mode.
   - Ví dụ và edge case.
5. Viết ghi chú Markdown tham khảo **hoàn toàn bằng tiếng Việt**.
6. Sử dụng ghi chú để thực hiện tác vụ nếu người dùng yêu cầu.
7. Báo cáo đường dẫn file `.md` đã tạo, kèm các điểm còn bỏ ngỏ.

## Tiêu chuẩn chất lượng

Ghi chú hoàn chỉnh khi một agent tương lai có thể trả lời:

- Video đã dạy điều gì?
- Tôi nên làm theo những bước nào?
- Những giả định và cảnh báo nào quan trọng?
- Mỗi điểm quan trọng xuất hiện ở đâu trong video (timestamp)?
- Kiến thức này ảnh hưởng tới tác vụ của người dùng như thế nào?

Sử dụng trích dẫn timestamp cho các luận điểm quan trọng khi có thể. Nếu transcript không có timestamp, hãy nêu rõ trong ghi chú.

## Áp dụng kiến thức

Khi người dùng có tác vụ tiếp theo, coi ghi chú như một tài liệu nguồn:

- Đọc các phần liên quan trước khi sửa code hoặc lập kế hoạch.
- Trích dẫn đường dẫn ghi chú và các điểm timestamp khi cần.
- Ưu tiên quy trình cụ thể từ video hơn là tóm tắt chung chung.
- Nếu lời khuyên của video xung đột với convention của repo, hãy theo repo trừ khi người dùng yêu cầu rõ làm theo video.

## Xử lý lỗi

Nếu không lấy được phụ đề:

- Kiểm tra `yt-dlp` đã được cài và URL có truy cập được không.
- Thử ngôn ngữ phụ đề khác (vi → en → bất kỳ).
- Chỉ hỏi người dùng cung cấp transcript khi đã thử mọi cách tự động.
- Nếu video không có phụ đề và không có tool transcription, tạo một ghi chú ngắn ghi nhận URL, các lệnh đã thử, công cụ thiếu, và bước input tiếp theo cần thiết — **vẫn bằng tiếng Việt**.

Nếu transcript dài:

- Làm việc theo chunk.
- Duy trì bản đồ chủ đề kèm timestamp.
- Tổng hợp sau khi đọc xong tất cả chunk để ghi chú phản ánh toàn bộ video, không chỉ phần đầu.

Nếu video bằng tiếng nước ngoài (không phải tiếng Việt):

- Luôn dịch nội dung tóm tắt và phân tích sang tiếng Việt (dịch hết thuật ngữ).
- Có thể giữ một vài trích dẫn nguyên văn ngắn kèm bản dịch khi điều đó hữu ích.

## Phụ thuộc

### Bắt buộc

```bash
# yt-dlp — lấy phụ đề chính
brew install yt-dlp                  # macOS
# hoặc
pip install --user yt-dlp            # cross-platform

# Chrome — đăng nhập YouTube trên Chrome
#    Script sẽ tự đọc cookies từ Chrome → request được auth.
```

### Khuyến nghị (cho fallback robust)

```bash
# Fallback khi yt-dlp fail
pip install --user youtube-transcript-api
```

## Khi vẫn bị rate-limit

Nếu bạn vẫn gặp `⚠️ RATE-LIMITED`:

1. **Kiểm tra** đã đăng nhập YouTube trên Chrome chưa.
2. **Đợi 30-60 phút** — đừng retry liên tục, sẽ kéo dài thêm.
3. **Cài** `youtube-transcript-api` để có fallback độc lập.
4. Nếu Chrome bị macOS khoá keychain để yt-dlp đọc cookies, mở Keychain Access và cho phép một lần.

## Tự Động Biên Dịch HTML (Auto-chain HTML Compiler)

Sau khi viết xong file `.md`, **tự động biên dịch sang HTML** bằng script đi kèm trong skill:

```bash
python3 "<SKILL_DIR>/scripts/build_html.py" "<NOTE_PATH>" --lang vi
```

Script này tự động:
1. **Phân tích Markdown & tạo cấu trúc**: Đọc nội dung Markdown, chuẩn hóa heading anchor IDs và tự động sinh Mục lục (TOC) thông minh.
2. **Áp dụng Design System chuẩn md2html**: Giao diện cao cấp, hỗ trợ Light/Dark mode, Print/PDF, Responsive trên mobile/tablet/desktop.
3. **Kích hoạt Flow Viewer tương tác**: Hỗ trợ phóng to (`＋`), thu nhỏ (`－`), đặt lại (`⟲`), toàn màn hình (`⛶`) và kéo thả (pan) cho sơ đồ Mermaid dòng chảy.
4. **Output file**: Tạo file `.html` cùng tên ngay cạnh file `.md` (dung lượng từ 70 KB – 100 KB).
5. **Mở file trong browser**: `open <file>.html` (trên macOS) để người dùng xem ngay.

## Cấu trúc đầu ra

```
knowledge/youtube/<slug>.md                # Ghi chú Markdown tiếng Việt thuần
knowledge/youtube/<slug>.html              # HTML self-contained (auto-generated bởi build_html.py)
knowledge/youtube/<slug>.transcript.txt    # Transcript thô (tiếng gốc)
```

## Khác biệt với các skill YouTube khác

| Skill | Mục đích | Ngôn ngữ | HTML output |
|---|---|---|---|
| `youtube-knowledge-vi` (skill này) | Ghi chú kiến thức tham khảo | Tiếng Việt thuần (dịch hết thuật ngữ) | ✅ Tự động compile (`build_html.py`) |
| `youtube-knowledge-vi-en` | Ghi chú kiến thức tham khảo | Song ngữ (Part 1 VI + EN giữ nguyên, Part 2 EN) | ✅ Tự động compile song ngữ tương tác |
| `youtube-knowledge-en` | Ghi chú kỹ thuật tham khảo | Tiếng Anh thuần (Full English Technical Reference) | ✅ Tự động compile (`build_html.py`) |
| `youtube-learn` | Khai quật worldview (Belief Archaeology) | Tiếng Anh | ❌ |

