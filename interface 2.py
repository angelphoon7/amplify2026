import tkinter as tk
from tkinter import ttk, font
import importlib.util
import os

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

        self.build_header()
        self.build_welcome_banner()
        self.build_search_and_catalog()
        self.build_part_details_panel()

    def open_landing_page(self):
        self.root.destroy()
        root2 = tk.Tk()
        spec = importlib.util.spec_from_file_location("interface1", os.path.join(os.path.dirname(os.path.abspath(__file__)), "interface 1.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.LandingPage(root2)
        root2.mainloop()

    def build_header(self):
        header = tk.Frame(self.root, bg="#008080", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🏥 Trust Portal: London General", font=self.title_font, fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
        tk.Button(header, text="Log Out", font=self.body_font, bg="#cc0000", fg="white", activebackground="#a30000", activeforeground="white", borderwidth=0, padx=15, pady=6, command=self.open_landing_page).pack(side="right", padx=20, pady=18)
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

        columns = ("Part ID", "Component Name", "OEM Owner", "Security Status")
        self.tree = ttk.Treeview(catalog_frame, columns=columns, show="headings", height=8, yscrollcommand=scroll_y.set)
        
        scroll_y.config(command=self.tree.yview)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.column("Component Name", width=300, anchor="w")
        
        self.tree.pack(fill="x", expand=True)
        self.tree.bind("<Double-1>", self.on_part_double_click)

        parts = [
            ("MC-104", "Ventilator Monitor Bracket", "Philips", "🛡️ Verified Hash"),
            ("MC-299", "Syringe Pump Gear Housing", "Baxter", "🛡️ Verified Hash"),
            ("MC-305", "IV Pole Clamp Assembly", "Medtronic", "🛡️ Verified Hash"),
            ("MC-412", "Bed Motor Mount Plate", "Stryker", "🛡️ Verified Hash"),
            ("MC-550", "Dialysis Machine Caster Lock", "Fresenius", "🛡️ Verified Hash"),
            ("MC-610", "Wheelchair Spoke Guard Mount", "Invacare", "🛡️ Verified Hash"),
            ("MC-722", "Oxygen Tank Holder Base", "Drive Medical", "🛡️ Verified Hash"),
            ("MC-805", "Defibrillator Cart Handle", "Zoll", "🛡️ Verified Hash"),
            ("MC-911", "Centrifuge Rotor Lid Knob", "Eppendorf", "🛡️ Verified Hash"),
            ("MC-950", "Endoscopy Cabinet Latch", "Olympus", "🛡️ Verified Hash"),
            ("MC-1002", "Anesthesia Machine Cable Clip", "GE Healthcare", "🛡️ Verified Hash"),
            ("MC-1105", "Surgical Light Handle Adapter", "Steris", "🛡️ Verified Hash"),
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
        info_frame.pack(fill="x")

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

        tk.Frame(self.details_content, bg="#eeeeee", height=2).pack(fill="x", pady=20)

        btn_frame = tk.Frame(self.details_content, bg="white")
        btn_frame.pack(fill="x")
        tk.Label(btn_frame, text="Status: Ready for Dispatch. File integrity verified.", font=self.body_font, bg="white", fg="#555555").pack(side="left")

        cart_container = tk.Frame(btn_frame, bg="white")
        cart_container.pack(side="right", padx=(10, 0))
        tk.Button(cart_container, text="🛒  Cart", font=self.header_font, bg="#0a2540", fg="white", activebackground="#113a63", activeforeground="white", padx=15, pady=10, borderwidth=0).pack()
        badge_text = str(self.cart_count) if self.cart_count > 0 else ""
        self.cart_badge = tk.Label(cart_container, text=badge_text, bg="#cc0000", fg="white", font=font.Font(family="Helvetica", size=9, weight="bold"), padx=4, pady=1)
        self.cart_badge.place(relx=1.0, rely=0.0, anchor="ne")

        tk.Button(btn_frame, text="Add to Cart ➔", font=self.header_font, bg="#00d4ff", fg="#0a2540", activebackground="#00b8e6", padx=20, pady=10, borderwidth=0, command=self._add_to_cart).pack(side="right")

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
        self._render_part_details(part_id)

    def _add_to_cart(self):
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
