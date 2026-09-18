/**
 * Make Slide Pro Web Studio V7.3
 * Client-side State Machine & Interactive Studio Controller
 */

class SlideStudioApp {
  constructor() {
    this.sessionId = null;
    this.blueprints = null;
    this.previews = null;
    this.activeStep = 1;
    this.currentSlideIdx = 0;
    this.activeDeckTheme = "DARK";
    this.ws = null;
    
    this.initElements();
    this.bindEvents();
  }

  initElements() {
    // Stepper
    this.stepNavs = document.querySelectorAll(".step-item");
    this.views = {
      1: document.getElementById("view-ingest"),
      2: document.getElementById("view-storyboard"),
      3: document.getElementById("view-rendering"),
      4: document.getElementById("view-gallery")
    };

    // View 1
    this.dropzone = document.getElementById("dropzone");
    this.fileInput = document.getElementById("file-input");
    this.btnBrowse = document.getElementById("btn-browse-file");
    this.anatomyCard = document.getElementById("anatomy-card");
    this.btnGotoStoryboard = document.getElementById("btn-goto-storyboard");
    this.btnSubmitRawText = document.getElementById("btn-submit-raw-text");

    // View 2
    this.deckTitleInput = document.getElementById("deck-title-input");
    this.slidesContainer = document.getElementById("slides-container");
    this.btnRunMaccQa = document.getElementById("btn-run-macc-qa");
    this.btnAddSlide = document.getElementById("btn-add-slide");
    this.btnTriggerRender = document.getElementById("btn-trigger-render");

    // View 3
    this.progressBar = document.getElementById("render-progress-bar");
    this.progressPercent = document.getElementById("progress-percent");
    this.progressStageName = document.getElementById("progress-stage-name");
    this.consoleOutput = document.getElementById("render-console-output");
    this.btnViewResults = document.getElementById("btn-view-results");

    // View 4
    this.btnThemeDark = document.getElementById("btn-theme-dark");
    this.btnThemeLight = document.getElementById("btn-theme-light");
    this.slideImg = document.getElementById("current-slide-img");
    this.slideIndexDisplay = document.getElementById("slide-index-display");
    this.speakerNotesDisplay = document.getElementById("current-speaker-notes");
    this.btnPrevSlide = document.getElementById("btn-prev-slide");
    this.btnNextSlide = document.getElementById("btn-next-slide");
    this.btnDownloadDark = document.getElementById("btn-download-dark");
    this.btnDownloadLight = document.getElementById("btn-download-light");
    this.btnLaunchPresenter = document.getElementById("btn-launch-presenter");
    this.btnBackToStoryboard = document.getElementById("btn-back-to-storyboard");

    // Copilot
    this.copilotInput = document.getElementById("copilot-input");
    this.btnSendCopilot = document.getElementById("btn-send-copilot");
    this.copilotHistory = document.getElementById("copilot-history");

    // Header
    this.sessionPill = document.getElementById("session-pill");
    this.sessionIdText = document.getElementById("session-id-text");
    this.btnToggleTheme = document.getElementById("btn-toggle-theme");
  }

  bindEvents() {
    // Stepper navigation
    this.stepNavs.forEach(item => {
      item.addEventListener("click", () => {
        const step = parseInt(item.dataset.step);
        if (step <= this.activeStep || (this.blueprints && step <= 2)) {
          this.setStep(step);
        }
      });
    });

    // Theme toggle
    this.btnToggleTheme.addEventListener("click", () => {
      const html = document.documentElement;
      const cur = html.getAttribute("data-studio-theme");
      const nxt = cur === "dark" ? "light" : "dark";
      html.setAttribute("data-studio-theme", nxt);
    });

    // File Dropzone
    this.btnBrowse.addEventListener("click", () => this.fileInput.click());
    this.fileInput.addEventListener("change", (e) => {
      if (e.target.files.length) this.handleFileUpload(e.target.files[0]);
    });

    this.dropzone.addEventListener("dragover", (e) => {
      e.preventDefault();
      this.dropzone.classList.add("dragover");
    });
    this.dropzone.addEventListener("dragleave", () => this.dropzone.classList.remove("dragover"));
    this.dropzone.addEventListener("drop", (e) => {
      e.preventDefault();
      this.dropzone.classList.remove("dragover");
      if (e.dataTransfer.files.length) this.handleFileUpload(e.dataTransfer.files[0]);
    });

    // Raw Text Submit
    this.btnSubmitRawText.addEventListener("click", () => this.handleRawTextSubmit());

    // Navigation buttons
    this.btnGotoStoryboard.addEventListener("click", () => this.setStep(2));
    this.btnBackToStoryboard.addEventListener("click", () => this.setStep(2));

    // Storyboard actions
    this.deckTitleInput.addEventListener("input", () => {
      if (this.blueprints) this.blueprints.deck_title = this.deckTitleInput.value;
    });
    this.btnAddSlide.addEventListener("click", () => this.addNewSlide());
    this.btnRunMaccQa.addEventListener("click", () => this.runMaccQaReview());
    this.btnTriggerRender.addEventListener("click", () => this.startRendering());

    // Render results
    this.btnViewResults.addEventListener("click", () => {
      this.loadSlideGallery();
      this.setStep(4);
    });

    // Gallery controls
    this.btnPrevSlide.addEventListener("click", () => this.navigateSlide(-1));
    this.btnNextSlide.addEventListener("click", () => this.navigateSlide(1));
    this.btnThemeDark.addEventListener("click", () => this.switchDeckTheme("DARK"));
    this.btnThemeLight.addEventListener("click", () => this.switchDeckTheme("LIGHT"));
    this.btnLaunchPresenter.addEventListener("click", () => this.launchFullscreenPresenter());

    // Keyboard navigation
    window.addEventListener("keydown", (e) => {
      if (this.activeStep === 4) {
        if (e.key === "ArrowLeft") this.navigateSlide(-1);
        if (e.key === "ArrowRight") this.navigateSlide(1);
      }
    });

    // AI Copilot
    this.btnSendCopilot.addEventListener("click", () => this.sendCopilotCommand());
    this.copilotInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") this.sendCopilotCommand();
    });
  }

  setStep(stepNum) {
    this.activeStep = stepNum;
    Object.keys(this.views).forEach(k => {
      if (parseInt(k) === stepNum) {
        this.views[k].classList.add("active");
      } else {
        this.views[k].classList.remove("active");
      }
    });

    this.stepNavs.forEach(nav => {
      const s = parseInt(nav.dataset.step);
      nav.classList.remove("active");
      if (s === stepNum) nav.classList.add("active");
      if (s < stepNum) nav.classList.add("completed");
    });
  }

  async handleFileUpload(file) {
    const depthMode = document.getElementById("select-depth-mode").value;
    const formData = new FormData();
    formData.append("file", file);
    formData.append("depth_mode", depthMode);

    this.dropzone.innerHTML = `
      <span class="dropzone-icon">⏳</span>
      <h2 class="dropzone-title">Đang Phân Tích Tài Liệu...</h2>
      <p class="dropzone-subtitle">${file.name}</p>
    `;

    try {
      const res = await fetch("/api/upload/file", { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Lỗi tải tệp");
      this.onIngestionSuccess(data);
    } catch (err) {
      alert("Lỗi: " + err.message);
      this.resetDropzone();
    }
  }

  async handleRawTextSubmit() {
    const title = document.getElementById("raw-text-title").value.trim() || "Chuyên Đề Đào Tạo";
    const content = document.getElementById("raw-text-content").value.trim();
    if (!content) {
      alert("Vui lòng nhập nội dung văn bản.");
      return;
    }

    try {
      const res = await fetch("/api/upload/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Lỗi bóc tách văn bản");
      this.onIngestionSuccess(data);
    } catch (err) {
      alert("Lỗi: " + err.message);
    }
  }

  resetDropzone() {
    this.dropzone.innerHTML = `
      <span class="dropzone-icon">📄</span>
      <h2 class="dropzone-title">Kéo & Thả Tài Liệu Vào Đây</h2>
      <p class="dropzone-subtitle">Hỗ trợ tự động bóc tách đa định dạng văn bản sang cấu trúc sư phạm</p>
      <div class="format-badges" style="margin-bottom: 1.5rem;">
        <span class="badge">.DOCX (Word & Tables)</span>
        <span class="badge">.PDF (PyMuPDF)</span>
        <span class="badge">.TXT / .MD</span>
      </div>
      <button id="btn-browse-file-reset" class="btn btn-primary" type="button">Chọn Tệp Từ Máy Tính</button>
    `;
    document.getElementById("btn-browse-file-reset").addEventListener("click", () => this.fileInput.click());
  }

  onIngestionSuccess(data) {
    this.sessionId = data.session_id;
    this.blueprints = data.blueprints;
    
    // Update Header Pill
    this.sessionPill.style.display = "inline-flex";
    this.sessionIdText.innerText = this.sessionId;

    // Populate Anatomy Stats
    document.getElementById("stat-sections").innerText = data.stats.sections;
    document.getElementById("stat-atoms").innerText = data.stats.atoms;
    document.getElementById("stat-tables").innerText = data.stats.tables;
    document.getElementById("stat-formulas").innerText = data.stats.formulas;
    this.anatomyCard.style.display = "block";

    // Set Deck Title
    this.deckTitleInput.value = data.deck_title || "Chuyên Đề Đào Tạo Chuẩn";

    // Render Storyboard
    this.renderStoryboard();

    // Reset Dropzone UI
    this.dropzone.innerHTML = `
      <span class="dropzone-icon" style="color: var(--accent-emerald);">✔</span>
      <h2 class="dropzone-title" style="color: var(--accent-emerald);">Bóc Tách Thành Công!</h2>
      <p class="dropzone-subtitle">${data.filename} (${data.stats.slides} slide sơ bộ)</p>
    `;
  }

  renderStoryboard() {
    if (!this.blueprints || !this.blueprints.slides) return;
    this.slidesContainer.innerHTML = "";

    this.blueprints.slides.forEach((slide, idx) => {
      const card = document.createElement("div");
      card.className = "slide-card";
      card.dataset.slideIdx = idx;

      const vJob = slide.visual_job || "CARDS";

      // Card Header
      let previewExtra = "";
      if (vJob === "FORMULA_CARD" && slide.formula) {
        previewExtra = `
          <div style="background: rgba(6,182,212,0.1); border: 1px solid var(--accent-cyan); border-radius: var(--radius-sm); padding: 8px 12px; font-family: monospace; color: var(--accent-cyan); font-weight: 700;">
            ∑ ${slide.formula}
          </div>
        `;
      } else if (vJob === "EDITORIAL_HERO" && slide.illustration) {
        previewExtra = `
          <div style="height: 100px; border-radius: var(--radius-sm); overflow: hidden; position: relative;">
            <img src="/assets/illustrations/${slide.illustration}" style="width: 100%; height: 100%; object-fit: cover;">
            <div style="position: absolute; bottom: 4px; left: 6px; background: rgba(0,0,0,0.7); font-size: 0.7rem; padding: 2px 6px; border-radius: 4px;">
              ${slide.illustration}
            </div>
          </div>
        `;
      }

      // Atoms list
      let atomsHtml = "";
      if (slide.atoms && slide.atoms.length) {
        atomsHtml = slide.atoms.map(a => `
          <div class="atom-item">
            <span class="atom-dot"></span>
            <div><strong>${a.title || 'Ý'}:</strong> ${a.text || ''}</div>
          </div>
        `).join("");
      }

      card.innerHTML = `
        <div class="slide-card-top">
          <span class="slide-badge-num">Slide ${(idx + 1).toString().padStart(2, '0')}</span>
          <select class="form-select select-vjob" style="width: auto; padding: 4px 10px; font-size: 0.75rem;">
            ${this.getVisualJobOptions(vJob)}
          </select>
        </div>

        <div>
          <label style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Tiêu Đề Luận Đề (Assertion Title)</label>
          <input type="text" class="slide-title-edit" value="${slide.assertion_title || ''}">
        </div>

        <div>
          <label style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Luận Điểm Cốt Lõi (Primary Claim)</label>
          <textarea class="slide-claim-edit" rows="2">${slide.primary_claim || ''}</textarea>
        </div>

        ${previewExtra}

        <div class="slide-atoms-preview">
          ${atomsHtml || '<span style="color: var(--text-muted);">Không có thẻ chi tiết</span>'}
        </div>

        <div class="slide-card-footer">
          <span style="font-size: 0.75rem; color: var(--text-muted);">${slide.section || 'NỘI DUNG'}</span>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-icon btn-move-up" title="Di chuyển lên">▲</button>
            <button class="btn btn-icon btn-move-down" title="Di chuyển xuống">▼</button>
            <button class="btn btn-icon btn-del-slide" style="color: var(--accent-rose);" title="Xóa slide">✕</button>
          </div>
        </div>
      `;

      // Event listeners for this card
      const titleInput = card.querySelector(".slide-title-edit");
      titleInput.addEventListener("input", (e) => {
        slide.assertion_title = e.target.value;
      });

      const claimInput = card.querySelector(".slide-claim-edit");
      claimInput.addEventListener("input", (e) => {
        slide.primary_claim = e.target.value;
      });

      const vjobSelect = card.querySelector(".select-vjob");
      vjobSelect.addEventListener("change", (e) => {
        slide.visual_job = e.target.value;
        this.renderStoryboard();
      });

      const btnUp = card.querySelector(".btn-move-up");
      btnUp.addEventListener("click", () => this.moveSlide(idx, -1));

      const btnDown = card.querySelector(".btn-move-down");
      btnDown.addEventListener("click", () => this.moveSlide(idx, 1));

      const btnDel = card.querySelector(".btn-del-slide");
      btnDel.addEventListener("click", () => this.deleteSlide(idx));

      this.slidesContainer.appendChild(card);
    });
  }

  getVisualJobOptions(current) {
    const jobs = [
      ["CARDS", "Thẻ Chuẩn (CARDS)"],
      ["BENTO_GRID", "Bento Grid (BENTO_GRID)"],
      ["EDITORIAL_HERO", "Minh Họa AI (EDITORIAL_HERO)"],
      ["FORMULA_CARD", "Công Thức Toán (FORMULA_CARD)"],
      ["DATA_TABLE", "Bảng Dữ Liệu (DATA_TABLE)"],
      ["CHART_AND_INSIGHTS", "Biểu Đồ Số Liệu (CHART)"],
      ["COMPARISON", "So Sánh Đối Chiếu (COMPARISON)"],
      ["PROCESS", "Quy Trình Các Bước (PROCESS)"]
    ];
    return jobs.map(([val, label]) => `
      <option value="${val}" ${val === current ? 'selected' : ''}>${label}</option>
    `).join("");
  }

  moveSlide(fromIdx, direction) {
    const toIdx = fromIdx + direction;
    if (toIdx < 0 || toIdx >= this.blueprints.slides.length) return;
    const temp = this.blueprints.slides[fromIdx];
    this.blueprints.slides[fromIdx] = this.blueprints.slides[toIdx];
    this.blueprints.slides[toIdx] = temp;
    this.renderStoryboard();
  }

  deleteSlide(idx) {
    if (confirm(`Bạn có chắc muốn xóa Slide ${idx + 1}?`)) {
      this.blueprints.slides.splice(idx, 1);
      this.renderStoryboard();
    }
  }

  addNewSlide() {
    const newSlide = {
      slide_id: `SLIDE_${(this.blueprints.slides.length + 1).toString().padStart(2, '0')}`,
      role: "CONTENT",
      section: "CHUYÊN ĐỀ",
      assertion_title: "Tiêu Đề Luận Điểm Mới",
      primary_claim: "Trình bày luận đề và thông điệp trọng tâm cần truyền tải.",
      visual_job: "CARDS",
      visual_anchor: "SECTION_CARDS",
      atoms: [
        { title: "Nội Dung 1", text: "Mô tả chi tiết luận cứ thứ nhất.", icon: "target" },
        { title: "Nội Dung 2", text: "Mô tả chi tiết luận cứ thứ hai.", icon: "activity" }
      ],
      speaker_notes: "Ghi chú thuyết trình cho slide mới."
    };
    this.blueprints.slides.push(newSlide);
    this.renderStoryboard();
  }

  async runMaccQaReview() {
    if (!this.sessionId) return;
    this.btnRunMaccQa.innerText = "⏳ Đang Thẩm Định...";
    try {
      const res = await fetch("/api/blueprint/qa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: this.sessionId })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Lỗi thẩm định");

      document.getElementById("macc-score").innerText = `${data.score}/100`;
      alert(`🎉 Thẩm Định MACC-QA Hoàn Tất!\nĐiểm chất lượng: ${data.score}/100 (${data.status})\nCác tiêu đề và cấu trúc sư phạm đã được chuẩn hóa tự động!`);
      this.blueprints = data.blueprints;
      this.renderStoryboard();
    } catch (err) {
      alert("Lỗi: " + err.message);
    } finally {
      this.btnRunMaccQa.innerText = "🛡️ Thẩm Định MACC-QA";
    }
  }

  async startRendering() {
    if (!this.sessionId) return;

    // Save blueprint state first
    await fetch("/api/blueprint/update", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: this.sessionId,
        slides: this.blueprints.slides,
        deck_title: this.deckTitleInput.value
      })
    });

    this.setStep(3);
    this.initWebSocket();

    // Trigger render
    try {
      const res = await fetch("/api/render", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: this.sessionId, theme: "ALL" })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
    } catch (err) {
      this.appendConsoleLog(`[ERROR] ${err.message}`);
    }
  }

  initWebSocket() {
    if (this.ws) {
      this.ws.close();
    }
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/${this.sessionId}`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleProgressUpdate(data);
    };

    this.ws.onclose = () => {
      console.log("WebSocket disconnected.");
    };
  }

  handleProgressUpdate(data) {
    this.progressBar.style.width = `${data.percent}%`;
    this.progressPercent.innerText = `${data.percent}%`;
    this.progressStageName.innerText = data.stage;
    this.appendConsoleLog(`[${data.stage}] ${data.message}`);

    if (data.stage === "COMPLETED") {
      this.btnViewResults.style.display = "inline-block";
    }
  }

  appendConsoleLog(msg) {
    const line = document.createElement("div");
    line.style.margin = "4px 0";
    line.innerText = `> ${msg}`;
    this.consoleOutput.appendChild(line);
    this.consoleOutput.scrollTop = this.consoleOutput.scrollHeight;
  }

  async loadSlideGallery() {
    try {
      const res = await fetch(`/api/slides/${this.sessionId}`);
      const data = await res.json();
      if (data.success) {
        this.previews = data.slides;
        this.currentSlideIdx = 0;
        this.updateSlideDisplay();
      }

      // Configure download buttons
      this.btnDownloadDark.href = `/api/download/${this.sessionId}/Presentation_Dark.pptx`;
      this.btnDownloadLight.href = `/api/download/${this.sessionId}/Presentation_Light.pptx`;
    } catch (err) {
      console.error(err);
    }
  }

  switchDeckTheme(theme) {
    this.activeDeckTheme = theme;
    if (theme === "DARK") {
      this.btnThemeDark.classList.add("active");
      this.btnThemeLight.classList.remove("active");
    } else {
      this.btnThemeLight.classList.add("active");
      this.btnThemeDark.classList.remove("active");
    }
    this.updateSlideDisplay();
  }

  navigateSlide(dir) {
    const slides = this.previews ? this.previews[this.activeDeckTheme] : [];
    if (!slides || !slides.length) return;
    const newIdx = this.currentSlideIdx + dir;
    if (newIdx >= 0 && newIdx < slides.length) {
      this.currentSlideIdx = newIdx;
      this.updateSlideDisplay();
    }
  }

  updateSlideDisplay() {
    const slides = this.previews ? this.previews[this.activeDeckTheme] : [];
    if (!slides || !slides.length) return;

    this.slideImg.src = slides[this.currentSlideIdx];
    this.slideIndexDisplay.innerText = `Slide ${this.currentSlideIdx + 1} / ${slides.length}`;

    if (this.blueprints && this.blueprints.slides && this.blueprints.slides[this.currentSlideIdx]) {
      const s = this.blueprints.slides[this.currentSlideIdx];
      this.speakerNotesDisplay.innerText = s.speaker_notes || "Không có ghi chú diễn giả.";
    }
  }

  launchFullscreenPresenter() {
    if (!this.slideImg) return;
    if (this.slideImg.requestFullscreen) {
      this.slideImg.requestFullscreen();
    } else if (this.slideImg.webkitRequestFullscreen) {
      this.slideImg.webkitRequestFullscreen();
    }
  }

  async sendCopilotCommand() {
    const cmd = this.copilotInput.value.trim();
    if (!cmd || !this.sessionId) return;

    // Add user message
    const userMsg = document.createElement("div");
    userMsg.style.background = "rgba(255,255,255,0.08)";
    userMsg.style.padding = "6px 10px";
    userMsg.style.borderRadius = "4px";
    userMsg.innerText = `Bạn: ${cmd}`;
    this.copilotHistory.appendChild(userMsg);
    this.copilotInput.value = "";
    this.copilotHistory.scrollTop = this.copilotHistory.scrollHeight;

    try {
      const res = await fetch("/api/copilot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: this.sessionId, command: cmd })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);

      const botMsg = document.createElement("div");
      botMsg.className = "copilot-msg-system";
      botMsg.innerText = `Copilot: ${data.message}`;
      this.copilotHistory.appendChild(botMsg);
      this.copilotHistory.scrollTop = this.copilotHistory.scrollHeight;

      if (data.modified) {
        this.blueprints = data.blueprints;
        this.renderStoryboard();
      }
    } catch (err) {
      alert("Lỗi: " + err.message);
    }
  }
}

// Instantiate on load
document.addEventListener("DOMContentLoaded", () => {
  window.app = new SlideStudioApp();
});
