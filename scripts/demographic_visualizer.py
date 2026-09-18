"""
demographic_visualizer.py
High-Resolution Demographic Infographic & Chart Generator for Make Slide Pro V7.2.
Generates publication-quality charts tailored to both DARK and LIGHT presentation themes
using Modern Refined design tokens (#0284C7, #0D9488, #10B981, #38BDF8).
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import numpy as np

# Styling defaults
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans"]
plt.rcParams["axes.linewidth"] = 0.8

THEMES = {
    "DARK": {
        "bg_fig": "#0B132B",
        "bg_ax": "#0B132B",
        "title": "#FFFFFF",
        "label": "#F8FAFC",
        "text": "#F8FAFC",
        "tick": "#94A3B8",
        "grid": "#1E293B",
        "spine": "#334155",
        "legend_bg": "#0F172A",
        "legend_edge": "#1E293B",
        "legend_text": "#F8FAFC",
    },
    "LIGHT": {
        "bg_fig": "#FFFFFF",
        "bg_ax": "#F8FAFC",
        "title": "#07172E",
        "label": "#102033",
        "text": "#102033",
        "tick": "#53677D",
        "grid": "#CBD5E1",
        "spine": "#CBD5E1",
        "legend_bg": "#FFFFFF",
        "legend_edge": "#CBD5E1",
        "legend_text": "#07172E",
    }
}


def _apply_theme(fig, ax, theme: str):
    t = THEMES.get(theme.upper(), THEMES["DARK"])
    fig.patch.set_facecolor(t["bg_fig"])
    ax.set_facecolor(t["bg_ax"])
    ax.tick_params(colors=t["tick"], labelsize=8.5)
    for spine in ax.spines.values():
        spine.set_color(t["spine"])
    return t


def generate_population_pyramid(output_path: Path, theme: str = "DARK") -> Path:
    """Generates a refined 2-sided Population Pyramid for Vietnam (TĐTDS)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ages = ["0-4", "5-14", "15-24", "25-39", "40-54", "55-64", "65-74", "75+"]
    male = [3.8, 7.6, 7.8, 12.5, 10.2, 5.8, 3.2, 1.4]
    female = [3.5, 7.1, 7.3, 12.1, 10.4, 6.4, 4.1, 2.3]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    y = np.arange(len(ages))
    bar_m = ax.barh(y, [-m for m in male], color="#0284C7", height=0.68, label="Nam giới (%)", zorder=3)
    bar_f = ax.barh(y, female, color="#0D9488", height=0.68, label="Nữ giới (%)", zorder=3)

    for i, (m, f) in enumerate(zip(male, female)):
        ax.text(-m - 0.4, i, f"{m}%", ha="right", va="center", fontsize=8.5, fontweight="bold", color=t["text"])
        ax.text(f + 0.4, i, f"{f}%", ha="left", va="center", fontsize=8.5, fontweight="bold", color=t["text"])

    ax.set_yticks(y)
    ax.set_yticklabels(ages, fontsize=9.5, fontweight="bold", color=t["label"])
    ax.set_xticks([-14, -7, 0, 7, 14])
    ax.set_xticklabels(["14%", "7%", "0", "7%", "14%"], fontsize=8.5, color=t["tick"])
    ax.grid(axis="x", linestyle="--", alpha=0.5, color=t["grid"], zorder=1)

    ax.axvline(0, color=t["title"], linewidth=1.2, zorder=4)
    ax.set_title("Tháp Dân Số Việt Nam: Đỉnh Dân Số Vàng & Bắt Đầu Già Hóa", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=9.5)
    for text in leg.get_texts():
        text.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_fertility_trends(output_path: Path, theme: str = "DARK") -> Path:
    """Generates TFR trend line chart vs 2.1 replacement fertility line."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    years = [1989, 1999, 2009, 2015, 2019, 2021, 2023]
    tfr_nation = [3.80, 2.33, 2.03, 2.10, 2.09, 2.11, 1.96]
    tfr_dnb = [2.90, 1.95, 1.70, 1.62, 1.56, 1.48, 1.39]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    ax.plot(years, tfr_nation, marker="o", linewidth=2.8, color="#0284C7", label="Toàn quốc (TFR)", zorder=3)
    ax.plot(years, tfr_dnb, marker="s", linewidth=2.4, color="#EF4444", linestyle="--", label="Đông Nam Bộ (TFR thấp)", zorder=3)
    ax.axhline(2.10, color="#10B981", linewidth=1.8, linestyle=":", label="Mức sinh thay thế (2.10 con)", zorder=2)

    for x, y in zip(years, tfr_nation):
        ax.text(x, y + 0.12, f"{y:.2f}", ha="center", fontsize=8.5, fontweight="bold", color="#38BDF8")
    for x, y in zip(years, tfr_dnb):
        ax.text(x, y - 0.20, f"{y:.2f}", ha="center", fontsize=8.5, fontweight="bold", color="#F87171")

    ax.set_ylim(1.0, 4.2)
    ax.set_yticks([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontsize=9, color=t["tick"])
    ax.grid(axis="y", linestyle="--", alpha=0.5, color=t["grid"], zorder=1)

    ax.set_title("Biến Động Tổng Tỷ Suất Sinh (TFR) Việt Nam (1989 - 2023)", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    leg = ax.legend(loc="upper right", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=8.5)
    for text in leg.get_texts():
        text.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_regional_density(output_path: Path, theme: str = "DARK") -> Path:
    """Generates bar chart of population density by 6 socio-economic regions."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    regions = [
        "Đồng Bằng Sông Hồng",
        "Đông Nam Bộ",
        "ĐBSCL",
        "Bắc Trung Bộ & DHMT",
        "Tây Nguyên",
        "Trung Du & MNPB"
    ]
    density = [1085, 788, 435, 218, 112, 136]
    colors = ["#0284C7", "#0D9488", "#38BDF8", "#64748B", "#475569", "#334155"]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    y_pos = np.arange(len(regions))
    bars = ax.barh(y_pos, density, color=colors, height=0.62, zorder=3)

    for bar, val in zip(bars, density):
        ax.text(val + 20, bar.get_y() + bar.get_height() / 2, f"{val:,} ng/km²", va="center", fontsize=8.5, fontweight="bold", color=t["text"])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(regions, fontsize=9, fontweight="bold", color=t["label"])
    ax.set_xlim(0, 1300)
    ax.grid(axis="x", linestyle="--", alpha=0.5, color=t["grid"], zorder=1)

    ax.axvline(321, color="#EF4444", linestyle=":", linewidth=1.5, label="Bình quân cả nước (321 ng/km²)")
    ax.set_title("Mật Độ Dân Số Sáu Vùng Kinh Tế - Xã Hội Việt Nam", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    leg = ax.legend(loc="lower right", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=8.5)
    for text in leg.get_texts():
        text.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_system_interaction(output_path: Path, theme: str = "DARK") -> Path:
    """Generates a matrix/flow conceptual infographic diagram."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    nodes = [
        ("QUY MÔ DÂN SỐ\n(100.3 Triệu người)", 2.5, 7.5, "#0284C7"),
        ("CƠ CẤU DÂN SỐ\n(Vàng & Già hóa nhanh)", 7.5, 7.5, "#0D9488"),
        ("PHÂN BỐ & DI DÂN\n(Đô thị hóa bứt phá)", 2.5, 2.5, "#38BDF8"),
        ("CHẤT LƯỢNG DÂN SỐ\n(Thể chất - Trí tuệ - Tinh thần)", 7.5, 2.5, "#10B981"),
    ]

    for label, x, y, col in nodes:
        rect = plt.Rectangle((x - 1.8, y - 1.1), 3.6, 2.2, facecolor=t["legend_bg"], edgecolor=col, linewidth=2.0, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=8.5, fontweight="bold", color=t["text"], zorder=4)

    # Connecting arrows
    arrow_props = dict(arrowstyle="<->", color="#64748B", lw=2.0, mutation_scale=15)
    ax.annotate("", xy=(4.3, 7.5), xytext=(5.7, 7.5), arrowprops=arrow_props)
    ax.annotate("", xy=(4.3, 2.5), xytext=(5.7, 2.5), arrowprops=arrow_props)
    ax.annotate("", xy=(2.5, 6.4), xytext=(2.5, 3.6), arrowprops=arrow_props)
    ax.annotate("", xy=(7.5, 6.4), xytext=(7.5, 3.6), arrowprops=arrow_props)
    ax.annotate("", xy=(4.3, 6.4), xytext=(5.7, 3.6), arrowprops=arrow_props)
    ax.annotate("", xy=(4.3, 3.6), xytext=(5.7, 6.4), arrowprops=arrow_props)

    center_circle = plt.Circle((5.0, 5.0), 0.9, facecolor="#0284C7", edgecolor=t["title"], linewidth=1.5, zorder=5)
    ax.add_patch(center_circle)
    ax.text(5.0, 5.0, "TÁI SẢN XUẤT\nDÂN SỐ", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#FFFFFF", zorder=6)

    ax.set_title("Hệ Thống Tương Tác Giữa Các Thành Tố Dân Số Học", fontsize=11, fontweight="bold", color=t["title"], pad=14)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_math_models_chart(output_path: Path, theme: str = "DARK") -> Path:
    """Generates curves comparing Linear, Exponential, and Logistic growth models."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    t = np.linspace(0, 50, 200)
    p0 = 50.0
    linear = p0 + 1.2 * t
    expo = p0 * np.exp(0.018 * t)
    K = 115.0
    logistic = K / (1.0 + ((K - p0) / p0) * np.exp(-0.08 * t))

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    th = _apply_theme(fig, ax, theme)

    ax.plot(t, linear, label="Ngoại suy tuyến tính (P_t = P_0 + bt)", color="#64748B", linestyle="--", linewidth=2.0)
    ax.plot(t, expo, label="Hàm số mũ (P_t = P_0 * e^rt)", color="#EF4444", linewidth=2.4)
    ax.plot(t, logistic, label="Hàm Logistic S-Curve (Có sức tải K=115Tr)", color="#0284C7", linewidth=2.8)

    ax.axhline(K, color="#10B981", linestyle=":", linewidth=1.5, label="Ngưỡng dung nạp tối đa (K)")
    ax.set_title("So Sánh Ba Mô Hình Toán Học Dự Báo Quy Mô Dân Số", fontsize=11, fontweight="bold", color=th["title"], pad=12)
    ax.set_xlabel("Thời gian dự báo (Năm)", fontsize=9.0, fontweight="bold", color=th["label"])
    ax.set_ylabel("Quy mô dân số (Triệu người)", fontsize=9.0, fontweight="bold", color=th["label"])
    ax.grid(True, linestyle="--", alpha=0.5, color=th["grid"])

    leg = ax.legend(loc="upper left", frameon=True, facecolor=th["legend_bg"], edgecolor=th["legend_edge"], fontsize=8.0)
    for text in leg.get_texts():
        text.set_color(th["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_population_metrics(output_path: Path, theme: str = "DARK") -> Path:
    """Generates multi-metric timeline of Vietnam population (1979 - 2024)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    years = [1979, 1989, 1999, 2009, 2019, 2024]
    pop = [52.7, 64.4, 76.3, 85.8, 96.2, 100.3]
    growth_rate = [2.16, 2.10, 1.51, 1.06, 1.14, 0.84]

    fig, ax1 = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    th = _apply_theme(fig, ax1, theme)

    ax2 = ax1.twinx()
    for spine in ax2.spines.values():
        spine.set_color(th["spine"])
    ax2.tick_params(colors=th["tick"], labelsize=8.5)

    bars = ax1.bar(years, pop, width=2.4, color="#0284C7", alpha=0.85, label="Quy mô dân số (Triệu người)", zorder=3)
    lines = ax2.plot(years, growth_rate, color="#EF4444", marker="s", linewidth=2.4, label="Tốc độ tăng trưởng (%/năm)", zorder=4)

    for bar, p in zip(bars, pop):
        ax1.text(bar.get_x() + bar.get_width() / 2, p + 1.5, f"{p:.1f}Tr", ha="center", fontsize=8.0, fontweight="bold", color=th["text"])
    for y, g in zip(years, growth_rate):
        ax2.text(y, g + 0.08, f"{g:.2f}%", ha="center", fontsize=8.0, fontweight="bold", color="#EF4444")

    ax1.set_ylim(0, 120)
    ax2.set_ylim(0, 3.0)
    ax1.set_ylabel("Quy mô dân số (Triệu người)", fontsize=9.0, fontweight="bold", color=th["label"])
    ax2.set_ylabel("Tốc độ tăng trưởng (%/năm)", fontsize=9.0, fontweight="bold", color="#EF4444")
    ax1.set_title("Tiến Trình Gia Tăng Dân Số & Giảm Tốc Độ Tăng (1979 - 2024)", fontsize=11, fontweight="bold", color=th["title"], pad=12)
    ax1.set_xticks(years)
    ax1.grid(axis="y", linestyle="--", alpha=0.4, color=th["grid"])

    lines_labels = [bars, lines[0]]
    labs = ["Quy mô (Triệu người)", "Tăng trưởng (%/năm)"]
    leg = ax1.legend(lines_labels, labs, loc="upper left", frameon=True, facecolor=th["legend_bg"], edgecolor=th["legend_edge"], fontsize=8.0)
    for text in leg.get_texts():
        text.set_color(th["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_demo_transition_stages(output_path: Path, theme: str = "DARK") -> Path:
    """Generates Demographic Transition Model 4 Stages Chart."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    x = np.linspace(0, 100, 300)

    # Birth rate
    cbr = np.piecewise(x, [x < 25, (x >= 25) & (x < 50), (x >= 50) & (x < 75), x >= 75],
                       [38.0, lambda x: 38.0 - 0.2 * (x - 25), lambda x: 33.0 - 0.75 * (x - 50), 14.25])
    # Death rate
    cdr = np.piecewise(x, [x < 20, (x >= 20) & (x < 45), (x >= 45) & (x < 75), x >= 75],
                       [36.0, lambda x: 36.0 - 0.9 * (x - 20), 13.5, lambda x: 13.5 + 0.05 * (x - 75)])

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    th = _apply_theme(fig, ax, theme)

    ax.plot(x, cbr, color="#0284C7", linewidth=2.8, label="Tỷ suất sinh thô (CBR)")
    ax.plot(x, cdr, color="#EF4444", linewidth=2.8, linestyle="--", label="Tỷ suất chết thô (CDR)")

    # Fill natural increase
    ax.fill_between(x, cdr, cbr, where=(cbr >= cdr), color="#38BDF8", alpha=0.25, label="Gia tăng tự nhiên (Bùng nổ dân số)")

    # Vertical stages dividers
    for st, name in [(25, "Giai đoạn 1\n(Cổ điển)"), (50, "Giai đoạn 2\n(Bùng nổ)"), (75, "Giai đoạn 3\n(Quá độ)"), (95, "Giai đoạn 4\n(Hậu quá độ)")]:
        ax.axvline(st, color=th["grid"], linestyle=":", linewidth=1.2)

    # Mark Vietnam position
    ax.scatter([70], [18], color="#F59E0B", s=90, zorder=6)
    ax.annotate("Việt Nam hiện nay\n(Cuối GĐ 3, TFR ≈ 1.96)", xy=(70, 18), xytext=(52, 26),
                arrowprops=dict(facecolor="#F59E0B", shrink=0.08, width=1.5, headwidth=6),
                fontsize=8.0, fontweight="bold", color=th["text"],
                bbox=dict(boxstyle="round,pad=0.3", fc=th["legend_bg"], ec="#F59E0B", lw=1.2))

    ax.set_ylim(0, 45)
    ax.set_xlim(0, 100)
    ax.set_ylabel("Tỷ suất trên 1.000 dân (‰)", fontsize=9.0, fontweight="bold", color=th["label"])
    ax.set_title("Mô Hình Chuyển Tiếp Dân Số Bốn Giai Đoạn & Vị Thế Việt Nam", fontsize=11, fontweight="bold", color=th["title"], pad=12)
    ax.set_xticks([12.5, 37.5, 62.5, 87.5])
    ax.set_xticklabels(["Giai đoạn 1", "Giai đoạn 2", "Giai đoạn 3", "Giai đoạn 4"], fontsize=9.0, color=th["tick"])
    ax.grid(True, linestyle="--", alpha=0.4, color=th["grid"])

    leg = ax.legend(loc="lower left", frameon=True, facecolor=th["legend_bg"], edgecolor=th["legend_edge"], fontsize=8.0)
    for text in leg.get_texts():
        text.set_color(th["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_hdi_dimensions(output_path: Path, theme: str = "DARK") -> Path:
    """Generates HDI 3-dimension components breakdown for Vietnam."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pillars = ["Sức Khỏe\n(LEI)", "Giáo Dục\n(EI)", "Thu Nhập\n(II)", "HDI\nTổng Hợp"]
    vn_scores = [0.826, 0.640, 0.725, 0.726]
    world_avg = [0.730, 0.645, 0.710, 0.732]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    th = _apply_theme(fig, ax, theme)

    x = np.arange(len(pillars))
    w = 0.35
    b1 = ax.bar(x - w/2, vn_scores, width=w, color="#0284C7", label="Việt Nam (2023)", zorder=3)
    b2 = ax.bar(x + w/2, world_avg, width=w, color="#64748B", alpha=0.6, label="Trung bình toàn cầu", zorder=3)

    for bar, val in zip(b1, vn_scores):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.3f}", ha="center", fontsize=8.0, fontweight="bold", color=th["text"])
    for bar, val in zip(b2, world_avg):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.3f}", ha="center", fontsize=7.5, color=th["tick"])

    ax.axhline(0.700, color="#10B981", linestyle="--", linewidth=1.2, label="Ngưỡng phát triển cao (0.700)")
    ax.axhline(0.800, color="#38BDF8", linestyle=":", linewidth=1.2, label="Ngưỡng rất cao (0.800 - Mục tiêu 2045)")

    ax.set_ylim(0, 1.05)
    ax.set_xticks(x)
    ax.set_xticklabels(pillars, fontsize=9.0, fontweight="bold", color=th["label"])
    ax.set_ylabel("Điểm chỉ số (0.000 - 1.000)", fontsize=9.0, fontweight="bold", color=th["label"])
    ax.set_title("Cấu Trúc Ba Trụ Cột Chỉ Số Phát Triển Con Người (HDI) Việt Nam", fontsize=11, fontweight="bold", color=th["title"], pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.4, color=th["grid"])

    leg = ax.legend(loc="upper left", frameon=True, facecolor=th["legend_bg"], edgecolor=th["legend_edge"], fontsize=7.5)
    for text in leg.get_texts():
        text.set_color(th["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_dependency_ratio_trends(output_path: Path, theme: str = "DARK") -> Path:
    """Generates Dependency Ratio Trends for Vietnam (1979 - 2050)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    years = [1979, 1989, 1999, 2009, 2019, 2029, 2039, 2049]
    ydr = [85.0, 72.0, 52.0, 36.0, 32.5, 30.0, 27.5, 25.0]
    adr = [8.5, 9.2, 10.5, 11.8, 14.5, 21.0, 31.5, 42.0]
    tdr = [y + a for y, a in zip(ydr, adr)]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    th = _apply_theme(fig, ax, theme)

    ax.plot(years, tdr, color="#0284C7", linewidth=2.8, marker="o", label="Tỷ số phụ thuộc chung (TDR)")
    ax.plot(years, ydr, color="#10B981", linewidth=2.0, linestyle="--", label="Phụ thuộc trẻ em (YDR)")
    ax.plot(years, adr, color="#EF4444", linewidth=2.4, linestyle="-.", label="Phụ thuộc người cao tuổi (ADR)")

    # Golden window threshold
    ax.axhline(50, color="#F59E0B", linestyle=":", linewidth=1.5, label="Ngưỡng Dân số vàng (TDR < 50)")

    # Highlight golden period
    ax.axvspan(2007, 2039, color="#F59E0B", alpha=0.15, label="Cửa sổ Dân số vàng (2007 - 2039)")

    for y, t_val in zip(years, tdr):
        ax.text(y, t_val + 2.5, f"{t_val:.1f}", ha="center", fontsize=7.5, fontweight="bold", color=th["text"])

    ax.set_ylim(0, 110)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontsize=8.5, color=th["tick"])
    ax.set_ylabel("Số người phụ thuộc / 100 người lao động", fontsize=9.0, fontweight="bold", color=th["label"])
    ax.set_title("Xu Hướng Tỷ Số Phụ Thuộc & Cửa Sổ Dân Số Vàng Việt Nam", fontsize=11, fontweight="bold", color=th["title"], pad=12)
    ax.grid(True, linestyle="--", alpha=0.4, color=th["grid"])

    leg = ax.legend(loc="upper right", frameon=True, facecolor=th["legend_bg"], edgecolor=th["legend_edge"], fontsize=7.5)
    for text in leg.get_texts():
        text.set_color(th["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_urbanization_scurve(output_path: Path, theme: str = "DARK") -> Path:
    """Generates S-curve Urbanization Model for Vietnam."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    t = np.linspace(1975, 2050, 150)
    L = 75.0
    k = 0.075
    t0 = 2028.0
    s_curve = L / (1.0 + np.exp(-k * (t - t0))) + 15.0

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    th = _apply_theme(fig, ax, theme)

    ax.plot(t, s_curve, color="#0284C7", linewidth=2.8, label="Đường cong chữ S Đô thị hóa (Mô hình Northam)", zorder=3)

    vn_years = [1975, 1989, 1999, 2009, 2019, 2024, 2030]
    vn_urban = [19.0, 19.4, 23.7, 29.6, 34.4, 42.6, 50.0]

    ax.scatter(vn_years[:-1], vn_urban[:-1], color="#10B981", s=65, zorder=5, label="Thực tế Tổng điều tra (1975-2024)")
    ax.scatter(vn_years[-1:], vn_urban[-1:], color="#EF4444", marker="*", s=140, zorder=5, label="Mục tiêu Nghị quyết 06 (50% năm 2030)")

    for y, u in zip(vn_years, vn_urban):
        ax.text(y, u + 2.2, f"{u:.1f}%", ha="center", fontsize=8.0, fontweight="bold", color=th["text"])

    ax.axhline(30, color="#64748B", linestyle=":", linewidth=1.2)
    ax.axhline(70, color="#64748B", linestyle=":", linewidth=1.2)
    ax.text(1976, 26, "Giai đoạn 1: Khởi đầu (<30%)", fontsize=8.0, color="#64748B")
    ax.text(1976, 46, "Giai đoạn 2: Tăng tốc (30% - 70%)", fontsize=8.0, fontweight="bold", color="#0284C7")
    ax.text(1976, 73, "Giai đoạn 3: Bão hòa (>70%)", fontsize=8.0, color="#64748B")

    ax.set_ylim(10, 85)
    ax.set_xlim(1973, 2052)
    ax.set_ylabel("Tỷ lệ dân số đô thị (%)", fontsize=9.0, fontweight="bold", color=th["label"])
    ax.set_xlabel("Năm", fontsize=9.0, fontweight="bold", color=th["label"])
    ax.grid(axis="both", linestyle="--", alpha=0.4, color=th["grid"])
    ax.set_title("Đường Cong Chữ S Đô Thị Hóa Việt Nam & Mục Tiêu 2030", fontsize=11, fontweight="bold", color=th["title"], pad=12)

    leg = ax.legend(loc="lower right", frameon=True, facecolor=th["legend_bg"], edgecolor=th["legend_edge"], fontsize=8.0)
    for text in leg.get_texts():
        text.set_color(th["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_age_structure_radar(output_path: Path, theme: str = "DARK") -> Path:
    """Radar chart comparing age structures across 1979, 1999, 2019, 2030."""
    categories = ["0-14 tuổi\n(Trẻ em)", "15-24 tuổi\n(Thanh niên)", "25-49 tuổi\n(Lao động chính)", "50-64 tuổi\n(Trung niên)", "65+ tuổi\n(Người già)"]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    v1979 = [42.5, 19.8, 25.1, 7.8, 4.8]
    v2019 = [24.3, 15.6, 36.8, 15.6, 7.7]
    v2030 = [18.2, 13.5, 34.6, 19.5, 14.2]

    v1979 += v1979[:1]
    v2019 += v2019[:1]
    v2030 += v2030[:1]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), subplot_kw=dict(polar=True), dpi=220)
    t = THEMES.get(theme.upper(), THEMES["DARK"])
    fig.patch.set_facecolor(t["bg_fig"])
    ax.set_facecolor(t["bg_ax"])

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8.0, fontweight="bold", color=t["label"])
    ax.tick_params(colors=t["tick"])
    ax.grid(color=t["grid"], linestyle="--", alpha=0.6)
    ax.spines["polar"].set_color(t["spine"])

    ax.plot(angles, v1979, color="#94A3B8", linewidth=1.8, linestyle="--", label="Năm 1979 (Trẻ hóa)")
    ax.fill(angles, v1979, color="#94A3B8", alpha=0.10)

    ax.plot(angles, v2019, color="#0284C7", linewidth=2.4, label="Năm 2019 (Dân số vàng)")
    ax.fill(angles, v2019, color="#0284C7", alpha=0.15)

    ax.plot(angles, v2030, color="#F59E0B", linewidth=2.4, label="Năm 2030 (Dự báo Già hóa)")
    ax.fill(angles, v2030, color="#F59E0B", alpha=0.15)

    ax.set_title("Chuyển Dịch Cơ Cấu Tuổi Dân Số Việt Nam (1979 - 2030)", fontsize=11, fontweight="bold", color=t["title"], pad=16)
    leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=8.0)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_mortality_curve_gompertz(output_path: Path, theme: str = "DARK") -> Path:
    """U/J-shaped Gompertz-Makeham mortality curve by age group."""
    ages = np.array([0, 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85])
    m_rates = np.array([14.2, 1.8, 0.7, 0.5, 0.8, 1.2, 1.4, 1.6, 2.1, 2.9, 4.3, 6.7, 10.5, 16.8, 27.5, 45.2, 74.6, 122.0, 198.5])

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    ax.plot(ages, m_rates, color="#EF4444", linewidth=2.6, marker="o", markersize=4, label="Tỷ suất chết theo tuổi (ASDR, ‰)", zorder=3)
    ax.fill_between(ages, m_rates, color="#EF4444", alpha=0.12, zorder=2)

    ax.annotate("Tử vong sơ sinh cao\n(14.2‰)", xy=(0, 14.2), xytext=(8, 35),
                arrowprops=dict(arrowstyle="->", color=t["title"], lw=1.2),
                fontsize=8.0, fontweight="bold", color=t["title"])

    ax.annotate("Đáy tử vong thấp nhất (10-14 tuổi: 0.5‰)", xy=(10, 0.5), xytext=(12, 12),
                arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.2),
                fontsize=8.0, fontweight="bold", color="#10B981")

    ax.annotate("Quy luật Gompertz: Tăng cấp số nhân từ 55 tuổi", xy=(65, 27.5), xytext=(30, 120),
                arrowprops=dict(arrowstyle="->", color="#F59E0B", lw=1.2),
                fontsize=8.0, fontweight="bold", color="#F59E0B")

    ax.set_yscale("log")
    ax.set_ylim(0.3, 300)
    ax.set_xlim(-2, 88)
    ax.set_xlabel("Độ tuổi (Năm)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_ylabel("Tỷ suất chết (‰, thang logarit)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Đường Cong Tử Vong Theo Độ Tuổi: Mô Hình Gompertz-Makeham", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(True, which="both", linestyle="--", alpha=0.35, color=t["grid"])

    leg = ax.legend(loc="upper left", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=8.0)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_migration_flows_matrix(output_path: Path, theme: str = "DARK") -> Path:
    """Heatmap matrix of net migration rates between socioeconomic regions."""
    regions = ["ĐB Sông Hồng", "Trung Du & MNPB", "Bắc Trung Bộ & DHMT", "Tây Nguyên", "Đông Nam Bộ", "ĐB Sông Cửu Long"]
    net_rates = np.array([
        [0.0, 1.2, 3.5, 0.8, -12.4, 1.1],
        [-1.8, 0.0, 0.5, -2.1, -9.6, -0.4],
        [-2.4, -0.3, 0.0, -1.9, -16.8, -0.7],
        [-0.6, 1.5, 1.8, 0.0, -8.2, 0.5],
        [14.2, 8.5, 18.4, 7.9, 0.0, 22.6],
        [-1.2, 0.2, 0.6, -0.8, -21.5, 0.0]
    ])

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    cmap = "Blues" if theme.upper() == "LIGHT" else "YlGnBu"
    im = ax.imshow(net_rates, cmap=cmap, aspect="auto", zorder=2)

    ax.set_xticks(np.arange(len(regions)))
    ax.set_yticks(np.arange(len(regions)))
    ax.set_xticklabels([r.split()[-1] if len(r) > 12 else r for r in regions], fontsize=8.0, fontweight="bold", color=t["label"], rotation=25, ha="right")
    ax.set_yticklabels(regions, fontsize=8.0, fontweight="bold", color=t["label"])

    for i in range(len(regions)):
        for j in range(len(regions)):
            val = net_rates[i, j]
            txt_color = "#0B132B" if abs(val) > 10 else t["text"]
            sign = "+" if val > 0 else ""
            ax.text(j, i, f"{sign}{val:.1f}" if val != 0 else "—", ha="center", va="center",
                    fontsize=8.0, fontweight="bold", color=txt_color)

    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(colors=t["tick"], labelsize=7.5)
    cbar.set_label("Tỷ suất di cư thuần (‰)", color=t["label"], fontsize=8.0, fontweight="bold")

    ax.set_title("Ma Trận Di Cư Thuần Giữa 6 Vùng Kinh Tế - Xã Hội", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_sex_ratio_birth_heatmap(output_path: Path, theme: str = "DARK") -> Path:
    """Sex Ratio at Birth (SRB) divergence chart vs biological norm 105."""
    years = [1999, 2005, 2009, 2014, 2019, 2021, 2023]
    srb_all = [106.2, 107.5, 110.5, 112.2, 111.5, 112.0, 112.1]
    srb_first = [105.5, 106.0, 107.2, 108.5, 108.0, 108.2, 108.4]
    srb_third = [108.0, 111.2, 116.5, 120.4, 119.8, 121.5, 122.3]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    x = np.arange(len(years))
    width = 0.26

    r1 = ax.bar(x - width, srb_first, width, label="Lần sinh 1", color="#0D9488", zorder=3)
    r2 = ax.bar(x, srb_all, width, label="Chung toàn quốc", color="#0284C7", zorder=3)
    r3 = ax.bar(x + width, srb_third, width, label="Lần sinh 3+ (Bất thường)", color="#EF4444", zorder=3)

    ax.axhline(105, color="#10B981", linestyle="--", linewidth=1.6, label="Ngưỡng sinh học chuẩn (105 nam/100 nữ)", zorder=4)

    for i in range(len(years)):
        ax.text(x[i], srb_all[i] + 0.6, f"{srb_all[i]:.1f}", ha="center", fontsize=7.0, fontweight="bold", color=t["text"])
        ax.text(x[i] + width, srb_third[i] + 0.6, f"{srb_third[i]:.1f}", ha="center", fontsize=7.0, fontweight="bold", color="#EF4444")

    ax.set_ylim(100, 126)
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years], fontsize=8.5, fontweight="bold", color=t["tick"])
    ax.set_ylabel("Số bé trai / 100 bé gái", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Mất Cân Bằng Tỷ Số Giới Tính Khi Sinh (SRB) Tại Việt Nam", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.4, color=t["grid"])

    leg = ax.legend(loc="upper left", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=7.5)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_population_forecast_scenarios(output_path: Path, theme: str = "DARK") -> Path:
    """Fan chart of Vietnam population projections 2025-2069."""
    years = np.array([2024, 2029, 2034, 2039, 2044, 2049, 2054, 2059, 2064, 2069])
    base = 100.3
    low = np.array([base, 102.5, 104.2, 104.8, 104.5, 103.2, 101.0, 98.4, 95.2, 91.8])
    med = np.array([base, 103.8, 106.5, 108.2, 108.9, 108.6, 107.5, 105.8, 103.6, 101.2])
    high = np.array([base, 105.2, 109.1, 112.5, 114.8, 116.2, 117.0, 117.2, 116.8, 115.5])

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    ax.fill_between(years, low, high, color="#0284C7", alpha=0.18, label="Dải biến thiên dự báo (Kịch bản thấp - cao)", zorder=2)
    ax.plot(years, high, color="#10B981", linestyle="--", linewidth=1.8, label="Kịch bản Mức sinh cao (TFR = 2.1)", zorder=3)
    ax.plot(years, med, color="#0284C7", linewidth=2.8, marker="o", markersize=4.5, label="Kịch bản Trung bình (Khả dĩ nhất)", zorder=4)
    ax.plot(years, low, color="#EF4444", linestyle="--", linewidth=1.8, label="Kịch bản Mức sinh thấp (TFR = 1.6)", zorder=3)

    ax.annotate("Đỉnh dân số kịch bản chuẩn:\n108.9 triệu người (năm 2044)", xy=(2044, 108.9), xytext=(2032, 113.5),
                arrowprops=dict(arrowstyle="->", color=t["title"], lw=1.3),
                fontsize=8.0, fontweight="bold", color=t["title"])

    for y, m in zip(years[::2], med[::2]):
        ax.text(y, m + 1.2, f"{m:.1f}M", ha="center", fontsize=7.5, fontweight="bold", color=t["text"])

    ax.set_ylim(88, 122)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontsize=8.0, color=t["tick"])
    ax.set_ylabel("Quy mô dân số (Triệu người)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Dự Báo Dân Số Việt Nam 2024 - 2069 (3 Kịch Bản)", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(True, linestyle="--", alpha=0.4, color=t["grid"])

    leg = ax.legend(loc="lower left", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=7.5)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_labor_force_donut(output_path: Path, theme: str = "DARK") -> Path:
    """Donut chart of labor force qualifications and sectoral distribution."""
    labels = [
        "Đại học & Sau ĐH (12.4%)",
        "Cao đẳng & Trung cấp (14.2%)",
        "Sơ cấp & Đào tạo nghề (8.8%)",
        "Lao động chưa qua đào tạo (64.6%)"
    ]
    sizes = [12.4, 14.2, 8.8, 64.6]
    colors = ["#0284C7", "#0D9488", "#F59E0B", "#64748B"]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct="%1.1f%%", pctdistance=0.75,
        startangle=140, colors=colors,
        wedgeprops=dict(width=0.45, edgecolor=t["bg_fig"], linewidth=2.0)
    )

    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_fontweight("bold")
        at.set_color("#FFFFFF")

    ax.text(0, 0.08, "LỰC LƯỢNG\nLAO ĐỘNG", ha="center", va="center", fontsize=9.5, fontweight="bold", color=t["title"])
    ax.text(0, -0.16, "52.4 Triệu người\n(2024)", ha="center", va="center", fontsize=8.0, color=t["tick"])

    leg = ax.legend(wedges, labels, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2, frameon=False, fontsize=8.0)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    ax.set_title("Cơ Cấu Chất Lượng Lực Lượng Lao Động Việt Nam", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_life_expectancy_waterfall(output_path: Path, theme: str = "DARK") -> Path:
    """Waterfall chart showing drivers of life expectancy gain in Vietnam."""
    factors = ["Năm 1989\n(Gốc)", "Tiến bộ\nY tế", "Cải thiện\nThu nhập", "Vệ sinh &\nNước sạch", "Dinh dưỡng\nBà mẹ-Trẻ em", "Năm 2023\n(Hiện tại)"]
    heights = [65.2, 3.2, 2.4, 1.6, 1.3, 73.7]
    bottoms = [0, 65.2, 68.4, 70.8, 72.4, 0]
    bar_colors = ["#0284C7", "#10B981", "#10B981", "#10B981", "#10B981", "#38BDF8"]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    x = np.arange(len(factors))
    bars = ax.bar(x, heights, bottom=bottoms, color=bar_colors, width=0.55, zorder=3)

    for i in range(len(factors)):
        val = heights[i]
        top_y = bottoms[i] + heights[i]
        lbl = f"{top_y:.1f} tuổi" if (i == 0 or i == 5) else f"+{val:.1f}"
        ax.text(x[i], top_y + 0.8, lbl, ha="center", fontsize=8.0, fontweight="bold", color=t["text"])

    ax.set_ylim(55, 78)
    ax.set_xticks(x)
    ax.set_xticklabels(factors, fontsize=8.0, fontweight="bold", color=t["label"])
    ax.set_ylabel("Tuổi thọ bình quân (Năm)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Các Động Lực Gia Tăng Tuổi Thọ Bình Quân Việt Nam (+8.5 Tuổi)", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.4, color=t["grid"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_demographic_dividend_stacked_area(output_path: Path, theme: str = "DARK") -> Path:
    """Stacked area chart of 3 age groups showing the demographic dividend window."""
    years = np.array([1979, 1989, 1999, 2007, 2014, 2019, 2024, 2030, 2039, 2050])
    young = np.array([42.5, 39.2, 33.1, 26.8, 24.0, 24.3, 23.5, 21.0, 18.2, 16.5])
    old = np.array([4.8, 4.7, 5.8, 6.5, 7.1, 7.7, 9.2, 12.4, 16.8, 22.0])
    working = 100.0 - young - old

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    ax.stackplot(years, young, working, old, labels=["Dưới 15 tuổi (Trẻ em)", "15-64 tuổi (Tuổi lao động)", "65+ tuổi (Người cao tuổi)"],
                 colors=["#F59E0B", "#0284C7", "#EF4444"], alpha=0.85, zorder=3)

    ax.axvspan(2007, 2039, color="#10B981", alpha=0.18, zorder=4)
    ax.text(2023, 50, "CỬA SỔ DÂN SỐ VÀNG\n(Lao động > 66%)", ha="center", va="center",
            fontsize=9.0, fontweight="bold", color="#FFFFFF", bbox=dict(boxstyle="round,pad=0.4", fc="#0B132B", ec="#10B981", lw=1.5))

    ax.set_ylim(0, 100)
    ax.set_xlim(1978, 2051)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontsize=8.0, color=t["tick"])
    ax.set_ylabel("Tỷ trọng cơ cấu dân số (%)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Cơ Cấu Dân Số 3 Nhóm Tuổi & Cửa Sổ Dân Số Vàng Việt Nam", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.35, color=t["grid"])

    leg = ax.legend(loc="upper right", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=7.5)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_urban_rural_divergence_bubble(output_path: Path, theme: str = "DARK") -> Path:
    """Bubble scatter plot of density vs urbanization vs population size."""
    data = [
        ("ĐB Sông Hồng", 1060, 38.5, 23.2, "#0284C7"),
        ("Đông Nam Bộ", 757, 67.2, 18.8, "#38BDF8"),
        ("ĐB Sông Cửu Long", 423, 25.1, 17.4, "#0D9488"),
        ("Bắc Trung Bộ & DHMT", 210, 28.4, 20.3, "#F59E0B"),
        ("Trung Du & MNPB", 132, 18.2, 12.9, "#10B981"),
        ("Tây Nguyên", 107, 28.8, 5.9, "#8B5CF6"),
    ]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    for name, dens, urb, pop, col in data:
        size = pop * 28.0
        ax.scatter(dens, urb, s=size, color=col, alpha=0.85, edgecolors=t["title"], linewidths=1.2, zorder=3)
        ax.text(dens + 22, urb, f"{name}\n({pop}M ng, {urb}%)", fontsize=7.5, fontweight="bold", color=t["text"], va="center")

    ax.set_xlim(50, 1250)
    ax.set_ylim(12, 75)
    ax.set_xlabel("Mật độ dân số (người/km²)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_ylabel("Tỷ lệ đô thị hóa (%)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Tương Quan Mật Độ, Đô Thị Hóa & Quy Mô Dân Số 6 Vùng", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(True, linestyle="--", alpha=0.4, color=t["grid"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_fertility_by_region_bar(output_path: Path, theme: str = "DARK") -> Path:
    """Horizontal bar chart showing TFR divergence across ecological regions."""
    regions = [
        "Đông Nam Bộ (Siêu thấp)",
        "Đồng Bằng Sông Cửu Long",
        "Bắc Trung Bộ & Duyên Hải Miền Trung",
        "Toàn Quốc (Mức trung bình)",
        "Đồng Bằng Sông Hồng",
        "Tây Nguyên",
        "Trung Du & Miền Núi Phía Bắc"
    ]
    tfr_vals = [1.47, 1.80, 2.04, 1.96, 2.15, 2.26, 2.40]
    colors = ["#EF4444", "#F59E0B", "#0D9488", "#0284C7", "#10B981", "#10B981", "#10B981"]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    y = np.arange(len(regions))
    bars = ax.barh(y, tfr_vals, color=colors, height=0.62, zorder=3)

    ax.axvline(2.1, color="#F59E0B", linestyle="--", linewidth=1.6, label="Mức sinh thay thế (TFR = 2.1)", zorder=4)

    for i, v in enumerate(tfr_vals):
        ax.text(v + 0.04, i, f"{v:.2f}", va="center", fontsize=8.0, fontweight="bold", color=t["text"])

    ax.set_yticks(y)
    ax.set_yticklabels(regions, fontsize=8.0, fontweight="bold", color=t["label"])
    ax.set_xlim(0, 2.7)
    ax.set_xlabel("Tổng tỷ suất sinh (Số con / phụ nữ)", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Phân Hóa Mức Sinh TFR Giữa Các Vùng Sinh Thái (2023)", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.4, color=t["grid"])

    leg = ax.legend(loc="lower right", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=8.0)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_dependency_components_grouped(output_path: Path, theme: str = "DARK") -> Path:
    """Grouped bar chart decomposing child vs old-age dependency ratio."""
    years = [1979, 1989, 1999, 2009, 2019, 2029, 2039]
    child_dep = [80.6, 69.8, 54.2, 35.8, 35.8, 30.2, 27.5]
    old_dep = [9.1, 8.4, 9.5, 9.9, 11.4, 17.8, 25.4]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)

    x = np.arange(len(years))
    width = 0.35

    ax.bar(x - width/2, child_dep, width, label="Phụ thuộc Trẻ em (0-14t)", color="#0284C7", zorder=3)
    ax.bar(x + width/2, old_dep, width, label="Phụ thuộc Người già (65+t)", color="#F59E0B", zorder=3)

    for i in range(len(years)):
        ax.text(x[i] - width/2, child_dep[i] + 1.5, f"{child_dep[i]:.1f}", ha="center", fontsize=7.0, fontweight="bold", color=t["text"])
        ax.text(x[i] + width/2, old_dep[i] + 1.5, f"{old_dep[i]:.1f}", ha="center", fontsize=7.0, fontweight="bold", color="#F59E0B")

    ax.set_ylim(0, 95)
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years], fontsize=8.5, fontweight="bold", color=t["tick"])
    ax.set_ylabel("Số người phụ thuộc / 100 người lao động", fontsize=9.0, fontweight="bold", color=t["label"])
    ax.set_title("Chuyển Dịch Thành Tố Phụ Thuộc: Trẻ Em Giảm & Người Già Tăng", fontsize=11, fontweight="bold", color=t["title"], pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.4, color=t["grid"])

    leg = ax.legend(loc="upper right", frameon=True, facecolor=t["legend_bg"], edgecolor=t["legend_edge"], fontsize=8.0)
    for txt in leg.get_texts():
        txt.set_color(t["legend_text"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def generate_census_data_collection_flow(output_path: Path, theme: str = "DARK") -> Path:
    """Flowchart/infographic of census data collection stages."""
    stages = [
        ("Giai đoạn 1", "Lập Bảng Kê Địa Bàn", "Vẽ sơ đồ địa bàn điều tra,\nphân định ranh giới tổ dân phố"),
        ("Giai đoạn 2", "Thu Thập CAPI / Web", "Phỏng vấn trực tiếp bằng CAPI,\nngười dân tự kê khai trực tuyến"),
        ("Giai đoạn 3", "Kiểm Định Chất Lượng", "Giám sát định vị GPS, đối soát\nlogic dữ liệu thời gian thực"),
        ("Giai đoạn 4", "Tổng Hợp & Phân Tích", "Làm sạch bộ dữ liệu lớn,\ntính toán các chỉ số nhân khẩu"),
        ("Giai đoạn 5", "Công Bố & Ứng Dụng", "Phát hành số liệu chính thức,\nphục vụ quy hoạch quốc gia"),
    ]

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=220)
    t = _apply_theme(fig, ax, theme)
    ax.axis("off")

    colors = ["#0284C7", "#0D9488", "#10B981", "#F59E0B", "#8B5CF6"]

    for i, (tag, title, desc) in enumerate(stages):
        y_center = 0.85 - i * 0.17
        rect = plt.Rectangle((0.05, y_center - 0.065), 0.90, 0.13,
                             facecolor=t["legend_bg"], edgecolor=colors[i], linewidth=1.5, zorder=2)
        ax.add_patch(rect)

        circle = plt.Circle((0.11, y_center), 0.045, color=colors[i], zorder=3)
        ax.add_patch(circle)
        ax.text(0.11, y_center, str(i+1), ha="center", va="center", fontsize=10.0, fontweight="bold", color="#FFFFFF", zorder=4)

        ax.text(0.18, y_center + 0.025, f"{tag}: {title}".upper(), fontsize=8.5, fontweight="bold", color=colors[i], zorder=4)
        ax.text(0.18, y_center - 0.035, desc, fontsize=7.5, color=t["text"], va="center", zorder=4)

        if i < len(stages) - 1:
            ax.annotate("", xy=(0.50, y_center - 0.075), xytext=(0.50, y_center - 0.065),
                        arrowprops=dict(arrowstyle="->", color=colors[i], lw=1.5), zorder=5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.95)
    ax.set_title("Quy Trình 5 Giai Đoạn Thu Thập Dữ Liệu Tổng Điều Tra Dân Số", fontsize=11, fontweight="bold", color=t["title"], pad=14)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close()
    return output_path


def render_all_demographic_charts(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    res = {}
    chart_funcs = {
        "system_interaction": generate_system_interaction,
        "population_pyramid": generate_population_pyramid,
        "fertility_trends": generate_fertility_trends,
        "regional_density": generate_regional_density,
        "math_models": generate_math_models_chart,
        "population_metrics": generate_population_metrics,
        "demo_transition_stages": generate_demo_transition_stages,
        "hdi_dimensions": generate_hdi_dimensions,
        "dependency_ratio_trends": generate_dependency_ratio_trends,
        "urbanization_scurve": generate_urbanization_scurve,
        "age_structure_radar": generate_age_structure_radar,
        "mortality_curve_gompertz": generate_mortality_curve_gompertz,
        "migration_flows_matrix": generate_migration_flows_matrix,
        "sex_ratio_birth_heatmap": generate_sex_ratio_birth_heatmap,
        "population_forecast_scenarios": generate_population_forecast_scenarios,
        "labor_force_donut": generate_labor_force_donut,
        "life_expectancy_waterfall": generate_life_expectancy_waterfall,
        "demographic_dividend_stacked_area": generate_demographic_dividend_stacked_area,
        "urban_rural_divergence_bubble": generate_urban_rural_divergence_bubble,
        "fertility_by_region_bar": generate_fertility_by_region_bar,
        "dependency_components_grouped": generate_dependency_components_grouped,
        "census_data_collection_flow": generate_census_data_collection_flow,
    }

    for name, func in chart_funcs.items():
        dark_p = output_dir / f"chart_{name}_dark.png"
        light_p = output_dir / f"chart_{name}_light.png"
        base_p = output_dir / f"chart_{name}.png"

        func(dark_p, theme="DARK")
        func(light_p, theme="LIGHT")
        shutil.copy2(dark_p, base_p)

        res[name.upper() + "_DARK"] = dark_p
        res[name.upper() + "_LIGHT"] = light_p
        res[name.upper()] = base_p

    return res


if __name__ == "__main__":
    out = Path("assets/charts")
    paths = render_all_demographic_charts(out)
    print(f"Rendered {len(paths)} dual-themed demographic charts successfully.")
