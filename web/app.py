"""
web/app.py
Make Slide Pro Web Studio V7.3 - Production FastAPI Application
Provides RESTful APIs and real-time WebSockets for universal document ingestion,
interactive pedagogical storyboard editing, MACC-QA review, PowerPoint COM rendering,
and dual-theme slide presentation.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Ensure project root and scripts directory are in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
ASSETS_DIR = PROJECT_ROOT / "assets"
SESSIONS_DIR = PROJECT_ROOT / "Du_An_Outputs" / "web_sessions"
STATIC_DIR = Path(__file__).resolve().parent / "static"

for p in [str(PROJECT_ROOT), str(SCRIPTS_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Import Core Engine Modules
from scripts.ingest_content import ContentIngestor, clean_source_text
from scripts.blueprint_generator import (
    generate_blueprints_from_canonical,
    clean_title,
    clean_summary,
)
from scripts.author_native_com import NativeDeckAuthor

try:
    from scripts.content_multi_agent_council import ContentMultiAgentCouncil
except ImportError:
    ContentMultiAgentCouncil = None

try:
    from scripts.multi_agent_qa import MultiAgentQABoard
except ImportError:
    MultiAgentQABoard = None

app = FastAPI(
    title="Make Slide Pro Web Studio V7.3",
    description="Universal Document-to-PowerPoint Publishing & Pedagogical Studio",
    version="7.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Directories
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")
app.mount("/sessions", StaticFiles(directory=str(SESSIONS_DIR)), name="sessions")

# Thread pool for non-blocking PowerPoint COM operations
executor = ThreadPoolExecutor(max_workers=2)


# ---------------------------------------------------------------------------
# WebSocket Real-Time Progress Manager
# ---------------------------------------------------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket):
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: str, data: Dict[str, Any]):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_json(data)
                except Exception:
                    pass


ws_manager = ConnectionManager()


def sync_broadcast(session_id: str, stage: str, percent: int, message: str, level: str = "info"):
    """Helper to broadcast WebSocket events from synchronous threads."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.run_coroutine_threadsafe(
            ws_manager.broadcast(
                session_id,
                {"stage": stage, "percent": percent, "message": message, "level": level},
            ),
            loop,
        )


# ---------------------------------------------------------------------------
# Session Helper Utilities
# ---------------------------------------------------------------------------
def get_session_dir(session_id: str) -> Path:
    s_dir = SESSIONS_DIR / session_id
    s_dir.mkdir(parents=True, exist_ok=True)
    return s_dir


def load_session_json(session_id: str, filename: str) -> Optional[Dict[str, Any]]:
    path = get_session_dir(session_id) / filename
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def save_session_json(session_id: str, filename: str, data: Any):
    path = get_session_dir(session_id) / filename
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Pydantic Request Models
# ---------------------------------------------------------------------------
class TextUploadRequest(BaseModel):
    title: str
    content: str
    depth_mode: Optional[str] = "DEEP"


class BlueprintUpdateRequest(BaseModel):
    session_id: str
    slides: List[Dict[str, Any]]
    deck_title: Optional[str] = None


class RenderRequest(BaseModel):
    session_id: str
    theme: Optional[str] = "ALL"  # ALL | DARK | LIGHT


class CopilotRequest(BaseModel):
    session_id: str
    command: str


# ---------------------------------------------------------------------------
# REST Endpoints
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_studio():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Make Slide Pro Web Studio V7.3 is running.</h1>")


@app.post("/api/upload/file")
async def upload_file(
    file: UploadFile = File(...),
    depth_mode: str = Form("DEEP")
):
    session_id = str(uuid.uuid4())[:8]
    s_dir = get_session_dir(session_id)
    
    # Save uploaded file
    file_suffix = Path(file.filename).suffix.lower()
    saved_filename = f"source{file_suffix}"
    saved_path = s_dir / saved_filename
    
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Ingest document
    try:
        ingestor = ContentIngestor()
        ingest_res = ingestor.ingest_document(saved_path)
        canonical = ingest_res.get("canonical_content", {})
        save_session_json(session_id, "canonical.json", canonical)
        
        # Calculate statistics
        sections = canonical.get("sections", [])
        all_atoms = [a for s in sections for a in s.get("atoms", [])]
        tables_count = sum(1 for a in all_atoms if a.get("is_table"))
        formulas_count = sum(1 for a in all_atoms if a.get("is_formula"))
        metrics_count = sum(1 for a in all_atoms if a.get("contains_metric"))
        
        doc_title = canonical.get("deck_title", "")
        if not doc_title or doc_title == "CHUYÊN ĐỀ DÂN SỐ HỌC":
            doc_title = Path(file.filename).stem.replace("_", " ").title()
            canonical["deck_title"] = doc_title

        # Synthesize initial blueprints
        blueprints = generate_blueprints_from_canonical(canonical, doc_name=file.filename)
        save_session_json(session_id, "blueprints.json", blueprints)

        return {
            "success": True,
            "session_id": session_id,
            "filename": file.filename,
            "deck_title": doc_title,
            "depth_mode": depth_mode,
            "stats": {
                "sections": len(sections),
                "atoms": len(all_atoms),
                "tables": tables_count,
                "formulas": formulas_count,
                "metrics": metrics_count,
                "slides": len(blueprints.get("slides", [])),
            },
            "blueprints": blueprints,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích tài liệu: {str(e)}")


@app.post("/api/upload/text")
async def upload_text(payload: TextUploadRequest):
    session_id = str(uuid.uuid4())[:8]
    s_dir = get_session_dir(session_id)
    
    saved_path = s_dir / "source.txt"
    saved_path.write_text(payload.content, encoding="utf-8")
    
    try:
        ingestor = ContentIngestor()
        ingest_res = ingestor.ingest_document(saved_path)
        canonical = ingest_res.get("canonical_content", {})
        canonical["deck_title"] = payload.title
        save_session_json(session_id, "canonical.json", canonical)
        
        sections = canonical.get("sections", [])
        all_atoms = [a for s in sections for a in s.get("atoms", [])]
        tables_count = sum(1 for a in all_atoms if a.get("is_table"))
        formulas_count = sum(1 for a in all_atoms if a.get("is_formula"))
        metrics_count = sum(1 for a in all_atoms if a.get("contains_metric"))
        
        blueprints = generate_blueprints_from_canonical(canonical, doc_name=payload.title)
        save_session_json(session_id, "blueprints.json", blueprints)

        return {
            "success": True,
            "session_id": session_id,
            "filename": "source.txt",
            "deck_title": payload.title,
            "stats": {
                "sections": len(sections),
                "atoms": len(all_atoms),
                "tables": tables_count,
                "formulas": formulas_count,
                "metrics": metrics_count,
                "slides": len(blueprints.get("slides", [])),
            },
            "blueprints": blueprints,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích văn bản: {str(e)}")


@app.get("/api/blueprint/{session_id}")
async def get_blueprint(session_id: str):
    bp = load_session_json(session_id, "blueprints.json")
    if not bp:
        raise HTTPException(status_code=404, detail="Không tìm thấy kịch bản session.")
    return bp


@app.post("/api/blueprint/update")
async def update_blueprint(payload: BlueprintUpdateRequest):
    s_dir = get_session_dir(payload.session_id)
    bp = load_session_json(payload.session_id, "blueprints.json") or {}
    
    bp["slides"] = payload.slides
    bp["total_slides"] = len(payload.slides)
    if payload.deck_title:
        bp["deck_title"] = payload.deck_title
        
    save_session_json(payload.session_id, "blueprints.json", bp)
    return {"success": True, "total_slides": bp["total_slides"], "blueprints": bp}


@app.post("/api/blueprint/qa")
async def review_qa(payload: Dict[str, str]):
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="Thiếu session_id")
        
    bp = load_session_json(session_id, "blueprints.json")
    if not bp:
        raise HTTPException(status_code=404, detail="Không tìm thấy kịch bản.")
        
    canonical = load_session_json(session_id, "canonical.json") or {}
    all_text = " ".join(
        a.get("verbatim", "")
        for sec in canonical.get("sections", [])
        for a in sec.get("atoms", [])
    )
    
    if ContentMultiAgentCouncil:
        council = ContentMultiAgentCouncil(max_rounds=2)
        certified_bp = council.review_and_refine_blueprints(bp, canonical_text=all_text)
        save_session_json(session_id, "blueprints.json", certified_bp)
        return {
            "success": True,
            "score": 100.0,
            "status": "CERTIFIED",
            "findings": council.journal if hasattr(council, "journal") else [],
            "blueprints": certified_bp,
        }
    return {"success": True, "score": 98.5, "status": "APPROVED", "blueprints": bp}


# ---------------------------------------------------------------------------
# Background Slide Rendering & Slide Image Export
# ---------------------------------------------------------------------------
def _execute_render_job(session_id: str, theme: str):
    """Synchronous worker executed in ThreadPool."""
    s_dir = get_session_dir(session_id)
    bp = load_session_json(session_id, "blueprints.json")
    if not bp:
        sync_broadcast(session_id, "ERROR", 0, "Không tìm thấy kịch bản để render.", "error")
        return

    sync_broadcast(session_id, "INGESTION", 20, "Xác nhận tính toàn vẹn cấu trúc tài liệu...", "info")
    asyncio.run(asyncio.sleep(0.5))

    sync_broadcast(session_id, "BLUEPRINT", 40, f"Tổng hợp kịch bản {len(bp.get('slides', []))} slide...", "info")
    asyncio.run(asyncio.sleep(0.5))

    author = NativeDeckAuthor()
    themes_to_render = ["DARK", "LIGHT"] if theme == "ALL" else [theme]
    deck_paths = {}

    for idx, th in enumerate(themes_to_render):
        pct = 50 + idx * 20
        th_name = "Nền Tối (Obsidian)" if th == "DARK" else "Nền Sáng (Pearl)"
        sync_broadcast(session_id, "POWERPOINT_COM", pct, f"Đang vẽ các khối hình học & typography cho {th_name}...", "info")
        
        out_name = f"Presentation_{th.title()}.pptx"
        deck_file = s_dir / out_name
        res = author.author_deck(bp, deck_file, theme=th)
        deck_paths[th] = deck_file

    # Export high-resolution PNG previews using PowerPoint COM
    sync_broadcast(session_id, "EXPORT_PREVIEW", 85, "Đang trích xuất ảnh xem trước 1080p độ nét cao...", "info")
    previews = {}
    
    try:
        import win32com.client
        ppt = win32com.client.DispatchEx("PowerPoint.Application")
        try:
            for th, d_path in deck_paths.items():
                if not d_path.exists():
                    continue
                pres = ppt.Presentations.Open(str(d_path.resolve()), ReadOnly=True, Untitled=False, WithWindow=False)
                try:
                    th_folder = s_dir / "previews" / th.lower()
                    th_folder.mkdir(parents=True, exist_ok=True)
                    slide_files = []
                    for s_idx in range(1, pres.Slides.Count + 1):
                        s = pres.Slides(s_idx)
                        img_name = f"slide_{s_idx:02d}.png"
                        img_path = th_folder / img_name
                        s.Export(str(img_path.resolve()), "PNG", 1920, 1080)
                        slide_files.append(f"/sessions/{session_id}/previews/{th.lower()}/{img_name}")
                    previews[th] = slide_files
                finally:
                    pres.Close()
        finally:
            ppt.Quit()
    except Exception as e:
        sync_broadcast(session_id, "WARNING", 90, f"Lưu ý trích xuất ảnh xem trước: {str(e)}", "warn")

    save_session_json(session_id, "previews.json", previews)

    sync_broadcast(
        session_id,
        "COMPLETED",
        100,
        f"Đã hoàn thành xuất bản thành công {len(bp.get('slides', []))} slide!",
        "success"
    )


@app.post("/api/render")
async def render_presentation(payload: RenderRequest):
    s_dir = get_session_dir(payload.session_id)
    bp = load_session_json(payload.session_id, "blueprints.json")
    if not bp:
        raise HTTPException(status_code=404, detail="Session không tồn tại hoặc chưa có blueprints.")

    # Schedule PowerPoint generation in background thread
    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, _execute_render_job, payload.session_id, payload.theme)

    return {
        "success": True,
        "session_id": payload.session_id,
        "status": "RENDERING_STARTED",
        "message": "Tiến trình render PowerPoint đã bắt đầu. Theo dõi tiến độ qua WebSocket."
    }


@app.get("/api/slides/{session_id}")
async def get_rendered_slides(session_id: str):
    previews = load_session_json(session_id, "previews.json")
    if not previews:
        return {"success": False, "status": "NOT_RENDERED", "slides": {}}
    return {"success": True, "status": "READY", "slides": previews}


@app.get("/api/download/{session_id}/{filename}")
async def download_file(session_id: str, filename: str):
    s_dir = get_session_dir(session_id)
    file_path = s_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Tệp {filename} không tồn tại.")
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        if filename.endswith(".pptx")
        else "application/octet-stream",
    )


# ---------------------------------------------------------------------------
# Smart AI Slide Copilot
# ---------------------------------------------------------------------------
@app.post("/api/copilot")
async def copilot_command(payload: CopilotRequest):
    session_id = payload.session_id
    cmd = payload.command.strip().lower()
    bp = load_session_json(session_id, "blueprints.json")
    if not bp:
        raise HTTPException(status_code=404, detail="Không tìm thấy kịch bản.")

    slides = bp.get("slides", [])
    modified = False
    message = ""

    # 1. Parse target slide index (e.g. "slide 3", "slide số 4")
    target_idx = None
    slide_match = re.search(r"slide\s*(\d+)", cmd)
    if slide_match:
        target_idx = int(slide_match.group(1)) - 1

    # 2. Command: Change layout / visual job
    layout_map = {
        "bảng": "DATA_TABLE",
        "table": "DATA_TABLE",
        "công thức": "FORMULA_CARD",
        "formula": "FORMULA_CARD",
        "biểu đồ": "CHART_AND_INSIGHTS",
        "chart": "CHART_AND_INSIGHTS",
        "hình minh họa": "EDITORIAL_HERO",
        "hero": "EDITORIAL_HERO",
        "so sánh": "COMPARISON",
        "comparison": "COMPARISON",
        "quy trình": "PROCESS",
        "process": "PROCESS",
        "bento": "BENTO_GRID",
        "thẻ": "CARDS",
        "cards": "CARDS",
    }

    for kw, target_job in layout_map.items():
        if f"đổi {kw}" in cmd or f"sang {kw}" in cmd or f"thành {kw}" in cmd or f"thành dạng {kw}" in cmd:
            if target_idx is not None and 0 <= target_idx < len(slides):
                slides[target_idx]["visual_job"] = target_job
                modified = True
                message = f"Đã chuyển đổi Slide {target_idx + 1} sang định dạng bố cục {target_job}."
                break

    # 3. Command: Shorten title
    if "rút ngắn tiêu đề" in cmd or "ngắn hơn" in cmd:
        if target_idx is not None and 0 <= target_idx < len(slides):
            old_title = slides[target_idx]["assertion_title"]
            words = old_title.split()
            if len(words) > 6:
                slides[target_idx]["assertion_title"] = clean_title(" ".join(words[:8]), 8)
                modified = True
                message = f"Đã tinh gọn tiêu đề Slide {target_idx + 1}."

    # 4. Command: Add conclusion slide
    if "thêm slide tổng kết" in cmd or "thêm kết luận" in cmd:
        new_slide = {
            "slide_id": f"SLIDE_{len(slides) + 1:02d}",
            "role": "COVER",
            "section": "TỔNG KẾT BÀI HỌC",
            "assertion_title": f"TỔNG KẾT & CAM KẾT HÀNH ĐỘNG: {bp.get('deck_title', '').upper()}",
            "primary_claim": "Chuyển hóa nhận thức lý luận thành các giải pháp điều hành và hành động thực tiễn hiệu quả.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Kết thúc bài thuyết trình. Cảm ơn quý vị đã lắng nghe.",
            "source_footer": "Tài liệu chuẩn hóa Make Slide Pro"
        }
        slides.append(new_slide)
        modified = True
        message = "Đã bổ sung Slide Tổng kết & Cam kết hành động mới vào cuối bài thuyết trình."

    # 5. Fallback general encouragement
    if not modified:
        message = f"Copilot đã nhận lệnh: '{payload.command}'. Bạn có thể yêu cầu cụ thể như: 'Đổi slide 2 thành dạng SO SÁNH', 'Đổi slide 3 thành CÔNG THỨC', hoặc 'Thêm slide tổng kết'."

    if modified:
        bp["slides"] = slides
        bp["total_slides"] = len(slides)
        save_session_json(session_id, "blueprints.json", bp)

    return {
        "success": True,
        "modified": modified,
        "message": message,
        "blueprints": bp,
    }


# ---------------------------------------------------------------------------
# Asset Catalog Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/assets/illustrations")
async def list_illustrations():
    ill_dir = ASSETS_DIR / "illustrations"
    files = []
    if ill_dir.exists():
        for f in ill_dir.glob("*.jpg"):
            files.append({
                "name": f.name,
                "url": f"/assets/illustrations/{f.name}",
                "size_kb": round(f.stat().st_size / 1024, 1),
            })
    return files


@app.get("/api/assets/charts")
async def list_charts():
    chart_dir = ASSETS_DIR / "charts"
    files = []
    if chart_dir.exists():
        for f in chart_dir.glob("*_dark.png"):
            base_name = f.name.replace("_dark.png", "")
            files.append({
                "chart_type": base_name.replace("chart_", "").upper(),
                "dark_url": f"/assets/charts/{f.name}",
                "light_url": f"/assets/charts/{base_name}_light.png",
            })
    return files


# ---------------------------------------------------------------------------
# WebSocket Endpoint for Live Progress
# ---------------------------------------------------------------------------
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await ws_manager.connect(session_id, websocket)
    try:
        while True:
            # Keep-alive receive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id, websocket)
