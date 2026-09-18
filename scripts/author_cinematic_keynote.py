# author_cinematic_keynote.py
# World-Class Cinematic Spatial Keynote Authoring Engine for Make Slide Pro V6.2
# High-end Dark Luxury Obsidian theme, bespoke 3D spatial artworks, unbroken Morph Zoom-Through,
# and in-slide presenter click sequencing (AdvanceOnClick).

from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path
from typing import Any, List, Optional

try:
    import win32com.client
    import pythoncom
except ImportError:
    win32com = None

# PowerPoint Constants
ppLayoutBlank = 12
msoShapeRectangle = 1
msoShapeRoundedRectangle = 5
msoShapeOval = 9
msoTextOrientationHorizontal = 1
ppAlignLeft = 1
ppAlignCenter = 2
ppAlignRight = 3
msoTrue = -1
msoFalse = 0

# Animation Constants
msoAnimTriggerOnPageClick = 1
msoAnimTriggerWithPrevious = 2
msoAnimTriggerAfterPrevious = 3
msoAnimEffectFade = 10
msoAnimEffectFly = 2
msoAnimateLevelNone = 0

# Transition Constants
ppTransitionFadeSmoothly = 3849
ppEffectMorphByObject = 3954

# Canvas Dimensions (16:9 Widescreen)
CANVAS_WIDTH = 960.0
CANVAS_HEIGHT = 540.0

# Color Tokens (Dark Luxury Obsidian)
DARK_KEYNOTE_TOKENS = {
    'bg_obsidian': '#060B14',
    'card_bg': '#0B132B',
    'card_border': '#1E293B',
    'hero_border': '#0284C7',
    'text_white': '#FFFFFF',
    'text_heading': '#F8FAFC',
    'text_body': '#CBD5E1',
    'text_muted': '#94A3B8',
    'cyan': '#06B6D4',
    'cyan_light': '#38BDF8',
    'cyan_bg': '#082F49',
    'emerald': '#10B981',
    'emerald_light': '#34D399',
    'emerald_bg': '#064E3B',
    'amber': '#F59E0B',
    'amber_light': '#FBBF24',
    'amber_bg': '#451A03',
    'violet': '#8B5CF6',
    'violet_light': '#A78BFA',
    'violet_bg': '#2E1065',
    'font_main': 'Segoe UI',
    'font_metric': 'Bahnschrift',
}

# Color Tokens (Clean Editorial Light / Executive Pearl Ivory)
LIGHT_KEYNOTE_TOKENS = {
    'bg_obsidian': '#F8FAFC',      # Clean Light Canvas (Slate 50)
    'card_bg': '#FFFFFF',          # Crisp White Card Surface
    'card_border': '#CBD5E1',      # Slate 300 Subtle Border
    'hero_border': '#0284C7',      # Sapphire Hero Accent
    'text_white': '#0F172A',       # Slate 900 High Contrast Text
    'text_heading': '#0F172A',     # Slate 900
    'text_body': '#334155',        # Slate 700 Readable Body Copy
    'text_muted': '#64748B',       # Slate 500 Caption / Kicker
    'cyan': '#0284C7',             # Sapphire Blue
    'cyan_light': '#0369A1',       # Deep Blue
    'cyan_bg': '#E0F2FE',          # Soft Sky Tint
    'emerald': '#059669',          # Forest Emerald
    'emerald_light': '#047857',    # Deep Forest
    'emerald_bg': '#D1FAE5',       # Soft Emerald Tint
    'amber': '#D97706',            # Warm Amber
    'amber_light': '#B45309',      # Deep Ochre
    'amber_bg': '#FEF3C7',         # Soft Amber Tint
    'violet': '#7C3AED',           # Royal Violet
    'violet_light': '#6D28D9',     # Deep Violet
    'violet_bg': '#EDE9FE',        # Soft Violet Tint
    'font_main': 'Segoe UI',
    'font_metric': 'Bahnschrift',
}

TOKENS = DARK_KEYNOTE_TOKENS

ICONS_DIR = Path('assets/icons')
ILLUSTRATIONS_DIR = Path('assets/illustrations')

def hex_to_bgr(hex_color: str) -> int:
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return r + (g * 256) + (b * 65536)

class CinematicKeynoteEngine:
    def __init__(self, theme: str = "DARK"):
        if win32com is None:
            raise RuntimeError('win32com is not available. Please install pywin32.')
        self.set_theme(theme)
        pythoncom.CoInitialize()
        try:
            self.app = win32com.client.GetActiveObject('PowerPoint.Application')
        except Exception:
            self.app = win32com.client.DispatchEx('PowerPoint.Application')
        self.app.Visible = msoTrue
        self.presentation = self.app.Presentations.Add()
        self.presentation.PageSetup.SlideWidth = CANVAS_WIDTH
        self.presentation.PageSetup.SlideHeight = CANVAS_HEIGHT

    def set_theme(self, theme: str):
        self.theme = theme.upper()
        global TOKENS
        TOKENS = LIGHT_KEYNOTE_TOKENS if self.theme == "LIGHT" else DARK_KEYNOTE_TOKENS

    def add_blank_slide(self):
        blank_slide = self.presentation.Slides.Add(self.presentation.Slides.Count + 1, ppLayoutBlank)
        blank_slide.FollowMasterBackground = msoFalse
        blank_slide.Background.Fill.Solid()
        blank_slide.Background.Fill.ForeColor.RGB = hex_to_bgr(TOKENS['bg_obsidian'])
        return blank_slide

    def set_slide_transition(self, slide, is_morph: bool = True, duration: float = 0.9):
        trans = slide.SlideShowTransition
        if is_morph:
            trans.EntryEffect = ppEffectMorphByObject
            trans.Duration = duration
        else:
            trans.EntryEffect = ppTransitionFadeSmoothly
            trans.Duration = 0.6
        trans.AdvanceOnClick = msoTrue
        trans.AdvanceOnTime = msoFalse

    def add_card(self, slide, left: float, top: float, width: float, height: float,
                 fill_hex: str = TOKENS['card_bg'], border_hex: str = TOKENS['card_border'],
                 border_width: float = 1.0, name: Optional[str] = None):
        shape = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        shape.Fill.Solid()
        shape.Fill.ForeColor.RGB = hex_to_bgr(fill_hex)
        if border_hex:
            shape.Line.Visible = msoTrue
            shape.Line.ForeColor.RGB = hex_to_bgr(border_hex)
            shape.Line.Weight = border_width
        else:
            shape.Line.Visible = msoFalse
        if name:
            shape.Name = name
        return shape

    def add_badge(self, slide, left: float, top: float, width: float, height: float,
                  text: str, bg_hex: str, text_hex: str, font_size: float = 10.5, name: Optional[str] = None):
        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(bg_hex)
        card.Line.Visible = msoFalse
        tf = card.TextFrame
        tf.MarginLeft = 6
        tf.MarginRight = 6
        tf.MarginTop = 2
        tf.MarginBottom = 2
        tf.VerticalAnchor = 3  # msoAnchorMiddle
        tr = tf.TextRange
        tr.Text = text
        tr.Font.Name = TOKENS['font_main']
        tr.Font.Size = font_size
        tr.Font.Bold = msoTrue
        tr.Font.Color.RGB = hex_to_bgr(text_hex)
        tr.ParagraphFormat.Alignment = ppAlignCenter
        if name:
            card.Name = name
        return card

    def add_text(self, slide, left: float, top: float, width: float, height: float,
                 text: str, font_size: float = 14.0, color_hex: str = TOKENS['text_body'],
                 bold: bool = False, font_name: str = TOKENS['font_main'], align: int = ppAlignLeft,
                 line_spacing: float = 1.2, name: Optional[str] = None):
        box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left, top, width, height)
        tf = box.TextFrame
        tf.WordWrap = msoTrue
        tf.MarginLeft = 0
        tf.MarginRight = 0
        tf.MarginTop = 0
        tf.MarginBottom = 0
        tr = tf.TextRange
        tr.Text = text
        tr.Font.Name = font_name
        tr.Font.Size = font_size
        tr.Font.Bold = msoTrue if bold else msoFalse
        tr.Font.Color.RGB = hex_to_bgr(color_hex)
        tr.ParagraphFormat.Alignment = align
        if line_spacing != 1.0:
            tr.ParagraphFormat.LineRuleWithin = msoFalse
            tr.ParagraphFormat.SpaceWithin = font_size * line_spacing
        if name:
            box.Name = name
        return box

    def add_icon(self, slide, icon_name: str, left: float, top: float, size: float = 24.0, name: Optional[str] = None):
        svg_file = ICONS_DIR / f'{icon_name}.svg'
        if svg_file.exists():
            try:
                pic = slide.Shapes.AddPicture(str(svg_file.resolve()), False, True, left, top, size, size)
                if name:
                    pic.Name = name
                return pic
            except Exception:
                pass
        return None

    def add_image(self, slide, img_path: Path, left: float, top: float, width: float, height: float, name: Optional[str] = None):
        if img_path.exists():
            pic = slide.Shapes.AddPicture(str(img_path.resolve()), False, True, left, top, width, height)
            if name:
                pic.Name = name
            return pic
        return None

    def group_and_animate(self, slide, shapes: List[Any], duration: float = 0.45,
                          trigger: int = msoAnimTriggerOnPageClick, effect: int = msoAnimEffectFly,
                          group_name: Optional[str] = None):
        valid = [s for s in shapes if s is not None]
        if not valid:
            return None
        if len(valid) == 1:
            grp = valid[0]
        else:
            names = [s.Name for s in valid]
            grp = slide.Shapes.Range(names).Group()
        if group_name:
            try:
                grp.Name = group_name
            except Exception:
                pass
        anim = slide.TimeLine.MainSequence.AddEffect(grp, effect, msoAnimateLevelNone, trigger)
        anim.Timing.Duration = duration
        anim.Timing.SmoothStart = msoTrue
        anim.Timing.SmoothEnd = msoTrue
        return grp

    def build_slide_1(self):
        slide = self.add_blank_slide()
        self.set_slide_transition(slide, is_morph=False)

        # Left Column
        self.add_badge(slide, 48, 50, 210, 26, '01 // CHUYÊN ĐỀ DÂN SỐ HỌC', TOKENS['cyan_bg'], TOKENS['cyan_light'], 10.5)
        self.add_text(slide, 48, 88, 390, 110, 'KHOA HỌC DÂN SỐ\nVÀ PHÁT TRIỂN', 36, TOKENS['text_white'], bold=True)
        self.add_text(slide, 48, 205, 380, 50, 'Hệ thống hóa quy luật biến động, cấu trúc nhân khẩu học và các chiến lược định hình tương lai quốc gia.', 13.5, TOKENS['text_muted'])

        # Left Stat Cards
        c1 = self.add_card(slide, 48, 275, 185, 120, TOKENS['card_bg'], TOKENS['card_border'])
        t1_num = self.add_text(slide, 64, 290, 150, 44, '8.1 TỶ', 34, TOKENS['cyan_light'], bold=True, font_name=TOKENS['font_metric'])
        t1_lbl = self.add_text(slide, 64, 340, 150, 40, 'Dân số toàn cầu (2024)\nQuy mô lịch sử', 11, TOKENS['text_muted'])

        c2 = self.add_card(slide, 248, 275, 185, 120, TOKENS['card_bg'], TOKENS['card_border'])
        t2_num = self.add_text(slide, 264, 290, 150, 44, '100.3 TR', 34, TOKENS['emerald_light'], bold=True, font_name=TOKENS['font_metric'])
        t2_lbl = self.add_text(slide, 264, 340, 150, 40, 'Dân số Việt Nam\nHạng 15 toàn cầu', 11, TOKENS['text_muted'])

        # Right Stage: The Monolith Visual Anchor
        hero_img = ILLUSTRATIONS_DIR / 'cinematic_bai_1_hero.jpg'
        self.add_image(slide, hero_img, 460, 50, 452, 440, name='!!Stage_Hero_Container')

    def build_slide_2(self):
        slide = self.add_blank_slide()
        self.set_slide_transition(slide, is_morph=True, duration=0.9)

        # Header
        self.add_badge(slide, 48, 40, 240, 24, 'KHÁI NIỆM & ĐỐI TƯỢNG NGHIÊN CỨU', TOKENS['cyan_bg'], TOKENS['cyan_light'], 10)
        self.add_text(slide, 48, 70, 600, 36, 'Bản Chất Cốt Lõi Của Dân Số Học', 26, TOKENS['text_white'], bold=True)

        # Left Stage: The Hero Container Morphs to the Left Side!
        hero_img = ILLUSTRATIONS_DIR / 'cinematic_bai_1_hero.jpg'
        self.add_image(slide, hero_img, 48, 115, 330, 385, name='!!Stage_Hero_Container')

        # Right Stage: Card 1 (Sequential On Click 1)
        c1 = self.add_card(slide, 405, 115, 507, 180, TOKENS['card_bg'], TOKENS['card_border'])
        ic1 = self.add_icon(slide, 'layers', 425, 135, 26)
        k1 = self.add_text(slide, 460, 133, 430, 20, '01 / ĐỐI TƯỢNG NGHIÊN CỨU ĐA CHIỀU', 11, TOKENS['cyan_light'], bold=True)
        t1 = self.add_text(slide, 425, 165, 465, 26, 'Quy luật biến động và phân bố nhân khẩu', 17, TOKENS['text_white'], bold=True)
        d1 = self.add_text(slide, 425, 198, 465, 56, 'Dân số học là khoa học nghiên cứu quy mô, cơ cấu lứa tuổi, tỷ lệ giới tính, phân bố không gian và các động thái biến động tự nhiên (sinh, chết) cùng biến động cơ học (di cư).', 13, TOKENS['text_body'])
        b1 = self.add_badge(slide, 425, 258, 170, 24, '4 Chiều Kích Phân Tích', TOKENS['cyan_bg'], TOKENS['cyan_light'], 9.5)
        self.group_and_animate(slide, [c1, ic1, k1, t1, d1, b1], trigger=msoAnimTriggerOnPageClick, group_name='!!Stage_Sub_Card_1')

        # Right Stage: Card 2 (Sequential On Click 2)
        c2 = self.add_card(slide, 405, 315, 507, 185, TOKENS['card_bg'], TOKENS['card_border'])
        ic2 = self.add_icon(slide, 'compass', 425, 335, 26)
        k2 = self.add_text(slide, 460, 333, 430, 20, '02 / SỨ MỆNH & GIÁ TRỊ THỰC TIỄN', 11, TOKENS['emerald_light'], bold=True)
        t2 = self.add_text(slide, 425, 365, 465, 26, 'La bàn khoa học cho phát triển bền vững', 17, TOKENS['text_white'], bold=True)
        d2 = self.add_text(slide, 425, 398, 465, 56, 'Cung cấp luận cứ thực chứng và hệ thống dự báo nhân khẩu học chính xác, làm nền tảng cốt lõi để xây dựng chiến lược phát triển kinh tế, an sinh xã hội, y tế và giáo dục quốc gia.', 13, TOKENS['text_body'])
        b2 = self.add_badge(slide, 425, 458, 220, 24, 'Nền Tảng Hoạch Định Chiến Lược', TOKENS['emerald_bg'], TOKENS['emerald_light'], 9.5)
        self.group_and_animate(slide, [c2, ic2, k2, t2, d2, b2], trigger=msoAnimTriggerOnPageClick, group_name='!!Stage_Sub_Card_2')

    def build_slide_3(self):
        slide = self.add_blank_slide()
        self.set_slide_transition(slide, is_morph=True, duration=0.9)

        # Header
        self.add_badge(slide, 48, 40, 230, 24, 'TAM GIÁC ĐỘNG THÁI DÂN SỐ', TOKENS['cyan_bg'], TOKENS['cyan_light'], 10)
        self.add_text(slide, 48, 70, 700, 36, 'Ba Trụ Cột Quyết Định Cấu Trúc Dân Số', 26, TOKENS['text_white'], bold=True)

        # Pillar 1 (Named !!Stage_Hero_Container so it smoothly morphs from Slide 2!)
        p1 = self.add_card(slide, 48, 115, 268, 385, TOKENS['card_bg'], TOKENS['cyan'], border_width=1.5, name='!!Stage_Hero_Container')
        ic1 = self.add_icon(slide, 'activity', 68, 135, 28)
        t1 = self.add_text(slide, 68, 172, 228, 26, 'Mức Sinh (Fertility)', 18, TOKENS['text_white'], bold=True)
        m1 = self.add_text(slide, 68, 205, 228, 44, '1.96', 36, TOKENS['cyan_light'], bold=True, font_name=TOKENS['font_metric'])
        l1 = self.add_text(slide, 68, 252, 228, 30, 'Tổng tỷ suất sinh (TFR VN 2023)\nNgưỡng thay thế chuẩn: 2.1', 11, TOKENS['text_muted'])
        b1_text = '• Xu hướng giảm sâu tại các đô thị lớn\n• Phụ nữ kết hôn muộn và giảm sinh\n• Tác động trực tiếp quy mô lao động tương lai'
        b1 = self.add_text(slide, 68, 295, 228, 140, b1_text, 12.5, TOKENS['text_body'], line_spacing=1.35)

        # Pillar 2 (Sequential On Click 1)
        p2 = self.add_card(slide, 346, 115, 268, 385, TOKENS['card_bg'], TOKENS['emerald'], border_width=1.5)
        ic2 = self.add_icon(slide, 'workflow', 366, 135, 28)
        t2 = self.add_text(slide, 366, 172, 228, 26, 'Mức Chết (Mortality)', 18, TOKENS['text_white'], bold=True)
        m2 = self.add_text(slide, 366, 205, 228, 44, '73.7 Tuổi', 36, TOKENS['emerald_light'], bold=True, font_name=TOKENS['font_metric'])
        l2 = self.add_text(slide, 366, 252, 228, 30, 'Tuổi thọ bình quân cả nước\nTăng ấn tượng qua 3 thập kỷ', 11, TOKENS['text_muted'])
        b2_text = '• Giảm mạnh tỷ lệ tử vong sơ sinh\n• Mô hình bệnh tật kép (bệnh không lây nhiễm)\n• Đòi hỏi chuyển dịch mạng lưới y tế lão khoa'
        b2 = self.add_text(slide, 366, 295, 228, 140, b2_text, 12.5, TOKENS['text_body'], line_spacing=1.35)
        self.group_and_animate(slide, [p2, ic2, t2, m2, l2, b2], trigger=msoAnimTriggerOnPageClick, group_name='!!Pillar_Card_2')

        # Pillar 3 (Sequential On Click 2)
        p3 = self.add_card(slide, 644, 115, 268, 385, TOKENS['card_bg'], TOKENS['amber'], border_width=1.5)
        ic3 = self.add_icon(slide, 'globe', 664, 135, 28)
        t3 = self.add_text(slide, 664, 172, 228, 26, 'Di Cư (Migration)', 18, TOKENS['text_white'], bold=True)
        m3 = self.add_text(slide, 664, 205, 228, 44, '38.1%', 36, TOKENS['amber_light'], bold=True, font_name=TOKENS['font_metric'])
        l3 = self.add_text(slide, 664, 252, 228, 30, 'Tỷ lệ đô thị hóa quốc gia\nĐộng lực kinh tế không gian', 11, TOKENS['text_muted'])
        b3_text = '• Di cư nông thôn - đô thị chiếm ưu thế\n• Dòng dịch chuyển lao động liên vùng mạnh\n• Áp lực lớn lên hạ tầng dịch vụ công'
        b3 = self.add_text(slide, 664, 295, 228, 140, b3_text, 12.5, TOKENS['text_body'], line_spacing=1.35)
        self.group_and_animate(slide, [p3, ic3, t3, m3, l3, b3], trigger=msoAnimTriggerOnPageClick, group_name='!!Pillar_Card_3')

    def build_slide_4(self):
        slide = self.add_blank_slide()
        self.set_slide_transition(slide, is_morph=True, duration=0.9)

        # Header
        self.add_badge(slide, 48, 40, 230, 24, 'CƠ CẤU NHÂN KHẨU HỌC', TOKENS['cyan_bg'], TOKENS['cyan_light'], 10)
        self.add_text(slide, 48, 70, 700, 36, 'Cửa Sổ Dân Số Vàng & Thách Thức Già Hóa', 26, TOKENS['text_white'], bold=True)

        # Left Stage: Card A (Sequential On Click 1)
        cA = self.add_card(slide, 48, 115, 452, 180, TOKENS['card_bg'], TOKENS['card_border'])
        icA = self.add_icon(slide, 'trending-up', 68, 135, 26)
        mA = self.add_text(slide, 105, 128, 150, 42, '68.0%', 36, TOKENS['cyan_light'], bold=True, font_name=TOKENS['font_metric'])
        tA = self.add_text(slide, 68, 175, 412, 24, 'Dân Số Trong Độ Tuổi Lao Động (15-64)', 15, TOKENS['text_white'], bold=True)
        dA = self.add_text(slide, 68, 205, 412, 65, 'Việt Nam đang trong thời kỳ "Dân số vàng" với tỷ lệ người phụ thuộc dưới 50%. Đây là dư địa vàng thúc đẩy năng suất và tích lũy của cải trước khi bước sang giai đoạn già hóa.', 12.5, TOKENS['text_body'], line_spacing=1.3)
        self.group_and_animate(slide, [cA, icA, mA, tA, dA], trigger=msoAnimTriggerOnPageClick, group_name='!!Card_Gold_Pop')

        # Left Stage: Card B (Sequential On Click 2)
        cB = self.add_card(slide, 48, 315, 452, 185, TOKENS['card_bg'], TOKENS['card_border'])
        icB = self.add_icon(slide, 'clock', 68, 335, 26)
        mB = self.add_text(slide, 105, 328, 150, 42, '< 20 Năm', 36, TOKENS['amber_light'], bold=True, font_name=TOKENS['font_metric'])
        tB = self.add_text(slide, 68, 375, 412, 24, 'Tốc Độ Già Hóa Nhanh Hàng Đầu Thế Giới', 15, TOKENS['text_white'], bold=True)
        dB = self.add_text(slide, 68, 405, 412, 70, 'Thời gian chuyển từ "già hóa" (7% người >65t) sang "dân số già" (14%) của Việt Nam thuộc nhóm nhanh nhất thế giới. Nguy cơ "chưa giàu đã già" đòi hỏi hành động quyết liệt ngay từ bây giờ.', 12.5, TOKENS['text_body'], line_spacing=1.3)
        self.group_and_animate(slide, [cB, icB, mB, tB, dB], trigger=msoAnimTriggerOnPageClick, group_name='!!Card_Aging_Pop')

        # Right Stage: The 3D System Diagram Morphs into Place!
        sys_img = ILLUSTRATIONS_DIR / 'cinematic_bai_1_system.jpg'
        self.add_image(slide, sys_img, 526, 115, 386, 385, name='!!Stage_Hero_Container')

    def build_slide_5(self):
        slide = self.add_blank_slide()
        self.set_slide_transition(slide, is_morph=True, duration=0.9)

        # Header
        self.add_badge(slide, 48, 40, 230, 24, 'HỆ SINH THÁI TÁC ĐỘNG TỔNG THỂ', TOKENS['cyan_bg'], TOKENS['cyan_light'], 10)
        self.add_text(slide, 48, 70, 750, 36, '4 Chiều Kích Tác Động Đến Phát Triển Quốc Gia', 26, TOKENS['text_white'], bold=True)

        # Quadrant 1 (Click 1)
        q1 = self.add_card(slide, 48, 115, 420, 180, TOKENS['card_bg'], TOKENS['cyan'], border_width=1.5)
        iq1 = self.add_icon(slide, 'trending-up', 68, 133, 24)
        kq1 = self.add_text(slide, 100, 131, 350, 20, '01 // KINH TẾ & THỊ TRƯỜNG LAO ĐỘNG', 11, TOKENS['cyan_light'], bold=True)
        tq1 = self.add_text(slide, 68, 162, 380, 24, 'Quy Mô & Năng Suất Nguồn Nhân Lực', 15, TOKENS['text_white'], bold=True)
        dq1 = self.add_text(slide, 68, 192, 380, 75, 'Quy mô nguồn nhân lực quyết định trực tiếp tiềm năng tăng trưởng GDP, năng suất lao động và năng lực hấp thụ các dòng vốn đầu tư trực tiếp nước ngoài (FDI).', 12.5, TOKENS['text_body'], line_spacing=1.3)
        self.group_and_animate(slide, [q1, iq1, kq1, tq1, dq1], trigger=msoAnimTriggerOnPageClick, group_name='!!Quad_1')

        # Quadrant 2 (Click 2)
        q2 = self.add_card(slide, 492, 115, 420, 180, TOKENS['card_bg'], TOKENS['emerald'], border_width=1.5)
        iq2 = self.add_icon(slide, 'activity', 512, 133, 24)
        kq2 = self.add_text(slide, 544, 131, 350, 20, '02 // AN SINH XÃ HỘI & Y TẾ LÃO KHOA', 11, TOKENS['emerald_light'], bold=True)
        tq2 = self.add_text(slide, 512, 162, 380, 24, 'Áp Lực Quỹ Hưu Trí & Chăm Sóc Dài Hạn', 15, TOKENS['text_white'], bold=True)
        dq2 = self.add_text(slide, 512, 192, 380, 75, 'Cân đối quỹ bảo hiểm xã hội, phát triển bảo hiểm y tế toàn dân và xây dựng mạng lưới viện dưỡng lão thích ứng với cộng đồng người cao tuổi.', 12.5, TOKENS['text_body'], line_spacing=1.3)
        self.group_and_animate(slide, [q2, iq2, kq2, tq2, dq2], trigger=msoAnimTriggerOnPageClick, group_name='!!Quad_2')

        # Quadrant 3 (Click 3)
        q3 = self.add_card(slide, 48, 315, 420, 185, TOKENS['card_bg'], TOKENS['violet'], border_width=1.5)
        iq3 = self.add_icon(slide, 'book-open', 68, 333, 24)
        kq3 = self.add_text(slide, 100, 331, 350, 20, '03 // GIÁO DỤC & NÂNG CAO VỐN NGƯỜI', 11, TOKENS['violet_light'], bold=True)
        tq3 = self.add_text(slide, 68, 362, 380, 24, 'Chuyển Trọng Tâm Sang Chất Lượng', 15, TOKENS['text_white'], bold=True)
        dq3 = self.add_text(slide, 68, 392, 380, 75, 'Chuyển trọng tâm từ khai thác lao động giá rẻ sang đào tạo kỹ năng số, chuyên môn cao và đổi mới sáng tạo, bứt phá khỏi bẫy thu nhập trung bình.', 12.5, TOKENS['text_body'], line_spacing=1.3)
        self.group_and_animate(slide, [q3, iq3, kq3, tq3, dq3], trigger=msoAnimTriggerOnPageClick, group_name='!!Quad_3')

        # Quadrant 4 (Click 4)
        q4 = self.add_card(slide, 492, 315, 420, 185, TOKENS['card_bg'], TOKENS['amber'], border_width=1.5)
        iq4 = self.add_icon(slide, 'map-pin', 512, 333, 24)
        kq4 = self.add_text(slide, 544, 331, 350, 20, '04 // QUY HOẠCH ĐÔ THỊ & TÀI NGUYÊN', 11, TOKENS['amber_light'], bold=True)
        tq4 = self.add_text(slide, 512, 362, 380, 24, 'Phân Bổ Cư Dân & Giảm Tải Hạ Tầng', 15, TOKENS['text_white'], bold=True)
        dq4 = self.add_text(slide, 512, 392, 380, 75, 'Quy hoạch phân bổ dân cư hợp lý, giải tỏa quá tải siêu đô thị và phát triển chuỗi đô thị vệ tinh sinh thái, thích ứng với biến đổi khí hậu.', 12.5, TOKENS['text_body'], line_spacing=1.3)
        self.group_and_animate(slide, [q4, iq4, kq4, tq4, dq4], trigger=msoAnimTriggerOnPageClick, group_name='!!Quad_4')

    def build_slide_6(self):
        slide = self.add_blank_slide()
        self.set_slide_transition(slide, is_morph=True, duration=0.9)

        # Header
        self.add_badge(slide, 48, 40, 230, 24, 'TỔNG KẾT & TẦM NHÌN HÀNH ĐỘNG', TOKENS['cyan_bg'], TOKENS['cyan_light'], 10)
        self.add_text(slide, 48, 70, 750, 36, 'Khuyến Nghị Chiến Lược Cho Nhà Hoạch Định', 26, TOKENS['text_white'], bold=True)

        # Hero Summary Banner (Named !!Stage_Hero_Container so it morphs seamlessly!)
        sb = self.add_card(slide, 48, 115, 864, 75, TOKENS['card_bg'], TOKENS['hero_border'], border_width=1.5, name='!!Stage_Hero_Container')
        quote = '“Dân số là gốc rễ của mọi nguồn lực quốc gia. Chính sách kinh tế - xã hội tách rời quy luật nhân khẩu học sẽ luôn đối mặt rủi ro tụt hậu và mất cân đối cơ cấu.”'
        self.add_text(slide, 68, 135, 824, 40, quote, 13.5, TOKENS['text_body'], align=ppAlignCenter)

        # Horizon 1 (Click 1)
        h1 = self.add_card(slide, 48, 208, 268, 292, TOKENS['card_bg'], TOKENS['cyan'], border_width=1.5)
        ih1 = self.add_icon(slide, 'trending-up', 68, 226, 26)
        kh1 = self.add_text(slide, 102, 224, 200, 20, 'GIAI ĐOẠN 2024 - 2030', 10.5, TOKENS['cyan_light'], bold=True)
        th1 = self.add_text(slide, 68, 258, 228, 26, 'Bứt Phá Cơ Cấu Vàng', 16, TOKENS['text_white'], bold=True)
        bullets_h1 = '• Tối đa hóa việc làm chất lượng cao\n• Đào tạo kỹ năng số cho 70% lao động\n• Nâng cao năng suất trước khi già hóa\n• Thúc đẩy công nghiệp bán dẫn & AI'
        dh1 = self.add_text(slide, 68, 292, 228, 180, bullets_h1, 12.5, TOKENS['text_body'], line_spacing=1.35)
        self.group_and_animate(slide, [h1, ih1, kh1, th1, dh1], trigger=msoAnimTriggerOnPageClick, group_name='!!Horizon_1')

        # Horizon 2 (Click 2)
        h2 = self.add_card(slide, 346, 208, 268, 292, TOKENS['card_bg'], TOKENS['emerald'], border_width=1.5)
        ih2 = self.add_icon(slide, 'shield-alert', 366, 226, 26)
        kh2 = self.add_text(slide, 400, 224, 200, 20, 'GIAI ĐOẠN 2030 - 2040', 10.5, TOKENS['emerald_light'], bold=True)
        th2 = self.add_text(slide, 366, 258, 228, 26, 'Chủ Động Thích Ứng Già', 16, TOKENS['text_white'], bold=True)
        bullets_h2 = '• Cải cách bảo hiểm xã hội đa tầng\n• Hoàn thiện mạng lưới y tế lão khoa\n• Tạo lập thị trường kinh tế bạc (Silver Economy)\n• Thúc đẩy già hóa tích cực & an toàn'
        dh2 = self.add_text(slide, 366, 292, 228, 180, bullets_h2, 12.5, TOKENS['text_body'], line_spacing=1.35)
        self.group_and_animate(slide, [h2, ih2, kh2, th2, dh2], trigger=msoAnimTriggerOnPageClick, group_name='!!Horizon_2')

        # Horizon 3 (Click 3)
        h3 = self.add_card(slide, 644, 208, 268, 292, TOKENS['card_bg'], TOKENS['violet'], border_width=1.5)
        ih3 = self.add_icon(slide, 'target', 664, 226, 26)
        kh3 = self.add_text(slide, 698, 224, 200, 20, 'TẦM NHÌN 2045+', 10.5, TOKENS['violet_light'], bold=True)
        th3 = self.add_text(slide, 664, 258, 228, 26, 'Nâng Tầm Tầm Vóc Việt', 16, TOKENS['text_white'], bold=True)
        bullets_h3 = '• Đưa chỉ số HDI vào nhóm Rất cao (>0.800)\n• Hệ thống an sinh bền vững mọi thế hệ\n• Chuỗi đô thị thông minh, sinh thái\n• Đưa Việt Nam thành quốc gia phát triển'
        dh3 = self.add_text(slide, 664, 292, 228, 180, bullets_h3, 12.5, TOKENS['text_body'], line_spacing=1.35)
        self.group_and_animate(slide, [h3, ih3, kh3, th3, dh3], trigger=msoAnimTriggerOnPageClick, group_name='!!Horizon_3')

    def render_and_save(self, output_pptx: Path, png_dir: Optional[Path] = None):
        output_pptx.parent.mkdir(parents=True, exist_ok=True)
        print('Building Slide 1 (Hero Monolith)...')
        self.build_slide_1()
        print('Building Slide 2 (Spatial Split-Stage & Morph)...')
        self.build_slide_2()
        print('Building Slide 3 (Three Pillars of Dynamics)...')
        self.build_slide_3()
        print('Building Slide 4 (Data Sculpture: Dynamics Matrix)...')
        self.build_slide_4()
        print('Building Slide 5 (Spatial Matrix: 4 Dimensions)...')
        self.build_slide_5()
        print('Building Slide 6 (Executive Strategic Synthesis)...')
        self.build_slide_6()

        resolved_pptx = output_pptx.resolve()
        if output_pptx.exists():
            try:
                output_pptx.unlink()
            except Exception:
                pass
        self.presentation.SaveAs(str(resolved_pptx))
        print(f'Successfully saved PPTX to: {resolved_pptx}')

        if png_dir:
            png_dir.mkdir(parents=True, exist_ok=True)
            for idx, slide in enumerate(self.presentation.Slides, start=1):
                png_path = png_dir / f'slide_{idx}.png'
                slide.Export(str(png_path.resolve()), 'PNG', 1920, 1080)
                print(f'Rendered 1080p preview: {png_path}')

    def close(self):
        try:
            self.presentation.Close()
        except Exception:
            pass
        try:
            self.app.Quit()
        except Exception:
            pass

def main():
    out_dir = Path('output/cinematic_keynote_bai_1')
    target_pptx = out_dir / 'Bai_1__Nhap_mon_DSH_Cinematic.pptx'
    target_png_dir = out_dir / 'rendered_slides'

    engine = CinematicKeynoteEngine()
    try:
        engine.render_and_save(target_pptx, target_png_dir)
    finally:
        engine.close()

    # Sync to user-facing folders
    sync_destinations = [
        Path('Du_An_Outputs/Bai_1__Nhap_mon_DSH/Bai_1__Nhap_mon_DSH.pptx'),
        Path('Du An/A Tuan Dan So/Bai_1__Nhap_mon_DSH.pptx'),
    ]
    for dest in sync_destinations:
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_pptx, dest)
            print(f'Synced PPTX to: {dest}')
        except Exception as e:
            print(f'Warning: Could not sync to {dest}: {e}')

if __name__ == '__main__':
    main()
