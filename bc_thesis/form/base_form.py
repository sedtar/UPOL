import tkinter as tk




class BaseForm:
    """Základní šablona pro formuláře, které slouží pro vytváření síťového připojení."""
    def __init__(self, app, root, thread):
        self.app = app
        self.root = root
        self.root.geometry("450x150+10+10")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.resizable(False, False)
        self.root.grab_set()
        self.thread = thread
        self.stop_event = None
        self.adapter_menu = None
        self.selected_adapter = None
        self.local_ip_label = None
        self.adapters = {}

    def init_base_ui(self, update_callback):
        """Inicializuje společné UI prvky pro výběr adaptéru"""
        """self.adapters = self.app.peer.get_network_adapters()

        adapter_names = list(self.adapters.keys())

        tk.Label(self.root, text="Select network adapter:").pack()
        self.selected_adapter = tk.StringVar(self.root)

        if adapter_names:
            self.selected_adapter.set(adapter_names[0])

        self.adapter_menu = tk.OptionMenu(self.root, self.selected_adapter, *adapter_names)
        self.adapter_menu.pack()"""

        self.local_ip_label = tk.Label(self.root, text="Your local IP: -")
        self.local_ip_label.pack()
        self.selected_adapter.trace("w", lambda *args: update_callback())
        update_callback()

    def get_selected_adapter_ip(self):
        """Získá vybraný adaptér z OptionMenu"""
        selected = self.selected_adapter.get()
        return self.adapters.get(selected, "Není k dispozici")

    def on_close(self):
        """Ukončí socket, zastaví vlákno a zničí okno."""
        print("Zavírání formuláře hostování hry...")
        self.stop_event.set()  # Zastaví vlákno

        # Uzavření socketu
        if self.app.peer and not self.app.peer.connected:
            self.app.peer.socket_close_connection()

        self.root.quit()
        self.root.destroy()
