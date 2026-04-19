import tkinter as tk
from tkinter import font

class CompliancePassport:
    def __init__(self, root):
        self.root = root
        self.root.title("MedCAD | Traceability & Compliance Passport")
        self.root.geometry("1000x700")
        self.root.state("zoomed")
        self.root.configure(bg="#f4f7f6")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=12)
        self.small_font = font.Font(family="Helvetica", size=10)

        self.build_header()
        self.build_order_summary()
        self.build_digital_thread()
        self.build_liability_signoff()

    def build_header(self):
        header = tk.Frame(self.root, bg="#0a2540", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🛡️ Digital Quality & Traceability Passport", font=self.title_font, fg="white", bg="#0a2540").pack(side="left", padx=20, pady=20)
        tk.Label(header, text="Status: ✅ CLEARED FOR USE", font=self.header_font, fg="#00ffcc", bg="#0a2540").pack(side="right", padx=20, pady=25)

    def build_order_summary(self):
        summary_frame = tk.Frame(self.root, bg="white", highlightbackground="#cccccc", highlightthickness=1, padx=20, pady=15)
        summary_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(summary_frame, text="Order Reference: #ORD-2026-884A", font=self.header_font, bg="white", fg="#0a2540").grid(row=0, column=0, sticky="w")
        tk.Label(summary_frame, text="Component: Ventilator Monitor Bracket (MC-104)", font=self.body_font, bg="white", fg="#555555").grid(row=1, column=0, sticky="w", pady=(5,0))
        
        tk.Label(summary_frame, text="Requesting Trust: Southampton General", font=self.header_font, bg="white", fg="#0a2540").grid(row=0, column=1, sticky="w", padx=150)
        tk.Label(summary_frame, text="Fabrication Hub: AM-South Hub", font=self.body_font, bg="white", fg="#555555").grid(row=1, column=1, sticky="w", padx=150, pady=(5,0))

    def build_digital_thread(self):
        thread_frame = tk.Frame(self.root, bg="#f4f7f6")
        thread_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(thread_frame, text="The Digital Thread (Audit Log)", font=self.header_font, bg="#f4f7f6", fg="#0a2540").pack(anchor="w", pady=(0, 10))

        # A clean, card-based timeline replacing the messy terminal text
        steps = [
            ("✅ OEM Authentication", "Philips confirmed CAD integrity. File Hash (SHA-256): 8f4e9a3b2c1...", "April 15, 08:14"),
            ("✅ Trust Authorization", "London General In-house Engineering approved local fabrication.", "April 17, 09:30"),
            ("✅ Manufacturing Parameters", "Printed via SLS. Material: PA12. Layer height: 0.1mm. 100% Infill.", "April 17, 14:15"),
            ("✅ Post-Process & QA", "Dimensional tolerances met (ISO 2768-mK). Chemical resistance layer applied.", "April 17, 15:45")
        ]

        for title, desc, timestamp in steps:
            card = tk.Frame(thread_frame, bg="white", highlightbackground="#e0e0e0", highlightthickness=1, padx=15, pady=10)
            card.pack(fill="x", pady=5)
            
            tk.Label(card, text=title, font=self.header_font, bg="white", fg="#008080").pack(side="left")
            tk.Label(card, text=desc, font=self.body_font, bg="white", fg="#444444").pack(side="left", padx=20)
            tk.Label(card, text=timestamp, font=self.small_font, bg="white", fg="#888888").pack(side="right")

    def build_liability_signoff(self):
        liability_frame = tk.Frame(self.root, bg="#e6f2f2", highlightbackground="#b3e6e6", highlightthickness=1, padx=20, pady=15)
        liability_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(liability_frame, text="⚖️ Legal & Governance Sign-Off", font=self.header_font, bg="#e6f2f2", fg="#004d4d").pack(anchor="w", pady=(0, 10))

        signoff_text = (
            "In accordance with ISO/ASTM 52920 guidelines:\n\n"
            "• Design Liability: Retained by OEM (Philips).\n"
            "• Manufacturing Liability: Assumed by Certified Production Site (AM-South Hub).\n"
            "• Installation Liability: Assumed by Requesting Trust (London General)."
        )
        tk.Label(liability_frame, text=signoff_text, font=self.body_font, bg="#e6f2f2", fg="#333333", justify="left").pack(anchor="w")

        # Fake signature/barcode area for visual effect
        bottom_row = tk.Frame(liability_frame, bg="#e6f2f2")
        bottom_row.pack(fill="x", pady=(15, 0))
        
        tk.Label(bottom_row, text="System Audited & Locked: 2026-04-17", font=self.small_font, bg="#e6f2f2", fg="#004d4d").pack(side="left")
        tk.Button(bottom_row, text="Download PDF Certificate", font=self.body_font, bg="#0a2540", fg="white", borderwidth=0, padx=15, pady=5).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    app = CompliancePassport(root)
    root.mainloop()
