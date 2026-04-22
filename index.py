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

        self.interface1 = _module_from_path("interface1", self.interface1_path)
        self.interface2 = _module_from_path("interface2", self.interface2_path)

        self._patch_navigation()
        self.show_landing()

    def _patch_navigation(self) -> None:
        app = self

        def landing_open_hospital_portal(self):  # noqa: ANN001
            app.show_portal()

        def portal_open_landing_page(self):  # noqa: ANN001
            app.show_landing()

        self.interface1.LandingPage.open_hospital_portal = landing_open_hospital_portal
        self.interface2.HospitalPortal.open_landing_page = portal_open_landing_page

    def show_landing(self) -> None:
        _clear_root(self.root)
        self.interface1.LandingPage(self.root)

    def show_portal(self) -> None:
        _clear_root(self.root)
        self.interface2.HospitalPortal(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    MedCADApp(root)
    root.mainloop()
