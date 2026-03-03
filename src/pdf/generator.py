"""
PDF Generator — builds the post-visit measurement report using ReportLab.

Layout per page:
  - Header: company logo (left) + report title (right)
  - Footer: page number
  - Content: module sections rendered sequentially
"""
import os
from datetime import date
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph,
    Spacer, Table, TableStyle, Image, HRFlowable,
    KeepTogether,
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Font registration (Unicode support for Polish characters) ─────────────────
_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/System/Library/Fonts",
    "C:/Windows/Fonts",
]

def _find_font(filename: str) -> str | None:
    for d in _FONT_DIRS:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
    return None

def _register_fonts():
    """Register DejaVu Sans (or fallback) for Unicode / Polish character support."""
    candidates = [
        ("DejaVuSans",       "DejaVuSans.ttf"),
        ("DejaVuSans-Bold",  "DejaVuSans-Bold.ttf"),
        ("LiberationSans",   "LiberationSans-Regular.ttf"),
        ("LiberationSans-Bold", "LiberationSans-Bold.ttf"),
    ]
    registered: dict[str, str] = {}
    for name, fname in candidates:
        path = _find_font(fname)
        if path:
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                registered[name] = name
            except Exception:
                pass

    # Register font families so <b> tags in Paragraphs work with TTFont
    if "DejaVuSans" in registered and "DejaVuSans-Bold" in registered:
        pdfmetrics.registerFontFamily(
            "DejaVuSans",
            normal="DejaVuSans",
            bold="DejaVuSans-Bold",
        )
    if "LiberationSans" in registered and "LiberationSans-Bold" in registered:
        pdfmetrics.registerFontFamily(
            "LiberationSans",
            normal="LiberationSans",
            bold="LiberationSans-Bold",
        )
    return registered

_REGISTERED = _register_fonts()

# Choose the best available font family
if "DejaVuSans" in _REGISTERED:
    _FONT_NORMAL = "DejaVuSans"
    _FONT_BOLD   = _REGISTERED.get("DejaVuSans-Bold", "DejaVuSans")
elif "LiberationSans" in _REGISTERED:
    _FONT_NORMAL = "LiberationSans"
    _FONT_BOLD   = _REGISTERED.get("LiberationSans-Bold", "LiberationSans")
else:
    # Fallback to built-in (Polish diacritics may not render)
    _FONT_NORMAL = "Helvetica"
    _FONT_BOLD   = "Helvetica-Bold"

# ── Constants ─────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_L = 20 * mm
MARGIN_R = 20 * mm
MARGIN_T = 28 * mm   # leaves room for header
MARGIN_B = 20 * mm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

HEADER_H = 22 * mm
FOOTER_H = 10 * mm

# Colors matching company logo palette: charcoal #2B2A28 + red #E31E25
RED    = colors.HexColor("#E31E25")   # primary / headings underline
DARK   = colors.HexColor("#2B2A28")   # header background (charcoal)
NAVY   = colors.HexColor("#2B2A28")   # kept as alias for compat
BLUE   = colors.HexColor("#E31E25")   # section heading accent line
LIGHT  = colors.HexColor("#F4F4F4")   # section heading background
BORDER = colors.HexColor("#E0E0E0")
TEXT   = colors.HexColor("#2B2A28")   # body text (charcoal)
GREY   = colors.HexColor("#6B6B69")
RED    = colors.HexColor("#DC2626")

LOGO_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "assets", "logo.png"
)


# ── Helper flowable: thin coloured rule ──────────────────────────────────────

class ColoredHR(HRFlowable):
    pass


# ── Page template helpers ─────────────────────────────────────────────────────

def _draw_header(canvas, doc):
    canvas.saveState()

    # White background
    canvas.setFillColor(colors.white)
    canvas.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)

    # Logo (left-aligned, vertically centred in header area above the red line)
    logo_path = LOGO_PATH
    logo_area_top    = PAGE_H - HEADER_H + 2 * mm   # 2mm gap from header bottom
    logo_area_height = HEADER_H - 4 * mm            # leave 2mm on each side
    if os.path.exists(logo_path):
        try:
            canvas.drawImage(
                logo_path,
                MARGIN_L, logo_area_top,
                width=50 * mm, height=logo_area_height,
                preserveAspectRatio=True, mask="auto",
            )
        except Exception:
            pass

    # Title text: right-aligned, vertically centred
    title = getattr(doc, "report_title", "Raport Powyjazdowy")
    report_date = getattr(doc, "report_date", "")
    full_title = f"{title}  |  {report_date}" if report_date else title
    canvas.setFillColor(DARK)
    canvas.setFont(_FONT_BOLD, 10)
    text_y = PAGE_H - HEADER_H / 2 - 4   # approximate vertical centre
    canvas.drawRightString(PAGE_W - MARGIN_R, text_y, full_title)

    # Red rule at the bottom edge of the header
    canvas.setFillColor(RED)
    canvas.rect(0, PAGE_H - HEADER_H, PAGE_W, 2, fill=1, stroke=0)

    canvas.restoreState()


def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BORDER)
    canvas.rect(MARGIN_L, MARGIN_B - 4 * mm, CONTENT_W, 0.3 * mm, fill=1, stroke=0)
    canvas.setFont(_FONT_NORMAL, 8)
    canvas.setFillColor(GREY)
    canvas.drawRightString(
        PAGE_W - MARGIN_R,
        MARGIN_B - 3 * mm,
        f"Strona {canvas.getPageNumber()}",
    )
    canvas.restoreState()


def _on_page(canvas, doc):
    _draw_header(canvas, doc)
    _draw_footer(canvas, doc)


# ── Style registry ────────────────────────────────────────────────────────────

def _build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["h1"] = ParagraphStyle(
        "h1",
        fontName=_FONT_BOLD,
        fontSize=14,
        textColor=NAVY,
        spaceAfter=4,
    )
    styles["h2"] = ParagraphStyle(
        "h2",
        fontName=_FONT_BOLD,
        fontSize=11,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=4,
        leftIndent=0,
    )
    styles["h3"] = ParagraphStyle(
        "h3",
        fontName=_FONT_BOLD,
        fontSize=10,
        textColor=GREY,
        spaceBefore=6,
        spaceAfter=2,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName=_FONT_NORMAL,
        fontSize=9,
        textColor=TEXT,
        leading=13,
        spaceAfter=2,
    )
    styles["label"] = ParagraphStyle(
        "label",
        fontName=_FONT_BOLD,
        fontSize=8,
        textColor=GREY,
        spaceAfter=1,
    )
    styles["value"] = ParagraphStyle(
        "value",
        fontName=_FONT_NORMAL,
        fontSize=9,
        textColor=TEXT,
        spaceAfter=4,
    )
    styles["small"] = ParagraphStyle(
        "small",
        fontName=_FONT_NORMAL,
        fontSize=8,
        textColor=GREY,
        spaceAfter=2,
    )
    return styles


# ── Flowable builders ─────────────────────────────────────────────────────────

def _section_heading(title: str, module_id: int, styles: dict) -> list:
    """Returns a list of flowables for a module section heading."""
    items = []
    items.append(Spacer(1, 6 * mm))
    # Coloured background
    heading_table = Table(
        [[Paragraph(f"<b>{module_id}. {title}</b>", styles["h2"])]],
        colWidths=[CONTENT_W],
    )
    heading_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 1, BLUE),
        ("ROUNDEDCORNERS", [4]),
    ]))
    items.append(heading_table)
    items.append(Spacer(1, 3 * mm))
    return items


def _kv(label: str, value: str, styles: dict) -> list:
    """Key-value pair; skipped entirely if value is empty."""
    if not value:
        return []
    return [
        Paragraph(label, styles["label"]),
        Paragraph(value, styles["value"]),
    ]


def _kv_table(pairs: list[tuple[str, str]], styles: dict, cols: int = 2) -> Table | None:
    """Renders multiple key-value pairs in a grid table. Skips empty values."""
    non_empty = [(k, v) for k, v in pairs if v]
    if not non_empty:
        return None

    # Pad to full rows
    while len(non_empty) % cols:
        non_empty.append(("", ""))

    col_w = CONTENT_W / cols
    data = []
    for i in range(0, len(non_empty), cols):
        label_row = []
        value_row = []
        for j in range(cols):
            k, v = non_empty[i + j]
            label_row.append(Paragraph(k, styles["label"]) if k else "")
            value_row.append(Paragraph(v, styles["value"]) if v else "")
        data.append(label_row)
        data.append(value_row)

    t = Table(data, colWidths=[col_w] * cols)
    style_cmds = [
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",     (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 2),
        ("LEFTPADDING",    (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 4),
    ]
    # Thin bottom border under each label row (even rows: 0, 2, 4 …)
    for r in range(0, len(data), 2):
        style_cmds.append(("LINEBELOW", (0, r), (-1, r), 0.5, BORDER))
    t.setStyle(TableStyle(style_cmds))
    return t


def _bullet_list(items: list[str], styles: dict) -> list:
    """Renders a bulleted list; skips empty items."""
    flowables = []
    for item in items:
        if item.strip():
            flowables.append(
                Paragraph(f"• {item.strip()}", styles["body"])
            )
    return flowables


def _add_image(path: str, max_w_mm: float = 120, max_h_mm: float = 80) -> Image | None:
    """Returns a ReportLab Image flowable, or None if path is invalid."""
    if not path or not os.path.exists(path):
        return None
    try:
        img = Image(path, width=max_w_mm * mm, height=max_h_mm * mm,
                    kind="proportional")
        img.hAlign = "LEFT"
        return img
    except Exception:
        return None


def _grid_table(headers: list[str], rows: list[list[str]], styles: dict) -> Table | None:
    """Generic table with styled header row."""
    if not headers and not rows:
        return None
    col_w = CONTENT_W / max(len(headers), 1)
    header_para = [Paragraph(h, styles["label"]) for h in headers]
    data = [header_para]
    for row in rows:
        data.append([Paragraph(str(c), styles["body"]) for c in row])

    t = Table(data, colWidths=[col_w] * len(headers))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("TEXTCOLOR", (0, 0), (-1, 0), GREY),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


# ── Module renderers ──────────────────────────────────────────────────────────

def _render_module1(data: dict, styles: dict) -> list:
    flowables = []
    flowables += _section_heading("Informacje Ogólne", 1, styles)

    dates = data.get("measurement_dates", [])
    dates_str = ", ".join(
        d.strftime("%d.%m.%Y") if isinstance(d, date) else str(d)
        for d in dates
    )
    report_date = data.get("report_date")
    report_date_str = (
        report_date.strftime("%d.%m.%Y") if isinstance(report_date, date)
        else str(report_date) if report_date else ""
    )

    tbl = _kv_table([
        ("Numer projektu",        data.get("project_number", "")),
        ("Nazwa projektu",        data.get("project_name", "")),
        ("Data pomiarów",         dates_str),
        ("Data wypełnienia",      report_date_str),
        ("Lokalizacja",           data.get("location", "")),
        ("Google Maps",           data.get("maps_link", "")),
        ("Kierownik pomiarów",    data.get("team_leader", "")),
        ("Skład zespołu",         data.get("team_members", "").replace("\n", ", ")),
    ], styles, cols=2)
    if tbl:
        flowables.append(tbl)
        flowables.append(Spacer(1, 3 * mm))

    # Contact person
    contact_parts = []
    for field in ["contact_title", "contact_first", "contact_last"]:
        v = data.get(field, "").strip()
        if v:
            contact_parts.append(v)
    contact_name = " ".join(contact_parts)
    contact_detail_pairs = [
        ("Osoba do kontaktu", contact_name),
        ("Telefon",           data.get("contact_phone", "")),
        ("E-mail",            data.get("contact_email", "")),
    ]
    ctbl = _kv_table(contact_detail_pairs, styles, cols=3)
    if ctbl:
        flowables.append(ctbl)
        flowables.append(Spacer(1, 2 * mm))

    return flowables


def _render_module2(data: dict, styles: dict) -> list:
    flowables = []
    flowables += _section_heading("Sprzęt Pomiarowy", 2, styles)

    optical = data.get("optical_recorders", {})
    all_optical = (optical.get("checked", []) + optical.get("custom", []))
    if all_optical:
        flowables.append(Paragraph("Rejestratory optyczne", styles["h3"]))
        flowables += _bullet_list(all_optical, styles)

    other = data.get("other_devices", {})
    all_other = (other.get("checked", []) + other.get("custom", []))
    if all_other:
        flowables.append(Spacer(1, 2 * mm))
        flowables.append(Paragraph("Inne urządzenia", styles["h3"]))
        flowables += _bullet_list(all_other, styles)

    return flowables


def _render_sensors(data: dict, module_id: int, title: str, styles: dict) -> list:
    flowables = []
    flowables += _section_heading(title, module_id, styles)

    sensors = data.get("sensors", [])
    if not sensors:
        return flowables

    # Determine columns
    has_type = any(s.get("sensor_type") for s in sensors)
    headers = ["Nazwa", "Nr seryjny"] + (["Rodzaj"] if has_type else []) + ["Uwagi"]
    rows = []
    for s in sensors:
        row = [s.get("name", ""), s.get("serial", "")]
        if has_type:
            row.append(s.get("sensor_type", ""))
        row.append(s.get("notes", ""))
        rows.append(row)

    tbl = _grid_table(headers, rows, styles)
    if tbl:
        flowables.append(tbl)

    # Images
    for i, s in enumerate(sensors):
        img = _add_image(s.get("image_path", ""), max_w_mm=80, max_h_mm=60)
        if img:
            flowables.append(Spacer(1, 2 * mm))
            flowables.append(Paragraph(f"Zdjęcie — {s.get('name', f'Czujnik {i+1}')}", styles["small"]))
            flowables.append(img)

    return flowables


def _render_module5(data: dict, styles: dict) -> list:
    flowables = []
    flowables += _section_heading("Inwentaryzacja", 5, styles)

    headers = data.get("headers", [])
    rows = data.get("rows", [])
    tbl = _grid_table(headers, rows, styles)
    if tbl:
        flowables.append(tbl)

    desc = data.get("description", "")
    if desc:
        flowables.append(Spacer(1, 2 * mm))
        flowables += _kv("Opis", desc, styles)

    img = _add_image(data.get("image_path", ""))
    if img:
        flowables.append(img)

    return flowables


def _render_module6(data: dict, styles: dict) -> list:
    flowables = []
    flowables += _section_heading("Przebieg Pomiarów", 6, styles)

    desc = data.get("description", "")
    if desc:
        flowables.append(Paragraph("Opis sposobu prowadzenia pomiarów", styles["h3"]))
        flowables.append(Paragraph(desc.replace("\n", "<br/>"), styles["body"]))
    for p in data.get("desc_images", []):
        img = _add_image(p)
        if img:
            flowables.append(img)

    schedule = data.get("schedule", [])
    valid_schedule = [s for s in schedule if s.get("stage") or s.get("duration")]
    if valid_schedule:
        flowables.append(Spacer(1, 2 * mm))
        flowables.append(Paragraph("Harmonogram pomiarów", styles["h3"]))
        tbl = _grid_table(
            ["Etap / Opis", "Czas trwania"],
            [[s.get("stage", ""), s.get("duration", "")] for s in valid_schedule],
            styles,
        )
        if tbl:
            flowables.append(tbl)

    problems = data.get("problems", "")
    if problems:
        flowables.append(Spacer(1, 2 * mm))
        flowables.append(Paragraph("Problemy w trakcie pomiarów", styles["h3"]))
        flowables.append(Paragraph(problems.replace("\n", "<br/>"), styles["body"]))
    for p in data.get("prob_images", []):
        img = _add_image(p)
        if img:
            flowables.append(img)

    return flowables


def _render_module7(data: dict, styles: dict) -> list:
    flowables = []
    flowables += _section_heading("Lista Rzeczy do Zabrania", 7, styles)
    items = data.get("items", [])
    flowables += _bullet_list(items, styles)
    return flowables


def _render_module8(data: dict, styles: dict) -> list:
    flowables = []
    flowables += _section_heading("Uwagi", 8, styles)
    notes = data.get("notes", "")
    if notes:
        flowables.append(Paragraph(notes.replace("\n", "<br/>"), styles["body"]))
    for p in data.get("images", []):
        img = _add_image(p)
        if img:
            flowables.append(img)
    return flowables


def _render_module9(data: dict, styles: dict) -> list:
    flowables = []
    flowables += _section_heading("Logistyka i Organizacja", 9, styles)
    pairs = [
        ("Parkowanie",              data.get("parking", "")),
        ("Lokalizacja pomiarów",    data.get("site_location", "")),
        ("Nocleg",                  data.get("accommodation", "")),
        ("Inne",                    data.get("other", "")),
    ]
    tbl = _kv_table(pairs, styles, cols=1)
    if tbl:
        flowables.append(tbl)
    return flowables


# ── Public API ────────────────────────────────────────────────────────────────

RENDERERS = {
    1: _render_module1,
    2: _render_module2,
    3: lambda d, s: _render_sensors(d, 3, "Czujniki Światłowodowe", s),
    4: lambda d, s: _render_sensors(d, 4, "Czujniki Inne", s),
    5: _render_module5,
    6: _render_module6,
    7: _render_module7,
    8: _render_module8,
    9: _render_module9,
}


def generate_pdf(all_data: dict, output_path: str) -> None:
    """
    Generate the PDF report.

    Parameters
    ----------
    all_data : dict
        Keys are module IDs (1-9). Each value is a dict with module data
        plus a special key 'enabled' (bool) to skip disabled modules.
        Module 1 data also contains 'initials', 'project_number', etc.
    output_path : str
        Absolute path where the PDF will be written.
    """
    styles = _build_styles()
    module1_data = all_data.get(1, {})
    project_number = module1_data.get("project_number", "")
    project_name = module1_data.get("project_name", "")
    report_title = f"Raport Powyjazdowy — {project_number}" if project_number else "Raport Powyjazdowy"

    # Build dates string for header
    measurement_dates = module1_data.get("measurement_dates", [])
    dates_str = ", ".join(
        d.strftime("%d.%m.%Y") if isinstance(d, date) else str(d)
        for d in measurement_dates
    )

    frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W, PAGE_H - MARGIN_T - MARGIN_B,
                  id="main", leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    page_template = PageTemplate(id="main", frames=[frame], onPage=_on_page)

    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        pageTemplates=[page_template],
    )
    doc.report_title = report_title
    doc.report_date  = dates_str

    flowables = []

    # Cover / title block
    flowables.append(Spacer(1, 6 * mm))
    flowables.append(Paragraph(report_title, styles["h1"]))
    if project_name:
        flowables.append(Paragraph(project_name, styles["body"]))
    flowables.append(HRFlowable(width=CONTENT_W, color=BLUE, thickness=2))
    flowables.append(Spacer(1, 3 * mm))

    # Render each module
    for mid in range(1, 10):
        module_data = all_data.get(mid, {})
        enabled = module_data.get("enabled", True)
        if not enabled:
            continue
        renderer = RENDERERS.get(mid)
        if renderer:
            section = renderer(module_data, styles)
            if section:
                flowables += section

    doc.build(flowables)
