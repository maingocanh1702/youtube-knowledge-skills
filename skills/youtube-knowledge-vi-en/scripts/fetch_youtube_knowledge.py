#!/usr/bin/env python3
"""Lấy phụ đề YouTube — chống rate-limit, tạo scaffold ghi chú TIẾNG VIỆT.

Chiến lược chống 429 (Too Many Requests):

1. Đường dẫn chính: yt-dlp + --cookies-from-browser <browser>
   - Request được auth bằng cookie YouTube → quota cao hơn rất nhiều.
   - Kết hợp --sleep-requests, --retries, --extractor-retries để retry nhẹ nhàng.
   - --extractor-args "youtube:player_client=android,web" để dùng client có quota khác.

2. Fallback: youtube-transcript-api (pip install youtube-transcript-api)
   - Dùng endpoint khác với yt-dlp → không chia sẻ rate-limit window.
   - Chỉ lấy được transcript; metadata (title, channel) lấy qua HTML scrape nhẹ.

3. Báo lỗi rõ ràng khi cả hai đều fail → để caller (agent) không tự retry.

Ưu tiên phụ đề tiếng Việt (vi), fallback sang en, rồi bất kỳ ngôn ngữ nào.

Ported from Claude plugin youtube-knowledge-learner-vi-en v0.6.0
Adapted for Gemini skills (standalone script, no MCP).
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Helpers chung
# ---------------------------------------------------------------------------

YOUTUBE_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/live/|youtube\.com/embed/|youtube\.com/v/)([A-Za-z0-9_-]{11})"
)


def extract_video_id(url: str) -> str | None:
    m = YOUTUBE_ID_RE.search(url)
    return m.group(1) if m else None


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def merge_repeated(rows: list[tuple[str | None, str]]) -> list[tuple[str | None, str]]:
    merged: list[tuple[str | None, str]] = []
    previous = ""
    for timestamp, text in rows:
        if text == previous:
            continue
        merged.append((timestamp, text))
        previous = text
    return merged


def seconds_to_timestamp(seconds: float) -> str:
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, seconds_only = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds_only:02d}"
    return f"{minutes:02d}:{seconds_only:02d}"


def ms_to_timestamp(value: Any) -> str | None:
    if value is None:
        return None
    return seconds_to_timestamp(int(value) / 1000)


def slugify(value: str) -> str:
    import unicodedata

    nfkd = unicodedata.normalize("NFKD", value)
    ascii_only = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_only = ascii_only.replace("đ", "d").replace("Đ", "D")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only.lower()).strip("-")
    return slug[:80] or "youtube-video"


def is_rate_limit_error(stderr: str) -> bool:
    s = stderr.lower()
    return any(token in s for token in (
        "http error 429",
        "too many requests",
        "rate-limit",
        "ratelimit",
        "sign in to confirm you're not a bot",
    ))


# ---------------------------------------------------------------------------
# Đường dẫn 1: yt-dlp (chính)
# ---------------------------------------------------------------------------

class RateLimitedError(RuntimeError):
    """yt-dlp/YouTube trả về 429 hoặc bot challenge."""


def run_yt_dlp_json(
    url: str,
    cookies_browser: str | None = None,
    sleep_requests: float = 1.0,
    retries: int = 5,
    extractor_retries: int = 3,
) -> dict[str, Any]:
    if not shutil.which("yt-dlp"):
        raise RuntimeError("yt-dlp is not installed or is not on PATH")

    cmd: list[str] = [
        "yt-dlp",
        "--dump-single-json",
        "--skip-download",
        "--sleep-requests", str(sleep_requests),
        "--retries", str(retries),
        "--extractor-retries", str(extractor_retries),
        "--extractor-args", "youtube:player_client=android,web",
    ]
    if cookies_browser and cookies_browser.lower() != "none":
        cmd += ["--cookies-from-browser", cookies_browser]
    cmd.append(url)

    result = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        err = result.stderr.strip() or "yt-dlp failed"
        if is_rate_limit_error(err):
            raise RateLimitedError(err)
        raise RuntimeError(err)
    return json.loads(result.stdout)


def choose_caption(
    info: dict[str, Any], lang_prefixes: list[str]
) -> tuple[str, dict[str, Any], str]:
    subtitles = info.get("subtitles") or {}
    automatic = info.get("automatic_captions") or {}

    for lang_prefix in lang_prefixes:
        for source_name, group in (
            ("phụ đề chính thức", subtitles),
            ("phụ đề tự động", automatic),
        ):
            for lang, entries in group.items():
                if not lang.lower().startswith(lang_prefix.lower()):
                    continue
                preferred = sorted(
                    entries,
                    key=lambda item: 0 if item.get("ext") in {"vtt", "json3", "srv3", "srt"} else 1,
                )
                if preferred:
                    return lang, preferred[0], source_name

    for source_name, group in (
        ("phụ đề chính thức", subtitles),
        ("phụ đề tự động", automatic),
    ):
        for lang, entries in group.items():
            preferred = sorted(
                entries,
                key=lambda item: 0 if item.get("ext") in {"vtt", "json3", "srv3", "srt"} else 1,
            )
            if preferred:
                return lang, preferred[0], source_name

    available = sorted(set(subtitles.keys()) | set(automatic.keys()))
    raise RuntimeError(
        f"Không tìm thấy phụ đề cho các tiền tố ngôn ngữ {lang_prefixes!r}. "
        f"Ngôn ngữ có sẵn: {', '.join(available) if available else 'không có'}"
    )


def fetch_caption_text(caption: dict[str, Any]) -> str:
    url = caption.get("url")
    if not url:
        raise RuntimeError("Selected caption has no URL")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return raw.decode("utf-8", errors="replace")


def parse_caption(raw: str, ext: str) -> list[tuple[str | None, str]]:
    ext = (ext or "").lower()
    if ext == "json3":
        return parse_json3(raw)
    return parse_timed_text(raw)


def parse_json3(raw: str) -> list[tuple[str | None, str]]:
    data = json.loads(raw)
    rows: list[tuple[str | None, str]] = []
    for event in data.get("events", []):
        parts = event.get("segs") or []
        text = "".join(part.get("utf8", "") for part in parts)
        text = normalize_text(text)
        if not text:
            continue
        timestamp = ms_to_timestamp(event.get("tStartMs"))
        rows.append((timestamp, text))
    return merge_repeated(rows)


def parse_timed_text(raw: str) -> list[tuple[str | None, str]]:
    rows: list[tuple[str | None, str]] = []
    current_time: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines, current_time
        text = normalize_text(" ".join(current_lines))
        if text:
            rows.append((current_time, text))
        current_lines = []

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "WEBVTT" or stripped.startswith(("Kind:", "Language:", "NOTE")):
            flush()
            continue
        if "-->" in stripped:
            flush()
            current_time = stripped.split("-->", 1)[0].strip().replace(",", ".")
            continue
        if re.match(r"^\d+$", stripped):
            continue
        current_lines.append(stripped)
    flush()
    return merge_repeated(rows)


# ---------------------------------------------------------------------------
# Đường dẫn 2: youtube-transcript-api (fallback)
# ---------------------------------------------------------------------------


def _get_transcript_list(video_id: str):
    """Tương thích cả API v0.x (classmethod list_transcripts) lẫn v1.x (instance method list).

    youtube-transcript-api v1.0 đã đổi từ classmethod sang instance method và
    rename list_transcripts → list. Hàm này detect và gọi đúng API.
    """
    from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore

    # v1.x: instance.list(video_id)
    if hasattr(YouTubeTranscriptApi, "list") and not hasattr(YouTubeTranscriptApi, "list_transcripts"):
        return YouTubeTranscriptApi().list(video_id)

    # v0.x: classmethod list_transcripts(video_id)
    if hasattr(YouTubeTranscriptApi, "list_transcripts"):
        return YouTubeTranscriptApi.list_transcripts(video_id)

    # Trường hợp hiếm: cả hai cùng có (chuyển tiếp). Ưu tiên instance.
    return YouTubeTranscriptApi().list(video_id)


def fetch_via_transcript_api(
    video_id: str, lang_prefixes: list[str]
) -> tuple[list[tuple[str | None, str]], str, str]:
    """Trả về (rows, language_code, source_name)."""
    try:
        import youtube_transcript_api  # type: ignore  # noqa: F401
    except ImportError as e:
        raise RuntimeError(
            "youtube-transcript-api chưa được cài (fallback không khả dụng). "
            "Cài bằng: python3 -m pip install --user --break-system-packages youtube-transcript-api"
        ) from e

    # Errors có thể nằm ở module gốc hoặc _errors tuỳ version
    try:
        from youtube_transcript_api import (  # type: ignore
            TranscriptsDisabled,
            NoTranscriptFound,
        )
    except ImportError:
        try:
            from youtube_transcript_api._errors import (  # type: ignore
                TranscriptsDisabled,
                NoTranscriptFound,
            )
        except ImportError:
            TranscriptsDisabled = NoTranscriptFound = Exception  # type: ignore

    try:
        transcripts = _get_transcript_list(video_id)
    except TranscriptsDisabled as e:
        raise RuntimeError(f"Video {video_id} đã tắt phụ đề (transcripts disabled).") from e
    except NoTranscriptFound as e:
        raise RuntimeError(f"Video {video_id} không có phụ đề.") from e
    except Exception as e:
        raise RuntimeError(f"youtube-transcript-api lỗi: {e}") from e

    # Thử theo ưu tiên ngôn ngữ
    selected = None
    for lang in lang_prefixes:
        try:
            selected = transcripts.find_transcript([lang])
            break
        except Exception:
            continue

    if selected is None:
        # Bất kỳ ngôn ngữ nào
        try:
            for t in transcripts:
                selected = t
                break
        except Exception:
            pass

    if selected is None:
        raise RuntimeError("youtube-transcript-api: không có transcript phù hợp.")

    try:
        fetched = selected.fetch()
    except Exception as e:
        raise RuntimeError(f"Không tải được transcript qua youtube-transcript-api: {e}") from e

    # v0.x: fetched là list[dict]; v1.x: fetched là FetchedTranscript (iterable of snippets)
    rows: list[tuple[str | None, str]] = []
    iterable = fetched if hasattr(fetched, "__iter__") else getattr(fetched, "snippets", [])
    for item in iterable:
        if isinstance(item, dict):
            text = item.get("text", "")
            start = item.get("start", 0)
        else:
            text = getattr(item, "text", "")
            start = getattr(item, "start", 0)
        text = normalize_text(text)
        if not text:
            continue
        rows.append((seconds_to_timestamp(start), text))

    rows = merge_repeated(rows)
    if not rows:
        raise RuntimeError("youtube-transcript-api: transcript rỗng sau khi xử lý.")

    source = "phụ đề tự động" if getattr(selected, "is_generated", False) else "phụ đề chính thức"
    language_code = getattr(selected, "language_code", "unknown")
    return rows, language_code, f"{source} (youtube-transcript-api)"


def fetch_metadata_via_html(video_id: str) -> dict[str, Any]:
    """Lấy title + channel từ HTML watch page. Không cần auth."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            ),
            "Accept-Language": "vi,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            html_text = response.read().decode("utf-8", errors="replace")
    except Exception:
        return {"id": video_id, "webpage_url": url, "title": None, "uploader": None}

    title = None
    m = re.search(r'<meta\s+name="title"\s+content="([^"]+)"', html_text)
    if m:
        title = html.unescape(m.group(1))
    if not title:
        m = re.search(r"<title>(.*?)</title>", html_text, re.DOTALL)
        if m:
            title = html.unescape(m.group(1)).replace(" - YouTube", "").strip()

    uploader = None
    m = re.search(r'"ownerChannelName":"([^"]+)"', html_text)
    if m:
        uploader = html.unescape(m.group(1))
    if not uploader:
        m = re.search(r'"author":"([^"]+)"', html_text)
        if m:
            uploader = html.unescape(m.group(1))

    return {
        "id": video_id,
        "webpage_url": url,
        "title": title,
        "uploader": uploader,
    }


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------

def write_transcript(path: Path, rows: list[tuple[str | None, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for timestamp, text in rows:
            if timestamp:
                handle.write(f"[{timestamp}] {text}\n")
            else:
                handle.write(f"{text}\n")


def write_note(
    path: Path,
    transcript_path: Path,
    info: dict[str, Any],
    transcript_source: str,
    language: str,
    task: str,
) -> None:
    title = info.get("title") or "Video YouTube"
    source = info.get("webpage_url") or info.get("original_url") or ""
    channel = info.get("uploader") or info.get("channel") or "Không rõ"
    captured = dt.date.today().isoformat()

    translate_note = ""
    if not language.lower().startswith("vi"):
        translate_note = (
            f"> **Lưu ý dịch**: Transcript gốc bằng `{language}`. "
            f"Khi hoàn thiện Part 1, hãy diễn giải sang tiếng Việt kết hợp giữ nguyên 100% thuật ngữ chuyên ngành tiếng Anh "
            f"(API, framework, career growth, talent bar, clock speed, trade-off...).\n"
        )

    content = f"""# {title}

> **Kiến trúc Song Ngữ (Bilingual Standard v2.0)**: Tài liệu được cấu trúc thành 2 phần độc lập theo Tiêu Chuẩn Vàng (Molly Graham Benchmark):
> - **Phần 1 (Bản Tiếng Việt + Thuật Ngữ EN)**: Giữ nguyên toàn bộ thuật ngữ chuyên ngành tiếng Anh (`career growth`, `talent bar`, `feedback`, `trade-off`, `clock speed`...), phân tích chuyên sâu đa chiều bằng tiếng Việt.
> - **Part 2 (Full English Technical Reference)**: Bản tiếng Anh chuẩn kỹ thuật toàn diện, phục vụ tra cứu quốc tế và làm ngữ cảnh cho AI Agents.
{translate_note}
---

# PHẦN 1: BẢN TIẾNG VIỆT (GIỮ THUẬT NGỮ CHUYÊN NGÀNH TIẾNG ANH)

## 1. Metadata & Quick Reference
- **Nguồn**: {source}
- **Kênh / Host**: {channel}
- **Khách mời**: TODO (Bio chi tiết, vai trò, thành tựu, background)
- **Thời lượng**: TODO
- **Nguồn transcript**: {transcript_source} ({language})
- **File transcript**: `{transcript_path.as_posix()}`
- **Ngữ cảnh tác vụ**: {task or "Chỉ tham khảo"}
- **Chỉ Mục Timestamp (Quick Navigation)**:
  - TODO: Liệt kê tối thiểu 15–20 mốc thời gian kèm tóm tắt chủ đề chi tiết.

## 2. Executive Summary
- TODO: 5–6 luận điểm vĩ mô cốt tử, phân tích sâu về bối cảnh, số liệu, tâm lý học tổ chức và kết luận thực tiễn.

## 3. Bản Đồ Tư Duy Hệ Thống (Dual-Mode Visualizer BẮT BUỘC)
- BẮT BUỘC thiết kế theo chuẩn `references/system-map-template.md`:
  * **Tab 1: ✨ Executive Bento Grid** — 3–4 thẻ kiến trúc Bento (step-pill 1-4, badge, highlight bar axiom vàng).
  * **Tab 2: 🔍 Technical Mermaid Flowchart LR Pipeline** — Sơ đồ Mermaid `flowchart LR` chuẩn tỷ lệ 16:9, chia 3–4 phân miền pastel via `classDef`, node mini-card 2 tầng, feedback loop nét đứt.

## 4. Thuật Ngữ Cốt Lõi
- TODO: Bảng từ điển 8–12 thuật ngữ chuyên môn tiếng Anh xuất hiện trong video, kèm giải thích ngữ nghĩa, bối cảnh thực tế và cách ứng dụng.

## 5. Phân Tích Chuyên Sâu (Deep Dive)
### 5.1 TODO
### 5.2 TODO
### 5.3 TODO
### 5.4 TODO
### 5.5 TODO

## 6. Frameworks & Playbooks Thực Chiến
### Playbook 1: TODO
### Playbook 2: TODO
### Playbook 3: TODO

## 7. Góc Nhìn Ngược Số Đông (Contrarian Perspectives)
- TODO: 3–5 góc nhìn phản trực giác, bảng so sánh "Quan niệm phổ biến" vs "Sự thật thực chiến".

## 8. Ma Trận So Sánh & Đánh Đổi (Trade-offs & Comparison Matrix)
- TODO: Bảng phân tích đa chiều về ưu/nhược điểm, chi phí ẩn, rủi ro và giải pháp giảm thiểu cho từng lựa chọn kỹ thuật hoặc chiến lược.

## 9. Giải Đáp Thắc Mắc Thực Chiến (Q&A Scenarios)
- TODO: 4–5 câu hỏi tình huống hóc búa nhất mà kỹ sư, PM hay lãnh đạo đối mặt khi triển khai.

## 10. Prompts & Action Checklist
- **Action Checklist**: Bảng checklist 5 bước hành động ngay.
- **Reusable Prompt Block**: Prompt mẫu chất lượng cao đóng gói làm system prompt cho AI Agents.

---

# PART 2: FULL ENGLISH VERSION (TECHNICAL & PRODUCT REFERENCE)

## 1. Metadata & Quick Reference
- **Source**: {source}
- **Channel / Host**: {channel}
- **Guest**: TODO (Detailed bio, background, role, key achievements)
- **Transcript Source**: {transcript_source} ({language})
- **Timestamp Navigation**:
  - TODO: Comprehensive timestamp breakdown (15-20 timestamps with descriptive summaries).

## 2. Executive Summary
- TODO: 5-6 core architectural & strategic takeaways with deep context and actionable conclusions.

## 3. System Architecture & Workflow Map (Dual-Mode Visualizer)
- Complete English version of the Dual-Mode Visualizer using `-en` suffix for all container IDs and handlers:
  * **Tab 1: ✨ Executive Bento Grid** — High-level architecture cards, step pills, and core axioms.
  * **Tab 2: 🔍 Technical Mermaid Flowchart LR Pipeline** — Rigorous `flowchart LR` diagram with 4 pastel subgraphs and interactive zoom controls.

## 4. Core Terminology & Technical Taxonomy
- TODO: 8-12 foundational technical terms defined with operational definitions and industry significance.

## 5. In-Depth Strategic & Technical Deep Dive
### 5.1 TODO
### 5.2 TODO
### 5.3 TODO
### 5.4 TODO
### 5.5 TODO

## 6. Implementation Frameworks & Step-by-Step Playbooks
### Playbook 1: TODO
### Playbook 2: TODO
### Playbook 3: TODO

## 7. Contrarian Insights & Non-Obvious Truths
- TODO: 3-5 counter-intuitive paradigms with comparison table ("Conventional Wisdom" vs "Battle-Tested Reality").

## 8. Trade-off Matrix & Engineering Evaluation
- TODO: Multi-dimensional decision matrix analyzing trade-offs, hidden costs, failure modes, and mitigation tactics.

## 9. Pragmatic Engineering & Product Management Q&A
- TODO: 4-5 high-stakes dilemmas and practical solutions for real-world scenarios.

## 10. AI System Prompts & Execution Checklist
- **Action Checklist**: 5-step concrete execution checklist.
- **Production Prompt Block**: Structured, copy-pasteable system prompt block for LLM agents.
"""
    path.write_text(content, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("--out", default="knowledge/youtube", help="Thư mục xuất")
    parser.add_argument("--lang", default="vi", help="Tiền tố ngôn ngữ ưu tiên (mặc định: vi)")
    parser.add_argument("--task", default="", help="Ngữ cảnh tác vụ, ghi vào note")
    parser.add_argument(
        "--cookies-from-browser",
        default="chrome",
        help="Browser để lấy cookies YouTube (chrome|safari|firefox|edge|none). Mặc định: chrome.",
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Không fallback sang youtube-transcript-api khi yt-dlp fail.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    preferred_langs = [args.lang]
    for fallback in ("vi", "en"):
        if fallback not in preferred_langs:
            preferred_langs.append(fallback)

    info: dict[str, Any] | None = None
    rows: list[tuple[str | None, str]] | None = None
    language: str | None = None
    transcript_source: str | None = None
    yt_dlp_err: str | None = None

    # === Đường 1: yt-dlp với cookies + hardening ===
    try:
        info = run_yt_dlp_json(args.url, cookies_browser=args.cookies_from_browser)
        language, caption, transcript_source = choose_caption(info, preferred_langs)
        raw = fetch_caption_text(caption)
        rows = parse_caption(raw, caption.get("ext", ""))
        if not rows:
            raise RuntimeError("Phụ đề rỗng sau khi parse")
    except RateLimitedError as e:
        yt_dlp_err = f"Rate-limited: {e}"
        rows = None
    except Exception as e:
        yt_dlp_err = str(e)
        rows = None

    # === Đường 2 (fallback): youtube-transcript-api ===
    if rows is None and not args.no_fallback:
        video_id = extract_video_id(args.url)
        if not video_id:
            raise SystemExit(
                f"yt-dlp fail ({yt_dlp_err}) và không trích xuất được video ID từ URL để fallback."
            )
        try:
            rows, language, transcript_source = fetch_via_transcript_api(
                video_id, preferred_langs
            )
            if info is None:
                info = fetch_metadata_via_html(video_id)
        except Exception as fallback_err:
            err_msg = (
                f"Cả yt-dlp và youtube-transcript-api đều fail.\n"
                f"--- yt-dlp ---\n{yt_dlp_err}\n"
                f"--- fallback ---\n{fallback_err}\n"
            )
            if yt_dlp_err and "Rate-limited" in yt_dlp_err:
                err_msg += (
                    "\nLỜI KHUYÊN: YouTube đang rate-limit IP của bạn. "
                    "Đợi 30-60 phút rồi thử lại. KHÔNG retry liên tục — điều đó "
                    "kéo dài thời gian rate-limit. Đảm bảo Chrome đã đăng nhập YouTube "
                    "để tận dụng quota cao hơn."
                )
            raise SystemExit(err_msg)

    if rows is None:
        raise SystemExit(f"Không lấy được transcript: {yt_dlp_err}")

    base = slugify(
        (info or {}).get("title")
        or (info or {}).get("id")
        or extract_video_id(args.url)
        or "youtube-video"
    )
    transcript_path = out_dir / f"{base}.transcript.txt"
    note_path = out_dir / f"{base}.md"

    write_transcript(transcript_path, rows)
    write_note(
        note_path,
        transcript_path,
        info or {"webpage_url": args.url},
        transcript_source or "không rõ",
        language or "không rõ",
        args.task,
    )

    print(json.dumps({
        "note": str(note_path),
        "transcript": str(transcript_path),
        "title": (info or {}).get("title"),
        "source": transcript_source,
        "language": language,
        "segments": len(rows),
        "path_used": "yt-dlp" if yt_dlp_err is None else "youtube-transcript-api",
        "yt_dlp_error": yt_dlp_err,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
