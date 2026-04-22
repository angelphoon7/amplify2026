import os
import subprocess
import sys
import tempfile
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _open_file(path: str) -> None:
    if sys.platform == "darwin":
        subprocess.Popen(["open", path])
        return
    if os.name == "nt":
        os.startfile(path)  # type: ignore[attr-defined]
        return
    subprocess.Popen(["xdg-open", path])


def generate_invoice_pdf(order: dict) -> str:
    """
    Generate a final invoice PDF for the given order dict:
    { "order_number": str, "items": [ {id,name,oem,hub,price,price_val}, ... ] }

    Returns the generated PDF path and also opens it with the OS default viewer.
    """
    today = date.today().strftime("%d %B %Y")
    order_num = order.get("order_number", "—")
    items = order.get("items", [])
    total = sum(it.get("price_val", 0.0) for it in items)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", prefix=f"Invoice_{order_num}_")
    save_path = tmp.name
    tmp.close()

    styles = getSampleStyleSheet()
    navy = colors.HexColor("#0a2540")
    teal = colors.HexColor("#008080")
    light = colors.HexColor("#e8f4f4")

    title_style = ParagraphStyle(
        "inv_title",
        parent=styles["Normal"],
        fontSize=22,
        textColor=navy,
        fontName="Helvetica-Bold",
        spaceAfter=4 * mm,
        spaceBefore=0,
    )
    sub_style = ParagraphStyle(
        "inv_sub",
        parent=styles["Normal"],
        fontSize=10,
        textColor=teal,
        fontName="Helvetica",
        spaceAfter=6 * mm,
    )
    meta_label_style = ParagraphStyle(
        "inv_meta_label",
        parent=styles["Normal"],
        fontSize=11,
        textColor=navy,
        fontName="Helvetica-Bold",
        spaceAfter=3 * mm,
    )
    meta_style = ParagraphStyle(
        "inv_meta",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#444444"),
        fontName="Helvetica",
        spaceAfter=2 * mm,
    )
    footer_style = ParagraphStyle(
        "inv_footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#888888"),
        fontName="Helvetica",
        alignment=TA_CENTER,
        spaceAfter=2 * mm,
    )
    total_style = ParagraphStyle(
        "inv_total",
        parent=styles["Normal"],
        fontSize=12,
        textColor=navy,
        fontName="Helvetica-Bold",
        alignment=TA_RIGHT,
    )

    doc = SimpleDocTemplate(
        save_path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    story: list = []
    story.append(Paragraph("MedCAD Digital Library", title_style))
    story.append(Paragraph("National Digital Supply Network | Partnered with NHS", sub_style))
    story.append(Paragraph("Invoice / Order Confirmation", meta_label_style))
    story.append(Paragraph(f"Order Number:  {order_num}", meta_style))
    story.append(Paragraph(f"Date Issued:  {today}", meta_style))
    story.append(Spacer(1, 6 * mm))

    def short_hub(hub_str: str) -> str:
        return hub_str.split(" (")[0] if " (" in hub_str else hub_str

    col_w = [20 * mm, 60 * mm, 25 * mm, 38 * mm, 27 * mm]
    table_data = [["Part ID", "Component Name", "OEM", "Hub", "Price"]]
    for it in items:
        table_data.append(
            [
                it.get("id", ""),
                it.get("name", ""),
                it.get("oem", ""),
                short_hub(it.get("hub", "")),
                it.get("price", ""),
            ]
        )

    tbl = Table(table_data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), navy),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, light]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(tbl)
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(f"<b>Total:  £{total:.2f}</b>", total_style))
    story.append(Spacer(1, 10 * mm))

    disclaimer = (
        "This invoice is issued in accordance with ISO/ASTM 52920 guidelines. "
        "Design liability is retained by the respective OEM. Manufacturing liability "
        "is assumed by the certified regional AM hub. "
        "For queries contact: support@medcad.nhs.uk"
    )
    story.append(Paragraph(disclaimer, footer_style))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("© 2026 MedCAD Digital Library | Partnered with NHS", footer_style))

    doc.build(story)
    _open_file(save_path)
    return save_path

