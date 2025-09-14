import threading
import tkinter as tk
from tkinter import messagebox

from bakalarska_prace.form.base_form import BaseForm
from bakalarska_prace.networking.client import Client


class GameHostForm(BaseForm):
    """
    GUI formulář pro hostování multiplayer hry.
    Umožňuje výběr síťového adaptéru a čeká na připojení hráče (peer).
    """
    def __init__(self, app, root, thread):
        super().__init__(app, root, thread)

        # nastavení okna
        self.root.title("Game hosting and adapter selection")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.grab_set()

        # inicializace klienta v režimu master
        self.app.peer = Client(self.app, True)

        self.stop_event = threading.Event()
        self.init_base_ui(self.update_local_ip_display)

        self.info_label = tk.Label(self.root, text="Waiting for the player...")

        self.info_label.pack(side='bottom', pady=10)

        self.host_thread = threading.Thread(target=self.wait_for_peer, daemon=True)
        self.host_thread.start()

        self.root.mainloop()

    def update_local_ip_display(self):
        """Aktualizuje aktuálně zobrazovanou IP adresu."""
        ip = self.get_selected_adapter_ip()
        self.local_ip_label.config(text=f"Your local IP {ip}")
        self.update_server_socket(ip)

    def update_server_socket(self, ip):
        if not self.app.peer.create_socket(ip):
            messagebox.showerror("Socket error", "Unable to create"
                                 " socket.\n\nA socket is likely already bound to this IP address and port.")
            print("Nelze vytvořit socket")

    def init_base_ui(self, update_callback):
        """Inicializuje společné UI prvky pro výběr adaptéru"""
        self.adapters = self.app.peer.get_network_adapters()
        adapter_names = list()
        for key in self.adapters:
            ip = self.adapters[key]
            if self.app.peer.create_socket(ip):
                adapter_names.append(key)
        tk.Label(self.root, text="Select network adapter:").pack()
        self.selected_adapter = tk.StringVar(self.root)

        if adapter_names:
            self.selected_adapter.set(adapter_names[0])

        self.adapter_menu = tk.OptionMenu(self.root, self.selected_adapter, *adapter_names)
        self.adapter_menu.pack()
        super().init_base_ui(update_callback)

    def wait_for_peer(self):
        while not self.stop_event.is_set():
            if self.app.peer.socket_wait():
                self.root.after(0, self.on_close)
                self.app.set_scene("LoadingGameScene", socket=self.app.peer)
                return
