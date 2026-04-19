import tkinter as tk
from tkinter import font

class LandingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("MedCAD Digital Library | National Digital Supply Network")
        self.root.geometry("950x750")
        self.root.configure(bg="#f4f7f6") # Soft light gray/blue background

        # Custom Fonts
        self.header_font = font.Font(family="Helvetica", size=32, weight="bold")
        self.sub_font = font.Font(family="Helvetica", size=14, slant="italic")
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.mission_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=12)
        self.small_font = font.Font(family="Helvetica", size=10)

        self.build_header()
        self.build_mission_vision()
        self.build_how_it_works()
        self.build_features()
        self.build_auth_buttons()
        self.build_footer()

    def build_header(self):
        # Dark Blue Header Banner
        header_frame = tk.Frame(self.root, bg="#0a2540", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False) 

        tk.Label(header_frame, text="MedCAD Digital Library", font=self.header_font, fg="white", bg="#0a2540").pack(pady=(20, 5))
        tk.Label(header_frame, text="Secure Additive Manufacturing for the NHS", font=self.sub_font, fg="#00d4ff", bg="#0a2540").pack()

    def build_mission_vision(self):
        content_frame = tk.Frame(self.root, bg="#f4f7f6")
        content_frame.pack(pady=(25, 10), padx=50, fill="x")

        # Bolded Mission Statement
        mission_text = (
            "OUR MISSION: To eliminate equipment downtime across NHS Trusts by localizing the production\n"
            "of eligible, critical non-patient contact components through a governance-controlled digital supply chain."
        )
        tk.Label(content_frame, text=mission_text, font=self.mission_font, bg="#f4f7f6", fg="#222222", justify="center").pack()

        # Divider
        tk.Frame(content_frame, bg="#cccccc", height=2, width=400).pack(pady=15)

    def build_how_it_works(self):
        workflow_frame = tk.Frame(self.root, bg="#f4f7f6")
        workflow_frame.pack(pady=10, fill="x")

        tk.Label(workflow_frame, text="How the MedCAD Hub Works", font=self.title_font, bg="#f4f7f6", fg="#0a2540").pack(pady=(0, 15))

        steps_frame = tk.Frame(workflow_frame, bg="#f4f7f6")
        steps_frame.pack()

        steps = [
            ("1. OEM Uploads", "Suppliers securely upload verified CAD files."),
            ("➔", ""),
            ("2. Hospital Requests", "Trusts order parts via the digital catalog."),
            ("➔", ""),
            ("3. Hub Fabricates", "Regional hubs print with full QA traceability.")
        ]

        for i, (title, desc) in enumerate(steps):
            col_frame = tk.Frame(steps_frame, bg="#f4f7f6")
            col_frame.grid(row=0, column=i, padx=10)
            
            if title == "➔":
                tk.Label(col_frame, text=title, font=self.title_font, bg="#f4f7f6", fg="#888888").pack(pady=10)
            else:
                tk.Label(col_frame, text=title, font=self.title_font, bg="#f4f7f6", fg="#008080").pack()
                tk.Label(col_frame, text=desc, font=self.small_font, bg="#f4f7f6", fg="#555555", wraplength=150, justify="center").pack()

    def build_features(self):
        features_container = tk.Frame(self.root, bg="#f4f7f6")
        features_container.pack(pady=(25, 10), padx=40, fill="x")

        tk.Label(features_container, text="Core Platform Capabilities", font=self.title_font, bg="#f4f7f6", fg="#0a2540").pack(pady=(0, 15))

        cards_frame = tk.Frame(features_container, bg="#f4f7f6")
        cards_frame.pack(fill="x")

        # Center-aligned text and increased padding inside the cards
        self.create_feature_card(cards_frame, 0, "🛡️ OEM Authorized", "Verified CAD files travel securely. Strict access controls and permitted use-cases ensure design integrity.")
        self.create_feature_card(cards_frame, 1, "🏥 Non-Patient Contact", "Specializing in the rapid deployment of functional replacements like brackets, housings, and mounts.")
        self.create_feature_card(cards_frame, 2, "📋 Audit & Traceability", "ISO/ASTM 52920 aligned. Every production event logs file version, parameters, and QA results.")

    def create_feature_card(self, parent, col, title, text):
        # Increased padx and pady here for breathing room
        card = tk.Frame(parent, bg="white", highlightbackground="#e0e0e0", highlightthickness=1, padx=20, pady=20)
        card.grid(row=0, column=col, padx=15, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1) 

        # Changed to anchor="center" and justify="center"
        tk.Label(card, text=title, font=self.title_font, bg="white", fg="#0a2540").pack(anchor="center", pady=(0, 10))
        tk.Label(card, text=text, font=self.body_font, bg="white", fg="#555555", justify="center", wraplength=220).pack(anchor="center")

    def build_auth_buttons(self):
        # New frame specifically for Login/Signup, with extra top padding to fill empty space
        auth_frame = tk.Frame(self.root, bg="#f4f7f6")
        auth_frame.pack(pady=(40, 20)) 

        # Log In Button
        login_btn = tk.Button(auth_frame, text="Log In", font=self.title_font, bg="#0a2540", fg="white", activebackground="#113a63", activeforeground="white", borderwidth=0, padx=30, pady=10)
        login_btn.grid(row=0, column=0, padx=10)

        # Sign Up Button
        signup_btn = tk.Button(auth_frame, text="Sign Up", font=self.title_font, bg="#00d4ff", fg="#0a2540", activebackground="#00b8e6", borderwidth=0, padx=30, pady=10)
        signup_btn.grid(row=0, column=1, padx=10)

    def build_footer(self):
        footer_frame = tk.Frame(self.root, bg="#f4f7f6")
        footer_frame.pack(side="bottom", fill="x")

        # Standard Website Footer Links
        footer_bottom = tk.Frame(footer_frame, bg="#0a2540", pady=10)
        footer_bottom.pack(fill="x")
        
        footer_text = "© 2026 MedCAD Digital Library | Partnered with NHS | Privacy Policy | OEM Portal Login | Support"
        tk.Label(footer_bottom, text=footer_text, font=self.small_font, bg="#0a2540", fg="#aaaaaa").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = LandingPage(root)
    root.mainloop()
