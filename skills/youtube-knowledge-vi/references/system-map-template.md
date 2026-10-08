# Dual-Mode System Map Template — Tiêu Chuẩn Trực Quan Hóa Hệ Thống Cho YouTube Learner

Tài liệu này định nghĩa cấu trúc chuẩn bắt buộc cho **Mục 3. Bản Đồ Tư Duy Hệ Thống** trong mọi bản tóm tắt và file HTML được tạo bởi skill `youtube-knowledge-vi`.

---

## 1. Triết Lý Thiết Kế: Dual-Mode Architecture

Mục 3 không được phép chỉ dùng một sơ đồ phẳng hoặc Mermaid đơn độc. BẮT BUỘC sử dụng cấu trúc **Dual-Mode Visualizer** với Segmented Control Tab Switcher:

1. **Tab 1 (Mặc định): ✨ Bản Đồ Trực Quan (Executive Bento Grid)**
   - Mục đích: Giúp người đọc/lãnh đạo nắm bắt 100% bản chất hệ thống trong **30 giây** mà không cần cuộn chuột dài.
   - Thiết kế: 3–4 thẻ kiến trúc Bento với viền màu nổi bật (`border-top: 3px solid ...`), huy hiệu `step-pill` (1, 2, 3, 4), `badge` phân loại, các bước `flow-steps` kèm biểu tượng trực quan, và thanh `bento-highlight-bar` đúc kết châm ngôn / nguyên lý cốt lõi.

2. **Tab 2: 🔍 Sơ Đồ Kỹ Thuật (Technical Flowchart LR Pipeline)**
   - Mục đích: Cho phép kỹ sư, PM và kiến trúc sư phân tích chi tiết các quan hệ nhân quả, luồng dữ liệu và điều kiện tuần tự.
   - Thiết kế: Sơ đồ Mermaid **`flowchart LR`** (Left-to-Right) chuẩn tỷ lệ 16:9, chia 3–4 phân miền rõ ràng (Blue / Amber / Purple / Emerald) thông qua `classDef`. Node thiết kế mini-card hai tầng (Biểu tượng + Tiêu đề đậm + Chú thích nhỏ).
   - Thanh công cụ điều khiển tương tác: Phóng to (`＋`), Thu nhỏ (`－`), Đặt lại kích thước (`⟲`), và Toàn màn hình (`⛶`).

---

## 2. Template HTML Hoàn Chỉnh Cho Mục 3

Copy và điền nội dung vào khung HTML chuẩn dưới đây khi build file HTML:

```html
<h2 id="mental-model">3. Bản Đồ Tư Duy Hệ Thống</h2>

<p>Hệ thống dưới đây biểu diễn kiến trúc vận hành toàn diện của <strong>{{SYSTEM_NAME}}</strong>. Bạn có thể chuyển đổi linh hoạt giữa <strong>Bản đồ trực quan (Bento Grid)</strong> để nắm bắt bản chất hoặc <strong>Sơ đồ kỹ thuật (Mermaid Flowchart)</strong> để theo dõi luồng quan hệ phối hợp chi tiết:</p>

<div class="system-map-container" id="system-map-root">
  <div class="system-map-header">
    <div class="system-map-meta">
      <span class="system-map-badge">
        <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" style="width:14px;height:14px;"><use href="#i-check"/></svg>
        HỆ THỐNG KIẾN TRÚC TOÀN CẢNH
      </span>
      <h3 class="system-map-title">{{SYSTEM_TITLE}}</h3>
    </div>
    <div class="segmented-control" role="tablist" aria-label="Chế độ xem sơ đồ">
      <button class="seg-btn active" id="tab-btn-bento" role="tab" aria-selected="true" aria-controls="view-bento" onclick="switchSystemView('bento')">
        <svg class="seg-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>
        <span>Bản Đồ Trực Quan (Bento)</span>
        <span class="badge-rec">Đề xuất</span>
      </button>
      <button class="seg-btn" id="tab-btn-flow" role="tab" aria-selected="false" aria-controls="view-flow" onclick="switchSystemView('flow')">
        <svg class="seg-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M6 9v3a3 3 0 0 0 3 3h6"/></svg>
        <span>Sơ Đồ Kỹ Thuật (Mermaid)</span>
      </button>
    </div>
  </div>

  <!-- VIEW 1: BENTO GRID ARCHITECTURE (EXECUTIVE VIEW) -->
  <div class="system-map-view active" id="view-bento" role="tabpanel" aria-labelledby="tab-btn-bento">
    <div class="bento-grid">
      
      <!-- CARD 1: BLUE THEME - SPECTRUM / HIERARCHY / SWEET SPOT -->
      <div class="bento-card" style="border-top: 3px solid #2563EB;">
        <div class="bento-card-header">
          <h4 class="bento-card-title">
            <span class="bento-step-pill" style="background: #EFF6FF; color: #2563EB; border-color: #BFDBFE;">1</span>
            {{CARD_1_TITLE}}
          </h4>
          <span class="bento-card-badge">{{CARD_1_BADGE}}</span>
        </div>
        <p style="font-size: 12.5px; color: var(--text-muted); margin: 0; line-height: 1.45;">
          <strong>Bản chất cốt lõi:</strong> {{CARD_1_SUMMARY}}
        </p>
        <div class="spectrum-wrap">
          <div class="spectrum-bar">
            <div class="spectrum-slot slot-danger">
              <span class="slot-title">❌ {{SLOT_1_TITLE}}</span>
              <span class="slot-desc">{{SLOT_1_DESC}}</span>
            </div>
            <div class="spectrum-slot slot-sweet">
              <span class="slot-title">🎯 {{SLOT_2_TITLE}}</span>
              <span class="slot-desc"><strong>Điểm ngọt:</strong> {{SLOT_2_DESC}}</span>
            </div>
            <div class="spectrum-slot slot-danger">
              <span class="slot-title">❌ {{SLOT_3_TITLE}}</span>
              <span class="slot-desc">{{SLOT_3_DESC}}</span>
            </div>
          </div>
        </div>
        <div class="bento-highlight-bar" style="border-left-color: #2563EB;">
          <strong>Nguyên tắc sống còn:</strong> <em>"{{CARD_1_AXIOM}}"</em>
        </div>
      </div>

      <!-- CARD 2: AMBER THEME - SPLIT-PANE CONTRAST BOX -->
      <div class="bento-card" style="border-top: 3px solid #D97706;">
        <div class="bento-card-header">
          <h4 class="bento-card-title">
            <span class="bento-step-pill" style="background: #FFFBEB; color: #D97706; border-color: #FDE68A;">2</span>
            {{CARD_2_TITLE}}
          </h4>
          <span class="bento-card-badge" style="background: #FFFBEB; color: #D97706; border-color: #FDE68A;">{{CARD_2_BADGE}}</span>
        </div>
        <div class="contrast-box">
          <div class="contrast-pane" style="background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 10px;">
            <span class="pane-label" style="font-weight: 700; color: #B45309; font-size: 11.5px;">{{PANE_LEFT_LABEL}}</span>
            <p class="pane-desc" style="font-size: 11.5px; margin: 4px 0 0; color: var(--text-muted); line-height: 1.35;">{{PANE_LEFT_DESC}}</p>
          </div>
          <div class="contrast-pane" style="background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 10px;">
            <span class="pane-label" style="font-weight: 700; color: #2563EB; font-size: 11.5px;">{{PANE_RIGHT_LABEL}}</span>
            <p class="pane-desc" style="font-size: 11.5px; margin: 4px 0 0; color: var(--text-muted); line-height: 1.35;">{{PANE_RIGHT_DESC}}</p>
          </div>
        </div>
        <div class="bento-highlight-bar" style="border-left-color: #D97706;">
          <strong>Nguyên tắc sống còn:</strong> <em>"{{CARD_2_AXIOM}}"</em>
        </div>
      </div>

      <!-- CARD 3: PURPLE / VIOLET THEME - EVOLUTION & CULTURE PILLS -->
      <div class="bento-card" style="border-top: 3px solid #7C3AED;">
        <div class="bento-card-header">
          <h4 class="bento-card-title">
            <span class="bento-step-pill" style="background: #F5F3FF; color: #7C3AED; border-color: #DDD6FE;">3</span>
            {{CARD_3_TITLE}}
          </h4>
          <span class="bento-card-badge" style="background: #F5F3FF; color: #7C3AED; border-color: #DDD6FE;">{{CARD_3_BADGE}}</span>
        </div>
        <div class="spectrum-wrap">
          <div class="spectrum-bar">
            <div class="spectrum-slot" style="background: var(--warn-soft); border: 1px solid var(--warn-border);">
              <span class="slot-title" style="color: var(--warn);">{{EVO_1_TITLE}}</span>
              <span class="slot-desc">{{EVO_1_DESC}}</span>
            </div>
            <div class="spectrum-slot slot-sweet">
              <span class="slot-title">{{EVO_2_TITLE}}</span>
              <span class="slot-desc"><strong>Trọng tâm:</strong> {{EVO_2_DESC}}</span>
            </div>
            <div class="spectrum-slot" style="background: var(--decision-soft); border: 1px solid var(--decision-border);">
              <span class="slot-title" style="color: var(--decision);">{{EVO_3_TITLE}}</span>
              <span class="slot-desc">{{EVO_3_DESC}}</span>
            </div>
          </div>
        </div>
        <div class="culture-pills">
          <span class="culture-pill">🎯 <strong>{{PILL_1_LABEL}}:</strong> {{PILL_1_DESC}}</span>
          <span class="culture-pill">⚡ <strong>{{PILL_2_LABEL}}:</strong> {{PILL_2_DESC}}</span>
        </div>
      </div>

      <!-- CARD 4: EMERALD THEME - ACTION / VALUE FLOW -->
      <div class="bento-card" style="border-top: 3px solid #059669;">
        <div class="bento-card-header">
          <h4 class="bento-card-title">
            <span class="bento-step-pill" style="background: #ECFDF5; color: #059669; border-color: #A7F3D0;">4</span>
            {{CARD_4_TITLE}}
          </h4>
          <span class="bento-card-badge" style="background: #ECFDF5; color: #059669; border-color: #A7F3D0;">{{CARD_4_BADGE}}</span>
        </div>
        <div class="flow-steps">
          <div class="flow-step-item">
            <span class="flow-icon">💎</span>
            <div class="flow-text">
              <h5>{{STEP_4_1_TITLE}}</h5>
              <p>{{STEP_4_1_DESC}}</p>
            </div>
          </div>
          <div class="flow-step-item">
            <span class="flow-icon">🚀</span>
            <div class="flow-text">
              <h5>{{STEP_4_2_TITLE}}</h5>
              <p>{{STEP_4_2_DESC}}</p>
            </div>
          </div>
        </div>
        <div class="bento-highlight-bar" style="border-left-color: #059669;">
          <strong>Nguyên tắc sống còn:</strong> <em>"{{CARD_4_AXIOM}}"</em>
        </div>
      </div>

    </div>
  </div>

  <!-- VIEW 2: DETAILED MERMAID FLOWCHART (TECHNICAL VIEW) -->
  <div class="system-map-view" id="view-flow" role="tabpanel" aria-labelledby="tab-btn-flow">
    <div class="flow-toolbar">
      <div class="flow-toolbar-left">
        <svg class="icon" viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><use href="#i-info"/></svg>
        <span>Sơ đồ dòng chảy Dagre: Biểu diễn quan hệ nhân quả và chuyển dịch mô hình</span>
      </div>
      <div class="flow-tools">
        <button class="flow-tool-btn" type="button" title="Phóng to (+)" onclick="zoomFlow(0.15)">＋</button>
        <button class="flow-tool-btn" type="button" title="Thu nhỏ (-)" onclick="zoomFlow(-0.15)">－</button>
        <button class="flow-tool-btn" type="button" title="Đặt lại kích thước" onclick="resetFlowZoom()">⟲</button>
        <button class="flow-tool-btn" type="button" title="Bật/Tắt toàn màn hình" onclick="toggleFlowFullscreen()">⛶</button>
      </div>
    </div>

    <div class="flow-viewport" id="flow-viewport-box">
      <div class="mermaid">
flowchart LR
    %% CLASS DEFINITIONS (Phân miền trực quan)
    classDef stage1 fill:#EFF6FF,stroke:#3B82F6,stroke-width:1.5px,color:#1E3A8A;
    classDef stage2 fill:#FFFBEB,stroke:#F59E0B,stroke-width:1.5px,color:#92400E;
    classDef stage3 fill:#F5F3FF,stroke:#8B5CF6,stroke-width:1.5px,color:#5B21B6;
    classDef stage4 fill:#ECFDF5,stroke:#10B981,stroke-width:1.5px,color:#065F46;

    subgraph S1["1. {{SUBGRAPH_1_NAME}}"]
        direction TB
        A1["🎯 <b>{{NODE_1_1_TITLE}}</b><br/><small>{{NODE_1_1_SUB}}</small>"]:::stage1
        A2["⚡ <b>{{NODE_1_2_TITLE}}</b><br/><small>{{NODE_1_2_SUB}}</small>"]:::stage1
        A1 --> A2
    end

    subgraph S2["2. {{SUBGRAPH_2_NAME}}"]
        direction TB
        B1["🛠️ <b>{{NODE_2_1_TITLE}}</b><br/><small>{{NODE_2_1_SUB}}</small>"]:::stage2
        B2["🔄 <b>{{NODE_2_2_TITLE}}</b><br/><small>{{NODE_2_2_SUB}}</small>"]:::stage2
        B1 <--> B2
    end

    subgraph S3["3. {{SUBGRAPH_3_NAME}}"]
        direction TB
        C1["🔭 <b>{{NODE_3_1_TITLE}}</b><br/><small>{{NODE_3_1_SUB}}</small>"]:::stage3
        C2["🧱 <b>{{NODE_3_2_TITLE}}</b><br/><small>{{NODE_3_2_SUB}}</small>"]:::stage3
        C1 --> C2
    end

    subgraph S4["4. {{SUBGRAPH_4_NAME}}"]
        direction TB
        D1["💎 <b>{{NODE_4_1_TITLE}}</b><br/><small>{{NODE_4_1_SUB}}</small>"]:::stage4
        D2["🚀 <b>{{NODE_4_2_TITLE}}</b><br/><small>{{NODE_4_2_SUB}}</small>"]:::stage4
        D1 --> D2
    end

    %% PIPELINE CONNECTIONS
    S1 ==>|"{{TRANSITION_1_LABEL}}"| S2
    S2 ==>|"{{TRANSITION_2_LABEL}}"| S3
    S3 ==>|"{{TRANSITION_3_LABEL}}"| S4
      </div>
    </div>
  </div>
</div>
```
