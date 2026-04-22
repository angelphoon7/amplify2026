import tkinter as tk
from tkinter import ttk, font
import importlib.util
import os
import random
import string
import subprocess
import tempfile
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

PART_SPECS = {
    "MC-104": {
        "name": "Ventilator Monitor Bracket (MC-104)",
        "geo": [
            "• Dimensions (X,Y,Z): 120 x 85 x 45 mm",
            "• Volume: 142,500 mm³",
            "• Max Load Rating: 15 kg (Static)",
            "• Assembly: 2x M4 Threaded Inserts req.",
        ],
        "mfg": [
            "• Material: PA12 Nylon (ISO 10993)",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-mK",
            "• Surface: Chemical resistant (IPA wipes)",
        ],
        "log": [
            "• Print Hub: AM-South Hub (12 miles)",
            "• Est. Print Time: 4 Hours 15 Mins",
            "• OEM Lead Time: 14 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-299": {
        "name": "Syringe Pump Gear Housing (MC-299)",
        "geo": [
            "• Dimensions (X,Y,Z): 65 x 40 x 30 mm",
            "• Volume: 52,000 mm³",
            "• Max Torque Rating: 0.8 Nm",
            "• Assembly: 4x M3 Threaded Inserts req.",
        ],
        "mfg": [
            "• Material: PA12-GB Glass-Bead Nylon",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-fH",
            "• Surface: Medical-grade smooth finish",
        ],
        "log": [
            "• Print Hub: AM-North Hub (8 miles)",
            "• Est. Print Time: 2 Hours 30 Mins",
            "• OEM Lead Time: 21 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-305": {
        "name": "IV Pole Clamp Assembly (MC-305)",
        "geo": [
            "• Dimensions (X,Y,Z): 80 x 60 x 55 mm",
            "• Volume: 198,000 mm³",
            "• Clamp Diameter Range: 22–32 mm",
            "• Assembly: 2x Wing-nut bolts req.",
        ],
        "mfg": [
            "• Material: PETG (ISO 10993)",
            "• Required Process: FDM",
            "• Tolerances: ISO 2768-mK",
            "• Surface: UV stabilised exterior",
        ],
        "log": [
            "• Print Hub: AM-East Hub (15 miles)",
            "• Est. Print Time: 3 Hours 00 Mins",
            "• OEM Lead Time: 10 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-412": {
        "name": "Bed Motor Mount Plate (MC-412)",
        "geo": [
            "• Dimensions (X,Y,Z): 210 x 160 x 12 mm",
            "• Volume: 241,920 mm³",
            "• Max Load Rating: 80 kg (Dynamic)",
            "• Assembly: 6x M6 Threaded Inserts req.",
        ],
        "mfg": [
            "• Material: PA2200 Nylon (ISO 10993)",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-mK",
            "• Surface: Anti-static coating req.",
        ],
        "log": [
            "• Print Hub: AM-Midlands Hub (22 miles)",
            "• Est. Print Time: 6 Hours 45 Mins",
            "• OEM Lead Time: 28 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-550": {
        "name": "Dialysis Machine Caster Lock (MC-550)",
        "geo": [
            "• Dimensions (X,Y,Z): 95 x 70 x 40 mm",
            "• Volume: 176,400 mm³",
            "• Hold Force: 120 N",
            "• Assembly: 1x M8 bolt insert req.",
        ],
        "mfg": [
            "• Material: PA12 Nylon (ISO 10993)",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-mK",
            "• Surface: Chemical wash resistant",
        ],
        "log": [
            "• Print Hub: AM-South Hub (18 miles)",
            "• Est. Print Time: 3 Hours 45 Mins",
            "• OEM Lead Time: 18 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-610": {
        "name": "Wheelchair Spoke Guard Mount (MC-610)",
        "geo": [
            "• Dimensions (X,Y,Z): 45 x 45 x 8 mm",
            "• Volume: 10,800 mm³",
            "• Max Load: 5 kg",
            "• Assembly: 3x M3 snap-fit clips",
        ],
        "mfg": [
            "• Material: ABS (ISO 10993)",
            "• Required Process: FDM",
            "• Tolerances: ISO 2768-fH",
            "• Surface: Smooth outer surface",
        ],
        "log": [
            "• Print Hub: AM-West Hub (5 miles)",
            "• Est. Print Time: 1 Hour 15 Mins",
            "• OEM Lead Time: 7 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-722": {
        "name": "Oxygen Tank Holder Base (MC-722)",
        "geo": [
            "• Dimensions (X,Y,Z): 180 x 180 x 20 mm",
            "• Volume: 388,800 mm³",
            "• Max Load Rating: 6 kg",
            "• Assembly: 4x M6 rubber feet inserts",
        ],
        "mfg": [
            "• Material: PA12 Nylon (ISO 10993)",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-mK",
            "• Surface: Non-slip base finish",
        ],
        "log": [
            "• Print Hub: AM-South Hub (12 miles)",
            "• Est. Print Time: 5 Hours 30 Mins",
            "• OEM Lead Time: 12 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-805": {
        "name": "Defibrillator Cart Handle (MC-805)",
        "geo": [
            "• Dimensions (X,Y,Z): 300 x 30 x 25 mm",
            "• Volume: 225,000 mm³",
            "• Pull Force Rating: 50 N",
            "• Assembly: 2x M6 Threaded Inserts req.",
        ],
        "mfg": [
            "• Material: PA12-CF Carbon-Fibre Nylon",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-mK",
            "• Surface: Ergonomic grip finish",
        ],
        "log": [
            "• Print Hub: AM-North Hub (8 miles)",
            "• Est. Print Time: 4 Hours 00 Mins",
            "• OEM Lead Time: 21 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-911": {
        "name": "Centrifuge Rotor Lid Knob (MC-911)",
        "geo": [
            "• Dimensions (X,Y,Z): 35 x 35 x 20 mm",
            "• Volume: 18,375 mm³",
            "• Max Torque Rating: 1.2 Nm",
            "• Assembly: 1x M6 hex insert req.",
        ],
        "mfg": [
            "• Material: PEEK (ISO 10993)",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-fH",
            "• Surface: Chemical resistant polished finish",
        ],
        "log": [
            "• Print Hub: AM-East Hub (15 miles)",
            "• Est. Print Time: 1 Hour 00 Mins",
            "• OEM Lead Time: 30 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-950": {
        "name": "Endoscopy Cabinet Latch (MC-950)",
        "geo": [
            "• Dimensions (X,Y,Z): 70 x 25 x 15 mm",
            "• Volume: 19,250 mm³",
            "• Latch Force: 8 N",
            "• Assembly: 2x M3 Threaded Inserts req.",
        ],
        "mfg": [
            "• Material: PA12 Nylon (ISO 10993)",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-fH",
            "• Surface: Cleanroom compatible finish",
        ],
        "log": [
            "• Print Hub: AM-Midlands Hub (22 miles)",
            "• Est. Print Time: 1 Hour 30 Mins",
            "• OEM Lead Time: 14 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-1002": {
        "name": "Anesthesia Machine Cable Clip (MC-1002)",
        "geo": [
            "• Dimensions (X,Y,Z): 50 x 20 x 12 mm",
            "• Volume: 8,400 mm³",
            "• Cable Dia. (max): 8 mm",
            "• Assembly: Snap-fit, no inserts req.",
        ],
        "mfg": [
            "• Material: TPU 95A Flex (ISO 10993)",
            "• Required Process: FDM",
            "• Tolerances: ISO 2768-fH",
            "• Surface: Flexible clip grip",
        ],
        "log": [
            "• Print Hub: AM-West Hub (5 miles)",
            "• Est. Print Time: 0 Hours 45 Mins",
            "• OEM Lead Time: 9 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
    "MC-1105": {
        "name": "Surgical Light Handle Adapter (MC-1105)",
        "geo": [
            "• Dimensions (X,Y,Z): 60 x 60 x 35 mm",
            "• Volume: 98,000 mm³",
            "• Max Load Rating: 10 kg",
            "• Assembly: 1x M8 sterile-insert req.",
        ],
        "mfg": [
            "• Material: PA12 Nylon (ISO 10993)",
            "• Required Process: SLS",
            "• Tolerances: ISO 2768-mK",
            "• Surface: Autoclave sterilisable",
        ],
        "log": [
            "• Print Hub: AM-South Hub (12 miles)",
            "• Est. Print Time: 2 Hours 15 Mins",
            "• OEM Lead Time: 25 Days",
            "• MedCAD Lead Time: < 24 Hours",
        ],
    },
}

PART_PRICES = {
    "MC-104":  ("£48.00",  48.00),
    "MC-299":  ("£36.00",  36.00),
    "MC-305":  ("£22.00",  22.00),
    "MC-412":  ("£85.00",  85.00),
    "MC-550":  ("£52.00",  52.00),
    "MC-610":  ("£18.00",  18.00),
    "MC-722":  ("£64.00",  64.00),
    "MC-805":  ("£74.00",  74.00),
    "MC-911":  ("£95.00",  95.00),
    "MC-950":  ("£28.00",  28.00),
    "MC-1002": ("£12.00",  12.00),
    "MC-1105": ("£112.00", 112.00),
}

class HospitalPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("MedCAD | Hospital Ordering Portal")
        self.root.geometry("1100x750")
        self.root.state("zoomed")
        self.root.configure(bg="#f4f7f6")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=13, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=11)
        self.small_font = font.Font(family="Helvetica", size=10)
        self.cart_count = 0
        self.cart_items = []
        self.confirmed_orders = []
        self.order_number = None
        self.current_part_id = "MC-104"

        self.build_header()
        self.build_welcome_banner()
        self.build_search_and_catalog()
        self.build_part_details_panel()

    def open_landing_page(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title("MedCAD Digital Library | National Digital Supply Network")
        self.root.geometry("950x750")
        spec = importlib.util.spec_from_file_location("interface1", os.path.join(os.path.dirname(os.path.abspath(__file__)), "interface 1.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.LandingPage(self.root)

    def build_header(self):
        header = tk.Frame(self.root, bg="#008080", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🏥 Trust Portal: London General", font=self.title_font, fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
        tk.Button(header, text="Log Out", font=self.body_font, bg="#cc0000", fg="white", activebackground="#a30000", activeforeground="white", borderwidth=0, padx=15, pady=6, command=self.open_landing_page).pack(side="right", padx=20, pady=18)
        tk.Button(header, text="📋  Your Order", font=self.body_font, bg="#005f5f", fg="white",
          activebackground="#004d4d", activeforeground="white", borderwidth=0,
          padx=15, pady=6, command=self.open_confirmed_orders).pack(side="right", padx=(0, 10), pady=18)
        tk.Label(header, text="Role: In-house Engineering", font=self.body_font, fg="#e0e0e0", bg="#008080").pack(side="right", padx=(20, 0), pady=20)

    def build_welcome_banner(self):
        banner = tk.Frame(self.root, bg="#e6f2f2", pady=15, padx=20)
        banner.pack(fill="x", pady=(0, 10))
        
        intro_text = (
            "Welcome to the MedCAD Digital Ordering System.\n"
            "Browse OEM-authorized, non-patient contact components below. Select a part to view its engineering "
            "specifications and dispatch a rapid fabrication request to your nearest approved regional AM Hub."
        )
        tk.Label(banner, text=intro_text, font=self.body_font, bg="#e6f2f2", fg="#004d4d", justify="left").pack(anchor="w")

    def build_search_and_catalog(self):
        search_frame = tk.Frame(self.root, bg="#f4f7f6", pady=5)
        search_frame.pack(fill="x", padx=20)
        
        tk.Label(search_frame, text="Search Digital Catalog:", font=self.header_font, bg="#f4f7f6", fg="#0a2540").pack(side="left")
        search_entry = ttk.Entry(search_frame, width=40, font=self.body_font)
        search_entry.pack(side="left", padx=10)
        search_entry.insert(0, "Filter by: Non-Patient Contact")
        ttk.Button(search_frame, text="Search").pack(side="left")

        catalog_frame = tk.Frame(self.root, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        catalog_frame.pack(fill="x", padx=20, pady=10)

        # Added a scrollbar for the longer list
        scroll_y = tk.Scrollbar(catalog_frame)
        scroll_y.pack(side="right", fill="y")

        columns = ("Part ID", "Component Name", "OEM Owner", "Security Status", "Price")
        self.tree = ttk.Treeview(catalog_frame, columns=columns, show="headings", height=8, yscrollcommand=scroll_y.set)

        scroll_y.config(command=self.tree.yview)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")
        self.tree.column("Component Name", width=260, anchor="w")
        self.tree.column("Price", width=90, anchor="center")

        self.tree.pack(fill="x", expand=True)
        self.tree.bind("<Double-1>", self.on_part_double_click)

        parts = [
            ("MC-104",  "Ventilator Monitor Bracket",    "Philips",      "🛡️ Verified Hash", "£48.00"),
            ("MC-299",  "Syringe Pump Gear Housing",     "Baxter",       "🛡️ Verified Hash", "£36.00"),
            ("MC-305",  "IV Pole Clamp Assembly",        "Medtronic",    "🛡️ Verified Hash", "£22.00"),
            ("MC-412",  "Bed Motor Mount Plate",         "Stryker",      "🛡️ Verified Hash", "£85.00"),
            ("MC-550",  "Dialysis Machine Caster Lock",  "Fresenius",    "🛡️ Verified Hash", "£52.00"),
            ("MC-610",  "Wheelchair Spoke Guard Mount",  "Invacare",     "🛡️ Verified Hash", "£18.00"),
            ("MC-722",  "Oxygen Tank Holder Base",       "Drive Medical","🛡️ Verified Hash", "£64.00"),
            ("MC-805",  "Defibrillator Cart Handle",     "Zoll",         "🛡️ Verified Hash", "£74.00"),
            ("MC-911",  "Centrifuge Rotor Lid Knob",     "Eppendorf",    "🛡️ Verified Hash", "£95.00"),
            ("MC-950",  "Endoscopy Cabinet Latch",       "Olympus",      "🛡️ Verified Hash", "£28.00"),
            ("MC-1002", "Anesthesia Machine Cable Clip", "GE Healthcare","🛡️ Verified Hash", "£12.00"),
            ("MC-1105", "Surgical Light Handle Adapter", "Steris",       "🛡️ Verified Hash", "£112.00"),
        ]

        self.selected_iid = None
        self.item_iids = {}
        for part in parts:
            iid = self.tree.insert("", tk.END, values=part)
            self.item_iids[part[0]] = iid

        self.tree.tag_configure('selected', background='#ccebff')

    def build_part_details_panel(self):
        self.details_panel = tk.Frame(self.root, bg="white", highlightbackground="#cccccc", highlightthickness=1, padx=20, pady=20)
        self.details_panel.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Persistent button bar — never destroyed when switching parts
        tk.Frame(self.details_panel, bg="#eeeeee", height=2).pack(side="bottom", fill="x", pady=(8, 0))
        btn_bar = tk.Frame(self.details_panel, bg="white")
        btn_bar.pack(side="bottom", fill="x")
        tk.Label(btn_bar, text="Status: Ready for Dispatch. File integrity verified.", font=self.body_font, bg="white", fg="#555555").pack(side="left")
        cart_container = tk.Frame(btn_bar, bg="white")
        cart_container.pack(side="right", padx=(10, 0))
        tk.Button(cart_container, text="🛒  Cart", font=self.header_font, bg="#0a2540", fg="white", activebackground="#113a63", activeforeground="white", padx=15, pady=10, borderwidth=0, command=self.open_order_summary).pack()
        badge_text = str(self.cart_count) if self.cart_count > 0 else ""
        self.cart_badge = tk.Label(cart_container, text=badge_text, bg="#cc0000", fg="white", font=font.Font(family="Helvetica", size=9, weight="bold"), padx=4, pady=1)
        self.cart_badge.place(relx=1.0, rely=0.0, anchor="ne")
        tk.Button(btn_bar, text="Add to Cart ➔", font=self.header_font, bg="#00d4ff", fg="#0a2540", activebackground="#00b8e6", padx=20, pady=10, borderwidth=0, command=self._add_to_cart).pack(side="right")

        self.details_content = None
        self._select_part(self.item_iids["MC-104"], "MC-104")

    def _render_part_details(self, part_id):
        if self.details_content:
            self.details_content.destroy()

        spec = PART_SPECS[part_id]
        self.details_content = tk.Frame(self.details_panel, bg="white")
        self.details_content.pack(fill="both", expand=True)

        tk.Label(self.details_content, text=f"Part Specifications: {spec['name']}", font=self.title_font, bg="white", fg="#0a2540").pack(anchor="w", pady=(0, 15))

        info_frame = tk.Frame(self.details_content, bg="white")
        info_frame.pack(fill="both", expand=True)

        col1 = tk.Frame(info_frame, bg="white")
        col1.pack(side="left", fill="both", expand=True)
        tk.Label(col1, text="📏 Geometric Data", font=self.header_font, bg="white", fg="#008080").pack(anchor="w", pady=(0, 5))
        for line in spec["geo"]:
            tk.Label(col1, text=line, font=self.body_font, bg="white").pack(anchor="w")

        col2 = tk.Frame(info_frame, bg="white")
        col2.pack(side="left", fill="both", expand=True)
        tk.Label(col2, text="⚙️ Manufacturing Specs", font=self.header_font, bg="white", fg="#008080").pack(anchor="w", pady=(0, 5))
        for line in spec["mfg"]:
            tk.Label(col2, text=line, font=self.body_font, bg="white").pack(anchor="w")

        col3 = tk.Frame(info_frame, bg="white")
        col3.pack(side="left", fill="both", expand=True)
        tk.Label(col3, text="🚚 Logistics & Impact", font=self.header_font, bg="white", fg="#008080").pack(anchor="w", pady=(0, 5))
        for i, line in enumerate(spec["log"]):
            color = "#cc0000" if i == 2 else "#009900" if i == 3 else "black"
            tk.Label(col3, text=line, font=self.body_font, bg="white", fg=color).pack(anchor="w")
        price_str = PART_PRICES.get(part_id, ("£N/A", 0))[0]
        tk.Label(col3, text=f"• MedCAD Price: {price_str}", font=self.body_font, bg="white", fg="#0a2540").pack(anchor="w")

    def open_traceability_passport(self):
        root3 = tk.Toplevel(self.root)
        spec = importlib.util.spec_from_file_location("interface3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "interface 3.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.CompliancePassport(root3)

    def generate_invoice(self, order):
        today = date.today().strftime("%d %B %Y")
        order_num = order["order_number"]
        items = order["items"]
        total = sum(it.get("price_val", 0.0) for it in items)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf",
                                         prefix=f"Invoice_{order_num}_")
        save_path = tmp.name
        tmp.close()

        styles = getSampleStyleSheet()
        navy = colors.HexColor("#0a2540")
        teal = colors.HexColor("#008080")
        light = colors.HexColor("#e8f4f4")

        title_style = ParagraphStyle("inv_title", parent=styles["Normal"],
                                     fontSize=22, textColor=navy,
                                     fontName="Helvetica-Bold",
                                     spaceAfter=4*mm, spaceBefore=0)
        sub_style = ParagraphStyle("inv_sub", parent=styles["Normal"],
                                   fontSize=10, textColor=teal,
                                   fontName="Helvetica", spaceAfter=6*mm)
        meta_label_style = ParagraphStyle("inv_meta_label", parent=styles["Normal"],
                                          fontSize=11, textColor=navy,
                                          fontName="Helvetica-Bold", spaceAfter=3*mm)
        meta_style = ParagraphStyle("inv_meta", parent=styles["Normal"],
                                    fontSize=10, textColor=colors.HexColor("#444444"),
                                    fontName="Helvetica", spaceAfter=2*mm)
        footer_style = ParagraphStyle("inv_footer", parent=styles["Normal"],
                                      fontSize=8, textColor=colors.HexColor("#888888"),
                                      fontName="Helvetica", alignment=TA_CENTER,
                                      spaceAfter=2*mm)
        total_style = ParagraphStyle("inv_total", parent=styles["Normal"],
                                     fontSize=12, textColor=navy,
                                     fontName="Helvetica-Bold", alignment=TA_RIGHT)

        doc = SimpleDocTemplate(save_path, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)

        story = []
        story.append(Paragraph("MedCAD Digital Library", title_style))
        story.append(Paragraph("National Digital Supply Network | Partnered with NHS", sub_style))
        story.append(Paragraph("Invoice / Order Confirmation", meta_label_style))
        story.append(Paragraph(f"Order Number:  {order_num}", meta_style))
        story.append(Paragraph(f"Date Issued:  {today}", meta_style))
        story.append(Spacer(1, 6*mm))

        # Strip distance info from hub text to keep cells compact
        def short_hub(hub_str):
            return hub_str.split(" (")[0] if " (" in hub_str else hub_str

        # Part ID 20 | Component Name 60 | OEM 25 | Hub 38 | Price 27 = 170mm
        col_w = [20*mm, 60*mm, 25*mm, 38*mm, 27*mm]
        table_data = [["Part ID", "Component Name", "OEM", "Hub", "Price"]]
        for it in items:
            table_data.append([
                it.get("id", ""),
                it.get("name", ""),
                it.get("oem", ""),
                short_hub(it.get("hub", "")),
                it.get("price", ""),
            ])

        tbl = Table(table_data, colWidths=col_w, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), navy),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, light]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
            ("LEFTPADDING", (0, 0), (-1, -1), 3*mm),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3*mm),
            ("TOPPADDING", (0, 0), (-1, -1), 3*mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3*mm),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph(f"<b>Total:  £{total:.2f}</b>", total_style))
        story.append(Spacer(1, 10*mm))

        disclaimer = (
            "This invoice is issued in accordance with ISO/ASTM 52920 guidelines. "
            "Design liability is retained by the respective OEM. Manufacturing liability "
            "is assumed by the certified regional AM hub. "
            "For queries contact: support@medcad.nhs.uk"
        )
        story.append(Paragraph(disclaimer, footer_style))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph("© 2026 MedCAD Digital Library | Partnered with NHS", footer_style))

        doc.build(story)

        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for chrome in chrome_paths:
            if os.path.exists(chrome):
                subprocess.Popen([chrome, save_path])
                return
        os.startfile(save_path)

    def open_confirmed_orders(self):
        page = tk.Toplevel(self.root)
        page.title("MedCAD | Your Orders")
        page.geometry("900x600")
        page.state("zoomed")
        page.configure(bg="#f4f7f6")

        header = tk.Frame(page, bg="#008080", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📋  Your Orders", font=self.title_font, fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
        tk.Button(header, text="✕  Close", font=self.body_font, bg="#cc0000", fg="white", activebackground="#a30000", borderwidth=0, padx=15, pady=6, command=page.destroy).pack(side="right", padx=20, pady=18)

        content = tk.Frame(page, bg="#f4f7f6")
        content.pack(fill="both", expand=True, padx=30, pady=20)

        if not self.confirmed_orders:
            tk.Label(content, text="No confirmed orders yet.", font=self.body_font, bg="#f4f7f6", fg="#888888").pack(pady=60)
            return

        canvas = tk.Canvas(content, bg="#f4f7f6", highlightthickness=0)
        scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#f4f7f6")
        scroll_frame.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        for order in self.confirmed_orders:
            order_card = tk.Frame(scroll_frame, bg="white", highlightbackground="#cccccc", highlightthickness=1)
            order_card.pack(fill="x", pady=10, padx=5)

            title_bar = tk.Frame(order_card, bg="#0a2540", pady=8, padx=15)
            title_bar.pack(fill="x")
            tk.Label(title_bar, text=f"Order Number:  {order['order_number']}", font=self.header_font, bg="#0a2540", fg="#00d4ff").pack(side="left")
            tk.Label(title_bar, text=f"{len(order['items'])} item(s)", font=self.body_font, bg="#0a2540", fg="#aaaaaa").pack(side="right")

            col_frame = tk.Frame(order_card, bg="#e8f4f4")
            col_frame.pack(fill="x")
            for text, w in [("Part ID", 10), ("Component Name", 30), ("OEM", 15), ("Hub", 22), ("Est. Time", 14)]:
                tk.Label(col_frame, text=text, font=self.small_font, bg="#e8f4f4", fg="#004d4d", width=w, anchor="w").pack(side="left", padx=8, pady=5)

            for i, item in enumerate(order["items"]):
                row_bg = "white" if i % 2 == 0 else "#f9f9f9"
                row = tk.Frame(order_card, bg=row_bg)
                row.pack(fill="x")
                for text, w in [(item["id"], 10), (item["name"], 30), (item["oem"], 15), (item["hub"], 22), (item["time"], 14)]:
                    tk.Label(row, text=text, font=self.small_font, bg=row_bg, fg="#333333", width=w, anchor="w").pack(side="left", padx=8, pady=6)

            passport_bar = tk.Frame(order_card, bg="white", pady=8, padx=10)
            passport_bar.pack(fill="x")
            tk.Button(passport_bar, text="🛡️  Quality & Traceability Passport", font=self.body_font, bg="#0a2540", fg="white", activebackground="#113a63", borderwidth=0, padx=15, pady=7, command=self.open_traceability_passport).pack(side="left")
            tk.Button(passport_bar, text="🧾  Invoice", font=self.body_font, bg="#008080", fg="white", activebackground="#005f5f", borderwidth=0, padx=15, pady=7, command=lambda o=order: self.generate_invoice(o)).pack(side="left", padx=(10, 0))

    def open_payment_page(self, total, on_success):
        payment = tk.Toplevel(self.root)
        payment.title("MedCAD | Secure Payment")
        payment.geometry("520x580")
        payment.resizable(False, False)
        payment.configure(bg="#f4f7f6")

        # Header
        header = tk.Frame(payment, bg="#0a2540", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="💳  Secure Payment", font=self.title_font,
                 fg="white", bg="#0a2540").pack(side="left", padx=20, pady=15)
        tk.Label(header, text="🔒 SSL Encrypted", font=self.small_font,
                 fg="#aaaaaa", bg="#0a2540").pack(side="right", padx=20)

        # Amount bar
        amt = tk.Frame(payment, bg="#e6f2f2", pady=12, padx=20)
        amt.pack(fill="x")
        tk.Label(amt, text="Amount Due:", font=self.header_font,
                 bg="#e6f2f2", fg="#004d4d").pack(side="left")
        tk.Label(amt, text=f"  £{total:.2f}", font=font.Font(family="Helvetica", size=18, weight="bold"),
                 bg="#e6f2f2", fg="#0a2540").pack(side="left")

        # Form
        form = tk.Frame(payment, bg="#f4f7f6", padx=35, pady=20)
        form.pack(fill="both", expand=True)

        lbl_font = font.Font(family="Helvetica", size=11)
        entry_font = font.Font(family="Helvetica", size=12)

        # Card type
        tk.Label(form, text="Card Type", font=lbl_font, bg="#f4f7f6", fg="#333333").pack(anchor="w")
        card_type_var = tk.StringVar(value="Visa")
        ct_frame = tk.Frame(form, bg="#f4f7f6")
        ct_frame.pack(anchor="w", pady=(4, 14))
        for ctype in ["Visa", "Mastercard", "Amex"]:
            tk.Radiobutton(ct_frame, text=ctype, variable=card_type_var, value=ctype,
                           font=lbl_font, bg="#f4f7f6", activebackground="#f4f7f6").pack(side="left", padx=(0, 16))

        # Cardholder name
        tk.Label(form, text="Cardholder Name", font=lbl_font, bg="#f4f7f6", fg="#333333").pack(anchor="w")
        name_entry = tk.Entry(form, font=entry_font, relief="solid", bd=1)
        name_entry.pack(fill="x", ipady=7, pady=(4, 14))

        # Card number
        tk.Label(form, text="Card Number", font=lbl_font, bg="#f4f7f6", fg="#333333").pack(anchor="w")
        card_entry = tk.Entry(form, font=entry_font, relief="solid", bd=1, fg="#aaaaaa")
        card_entry.pack(fill="x", ipady=7, pady=(4, 14))
        card_entry.insert(0, "XXXX  XXXX  XXXX  XXXX")

        def card_focus_in(_):
            if card_entry.get() == "XXXX  XXXX  XXXX  XXXX":
                card_entry.delete(0, "end")
                card_entry.config(fg="#111111")

        def card_focus_out(_):
            if card_entry.get().strip() == "":
                card_entry.insert(0, "XXXX  XXXX  XXXX  XXXX")
                card_entry.config(fg="#aaaaaa")

        card_entry.bind("<FocusIn>", card_focus_in)
        card_entry.bind("<FocusOut>", card_focus_out)

        # Expiry + CVV row
        row2 = tk.Frame(form, bg="#f4f7f6")
        row2.pack(fill="x", pady=(0, 14))

        exp_frame = tk.Frame(row2, bg="#f4f7f6")
        exp_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))
        tk.Label(exp_frame, text="Expiry Date (MM/YY)", font=lbl_font, bg="#f4f7f6", fg="#333333").pack(anchor="w")
        exp_entry = tk.Entry(exp_frame, font=entry_font, relief="solid", bd=1, width=10, fg="#aaaaaa")
        exp_entry.pack(anchor="w", ipady=7, pady=(4, 0))
        exp_entry.insert(0, "MM/YY")

        def exp_focus_in(_):
            if exp_entry.get() == "MM/YY":
                exp_entry.delete(0, "end")
                exp_entry.config(fg="#111111")

        def exp_focus_out(_):
            if exp_entry.get().strip() == "":
                exp_entry.insert(0, "MM/YY")
                exp_entry.config(fg="#aaaaaa")

        exp_entry.bind("<FocusIn>", exp_focus_in)
        exp_entry.bind("<FocusOut>", exp_focus_out)

        cvv_frame = tk.Frame(row2, bg="#f4f7f6")
        cvv_frame.pack(side="right", padx=(0, 0))
        tk.Label(cvv_frame, text="CVV", font=lbl_font, bg="#f4f7f6", fg="#333333").pack(anchor="w")
        cvv_entry = tk.Entry(cvv_frame, font=entry_font, relief="solid", bd=1, width=6, show="●")
        cvv_entry.pack(anchor="w", ipady=7, pady=(4, 0))

        # Error label
        error_lbl = tk.Label(form, text="", font=lbl_font, bg="#f4f7f6", fg="#cc0000")
        error_lbl.pack(anchor="w")

        def process_payment():
            name = name_entry.get().strip()
            exp = exp_entry.get().strip()
            cvv = cvv_entry.get().strip()

            if not name:
                error_lbl.config(text="⚠  Please enter the cardholder name.")
                return
            raw_card = card_entry.get().replace(" ", "")
            if len(raw_card) != 16 or not raw_card.isdigit():
                error_lbl.config(text="⚠  Card number must be 16 digits.")
                return
            if len(exp) != 5 or exp[2] != "/" or not exp[:2].isdigit() or not exp[3:].isdigit():
                error_lbl.config(text="⚠  Enter expiry as MM/YY.")
                return
            if len(cvv) not in (3, 4) or not cvv.isdigit():
                error_lbl.config(text="⚠  CVV must be 3 or 4 digits.")
                return

            on_success()
            payment.destroy()

        tk.Button(form, text=f"  Pay  £{total:.2f}  Now  🔒  ", font=self.header_font,
                  bg="#0a2540", fg="white", activebackground="#113a63",
                  borderwidth=0, padx=10, pady=12, command=process_payment).pack(fill="x", pady=(6, 0))

        tk.Label(form, text="🔒  256-bit SSL encrypted. Your card details are never stored.",
                 font=self.small_font, bg="#f4f7f6", fg="#888888").pack(pady=(10, 0))

    def open_order_summary(self):
        summary = tk.Toplevel(self.root)
        summary.title("MedCAD | Order Summary")
        summary.geometry("900x600")
        summary.configure(bg="#f4f7f6")
        summary.resizable(True, True)

        # ── Header ──
        header = tk.Frame(summary, bg="#008080", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🛒 Order Summary", font=self.title_font,
                 fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
        tk.Button(header, text="✕  Close", font=self.body_font, bg="#cc0000",
                  fg="white", activebackground="#a30000", borderwidth=0,
                  padx=15, pady=6, command=summary.destroy).pack(side="right", padx=20, pady=18)

        # ── Order number bar (permanent) ──
        order_bar = tk.Frame(summary, bg="#e6f2f2", pady=8, padx=15)
        order_bar.pack(fill="x", padx=20, pady=(12, 0))
        order_num_var = tk.StringVar(value=f"Order Number:  {self.order_number or '—'}")
        tk.Label(order_bar, textvariable=order_num_var,
                 font=self.header_font, bg="#e6f2f2", fg="#004d4d").pack(side="left")

        # ── Empty-cart label (hidden when items present) ──
        empty_lbl = tk.Label(summary, text="Your cart is empty. Add items from the catalog.",
                             font=self.body_font, bg="#f4f7f6", fg="#888888")

        # ── Treeview (permanent) ──
        tree_frame = tk.Frame(summary, bg="#f4f7f6")
        columns = ("#", "Part ID", "Component Name", "OEM", "Price", "Est. Time")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        widths = [40, 80, 250, 120, 80, 110]
        for col, w in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="w", stretch=False)
        tree.column("Component Name", stretch=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        # ── Bottom controls (permanent) ──
        bottom = tk.Frame(summary, bg="#f4f7f6")
        bottom.pack(side="bottom", fill="x", padx=20, pady=10)
        tk.Frame(summary, bg="#cccccc", height=1).pack(side="bottom", fill="x", padx=20)

        footer_lbl = tk.Label(bottom, text="", font=self.header_font,
                               bg="#f4f7f6", fg="#0a2540")
        footer_lbl.pack(side="left")

        pay_btn = tk.Button(bottom, text="Confirm Order & Make Payment  💳",
                            font=self.header_font, bg="#008080", fg="white",
                            activebackground="#006666", borderwidth=0, padx=20, pady=8)
        pay_btn.pack(side="right")

        def remove_selected():
            sel = tree.selection()
            if not sel:
                return
            remove_item(int(sel[0]))

        tk.Button(bottom, text="✕  Remove Selected", font=self.body_font,
                  bg="#cc0000", fg="white", activebackground="#a30000",
                  borderwidth=0, padx=12, pady=5,
                  command=remove_selected).pack(side="left", padx=(10, 0))

        def refresh():
            # Clear treeview
            for row in tree.get_children():
                tree.delete(row)

            if not self.cart_items:
                tree_frame.pack_forget()
                empty_lbl.pack(pady=60)
                footer_lbl.config(text="")
                pay_btn.config(state="disabled")
                order_num_var.set("Order Number:  —")
                return

            empty_lbl.pack_forget()
            tree_frame.pack(fill="both", expand=True, padx=20, pady=(8, 0))

            order_num_var.set(f"Order Number:  {self.order_number or '—'}")

            for i, it in enumerate(self.cart_items):
                tree.insert("", tk.END, iid=str(i),
                            values=(i + 1, it["id"], it["name"],
                                    it["oem"], it["price"], it["time"]))

            total = sum(it["price_val"] for it in self.cart_items)
            footer_lbl.config(text=f"Items: {len(self.cart_items)}    Total: £{total:.2f}")
            pay_btn.config(state="normal",
                           command=lambda t=total: self.open_payment_page(t, confirm_order))

        def confirm_order():
            self.confirmed_orders.append({
                "order_number": self.order_number,
                "items": list(self.cart_items),
            })
            self.cart_items.clear()
            self.cart_count = 0
            self.order_number = None
            self.cart_badge.config(text="")
            notif = tk.Frame(summary, bg="#28a745", padx=15, pady=12)
            notif.place(relx=1.0, rely=0.0, anchor="ne", x=-15, y=15)
            tk.Label(notif, text="✓  Order confirmed, you may close this page now",
                     font=self.body_font, bg="#28a745", fg="white").pack()
            refresh()

        def remove_item(index):
            self.cart_items.pop(index)
            self.cart_count -= 1
            self.cart_badge.config(text=str(self.cart_count) if self.cart_count > 0 else "")
            if not self.cart_items:
                self.order_number = None
            refresh()

        refresh()

    def _select_part(self, iid, part_id):
        if self.selected_iid and self.selected_iid != iid:
            prev = list(self.tree.item(self.selected_iid, "values"))
            prev[1] = prev[1].replace(" (SELECTED)", "")
            self.tree.item(self.selected_iid, values=prev, tags=())
        values = list(self.tree.item(iid, "values"))
        if "(SELECTED)" not in values[1]:
            values[1] = values[1] + " (SELECTED)"
        self.tree.item(iid, values=values, tags=('selected',))
        self.selected_iid = iid
        self.current_part_id = part_id
        self._render_part_details(part_id)

    def _add_to_cart(self):
        spec = PART_SPECS[self.current_part_id]
        oem = self.tree.item(self.item_iids[self.current_part_id], "values")[2]
        price_str, price_val = PART_PRICES.get(self.current_part_id, ("£N/A", 0.0))
        item = {
            "id": self.current_part_id,
            "name": spec["name"].rsplit(" (", 1)[0],
            "oem": oem,
            "hub": spec["log"][0].replace("• Print Hub: ", ""),
            "time": spec["log"][1].replace("• Est. Print Time: ", ""),
            "price": price_str,
            "price_val": price_val,
        }
        if self.order_number is None:
            chars = string.ascii_uppercase + string.digits
            self.order_number = "ORD-" + "".join(random.choices(chars, k=3)) + "-" + "".join(random.choices(chars, k=4))
        self.cart_items.append(item)
        self.cart_count += 1
        self.cart_badge.config(text=str(self.cart_count))

    def on_part_double_click(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        iid = selected[0]
        part_id = self.tree.item(iid, "values")[0]
        if part_id in PART_SPECS:
            self._select_part(iid, part_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalPortal(root)
    root.mainloop()
