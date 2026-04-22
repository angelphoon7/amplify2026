import tkinter as tk
from tkinter import ttk


def open_order_window(
    *,
    parent: tk.Misc,
    order: dict,
    title_font,
    header_font,
    body_font,
    small_font,
    on_open_passport=None,
    on_open_invoice=None,
):
    win = tk.Toplevel(parent)
    win.title("MedCAD | Order Confirmed")
    win.geometry("900x600")
    win.configure(bg="#f4f7f6")
    win.resizable(True, True)

    header = tk.Frame(win, bg="#28a745", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(
        header,
        text="✓  Payment Received — Order Confirmed",
        font=title_font,
        fg="white",
        bg="#28a745",
    ).pack(side="left", padx=20, pady=15)
    tk.Button(
        header,
        text="✕  Close",
        font=body_font,
        bg="#0a2540",
        fg="white",
        activebackground="#113a63",
        borderwidth=0,
        padx=15,
        pady=6,
        command=win.destroy,
    ).pack(side="right", padx=20, pady=18)

    top = tk.Frame(win, bg="#e6f2f2", pady=10, padx=15)
    top.pack(fill="x", padx=20, pady=(12, 0))
    tk.Label(
        top,
        text=f"Order Number:  {order.get('order_number', '—')}",
        font=header_font,
        bg="#e6f2f2",
        fg="#004d4d",
    ).pack(side="left")

    items = order.get("items", [])
    total = sum(it.get("price_val", 0.0) for it in items)
    tk.Label(
        top,
        text=f"{len(items)} item(s)    Total: £{total:.2f}",
        font=body_font,
        bg="#e6f2f2",
        fg="#0a2540",
    ).pack(side="right")

    content = tk.Frame(win, bg="#f4f7f6")
    content.pack(fill="both", expand=True, padx=20, pady=12)

    columns = ("#", "Part ID", "Component Name", "OEM", "Hub", "Est. Time", "Price")
    tree = ttk.Treeview(content, columns=columns, show="headings", selectmode="browse")
    widths = [40, 80, 260, 120, 170, 110, 90]
    for col, w in zip(columns, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="w", stretch=False)
    tree.column("Component Name", stretch=True)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    for i, it in enumerate(items):
        tree.insert(
            "",
            tk.END,
            iid=str(i),
            values=(
                i + 1,
                it.get("id", ""),
                it.get("name", ""),
                it.get("oem", ""),
                it.get("hub", ""),
                it.get("time", ""),
                it.get("price", ""),
            ),
        )

    actions = tk.Frame(win, bg="#f4f7f6")
    actions.pack(fill="x", padx=20, pady=(0, 14))

    tk.Label(
        actions,
        text="Next steps:",
        font=header_font,
        bg="#f4f7f6",
        fg="#0a2540",
    ).pack(side="left")

    btns = tk.Frame(actions, bg="#f4f7f6")
    btns.pack(side="right")

    passport_btn = tk.Button(
        btns,
        text="🛡️  Quality & Traceability Passport",
        font=body_font,
        bg="#0a2540",
        fg="white",
        activebackground="#113a63",
        borderwidth=0,
        padx=15,
        pady=7,
        command=on_open_passport if on_open_passport else None,
    )
    passport_btn.pack(side="left")

    invoice_btn = tk.Button(
        btns,
        text="🧾  Invoice",
        font=body_font,
        bg="#008080",
        fg="white",
        activebackground="#005f5f",
        borderwidth=0,
        padx=15,
        pady=7,
        command=(lambda: on_open_invoice(order)) if on_open_invoice else None,
    )
    invoice_btn.pack(side="left", padx=(10, 0))

    if not on_open_passport:
        passport_btn.config(state="disabled")
    if not on_open_invoice:
        invoice_btn.config(state="disabled")

    tk.Label(
        win,
        text="A copy of this order is stored in “Your Orders”.",
        font=small_font,
        bg="#f4f7f6",
        fg="#888888",
    ).pack(pady=(0, 12))

    return win
