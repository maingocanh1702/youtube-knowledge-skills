---
name: youtube-knowledge-learner-vi-en
description: >-
  Biến video YouTube thành ghi chú Markdown TRỘN tiếng Việt + tiếng Anh. Giữ NGUYÊN tất cả thuật ngữ chuyên
  ngành tiếng Anh (career growth, talent bar, feedback, trade-off, ecosystem...), chỉ dịch nội dung chính sang
  tiếng Việt. Kích hoạt khi người dùng cung cấp URL YouTube và muốn "học video YouTube bản vi-en", tóm tắt /
  dịch / tạo ghi chú từ video bằng tiếng Việt. Skill độc lập: tự lấy transcript bằng script đi kèm (yt-dlp +
  fallback), không cần MCP server. Đầu ra Markdown trộn VN+EN, tự động chain sang HTML bằng script đi kèm
  scripts/md2html.py. Đây là bản gọn một ngôn ngữ trộn Việt + Anh; nếu cần bản song ngữ 2 phần có nút chuyển
  ngôn ngữ thì dùng skill youtube-knowledge-vi-en.
metadata:
  version: "1.0.0"
---

# YouTube Knowledge Learner — Bản Trộn Việt + Anh (vi-en, standalone)

Skill này biến một video YouTube thành kiến thức sẵn sàng dùng **bằng tiếng Việt trộn các cụm tiếng Anh chuyên ngành**:

1. Lấy transcript/phụ đề bằng **script đi kèm trong skill** (ưu tiên tiếng Việt; nếu không có thì lấy tiếng Anh và DỊCH sang tiếng Việt).
2. Bảo toàn metadata gốc và các tham chiếu theo timestamp.
3. Chưng cất video thành một tài liệu tham khảo Markdown **tiếng Việt** có thể tái sử dụng.
4. **TỰ ĐỘNG** chuyển file Markdown sang HTML bằng script đi kèm `scripts/md2html.py` (không cần skill md2html riêng).
5. Áp dụng kiến thức học được vào tác vụ hiện tại của người dùng nếu có.

Mục tiêu không phải bản tóm tắt chung chung. Đầu ra phải giúp một agent trong tương lai tái sử dụng nhanh chóng nội dung video làm ngữ cảnh đáng tin cậy mà không cần xem lại.

## Quy tắc ngôn ngữ — Bản TRỘN VN+EN (NGHIÊM NGẶT giữ thuật ngữ)

**Nguyên tắc cốt lõi:**

1. **GIỮ NGUYÊN TẤT CẢ thuật ngữ chuyên ngành tiếng Anh.** Không dịch sang tiếng Việt, kể cả khi có bản dịch quen thuộc. Cụ thể:
   - Thuật ngữ kỹ thuật cứng: `API`, `framework`, `deploy`, `CI/CD`, `Docker`, `Kubernetes`, `machine learning`, `embedding`, `transformer`, `prompt`, `LLM`, `context window`, `token`, `fine-tuning`, `agent`, `MCP`, `RAG`...
   - Thuật ngữ business / startup / management: `career growth`, `fast pace`, `talent bar`, `zone of genius`, `kind vs nice`, `brilliant jerk`, `clock speed`, `personal SLA`, `T-shaped leadership`, `cross-functional`, `OKR`, `KPI`, `MVP`, `PRD`, `roadmap`, `backlog`, `sprint`, `retro`, `stand-up`, `imposter syndrome`, `growth hack`, `ecosystem`, `feedback`, `team`, `leader`, `stakeholder`, `pipeline`, `funnel`...
   - Thuật ngữ marketing / GTM: `product-led`, `sales-led`, `bottom-up`, `top-down`, `PLG`, `ICP`, `pricing`, `unit economics`, `TAM`, `SAM`, `SOM`, `churn`, `retention`, `activation`, `acquisition`...
   - Thuật ngữ design / UX: `UX`, `UI`, `accessibility`, `design system`, `loonshots framework`, `council practice`, `psychological safety`...
   - Tên riêng: tên người, công ty, sản phẩm, địa danh, công cụ, hàm/lệnh shell.
   - Quotes nguyên văn của diễn giả.

2. **CHỈ DỊCH NỘI DUNG CHÍNH** sang tiếng Việt: cấu trúc câu, từ nối ("và", "nhưng", "vì vậy"), mô tả tổng quát, narrative, ngữ cảnh, lời giải thích chung. Tiêu đề các phần lớn có thể dịch sang tiếng Việt nếu chúng là cụm tổng quát (vd "Tóm Tắt Điều Hành"), nhưng giữ nguyên nếu chứa thuật ngữ ngành ("Career growth playbook", "Fast pace inside a big company").

3. **Khi không chắc** một từ tiếng Việt có phải bản dịch của thuật ngữ chuyên ngành tiếng Anh hay không, **mặc định dùng template**: `english term (nghĩa tiếng việt)`.
   - Ví dụ: `latency (độ trễ)`, `throughput (thông lượng)`, `cohort (nhóm người dùng theo thời điểm)`, `bottleneck (điểm nghẽn)`, `pivot (xoay trục chiến lược)`.
   - Lần đầu xuất hiện trong document thì dùng template. Lần sau có thể chỉ giữ tiếng Anh.

4. **TUYỆT ĐỐI KHÔNG** tự dịch các cụm như: "career growth → thăng tiến sự nghiệp", "fast pace → tốc độ nhanh", "talent bar → chuẩn nhân sự", "brilliant jerk → thiên tài đểu", "zone of genius → vùng thiên tài", "feedback → phản hồi", "team → đội", "leader → lãnh đạo", "scrappy → lì lợm", "ecosystem → hệ sinh thái", "imposter syndrome → hội chứng kẻ mạo danh", "trade-off → đánh đổi"... Đây là **lỗi** ở phiên bản này. Người dùng dùng bản vi-en chính vì muốn đọc bằng các thuật ngữ tiếng Anh gốc.

### Bảng đối chiếu — PHẢI giữ nguyên tiếng Anh

| Tiếng Anh (giữ nguyên) | KHÔNG dịch thành |
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
| feature | ~~tính năng~~ |
| customer / user | ~~khách hàng / người dùng~~ |
| short-term / long-term | ~~ngắn hạn / dài hạn~~ |
| imposter syndrome | ~~hội chứng kẻ mạo danh~~ |
| trade-off | ~~đánh đổi~~ |
| stakeholder | ~~bên liên quan~~ |
| cross-functional | ~~đa chức năng~~ |
| ladder / level | ~~bậc / cấp~~ |
| onboarding | ~~đào tạo gia nhập~~ |
| pipeline / funnel | ~~đường ống / phễu~~ |

### Self-check trước khi finalize

Trước khi chain sang `md2html`, đọc lại file `.md` và tự hỏi:

- [ ] Tất cả thuật ngữ chuyên ngành tiếng Anh được giữ nguyên?
- [ ] Không có cụm nào trong bảng "KHÔNG dịch thành" xuất hiện ở dạng tiếng Việt?
- [ ] Các thuật ngữ ít phổ biến đã được giải thích bằng template `english (nghĩa VN)` ở lần xuất hiện đầu tiên?
- [ ] Văn phong tổng thể: tiếng Việt làm khung, thuật ngữ tiếng Anh nguyên gốc bên trong?

Nếu trả lời "không" cho bất kỳ checkbox nào → sửa trước khi chain sang md2html.

## Đầu vào

Chấp nhận bất kỳ dạng nào sau đây:

- URL YouTube.
- File audio/video cục bộ.
- File transcript do người dùng cung cấp.
- URL YouTube kèm yêu cầu tác vụ, ví dụ "xem video này và triển khai cách tiếp cận đó".

Nếu người dùng đưa cả video và tác vụ, hãy tạo ghi chú tham khảo trước, sau đó dùng ghi chú đó làm ngữ cảnh cho tác vụ.

## Cách lấy transcript — thứ tự ưu tiên

### 1. Script đi kèm `scripts/fetch_youtube_knowledge.py` (mặc định)

Skill này đóng gói sẵn một script Python tự lo việc lấy transcript với chiến lược chống rate-limit. **Chạy script này trước** mỗi khi người dùng đưa URL YouTube — không cần MCP server, không cần clipboard, không cần thao tác bàn phím từ người dùng.

Script nằm trong thư mục của skill này, tại `scripts/fetch_youtube_knowledge.py`. Chạy bằng bash với đường dẫn tuyệt đối tới script (thay `<SKILL_DIR>` bằng thư mục chứa SKILL.md này):

```bash
python3 "<SKILL_DIR>/scripts/fetch_youtube_knowledge.py" "<URL>" \
  --out "<đường dẫn tuyệt đối tới knowledge/youtube/ trong project>" \
  --lang vi \
  --cookies-from-browser chrome
```

> **Khi chạy trong Claude.ai / Cowork** (sandbox không có trình duyệt nên không có cookie Chrome): đổi thành `--cookies-from-browser none`. Nếu YouTube vẫn chặn, script tự fallback sang `youtube-transcript-api`; nếu thất bại nữa, nhờ người dùng dán transcript rồi làm tiếp từ bước viết ghi chú. Trên Claude Code, `<SKILL_DIR>` thường là `~/.claude/skills/youtube-knowledge-learner-vi-en`.

Tham số:

| Tham số | Mặc định | Mô tả |
|---|---|---|
| `url` (positional) | — | URL YouTube |
| `--out` | `knowledge/youtube` | Thư mục xuất transcript + scaffold ghi chú |
| `--lang` | `vi` | Ngôn ngữ phụ đề ưu tiên (tự fallback sang `vi` → `en` → bất kỳ) |
| `--task` | `""` | Ngữ cảnh tác vụ, ghi vào scaffold ghi chú |
| `--cookies-from-browser` | `chrome` | `chrome \| safari \| firefox \| edge \| brave \| none` |
| `--no-fallback` | off | Bỏ qua fallback `youtube-transcript-api` |

Chiến lược chống rate-limit của script:

- Mặc định dùng `yt-dlp` với `--cookies-from-browser chrome` → request được auth bằng cookie YouTube của người dùng → quota cao hơn rất nhiều.
- Nếu `yt-dlp` vẫn fail (vd 429 hoặc bot challenge), tự fallback sang `youtube-transcript-api` (endpoint khác, không chia sẻ rate-limit window).
- Khi cả hai fail vì rate-limit, script in error rõ ràng với prefix `⚠️ RATE-LIMITED`.

Script ưu tiên phụ đề tiếng Việt (`vi`), nếu không có thì fallback sang `en`. Nó ghi xuống đĩa:

```
<out_dir>/<slug>.transcript.txt   # transcript thô (tiếng gốc)
<out_dir>/<slug>.md               # scaffold ghi chú để Claude điền tiếp
```

và in JSON gồm `note`, `transcript`, `title`, `source`, `language`, `path_used`. Sau đó:

1. Đọc file `transcript` từ đĩa.
2. **Nếu `language` không phải `vi`**, dịch nội dung sang tiếng Việt khi viết ghi chú (giữ thuật ngữ chuyên ngành tiếng Anh theo quy tắc ở trên).
3. Viết ghi chú thực sự đè lên scaffold tại đường dẫn `note`.

> **Lưu ý môi trường:** script gọi mạng tới YouTube. Trong Claude Code CLI hoặc môi trường có quyền mạng đầy đủ, nó chạy tốt. Trong một số sandbox bị proxy chặn `youtube.com`, script có thể fail — khi đó dùng cách 2 bên dưới.

### Quy tắc xử lý lỗi — RẤT QUAN TRỌNG

- Nếu output chứa `⚠️ RATE-LIMITED` hoặc `HTTP 429`: **KHÔNG CHẠY LẠI ngay**. Báo cho người dùng: YouTube đang rate-limit IP, đợi 30-60 phút rồi thử lại, và đảm bảo đã đăng nhập YouTube trên Chrome. Retry liên tục chỉ kéo dài thời gian rate-limit.
- Nếu error đề cập `yt-dlp is not installed`: hướng dẫn cài (`brew install yt-dlp` trên macOS, `pip install --user yt-dlp` cross-platform).
- Nếu error đề cập `youtube-transcript-api chưa được cài`: hướng dẫn cài (`pip install --user youtube-transcript-api`). Đây là fallback nên không bắt buộc, nhưng có sẽ giúp tránh fail toàn bộ.
- Nếu error đề cập cookies (vd keyring locked, browser not found): thử lại với `--cookies-from-browser none` hoặc một browser khác.

### 2. Người dùng tự cung cấp transcript

Nếu không lấy được tự động (sandbox chặn mạng, video không có phụ đề, rate-limit kéo dài), hãy nhờ người dùng cung cấp transcript hoặc đường dẫn file transcript, rồi xử lý từ đó. Vẫn áp dụng đầy đủ quy tắc ngôn ngữ vi-en và cấu trúc ghi chú bên dưới.

## Đầu ra mặc định

Tạo một file Markdown dưới thư mục có nghĩa trong project, thường là:

```text
knowledge/youtube/<slug>.md
```

Nếu project đã có thư mục `docs`, `notes`, `research`, hoặc `knowledge`, hãy theo quy ước đó.

Sử dụng cấu trúc Markdown như sau (**bằng tiếng Việt**, giữ thuật ngữ tiếng Anh):

```markdown
# <Tiêu đề video — có thể giữ nguyên gốc hoặc dịch nếu video tiếng Anh>

Nguồn: <URL hoặc đường dẫn file>
Kênh/tác giả: <tên nếu biết>
Ngày ghi nhận: <YYYY-MM-DD>
Nguồn transcript: <phụ đề chính thức | phụ đề tự động | bản chép cục bộ | do người dùng cung cấp>
Ngôn ngữ gốc: <vi | en | ...>
Ngữ cảnh tác vụ: <điều người dùng muốn làm với video, hoặc "chỉ tham khảo">

## Tóm Tắt Điều Hành
<5-10 gạch đầu dòng với các luận điểm chính và kết luận thực tế của video.>

## Khái Niệm Cốt Lõi
<Giải thích từng khái niệm, bảo toàn định nghĩa, giả định và ràng buộc.>

## Quy Trình Và Cách Thực Hiện
<Phương pháp từng bước được dạy trong video. Bao gồm timestamp khi có.>

## Quyết Định, Đánh Đổi Và Cảnh Báo
<Việc cần làm, việc cần tránh, khi nào lời khuyên thay đổi, giới hạn, lưu ý.>

## Ghi Chú Liên Quan Tới Tác Vụ
<Chỉ thêm phần này nếu người dùng có giao tác vụ cụ thể. Giải thích cách áp dụng kiến thức vào tác vụ đó.>

## Chỉ Mục Timestamp
- <00:00> <chủ đề>
- <03:12> <chủ đề>

## Ngữ Cảnh Prompt Tái Sử Dụng
<Một khối ngắn gọn mà agent tương lai có thể dán vào prompt để tái sử dụng kiến thức này.>

## Câu Hỏi Còn Bỏ Ngỏ
<Những điểm chưa rõ, thiếu, hoặc không thể xác minh.>
```

Không dán toàn bộ transcript có bản quyền vào câu trả lời cuối. Với file project cục bộ, chỉ lưu transcript thô khi cần thiết hoặc khi người dùng yêu cầu rõ. Ghi chú tham khảo nên chủ yếu là tổng hợp diễn giải bằng tiếng Việt, kèm trích đoạn timestamp ngắn khi thực sự cần.

## Bước cuối — TỰ ĐỘNG chain sang HTML bằng `scripts/md2html.py`

Skill này **đóng gói sẵn** bộ chuyển đổi `scripts/md2html.py` (template "Notes": TOC sticky + scroll-spy, dark-mode toggle, scroll progress, callout, mermaid, collapsible, in/PDF). KHÔNG phụ thuộc một skill `md2html` riêng và KHÔNG cần mạng để convert (chỉ font + mermaid tải từ CDN khi mở file).

Sau khi đã ghi xong nội dung tổng hợp vào file `.md` (KHÔNG còn placeholder `TODO:` nào), **luôn chạy** (thay `<SKILL_DIR>` bằng thư mục chứa SKILL.md này):

```bash
python3 "<SKILL_DIR>/scripts/md2html.py" "<đường dẫn tuyệt đối tới file .md>" \
  --eyebrow "NOTES · vi-en" \
  --subtitle "<một câu tóm tắt ngắn, tùy chọn>"
```

- Mặc định file `.html` được ghi **cạnh** file `.md` (cùng slug, đổi `.md` → `.html`); truyền `--out` để đổi đích.
- Script tự: tách H1 đầu làm tiêu đề; biến khối "Key: value" ngay sau H1 thành hộp "Thông tin nguồn"; sinh TOC từ H2/H3; ước lượng read-time.
- Báo cáo cho người dùng cả hai đường dẫn (`.md` và `.html`).

**Để output giàu component giống template gốc, hãy dùng các cú pháp sau NGAY TRONG file `.md`:**

- Callout / admonition — blockquote mở đầu bằng `[!TYPE] Tiêu đề` (TYPE ∈ `INFO|NOTE|WARN|DANGER|TIP|SUCCESS|DECISION`):

  ```markdown
  > [!WARN] Cảnh báo quan trọng
  > Nội dung cảnh báo ở đây.
  ```

- Sơ đồ — fenced code khối ` ```mermaid `:

  ```markdown
  ```mermaid
  flowchart LR
    A[Present] --> B[Withdraw] --> C[Reappear] --> A
  ```
  ```

- Bảng Markdown bình thường (tự được bọc `.table-wrap` để scroll ngang).

> Nếu skill `md2html` ngoài cũng có mặt, có thể dùng thay; nhưng mặc định ưu tiên script đi kèm để chain luôn chạy được. Nếu thiếu thư viện `markdown`, script in hướng dẫn cài: `python3 -m pip install --user --break-system-packages markdown`.

## Quy trình học

1. Xác định mục tiêu của người dùng: chỉ cần ghi chú tham khảo / áp dụng video vào tác vụ code-design-research / cần cả transcript và ghi chú.
2. Lấy transcript và metadata (xem mục "Cách lấy transcript" ở trên).
3. Phân đoạn transcript theo timestamp và sự chuyển chủ đề.
4. Trích kiến thức có giá trị lâu dài: định nghĩa và thuật ngữ (giữ thuật ngữ kỹ thuật bằng tiếng Anh); tuyên bố và bằng chứng; quy trình, lệnh, công thức, code pattern, cấu hình; ràng buộc, prerequisite, cảnh báo, failure mode; ví dụ và edge case.
5. Viết ghi chú Markdown tham khảo **bằng tiếng Việt** (trộn thuật ngữ EN).
6. **TỰ ĐỘNG** chạy `scripts/md2html.py` để sinh file `.html` cạnh file `.md`.
7. Sử dụng ghi chú để thực hiện tác vụ nếu người dùng yêu cầu.
8. Báo cáo đường dẫn file đã tạo, kèm các điểm còn bỏ ngỏ.

## Tiêu chuẩn chất lượng

Ghi chú hoàn chỉnh khi một agent tương lai có thể trả lời: video đã dạy điều gì; nên làm theo những bước nào; những giả định và cảnh báo nào quan trọng; mỗi điểm quan trọng xuất hiện ở đâu trong video (timestamp); kiến thức này ảnh hưởng tới tác vụ của người dùng như thế nào. Dùng trích dẫn timestamp cho các luận điểm quan trọng khi có thể; nếu transcript không có timestamp, nêu rõ trong ghi chú.

## Áp dụng kiến thức

Khi người dùng có tác vụ tiếp theo, coi ghi chú như một tài liệu nguồn: đọc các phần liên quan trước khi sửa code hoặc lập kế hoạch; trích dẫn đường dẫn ghi chú và các điểm timestamp khi cần; ưu tiên quy trình cụ thể từ video hơn tóm tắt chung chung. Nếu lời khuyên của video xung đột với convention của repo, hãy theo repo trừ khi người dùng yêu cầu rõ làm theo video.

## Xử lý lỗi

Nếu không lấy được phụ đề: kiểm tra `yt-dlp` đã cài và URL có truy cập được không; thử ngôn ngữ phụ đề khác (vi → en → bất kỳ); chỉ hỏi người dùng cung cấp transcript khi đã thử mọi cách tự động. Nếu video không có phụ đề và không có tool transcription, tạo một ghi chú ngắn ghi nhận URL, các lệnh đã thử, công cụ thiếu, và bước input tiếp theo cần thiết — **vẫn bằng tiếng Việt**.

Nếu transcript dài: làm việc theo chunk; duy trì bản đồ chủ đề kèm timestamp; tổng hợp sau khi đọc xong tất cả chunk để ghi chú phản ánh toàn bộ video.

Nếu video bằng tiếng nước ngoài (không phải tiếng Việt): luôn dịch nội dung tóm tắt và phân tích sang tiếng Việt; có thể giữ vài trích dẫn nguyên văn ngắn kèm bản dịch khi hữu ích.

## Nguồn gốc

Tách ra thành skill độc lập từ plugin `youtube-knowledge-learner-vi-en` (v0.6.0) của Ngoc-Anh. Bản gốc tiếng Anh: https://github.com/longmaba/youtube-knowledge-learner
