import tkinter as tk
from tkinter import ttk, font

class HospitalPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("MedCAD | Hospital Ordering Portal")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f4f7f6")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=13, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=11)
        self.small_font = font.Font(family="Helvetica", size=10)

        self.build_header()
        self.build_welcome_banner()
        self.build_search_and_catalog()
        self.build_part_details_panel()

    def build_header(self):
        header = tk.Frame(self.root, bg="#008080", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🏥 Trust Portal: London General", font=self.title_font, fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
        tk.Label(header, text="Role: In-house Engineering", font=self.body_font, fg="#e0e0e0", bg="#008080").pack(side="right", padx=20, pady=20)

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

        # Expanded Dummy Data
        parts = [
            ("MC-104", "Ventilator Monitor Bracket (SELECTED)", "Philips", "🛡️ Verified Hash"),
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
            ("MC-1105", "Surgical Light Handle Adapter", "Steris", "🛡️ Verified Hash")
        ]
        
        for part in parts:
            tags = ('selected',) if part[0] == "MC-104" else ()
            self.tree.insert("", tk.END, values=part, tags=tags)
        
        self.tree.tag_configure('selected', background='#ccebff')

    def build_part_details_panel(self):
        panel = tk.Frame(self.root, bg="white", highlightbackground="#cccccc", highlightthickness=1, padx=20, pady=20)
        panel.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(panel, text="Part Specifications: Ventilator Monitor Bracket (MC-104)", font=self.title_font, bg="white", fg="#0a2540").pack(anchor="w", pady=(0, 15))

        # 3-Column Info Grid
        info_frame = tk.Frame(panel, bg="white")
        info_frame.pack(fill="x")

        # Column 1: Mechanical Specs
        col1 = tk.Frame(info_frame, bg="white")
        col1.pack(side="left", fill="both", expand=True)
        tk.Label(col1, text="📏 Geometric Data", font=self.header_font, bg="white", fg="#008080").pack(anchor="w", pady=(0, 5))
        tk.Label(col1, text="• Dimensions (X,Y,Z): 120 x 85 x 45 mm", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col1, text="• Volume: 142,500 mm³", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col1, text="• Max Load Rating: 15 kg (Static)", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col1, text="• Assembly: 2x M4 Threaded Inserts req.", font=self.body_font, bg="white").pack(anchor="w")

        # Column 2: AM Constraints
        col2 = tk.Frame(info_frame, bg="white")
        col2.pack(side="left", fill="both", expand=True)
        tk.Label(col2, text="⚙️ Manufacturing Specs", font=self.header_font, bg="white", fg="#008080").pack(anchor="w", pady=(0, 5))
        tk.Label(col2, text="• Material: PA12 Nylon (ISO 10993)", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col2, text="• Required Process: SLS", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col2, text="• Tolerances: ISO 2768-mK", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col2, text="• Surface: Chemical resistant (IPA wipes)", font=self.body_font, bg="white").pack(anchor="w")

        # Column 3: Logistics
        col3 = tk.Frame(info_frame, bg="white")
        col3.pack(side="left", fill="both", expand=True)
        tk.Label(col3, text="🚚 Logistics & Impact", font=self.header_font, bg="white", fg="#008080").pack(anchor="w", pady=(0, 5))
        tk.Label(col3, text="• Print Hub: AM-South Hub (12 miles)", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col3, text="• Est. Print Time: 4 Hours 15 Mins", font=self.body_font, bg="white").pack(anchor="w")
        tk.Label(col3, text="• OEM Lead Time: 14 Days", font=self.body_font, bg="white", fg="#cc0000").pack(anchor="w")
        tk.Label(col3, text="• MedCAD Lead Time: < 24 Hours", font=self.body_font, bg="white", fg="#009900").pack(anchor="w")

        tk.Frame(panel, bg="#eeeeee", height=2).pack(fill="x", pady=20)

        # Action Button Area
        btn_frame = tk.Frame(panel, bg="white")
        btn_frame.pack(fill="x")
        
        tk.Label(btn_frame, text="Status: Ready for Dispatch. File integrity verified.", font=self.body_font, bg="white", fg="#555555").pack(side="left")
        
        # Updated Button Text Here
        btn = tk.Button(btn_frame, text="Add to Cart ➔", font=self.header_font, bg="#00d4ff", fg="#0a2540", activebackground="#00b8e6", padx=20, pady=10, borderwidth=0)
        btn.pack(side="right")

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalPortal(root)
    root.mainloop()
