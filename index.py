import importlib.util
import os
import tkinter as tk


def _module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module {module_name} from {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _clear_root(root: tk.Tk) -> None:
    for w in root.winfo_children():
        w.destroy()


class MedCADApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.interface1_path = os.path.join(self.base_dir, "interface 1.py")
        self.interface2_path = os.path.join(self.base_dir, "interface 2.py")
        self.payment_path = os.path.join(self.base_dir, "payment.py")
        self.your_order_path = os.path.join(self.base_dir, "your_order.py")
        self.invoice_path = os.path.join(self.base_dir, "invoice.py")

        self.interface1 = _module_from_path("interface1", self.interface1_path)
        self.interface2 = _module_from_path("interface2", self.interface2_path)
        self.payment = _module_from_path("payment", self.payment_path)
        self.your_order = _module_from_path("your_order", self.your_order_path)
        self.invoice = _module_from_path("invoice", self.invoice_path)
        self.portal = None

        self._patch_navigation()
        self.show_landing()

    def _patch_navigation(self) -> None:
        app = self

        def landing_open_hospital_portal(self):  # noqa: ANN001
            app.show_portal()

        def portal_open_landing_page(self):  # noqa: ANN001
            app.show_landing()

        def portal_open_your_orders_page(self, amount_paid=None):  # noqa: ANN001
            # Show final "Your Orders" page; invoice button generates PDF via invoice.py.
            app.your_order.open_your_orders_window(
                parent=self.root,
                orders=list(self.confirmed_orders),
                amount_paid=amount_paid,
                title_font=self.title_font,
                header_font=self.header_font,
                body_font=self.body_font,
                small_font=self.small_font,
                on_open_passport=self.open_traceability_passport,
                on_open_invoice=app.invoice.generate_invoice_pdf,
            )

        def portal_open_order_summary(self):  # noqa: ANN001
            # Orchestrate checkout from the app entrypoint:
            # Cart -> Payment -> (Pay Now) -> Order confirmation window (order.py)
            def confirm_order(total, refresh, close_cart_window):
                close_cart_window()

                def after_payment():
                    confirmed = {
                        "order_number": self.cart.order_number,
                        "items": list(self.cart.items),
                    }
                    self.confirmed_orders.append(confirmed)
                    amount_paid = sum(it.get("price_val", 0.0) for it in confirmed["items"])
                    self.cart.clear()
                    self.cart_badge.config(text="")
                    # Show the same UI as clicking "📋 Your Order" in the header.
                    self.open_your_orders_page(amount_paid=amount_paid)

                self.open_payment_page(total, after_payment)

            app.interface2.cart_list.open_cart_window(
                parent=self.root,
                cart=self.cart,
                title_font=self.title_font,
                header_font=self.header_font,
                body_font=self.body_font,
                small_font=self.small_font,
                on_confirm_order=confirm_order,
                on_cart_changed=lambda c: self.cart_badge.config(text=str(c.count) if c.count > 0 else ""),
            )

        self.interface1.LandingPage.open_hospital_portal = landing_open_hospital_portal
        self.interface2.HospitalPortal.open_landing_page = portal_open_landing_page
        self.interface2.HospitalPortal.open_order_summary = portal_open_order_summary
        self.interface2.HospitalPortal.open_your_orders_page = portal_open_your_orders_page

    def show_landing(self) -> None:
        _clear_root(self.root)
        self.interface1.LandingPage(self.root)

    def show_portal(self) -> None:
        _clear_root(self.root)
        self.portal = self.interface2.HospitalPortal(self.root)

    def show_final_orders(self, confirmed_order: dict) -> None:
        portal = self.portal
        if portal is None:
            return
        amount_paid = sum(it.get("price_val", 0.0) for it in confirmed_order.get("items", []))
        self.your_order.open_your_orders_window(
            parent=self.root,
            orders=[confirmed_order],
            amount_paid=amount_paid,
            title_font=portal.title_font,
            header_font=portal.header_font,
            body_font=portal.body_font,
            small_font=portal.small_font,
            on_open_passport=portal.open_traceability_passport,
            on_open_invoice=self.invoice.generate_invoice_pdf,
        )


if __name__ == "__main__":
    root = tk.Tk()
    MedCADApp(root)
    root.mainloop()
