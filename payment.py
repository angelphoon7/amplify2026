import tkinter as tk
from tkinter import font


def open_payment_page(
    *,
    parent: tk.Misc,
    total: float,
    on_success,
    title_font,
    header_font,
    small_font,
):
    payment = tk.Toplevel(parent)
    payment.title("MedCAD | Secure Payment")
    payment.geometry("520x580")
    payment.resizable(False, False)
    payment.configure(bg="#f4f7f6")

    header = tk.Frame(payment, bg="#0a2540", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="💳  Secure Payment", font=title_font, fg="white", bg="#0a2540").pack(side="left", padx=20, pady=15)
    tk.Label(header, text="🔒 SSL Encrypted", font=small_font, fg="#aaaaaa", bg="#0a2540").pack(side="right", padx=20)

    amt = tk.Frame(payment, bg="#e6f2f2", pady=12, padx=20)
    amt.pack(fill="x")
    tk.Label(amt, text="Amount Due:", font=header_font, bg="#e6f2f2", fg="#004d4d").pack(side="left")
    tk.Label(
        amt,
        text=f"  £{total:.2f}",
        font=font.Font(family="Helvetica", size=18, weight="bold"),
        bg="#e6f2f2",
        fg="#0a2540",
    ).pack(side="left")

    form = tk.Frame(payment, bg="#f4f7f6", padx=35, pady=20)
    form.pack(fill="both", expand=True)

    lbl_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=12)

    tk.Label(form, text="Card Type", font=lbl_font, bg="#f4f7f6", fg="#333333").pack(anchor="w")
    card_type_var = tk.StringVar(value="Visa")
    ct_frame = tk.Frame(form, bg="#f4f7f6")
    ct_frame.pack(anchor="w", pady=(4, 14))
    for ctype in ["Visa", "Mastercard", "Amex"]:
        tk.Radiobutton(
            ct_frame,
            text=ctype,
            variable=card_type_var,
            value=ctype,
            font=lbl_font,
            bg="#f4f7f6",
            activebackground="#f4f7f6",
        ).pack(side="left", padx=(0, 16))

    tk.Label(form, text="Cardholder Name", font=lbl_font, bg="#f4f7f6", fg="#333333").pack(anchor="w")
    name_entry = tk.Entry(form, font=entry_font, relief="solid", bd=1)
    name_entry.pack(fill="x", ipady=7, pady=(4, 14))

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

        # Immediately proceed to the success flow (index.py will open your_order.py).
        payment.destroy()
        parent.after(0, on_success)

    tk.Button(
        form,
        text=f"  Pay  £{total:.2f}  Now  🔒  ",
        font=header_font,
        bg="#0a2540",
        fg="white",
        activebackground="#113a63",
        borderwidth=0,
        padx=10,
        pady=12,
        command=process_payment,
    ).pack(fill="x", pady=(6, 0))

    tk.Label(
        form,
        text="🔒  256-bit SSL encrypted. Your card details are never stored.",
        font=small_font,
        bg="#f4f7f6",
        fg="#888888",
    ).pack(pady=(10, 0))

    return payment
