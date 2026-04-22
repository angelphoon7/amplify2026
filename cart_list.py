import random
import string
import tkinter as tk
from tkinter import ttk


class Cart:
    def __init__(self):
        self.items: list[dict] = []
        self.order_number: str | None = None

    @property
    def count(self) -> int:
        return len(self.items)

    def total(self) -> float:
        return sum(it.get("price_val", 0.0) for it in self.items)

    def ensure_order_number(self) -> str:
        if self.order_number is None:
            chars = string.ascii_uppercase + string.digits
            self.order_number = "ORD-" + "".join(random.choices(chars, k=3)) + "-" + "".join(random.choices(chars, k=4))
        return self.order_number

    def add(self, item: dict) -> None:
        self.ensure_order_number()
        self.items.append(item)

    def remove_at(self, index: int) -> None:
        self.items.pop(index)
        if not self.items:
            self.order_number = None

    def clear(self) -> None:
        self.items.clear()
        self.order_number = None


def open_cart_window(
    *,
    parent: tk.Misc,
    cart: Cart,
    title_font,
    header_font,
    body_font,
    small_font,
    on_confirm_order,
    on_cart_changed=None,
):
    summary = tk.Toplevel(parent)
    summary.title("MedCAD | Order Summary")
    summary.geometry("900x600")
    summary.configure(bg="#f4f7f6")
    summary.resizable(True, True)

    header = tk.Frame(summary, bg="#008080", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="🛒 Order Summary", font=title_font, fg="white", bg="#008080").pack(side="left", padx=20, pady=15)
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
        command=summary.destroy,
    ).pack(side="right", padx=20, pady=18)

    order_bar = tk.Frame(summary, bg="#e6f2f2", pady=8, padx=15)
    order_bar.pack(fill="x", padx=20, pady=(12, 0))
    order_num_var = tk.StringVar(value=f"Order Number:  {cart.order_number or '—'}")
    tk.Label(order_bar, textvariable=order_num_var, font=header_font, bg="#e6f2f2", fg="#004d4d").pack(side="left")

    empty_lbl = tk.Label(
        summary,
        text="Your cart is empty. Add items from the catalog.",
        font=body_font,
        bg="#f4f7f6",
        fg="#888888",
    )

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

    bottom = tk.Frame(summary, bg="#f4f7f6")
    bottom.pack(side="bottom", fill="x", padx=20, pady=10)
    tk.Frame(summary, bg="#cccccc", height=1).pack(side="bottom", fill="x", padx=20)

    footer_lbl = tk.Label(bottom, text="", font=header_font, bg="#f4f7f6", fg="#0a2540")
    footer_lbl.pack(side="left")

    pay_btn = tk.Button(
        bottom,
        text="Confirm Order & Make Payment  💳",
        font=header_font,
        bg="#008080",
        fg="white",
        activebackground="#006666",
        borderwidth=0,
        padx=20,
        pady=8,
    )
    pay_btn.pack(side="right")

    def remove_selected():
        sel = tree.selection()
        if not sel:
            return
        remove_item(int(sel[0]))

    tk.Button(
        bottom,
        text="✕  Remove Selected",
        font=body_font,
        bg="#cc0000",
        fg="white",
        activebackground="#a30000",
        borderwidth=0,
        padx=12,
        pady=5,
        command=remove_selected,
    ).pack(side="left", padx=(10, 0))

    tk.Label(
        bottom,
        text="Tip: Select a row then click Remove.",
        font=small_font,
        bg="#f4f7f6",
        fg="#888888",
    ).pack(side="left", padx=(12, 0))

    def refresh():
        for row in tree.get_children():
            tree.delete(row)

        if not cart.items:
            tree_frame.pack_forget()
            empty_lbl.pack(pady=60)
            footer_lbl.config(text="")
            pay_btn.config(state="disabled", command=None)
            order_num_var.set("Order Number:  —")
            if on_cart_changed:
                on_cart_changed(cart)
            return

        empty_lbl.pack_forget()
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(8, 0))

        order_num_var.set(f"Order Number:  {cart.order_number or '—'}")

        for i, it in enumerate(cart.items):
            tree.insert("", tk.END, iid=str(i), values=(i + 1, it["id"], it["name"], it["oem"], it["price"], it["time"]))

        total = cart.total()
        footer_lbl.config(text=f"Items: {cart.count}    Total: £{total:.2f}")
        pay_btn.config(state="normal", command=lambda t=total: on_confirm_order(t, refresh, summary.destroy))
        if on_cart_changed:
            on_cart_changed(cart)

    def remove_item(index: int):
        cart.remove_at(index)
        refresh()

    refresh()
    return summary
