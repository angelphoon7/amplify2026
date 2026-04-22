import tkinter as tk
from tkinter import font as tkfont


def open_your_orders_window(
    *,
    parent: tk.Misc,
    orders: list[dict],
    amount_paid: float | None = None,
    title_font=None,
    header_font=None,
    body_font=None,
    small_font=None,
    on_open_passport=None,
    on_open_invoice=None,
):
    """
    Final page: shows confirmed order(s), items, and amount paid.
    `orders` is a list of dicts: {"order_number": str, "items": [item,...]}
    """
    page = tk.Toplevel(parent)
    page.title("MedCAD | Your Orders")
    page.geometry("900x600")
    page.configure(bg="#f4f7f6")
    page.resizable(True, True)

    # Fonts fallback
    title_font = title_font or tkfont.Font(family="Helvetica", size=18, weight="bold")
    header_font = header_font or tkfont.Font(family="Helvetica", size=13, weight="bold")
    body_font = body_font or tkfont.Font(family="Helvetica", size=11)
    small_font = small_font or tkfont.Font(family="Helvetica", size=10)

    header = tk.Frame(page, bg="#008080", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="📋  Your Orders", font=title_font, fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
    tk.Button(
        header,
        text="✕  Close",
        font=body_font,
        bg="#cc0000",
        fg="white",
        activebackground="#a30000",
        borderwidth=0,
        padx=15,
        pady=6,
        command=page.destroy,
    ).pack(side="right", padx=20, pady=18)

    if amount_paid is not None:
        paid = tk.Frame(page, bg="#e6f2f2", pady=10, padx=15)
        paid.pack(fill="x", padx=20, pady=(12, 0))
        tk.Label(paid, text="Amount Paid:", font=header_font, bg="#e6f2f2", fg="#004d4d").pack(side="left")
        tk.Label(
            paid,
            text=f"  £{amount_paid:.2f}",
            font=tkfont.Font(family="Helvetica", size=16, weight="bold"),
            bg="#e6f2f2",
            fg="#0a2540",
        ).pack(side="left")
        tk.Label(
            paid,
            text="✓ Payment Successful",
            font=body_font,
            bg="#e6f2f2",
            fg="#28a745",
        ).pack(side="right")

    content = tk.Frame(page, bg="#f4f7f6")
    content.pack(fill="both", expand=True, padx=30, pady=20)

    if not orders:
        tk.Label(content, text="No confirmed orders yet.", font=body_font, bg="#f4f7f6", fg="#888888").pack(pady=60)
        return page

    canvas = tk.Canvas(content, bg="#f4f7f6", highlightthickness=0)
    scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f4f7f6")
    scroll_frame.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    for order in orders:
        items = order.get("items", [])
        order_total = sum(it.get("price_val", 0.0) for it in items)

        order_card = tk.Frame(scroll_frame, bg="white", highlightbackground="#cccccc", highlightthickness=1)
        order_card.pack(fill="x", pady=10, padx=5)

        title_bar = tk.Frame(order_card, bg="#0a2540", pady=8, padx=15)
        title_bar.pack(fill="x")
        tk.Label(
            title_bar,
            text=f"Order Number:  {order.get('order_number', '—')}",
            font=header_font,
            bg="#0a2540",
            fg="#00d4ff",
        ).pack(side="left")
        tk.Label(
            title_bar,
            text=f"{len(items)} item(s)    Total: £{order_total:.2f}",
            font=body_font,
            bg="#0a2540",
            fg="#aaaaaa",
        ).pack(side="right")

        col_frame = tk.Frame(order_card, bg="#e8f4f4")
        col_frame.pack(fill="x")
        for text, w in [("Part ID", 10), ("Component Name", 30), ("OEM", 15), ("Hub", 22), ("Est. Time", 14)]:
            tk.Label(col_frame, text=text, font=small_font, bg="#e8f4f4", fg="#004d4d", width=w, anchor="w").pack(
                side="left", padx=8, pady=5
            )

        for i, item in enumerate(items):
            row_bg = "white" if i % 2 == 0 else "#f9f9f9"
            row = tk.Frame(order_card, bg=row_bg)
            row.pack(fill="x")
            for text, w in [
                (item.get("id", ""), 10),
                (item.get("name", ""), 30),
                (item.get("oem", ""), 15),
                (item.get("hub", ""), 22),
                (item.get("time", ""), 14),
            ]:
                tk.Label(row, text=text, font=small_font, bg=row_bg, fg="#333333", width=w, anchor="w").pack(
                    side="left", padx=8, pady=6
                )

        passport_bar = tk.Frame(order_card, bg="white", pady=8, padx=10)
        passport_bar.pack(fill="x")

        tk.Button(
            passport_bar,
            text="🛡️  Quality & Traceability Passport",
            font=body_font,
            bg="#0a2540",
            fg="white",
            activebackground="#113a63",
            borderwidth=0,
            padx=15,
            pady=7,
            command=on_open_passport if on_open_passport else None,
            state="normal" if on_open_passport else "disabled",
        ).pack(side="left")

        tk.Button(
            passport_bar,
            text="🧾  Invoice",
            font=body_font,
            bg="#008080",
            fg="white",
            activebackground="#005f5f",
            borderwidth=0,
            padx=15,
            pady=7,
            command=(lambda o=order: on_open_invoice(o)) if on_open_invoice else None,
            state="normal" if on_open_invoice else "disabled",
        ).pack(side="left", padx=(10, 0))

    return page


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    sample = {
        "order_number": "ORD-HYA-A502",
        "items": [
            {
                "id": "MC-305",
                "name": "IV Pole Clamp Assembly",
                "oem": "Medtronic",
                "hub": "AM-East Hub (15 miles)",
                "time": "3 Hours 00 Mins",
                "price": "£22.00",
                "price_val": 22.0,
            },
            {
                "id": "MC-550",
                "name": "Dialysis Machine Caster Lock",
                "oem": "Fresenius",
                "hub": "AM-South Hub (18 miles)",
                "time": "3 Hours 45 Mins",
                "price": "£52.00",
                "price_val": 52.0,
            },
        ],
    }

    open_your_orders_window(parent=root, orders=[sample], amount_paid=74.0)
    root.mainloop()

import tkinter as tk
from tkinter import font as tkfont


def open_your_orders_window(
    *,
    parent: tk.Misc,
    orders: list[dict],
    amount_paid: float | None = None,
    title_font=None,
    header_font=None,
    body_font=None,
    small_font=None,
    on_open_passport=None,
    on_open_invoice=None,
):
    """
    Final page: shows confirmed order(s), items, and amount paid.
    `orders` is a list of dicts: {"order_number": str, "items": [item,...]}
    item is expected to have keys like id, name, oem, hub, time, price, price_val.
    """
    page = tk.Toplevel(parent)
    page.title("MedCAD | Your Orders")
    page.geometry("900x600")
    page.configure(bg="#f4f7f6")
    page.resizable(True, True)

    # Fonts fallback
    title_font = title_font or tkfont.Font(family="Helvetica", size=18, weight="bold")
    header_font = header_font or tkfont.Font(family="Helvetica", size=13, weight="bold")
    body_font = body_font or tkfont.Font(family="Helvetica", size=11)
    small_font = small_font or tkfont.Font(family="Helvetica", size=10)

    # Header (teal) like screenshot
    header = tk.Frame(page, bg="#008080", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="📋  Your Orders", font=title_font, fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
    tk.Button(
        header,
        text="✕  Close",
        font=body_font,
        bg="#cc0000",
        fg="white",
        activebackground="#a30000",
        borderwidth=0,
        padx=15,
        pady=6,
        command=page.destroy,
    ).pack(side="right", padx=20, pady=18)

    # Amount paid banner (only when provided)
    if amount_paid is not None:
        paid = tk.Frame(page, bg="#e6f2f2", pady=10, padx=15)
        paid.pack(fill="x", padx=20, pady=(12, 0))
        tk.Label(paid, text="Amount Paid:", font=header_font, bg="#e6f2f2", fg="#004d4d").pack(side="left")
        tk.Label(
            paid,
            text=f"  £{amount_paid:.2f}",
            font=tkfont.Font(family="Helvetica", size=16, weight="bold"),
            bg="#e6f2f2",
            fg="#0a2540",
        ).pack(side="left")
        tk.Label(
            paid,
            text="✓ Payment Successful",
            font=body_font,
            bg="#e6f2f2",
            fg="#28a745",
        ).pack(side="right")

    content = tk.Frame(page, bg="#f4f7f6")
    content.pack(fill="both", expand=True, padx=30, pady=20)

    if not orders:
        tk.Label(content, text="No confirmed orders yet.", font=body_font, bg="#f4f7f6", fg="#888888").pack(pady=60)
        return page

    # Scrollable area
    canvas = tk.Canvas(content, bg="#f4f7f6", highlightthickness=0)
    scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f4f7f6")
    scroll_frame.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    for order in orders:
        items = order.get("items", [])
        order_total = sum(it.get("price_val", 0.0) for it in items)

        order_card = tk.Frame(scroll_frame, bg="white", highlightbackground="#cccccc", highlightthickness=1)
        order_card.pack(fill="x", pady=10, padx=5)

        title_bar = tk.Frame(order_card, bg="#0a2540", pady=8, padx=15)
        title_bar.pack(fill="x")
        tk.Label(
            title_bar,
            text=f"Order Number:  {order.get('order_number', '—')}",
            font=header_font,
            bg="#0a2540",
            fg="#00d4ff",
        ).pack(side="left")
        tk.Label(
            title_bar,
            text=f"{len(items)} item(s)    Total: £{order_total:.2f}",
            font=body_font,
            bg="#0a2540",
            fg="#aaaaaa",
        ).pack(side="right")

        col_frame = tk.Frame(order_card, bg="#e8f4f4")
        col_frame.pack(fill="x")
        for text, w in [("Part ID", 10), ("Component Name", 30), ("OEM", 15), ("Hub", 22), ("Est. Time", 14)]:
            tk.Label(col_frame, text=text, font=small_font, bg="#e8f4f4", fg="#004d4d", width=w, anchor="w").pack(
                side="left", padx=8, pady=5
            )

        for i, item in enumerate(items):
            row_bg = "white" if i % 2 == 0 else "#f9f9f9"
            row = tk.Frame(order_card, bg=row_bg)
            row.pack(fill="x")
            for text, w in [
                (item.get("id", ""), 10),
                (item.get("name", ""), 30),
                (item.get("oem", ""), 15),
                (item.get("hub", ""), 22),
                (item.get("time", ""), 14),
            ]:
                tk.Label(row, text=text, font=small_font, bg=row_bg, fg="#333333", width=w, anchor="w").pack(
                    side="left", padx=8, pady=6
                )

        passport_bar = tk.Frame(order_card, bg="white", pady=8, padx=10)
        passport_bar.pack(fill="x")

        tk.Button(
            passport_bar,
            text="🛡️  Quality & Traceability Passport",
            font=body_font,
            bg="#0a2540",
            fg="white",
            activebackground="#113a63",
            borderwidth=0,
            padx=15,
            pady=7,
            command=on_open_passport if on_open_passport else None,
            state="normal" if on_open_passport else "disabled",
        ).pack(side="left")

        tk.Button(
            passport_bar,
            text="🧾  Invoice",
            font=body_font,
            bg="#008080",
            fg="white",
            activebackground="#005f5f",
            borderwidth=0,
            padx=15,
            pady=7,
            command=(lambda o=order: on_open_invoice(o)) if on_open_invoice else None,
            state="normal" if on_open_invoice else "disabled",
        ).pack(side="left", padx=(10, 0))

    return page


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    sample = {
        "order_number": "ORD-HYA-A502",
        "items": [
            {
                "id": "MC-305",
                "name": "IV Pole Clamp Assembly",
                "oem": "Medtronic",
                "hub": "AM-East Hub (15 miles)",
                "time": "3 Hours 00 Mins",
                "price": "£22.00",
                "price_val": 22.0,
            },
            {
                "id": "MC-550",
                "name": "Dialysis Machine Caster Lock",
                "oem": "Fresenius",
                "hub": "AM-South Hub (18 miles)",
                "time": "3 Hours 45 Mins",
                "price": "£52.00",
                "price_val": 52.0,
            },
        ],
    }

    open_your_orders_window(parent=root, orders=[sample], amount_paid=74.0)
    root.mainloop()
