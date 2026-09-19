# MAKE SLIDE PRO V8.2.0 - HỆ THỐNG KIẾN TRÚC DOANH NGHIỆP (CANONICAL ENTERPRISE ARCHITECTURE)

Tài liệu này quy định chi tiết cấu trúc phân tầng, luồng dữ liệu, cơ chế hàng đợi bất đồng bộ, giải pháp cô lập Microsoft Office COM và kịch bản triển khai container hóa cho ứng dụng Web App SaaS Make Slide Pro.

---

## 1. Cấu Trúc Phân Tầng Hệ Thống (Layered Architecture)

```
[CLIENT TIER]
  └── Web Studio SPA (Vanilla ES6+, CSS Design Tokens, WebSockets)
        │
[INGRESS & REVERSE PROXY]
  └── Nginx / Cloudflare (SSL Termination, WAF, Rate Limiter, 25MB Body Guard)
        │
[APPLICATION SERVER TIER]
  └── FastAPI Gateway (Stateless ASGI, JWT Auth, Ingestion, MACC-QA, Billing, Copilot)
        │
        ├── [CACHE & QUEUE BROKER] ──> Redis 7 (Pub/Sub, Rate Limits, Job Queue)
        │                                   │
        │                                   ▼
        ├── [RENDERING WORKER FLEET] ─> Dedicated Windows COM Workers / Linux Headless Workers
        │                                   │
        ├── [DATABASE TIER] ──────────> PostgreSQL 16 (Multi-Tenant RLS, Users, Projects)
        │
        └── [STORAGE TIER] ───────────> S3 / MinIO / Local Volume (PPTX Decks, 1080p PNGs)
```

---

## 2. Quy Chuẩn Động Cơ Biên Dịch (PowerPoint COM Sandbox)

- **Nguyên tắc STA Isolation**: Mọi tác vụ sinh slide native qua PowerPoint COM phải bọc trong:
  ```python
  import pythoncom
  pythoncom.CoInitialize()
  try:
      # Thực thi tác vụ tạo slide native...
  finally:
      pythoncom.CoUninitialize()
  ```
- **Tiến trình Giám sát (Watchdog)**:
  - Khởi tạo tiến trình PowerPoint độc lập với cửa sổ ẩn (`Visible = False`).
  - Đóng và tái tạo phiên PowerPoint sau mỗi 10 tác vụ để chống rò rỉ RAM.
  - Ngắt tiến trình khẩn cấp (`taskkill /f /im POWERPNT.EXE`) nếu thời gian render vượt quá 90 giây.

---

## 3. Quy Chuẩn An Ninh Đa Khách Hàng (Multi-Tenant Security)

1. **Chống Tấn Công IDOR (Insecure Direct Object Reference)**:
   - Tất cả các endpoint truy xuất tài nguyên (`/api/projects/{id}`, `/api/download/{id}/...`) bắt buộc kiểm tra định danh `project.user_id == current_user.id`.
2. **Kiểm Soát Dung Lượng Đầu Vào (Upload Guards)**:
   - Tệp tải lên tối đa: `25MB`.
   - Ký tự văn bản thô tối đa: `500.000` ký tự.
3. **Mã Hóa & Xác Thực**:
   - Mật khẩu người dùng được băm bằng thuật toán `bCrypt` với salt động.
   - Truy cập API bảo vệ bằng chuẩn `JWT Bearer Token` (thuật toán HS256, hạn dùng 7 ngày).

---

## 4. Hướng Dẫn Vận Hành Triển Khai

### A. Chạy Trực Tiếp Trên Máy Chủ Windows
```powershell
# 1. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 2. Thiết lập biến môi trường
copy .env.example .env

# 3. Khởi chạy Web Studio
python -m uvicorn web.app:app --host 0.0.0.0 --port 8000 --reload
```

### B. Chạy Cụm Container Bằng Docker Compose
```bash
docker-compose up -d --build
```
Hệ thống sẽ tự động kích hoạt cụm 4 dịch vụ:
- `app`: FastAPI Web Application Server
- `redis`: In-memory Broker & Cache
- `db`: PostgreSQL 16 Relational Database
- `nginx`: Edge Reverse Proxy & Static Caching Gateway
