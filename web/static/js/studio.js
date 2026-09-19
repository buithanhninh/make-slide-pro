/**
 * Make Slide Pro Web Studio V8.3.0
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

    // SaaS Multi-Tenant State
    this.token = localStorage.getItem("make_slide_pro_token") || null;
    this.currentUser = null;
    this.myProjects = [];
    
    this.initElements();
    this.bindEvents();
    this.checkAuth();
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

    // Header & SaaS Controls
    this.sessionPill = document.getElementById("session-pill");
    this.sessionIdText = document.getElementById("session-id-text");
    this.btnToggleTheme = document.getElementById("btn-toggle-theme");
    this.authGuestControls = document.getElementById("auth-guest-controls");
    this.authUserControls = document.getElementById("auth-user-controls");
    this.btnOpenAuth = document.getElementById("btn-open-auth");
    this.btnOpenProjects = document.getElementById("btn-open-projects");
    this.userProjectCount = document.getElementById("user-project-count");
    this.userCreditsBadge = document.getElementById("user-credits-badge");
    this.userEmailBadge = document.getElementById("user-email-badge");
    this.btnLogout = document.getElementById("btn-logout");

    // Modals
    this.modalAuth = document.getElementById("modal-auth");
    this.btnCloseAuthModal = document.getElementById("btn-close-auth-modal");
    this.tabLogin = document.getElementById("tab-login");
    this.tabRegister = document.getElementById("tab-register");
    this.formLogin = document.getElementById("form-login");
    this.formRegister = document.getElementById("form-register");
    this.authErrorMsg = document.getElementById("auth-error-msg");
    this.authSuccessMsg = document.getElementById("auth-success-msg");

    this.modalProjects = document.getElementById("modal-projects");
    this.btnCloseProjectsModal = document.getElementById("btn-close-projects-modal");
    this.projectsListContainer = document.getElementById("projects-list-container");

    // Demo Documents 1-Click
    this.demoDocBtns = document.querySelectorAll(".demo-doc-btn");

    // Filmstrip Carousel
    this.filmstripTrack = document.getElementById("filmstrip-track");
    this.filmstripCountText = document.getElementById("filmstrip-count-text");

    // Timeline Stepper & Timer
    this.renderTimeline = document.getElementById("render-timeline");
    this.renderElapsedTime = document.getElementById("render-elapsed-time");
    this.timelineSteps = [1, 2, 3, 4, 5].map(i => document.getElementById(`tstep-${i}`));
    this.renderTimerInterval = null;
    this.renderStartTime = null;

    // Copilot Quick Prompt Chips
    this.copilotChips = document.querySelectorAll(".copilot-chip");

    // Pricing & VietQR Modal
    this.modalPricing = document.getElementById("modal-pricing");
    this.btnGuestPricing = document.getElementById("btn-guest-pricing");
    this.btnOpenPricing = document.getElementById("btn-open-pricing");
    this.btnClosePricingModal = document.getElementById("btn-close-pricing-modal");
    this.pricingCards = document.querySelectorAll(".pricing-card");
    this.vietqrPaymentBox = document.getElementById("vietqr-payment-box");
    this.vietqrImage = document.getElementById("vietqr-image");
    this.qrAmount = document.getElementById("qr-amount");
    this.qrMemo = document.getElementById("qr-memo");
    this.btnSimulatePaid = document.getElementById("btn-simulate-paid");
    this.selectedTier = { tier: "PRO", price: 199000, credits: 100 };
  }

  bindEvents() {
    // SaaS Auth Listeners
    if (this.btnOpenAuth) {
      this.btnOpenAuth.addEventListener("click", () => this.openAuthModal());
    }
    if (this.btnCloseAuthModal) {
      this.btnCloseAuthModal.addEventListener("click", () => this.closeAuthModal());
    }
    if (this.tabLogin) {
      this.tabLogin.addEventListener("click", () => this.switchAuthTab("login"));
    }
    if (this.tabRegister) {
      this.tabRegister.addEventListener("click", () => this.switchAuthTab("register"));
    }
    if (this.formLogin) {
      this.formLogin.addEventListener("submit", (e) => this.handleLoginSubmit(e));
    }
    if (this.formRegister) {
      this.formRegister.addEventListener("submit", (e) => this.handleRegisterSubmit(e));
    }
    if (this.btnLogout) {
      this.btnLogout.addEventListener("click", () => this.handleLogout());
    }
    if (this.btnOpenProjects) {
      this.btnOpenProjects.addEventListener("click", () => this.openProjectsModal());
    }
    if (this.btnCloseProjectsModal) {
      this.btnCloseProjectsModal.addEventListener("click", () => this.modalProjects.style.display = "none");
    }

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

    // Demo documents 1-click
    if (this.demoDocBtns) {
      this.demoDocBtns.forEach(btn => {
        btn.addEventListener("click", () => this.loadDemoDocument(btn.dataset.demo));
      });
    }

    // Copilot prompt chips
    if (this.copilotChips) {
      this.copilotChips.forEach(chip => {
        chip.addEventListener("click", () => this.handleCopilotChip(chip.dataset.cmd));
      });
    }

    // Pricing & VietQR Listeners
    if (this.btnGuestPricing) {
      this.btnGuestPricing.addEventListener("click", () => this.openPricingModal());
    }
    if (this.btnOpenPricing) {
      this.btnOpenPricing.addEventListener("click", () => this.openPricingModal());
    }
    if (this.btnClosePricingModal) {
      this.btnClosePricingModal.addEventListener("click", () => this.closePricingModal());
    }
    if (this.pricingCards) {
      this.pricingCards.forEach(card => {
        card.addEventListener("click", () => {
          const tier = card.dataset.tier;
          const price = parseInt(card.dataset.price);
          const credits = parseInt(card.dataset.credits);
          this.selectPricingTier(tier, price, credits);
        });
      });
    }
    if (this.btnSimulatePaid) {
      this.btnSimulatePaid.addEventListener("click", () => this.handleSimulatePaid());
    }
  }

  // -------------------------------------------------------------------------
  // SaaS Multi-Tenant & Auth Methods
  // -------------------------------------------------------------------------
  getAuthHeaders(includeJson = true) {
    const headers = {};
    if (includeJson) headers["Content-Type"] = "application/json";
    if (this.token) headers["Authorization"] = `Bearer ${this.token}`;
    return headers;
  }

  async checkAuth() {
    if (!this.token) {
      this.renderGuestUI();
      return;
    }
    try {
      const res = await fetch("/api/auth/me", {
        headers: this.getAuthHeaders(false)
      });
      if (res.ok) {
        const user = await res.json();
        this.currentUser = user;
        this.renderUserUI();
      } else {
        this.token = null;
        localStorage.removeItem("make_slide_pro_token");
        this.renderGuestUI();
      }
    } catch (e) {
      this.renderGuestUI();
    }
  }

  renderUserUI() {
    if (this.authGuestControls) this.authGuestControls.style.display = "none";
    if (this.authUserControls) this.authUserControls.style.display = "flex";
    if (this.userCreditsBadge) this.userCreditsBadge.innerText = this.currentUser.credits;
    if (this.userEmailBadge) this.userEmailBadge.innerText = this.currentUser.email;
    if (this.userProjectCount) this.userProjectCount.innerText = this.currentUser.project_count || 0;
  }

  renderGuestUI() {
    if (this.authGuestControls) this.authGuestControls.style.display = "flex";
    if (this.authUserControls) this.authUserControls.style.display = "none";
  }

  openAuthModal() {
    if (this.authErrorMsg) this.authErrorMsg.style.display = "none";
    if (this.authSuccessMsg) this.authSuccessMsg.style.display = "none";
    if (this.modalAuth) this.modalAuth.style.display = "flex";
  }

  closeAuthModal() {
    if (this.modalAuth) this.modalAuth.style.display = "none";
  }

  switchAuthTab(tab) {
    if (this.authErrorMsg) this.authErrorMsg.style.display = "none";
    if (this.authSuccessMsg) this.authSuccessMsg.style.display = "none";
    if (tab === "login") {
      this.tabLogin.classList.add("btn-primary");
      this.tabLogin.classList.remove("btn-secondary");
      this.tabRegister.classList.add("btn-secondary");
      this.tabRegister.classList.remove("btn-primary");
      this.formLogin.style.display = "block";
      this.formRegister.style.display = "none";
    } else {
      this.tabRegister.classList.add("btn-primary");
      this.tabRegister.classList.remove("btn-secondary");
      this.tabLogin.classList.add("btn-secondary");
      this.tabLogin.classList.remove("btn-primary");
      this.formRegister.style.display = "block";
      this.formLogin.style.display = "none";
    }
  }

  async handleLoginSubmit(e) {
    e.preventDefault();
    if (this.authErrorMsg) this.authErrorMsg.style.display = "none";
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Đăng nhập không thành công.");

      this.token = data.access_token;
      localStorage.setItem("make_slide_pro_token", this.token);
      this.currentUser = data.user;
      this.renderUserUI();
      this.closeAuthModal();
      this.checkAuth();
    } catch (err) {
      if (this.authErrorMsg) {
        this.authErrorMsg.innerText = err.message;
        this.authErrorMsg.style.display = "block";
      }
    }
  }

  async handleRegisterSubmit(e) {
    e.preventDefault();
    if (this.authErrorMsg) this.authErrorMsg.style.display = "none";
    const fullName = document.getElementById("reg-fullname").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ full_name: fullName, email, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Đăng ký không thành công.");

      this.token = data.access_token;
      localStorage.setItem("make_slide_pro_token", this.token);
      this.currentUser = data.user;
      this.renderUserUI();
      if (this.authSuccessMsg) {
        this.authSuccessMsg.innerText = "Đăng ký thành công! Bạn được tặng 5 Credits miễn phí.";
        this.authSuccessMsg.style.display = "block";
      }
      setTimeout(() => {
        this.closeAuthModal();
        this.checkAuth();
      }, 1200);
    } catch (err) {
      if (this.authErrorMsg) {
        this.authErrorMsg.innerText = err.message;
        this.authErrorMsg.style.display = "block";
      }
    }
  }

  handleLogout() {
    this.token = null;
    this.currentUser = null;
    localStorage.removeItem("make_slide_pro_token");
    this.renderGuestUI();
  }

  async openProjectsModal() {
    if (this.modalProjects) this.modalProjects.style.display = "flex";
    if (this.projectsListContainer) {
      this.projectsListContainer.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 2rem;">Đang tải danh sách bài thuyết trình...</div>`;
    }

    try {
      const res = await fetch("/api/projects", {
        headers: this.getAuthHeaders(false)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Không thể tải danh sách dự án.");

      this.myProjects = data;
      if (!data.length) {
        this.projectsListContainer.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 2rem;">Bạn chưa có bài thuyết trình nào. Hãy nạp tài liệu để bắt đầu!</div>`;
        return;
      }

      this.projectsListContainer.innerHTML = data.map(p => `
        <div class="project-item-card">
          <div class="project-info">
            <h4>${p.title || 'Bài Thuyết Trình Không Tên'}</h4>
            <p>📄 ${p.source_filename || 'Tài liệu'} • 📊 ${p.total_slides} slides • Trạng thái: <strong style="color: var(--accent-cyan);">${p.status}</strong></p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" onclick="window.app.loadProject('${p.id}')" style="padding: 6px 12px; font-size: 0.8rem;">
              Mở Dự Án
            </button>
            ${p.status === "COMPLETED" ? `
              <a href="/api/download/${p.id}/Presentation_Dark.pptx" class="btn btn-primary" style="padding: 6px 12px; font-size: 0.8rem;">
                Tải PPTX
              </a>
            ` : ''}
          </div>
        </div>
      `).join("");
    } catch (err) {
      if (this.projectsListContainer) {
        this.projectsListContainer.innerHTML = `<div style="color: var(--accent-rose); padding: 1rem;">Lỗi: ${err.message}</div>`;
      }
    }
  }

  async loadProject(projectId) {
    if (this.modalProjects) this.modalProjects.style.display = "none";
    try {
      const res = await fetch(`/api/projects/${projectId}`, {
        headers: this.getAuthHeaders(false)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Không thể tải dự án.");

      this.sessionId = data.id;
      this.blueprints = data.blueprints;
      this.sessionPill.style.display = "inline-flex";
      this.sessionIdText.innerText = this.sessionId;
      this.deckTitleInput.value = data.title;
      this.renderStoryboard();

      // Check if rendered
      const statusRes = await fetch(`/api/projects/${projectId}/status`, {
        headers: this.getAuthHeaders(false)
      });
      const statusData = await statusRes.json();
      if (statusData.has_previews) {
        this.previews = statusData.previews;
        this.currentSlideIdx = 0;
        this.btnDownloadDark.href = `/api/download/${projectId}/Presentation_Dark.pptx`;
        this.btnDownloadLight.href = `/api/download/${projectId}/Presentation_Light.pptx`;
        this.updateSlideDisplay();
        this.renderFilmstrip();
        this.setStep(4);
      } else {
        this.setStep(2);
      }
    } catch (err) {
      alert("Lỗi tải dự án: " + err.message);
    }
  }

  // -------------------------------------------------------------------------
  // Pricing & VietQR Top-Up Flow
  // -------------------------------------------------------------------------
  openPricingModal() {
    if (this.modalPricing) {
      this.modalPricing.style.display = "flex";
      this.selectPricingTier(this.selectedTier.tier, this.selectedTier.price, this.selectedTier.credits);
    }
  }

  closePricingModal() {
    if (this.modalPricing) {
      this.modalPricing.style.display = "none";
    }
  }

  selectPricingTier(tier, price, credits) {
    this.selectedTier = { tier, price, credits };

    if (this.pricingCards) {
      this.pricingCards.forEach(card => {
        if (card.dataset.tier === tier) {
          card.style.borderColor = "var(--accent-cyan)";
          card.style.boxShadow = "0 0 20px rgba(6, 182, 212, 0.35)";
        } else {
          card.style.borderColor = "";
          card.style.boxShadow = "";
        }
      });
    }

    if (this.vietqrPaymentBox) {
      this.vietqrPaymentBox.style.display = "block";
    }

    const memo = `MSP ${this.currentUser ? this.currentUser.id.substring(0, 8).toUpperCase() : 'DEMO'}`;
    const formattedPrice = price.toLocaleString("vi-VN") + " đ";

    if (this.qrAmount) this.qrAmount.innerText = formattedPrice;
    if (this.qrMemo) this.qrMemo.innerText = memo;

    const qrUrl = `https://api.vietqr.io/image/970422-999988886666-compact.jpg?amount=${price}&addInfo=${encodeURIComponent(memo)}&accountName=MAKE%20SLIDE%20PRO`;
    if (this.vietqrImage) this.vietqrImage.src = qrUrl;
  }

  async handleSimulatePaid() {
    if (!this.token || !this.currentUser) {
      alert("Vui lòng đăng nhập hoặc đăng ký tài khoản để lưu trữ Credits sau khi nạp!");
      this.closePricingModal();
      this.openAuthModal();
      return;
    }

    if (this.btnSimulatePaid) {
      this.btnSimulatePaid.innerText = "⏳ Đang xác nhận giao dịch...";
      this.btnSimulatePaid.disabled = true;
    }

    try {
      const res = await fetch("/api/payments/topup", {
        method: "POST",
        headers: this.getAuthHeaders(true),
        body: JSON.stringify({
          tier: this.selectedTier.tier,
          amount: this.selectedTier.price,
          credits: this.selectedTier.credits
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Không thể thực hiện nạp credits.");

      if (this.currentUser) {
        this.currentUser.credits = data.new_credits;
      }
      this.renderUserUI();
      alert(`🎉 Chúc mừng! ${data.message}\nSố dư hiện tại: ${data.new_credits} Credits.`);
      this.closePricingModal();
    } catch (err) {
      alert("Lỗi nạp tiền: " + err.message);
    } finally {
      if (this.btnSimulatePaid) {
        this.btnSimulatePaid.innerText = "⚡ Xác Nhận Nạp Tiền (Mô phỏng Sandbox)";
        this.btnSimulatePaid.disabled = false;
      }
    }
  }

  // -------------------------------------------------------------------------
  // 1-Click Demo Documents & AI Copilot Chips
  // -------------------------------------------------------------------------
  loadDemoDocument(type) {
    const rawTitle = document.getElementById("raw-text-title");
    const rawContent = document.getElementById("raw-text-content");
    if (!rawTitle || !rawContent) return;

    if (type === "population") {
      rawTitle.value = "Thực Trạng Dân Số và Cơ Cấu Lao Động Việt Nam 2025-2030";
      rawContent.value = `CHUYÊN ĐỀ DÂN SỐ VÀ PHÁT TRIỂN BỀN VỮNG VIỆT NAM
Phần 1: Chỉ Số Tử Vong & Tỷ Suất Chết Thô (CDR)
Tỷ suất chết thô (Crude Death Rate - CDR) là chỉ số đo lường số lượng tử vong trên 1.000 dân số bình quân trong một năm xác định.
Công thức tính toán chuẩn mực:
CDR = (D / P) * 1000 (đơn vị: ‰)
Trong đó: D là tổng số ca tử vong trong năm, P là dân số bình quân giữa năm.
Xu hướng CDR tại Việt Nam duy trì ổn định phản ánh chất lượng y tế cộng đồng được củng cố.

Phần 2: Bảng Phân Tích Di Dân & Tăng Trưởng Lao Động Theo Vùng
Dưới đây là bảng số liệu phân bố luồng di dân thuần và tốc độ tăng trưởng lực lượng lao động:
| Vùng Kinh Tế | Tỷ Lệ Tăng Trưởng Lao Động | Di Dân Thuần (Người/Năm) | Tỷ Trọng GDP Đóng Góp |
| Đông Nam Bộ | 2.8% | +185,000 | 31.5% |
| Đồng Bằng Sông Hồng | 1.6% | +72,000 | 26.2% |
| Đồng Bằng Sông Cửu Long | 0.4% | -54,000 | 12.1% |
| Duyên Hải Miền Trung | 0.9% | -28,000 | 14.8% |

Phần 3: Thách Thức Già Hóa Dân Số & Cơ Hội Dân Số Vàng
Việt Nam đang trải qua giai đoạn chuyển giao nhân khẩu học nhanh nhất khu vực Đông Nam Á. Tỷ lệ người cao tuổi (trên 60 tuổi) dự báo sẽ vượt 20% vào năm 2038, chính thức bước vào thời kỳ dân số già.
Cần nhanh chóng tối ưu hóa năng suất lao động giai đoạn dân số vàng còn lại, thiết lập mạng lưới an sinh xã hội đa tầng và đầu tư vào kinh tế bạc (Silver Economy).`;
    } else if (type === "energy") {
      rawTitle.value = "Chiến Lược Chuyển Dịch Năng Lượng Tái Tạo & Lộ Trình Net-Zero 2050";
      rawContent.value = `QUY HOẠCH NĂNG LƯỢNG TÁI TẠO QUỐC GIA 2030 - TẦM NHÌN 2050
Phần 1: Mục Tiêu Phát Triển Theo Quy Hoạch Điện VIII
Việt Nam cam kết mạnh mẽ đạt mức phát thải ròng bằng '0' (Net Zero) vào năm 2050 tại COP26. Đến năm 2030, tỷ trọng năng lượng tái tạo (điện gió ngoài khơi, điện mặt trời, sinh khối) dự kiến chiếm từ 30.9% đến 39.2% tổng công suất nguồn điện toàn quốc.

Phần 2: Bảng So Sánh Suất Đầu Tư & Hiệu Suất Nguồn Điện
| Loại Hình Năng Lượng | Suất Đầu Tư (USD/kW) | Chi Phí Bình Quân LCOE (USD/MWh) | Hệ Số Công Suất (CF) |
| Điện Gió Ngoài Khơi | 2,200 - 2,800 | 78 - 95 | 42% - 48% |
| Điện Gió Trên Bờ | 1,300 - 1,600 | 55 - 68 | 28% - 35% |
| Điện Mặt Trời Mặt Đất | 700 - 950 | 45 - 58 | 18% - 22% |
| Thủy Điện Vừa & Nhỏ | 1,400 - 1,800 | 48 - 62 | 45% - 55% |

Phần 3: Cơ Chế Tài Chính Xanh & Trái Phiếu Chuyển Dịch
Việc phát triển lưới điện thông minh (Smart Grid) và các trạm lưu trữ năng lượng pin (BESS) đòi hỏi dòng vốn đầu tư hơn 135 tỷ USD đến 2030. Nguồn vốn này sẽ được huy động qua Khung Phân loại Tài chính Xanh (Green Taxonomy), trái phiếu bền vững và cơ chế JETP.`;
    } else if (type === "health") {
      rawTitle.value = "Chuyển Đổi Số Y Tế Toàn Diện: Bệnh Án Điện Tử & AI Lâm Sàng";
      rawContent.value = `CHIẾN LƯỢC CHUYỂN ĐỔI SỐ NGÀNH Y TẾ VIỆT NAM GIAI ĐOẠN 2025-2030
Phần 1: Số Hóa Bệnh Án Điện Tử (EMR) Không Giấy Tờ
Toàn bộ các bệnh viện hạng I và bệnh viện đặc biệt hoàn thành triển khai Hệ thống Bệnh án Điện tử (EMR), hướng tới mô hình bệnh viện thông minh không giấy tờ (Paperless Hospital), kết nối liên thông kết quả xét nghiệm và chẩn đoán hình ảnh trên toàn quốc.

Phần 2: Ứng Dụng Trí Tuệ Nhân Tạo (AI) Trong Chẩn Đoán Sớm
Tích hợp mạng nơ-ron tích chập (CNN) và các mô hình thị giác AI trong phân tích ảnh X-quang phổi, cắt lớp vi tính (CT) và cộng hưởng từ (MRI).
Độ chính xác sàng lọc tổn thương đạt trên 94.5%, hỗ trợ đắc lực cho các bác sĩ tuyến cơ sở phát hiện sớm ung thư phổi, đột quỵ não và bệnh lý võng mạc đái tháo đường.

Phần 3: Mạng Lưới Telehealth Chăm Sóc Sức Khỏe Từ Xa
Triển khai hệ thống khám chữa bệnh từ xa Telehealth tới 100% trạm y tế xã, vùng sâu, vùng xa và hải đảo. Giảm tỷ lệ chuyển tuyến không cần thiết xuống dưới 15%, tiết kiệm hàng nghìn tỷ đồng chi phí xã hội và nâng cao năng lực cho đội ngũ y bác sĩ cơ sở.`;
    }

    this.handleRawTextSubmit();
  }

  handleCopilotChip(cmd) {
    if (!this.copilotInput) return;
    this.copilotInput.value = cmd;
    this.sendCopilotCommand();
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
      const uploadUrl = this.token ? "/api/projects/upload" : "/api/upload/file";
      const headers = this.token ? { "Authorization": `Bearer ${this.token}` } : {};
      const res = await fetch(uploadUrl, { method: "POST", headers, body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Lỗi tải tệp");
      this.onIngestionSuccess(data);
      if (this.token) this.checkAuth();
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
        headers: this.getAuthHeaders(true),
        body: JSON.stringify({ title, content })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Lỗi bóc tách văn bản");
      this.onIngestionSuccess(data);
      if (this.token) this.checkAuth();
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
            <button class="btn btn-icon btn-dup-slide" title="Nhân bản slide (Duplicate)">📋</button>
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

      const btnDup = card.querySelector(".btn-dup-slide");
      if (btnDup) {
        btnDup.addEventListener("click", () => this.duplicateSlide(idx));
      }

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

  duplicateSlide(idx) {
    if (!this.blueprints || !this.blueprints.slides || !this.blueprints.slides[idx]) return;
    const orig = this.blueprints.slides[idx];
    const clone = JSON.parse(JSON.stringify(orig));
    clone.slide_id = `SLIDE_${Date.now().toString().slice(-4)}`;
    clone.assertion_title = `${clone.assertion_title || 'Slide'} (Bản sao)`;
    this.blueprints.slides.splice(idx + 1, 0, clone);
    this.renderStoryboard();
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

  // -------------------------------------------------------------------------
  // High-Precision Rendering Timer & 5-Stage Stepper
  // -------------------------------------------------------------------------
  startRenderTimer() {
    this.stopRenderTimer();
    this.renderStartTime = Date.now();
    if (this.renderElapsedTime) this.renderElapsedTime.innerText = "00:00";
    this.renderTimerInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - this.renderStartTime) / 1000);
      const m = Math.floor(elapsed / 60).toString().padStart(2, "0");
      const s = (elapsed % 60).toString().padStart(2, "0");
      if (this.renderElapsedTime) this.renderElapsedTime.innerText = `${m}:${s}`;
    }, 1000);
  }

  stopRenderTimer() {
    if (this.renderTimerInterval) {
      clearInterval(this.renderTimerInterval);
      this.renderTimerInterval = null;
    }
  }

  updateTimelineStep(stageIndex) {
    if (!this.timelineSteps) return;
    this.timelineSteps.forEach((el, i) => {
      if (!el) return;
      const stepNum = i + 1;
      el.classList.remove("active", "completed");
      if (stepNum < stageIndex) {
        el.classList.add("completed");
      } else if (stepNum === stageIndex) {
        el.classList.add("active");
      }
    });
  }

  async startRendering() {
    if (!this.sessionId) return;

    if (this.token && this.currentUser && this.currentUser.credits < 1) {
      alert("Tài khoản của bạn đã hết Credits (cần 1 credit/lần render). Vui lòng nạp thêm để tiếp tục xuất bản PowerPoint!");
      this.openPricingModal();
      return;
    }

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
    this.startRenderTimer();
    this.updateTimelineStep(1);
    if (this.btnViewResults) this.btnViewResults.style.display = "none";
    this.initWebSocket();

    // Trigger render
    try {
      const renderUrl = this.token ? `/api/projects/${this.sessionId}/render` : "/api/render";
      const res = await fetch(renderUrl, {
        method: "POST",
        headers: this.getAuthHeaders(true),
        body: JSON.stringify({ session_id: this.sessionId, theme: "ALL" })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);

      if (this.token && data.remaining_credits !== undefined) {
        if (this.currentUser) this.currentUser.credits = data.remaining_credits;
        if (this.userCreditsBadge) this.userCreditsBadge.innerText = data.remaining_credits;
      }
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

    // Update 5-stage timeline stepper
    let currentStep = 1;
    if (data.stage === "COMPLETED" || data.percent >= 100) {
      currentStep = 5;
      if (this.timelineSteps) {
        this.timelineSteps.forEach(el => el && el.classList.add("completed"));
      }
      this.stopRenderTimer();
      if (this.btnViewResults) this.btnViewResults.style.display = "inline-block";
    } else {
      if (data.percent < 20) currentStep = 1;
      else if (data.percent < 40) currentStep = 2;
      else if (data.percent < 60) currentStep = 3;
      else if (data.percent < 85) currentStep = 4;
      else currentStep = 5;
      this.updateTimelineStep(currentStep);
    }
  }

  appendConsoleLog(msg) {
    const line = document.createElement("div");
    line.style.margin = "4px 0";
    line.innerText = `> ${msg}`;
    this.consoleOutput.appendChild(line);
    this.consoleOutput.scrollTop = this.consoleOutput.scrollHeight;
  }

  // -------------------------------------------------------------------------
  // Gallery, Dual-Theme & Filmstrip Carousel
  // -------------------------------------------------------------------------
  async loadSlideGallery() {
    try {
      const res = await fetch(`/api/slides/${this.sessionId}`);
      const data = await res.json();
      if (data.success) {
        this.previews = data.slides;
        this.currentSlideIdx = 0;
        this.renderFilmstrip();
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
    this.renderFilmstrip();
    this.updateSlideDisplay();
  }

  renderFilmstrip() {
    if (!this.filmstripTrack) return;
    const slides = this.previews ? this.previews[this.activeDeckTheme] : [];
    if (!slides || !slides.length) {
      this.filmstripTrack.innerHTML = `<span style="color: var(--text-muted); font-size: 0.8rem; padding: 1rem;">Chưa có ảnh slide preview</span>`;
      return;
    }

    if (this.filmstripCountText) {
      this.filmstripCountText.innerText = `${slides.length} slides (${this.activeDeckTheme === 'DARK' ? 'Nền Tối' : 'Nền Sáng'}) • Nhấp vào ảnh để chuyển slide`;
    }

    this.filmstripTrack.innerHTML = slides.map((url, i) => `
      <div class="filmstrip-thumb ${i === this.currentSlideIdx ? 'active' : ''}" data-idx="${i}">
        <span class="thumb-badge">${(i + 1).toString().padStart(2, '0')}</span>
        <img src="${url}" alt="Slide ${i + 1}" loading="lazy">
      </div>
    `).join("");

    this.filmstripTrack.querySelectorAll(".filmstrip-thumb").forEach(thumb => {
      thumb.addEventListener("click", () => {
        const idx = parseInt(thumb.dataset.idx);
        this.selectSlide(idx);
      });
    });
  }

  selectSlide(idx) {
    const slides = this.previews ? this.previews[this.activeDeckTheme] : [];
    if (!slides || idx < 0 || idx >= slides.length) return;
    this.currentSlideIdx = idx;
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

    // Update filmstrip active state & scroll into view
    if (this.filmstripTrack) {
      const thumbs = this.filmstripTrack.querySelectorAll(".filmstrip-thumb");
      thumbs.forEach((t, i) => {
        if (i === this.currentSlideIdx) {
          t.classList.add("active");
          t.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
        } else {
          t.classList.remove("active");
        }
      });
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
