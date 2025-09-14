import socket
import threading
import tkinter as tk
from tkinter import messagebox
import psutil  # pro získání seznamu adaptérů

from bakalarska_prace.form.base_form import BaseForm
from bakalarska_prace.networking.client import Client


class AdapterForm(BaseForm):
    def __init__(self, app, root, thread):
        super().__init__(app, root, thread)
        self.app.peer = Client(self.app, False, port=5002)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title("Vyberte adaptér a IP")
        self.stop_event = threading.Event()
        self.connection_thread = None
        self.root.geometry("450x180+10+10")
        self.root.grab_set()

        # ziksa seznam sitovych adapteru
        self.adapters = self.get_network_adapters()
        adapter_names = list(self.adapters.keys())

        tk.Label(self.root, text="Zvolte síťový adaptér:").pack()
        self.selected_adapter = tk.StringVar(self.root)
        if adapter_names:
            self.selected_adapter.set(adapter_names[0])
        self.adapter_menu = tk.OptionMenu(self.root, self.selected_adapter, *adapter_names)
        self.adapter_menu.pack()

        # --- Vlastní IP adresa ---
        self.local_ip_label = tk.Label(self.root, text="Vaše lokální IP: -")
        self.local_ip_label.pack()
        self.update_local_ip_display()

        # --- Vzdálená IP ---
        tk.Label(self.root, text="IP adresa, kam se chcete připojit:").pack()
        self.ip_text = tk.Entry(self.root, width=50)
        self.ip_text.pack()

        tk.Button(self.root, text="Submit", command=self.submit).pack()
        self.root.mainloop()

    def get_network_adapters(self):
        """Získa sitove adaptery"""
        adapters = {}
        for name, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    adapters[name] = addr.address
        return adapters

    def update_local_ip_display(self):
        selected = self.selected_adapter.get()
        ip = self.adapters.get(selected, "Není k dispozici")
        self.local_ip_label.config(text=f"Vaše lokální IP: {ip}")
        if self.app.peer.server_socket:
            self.app.peer.close_connection()
        self.app.peer.create
        self.app.peer.local_ip = ip

        # Automaticky aktualizuj při změně výběru adaptéru
        self.selected_adapter.trace("w", lambda *args: self.update_local_ip_display())

    def submit(self):

        print(self.app.peer.local_ip)
        #print(self.app.peer.local_ip)

    def on_close(self):
        print("Zavírám ConnectionForm...")
        self.stop_event.set()
        if self.connection_thread and self.connection_thread.is_alive():
            self.connection_thread.join()
        self.root.quit()
        self.root.destroy()