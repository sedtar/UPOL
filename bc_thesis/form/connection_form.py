import threading
import tkinter as tk
import ipaddress
from tkinter import messagebox
from bakalarska_prace.form.base_form import BaseForm
from bakalarska_prace.networking.client import Client


class ConnectionForm(BaseForm):
    def __init__(self, app, root, thread):
        super().__init__(app, root, thread)
        self.app.peer = Client(self.app, False, port=5002)
        self.root.title("Select Connection")
        self.stop_event = threading.Event()

        self.init_base_ui(self.update_local_ip_display)

        tk.Label(self.root, text="IP adress you want to connect to:").pack()
        self.ip_text = tk.Entry(self.root, width=50)
        self.ip_text.pack()

        tk.Button(self.root, text="Join", command=self.submit).pack()

        self.connection_thread = None
        self.root.mainloop()


    def init_base_ui(self, update_callback):
        """Inicializuje společné UI prvky pro výběr adaptéru"""

        self.adapters = self.app.peer.get_network_adapters()

        adapter_names = list(self.adapters.keys())

        tk.Label(self.root, text="Select network adapter:").pack()
        self.selected_adapter = tk.StringVar(self.root)

        if adapter_names:
            self.selected_adapter.set(adapter_names[0])

        self.adapter_menu = tk.OptionMenu(self.root, self.selected_adapter, *adapter_names)
        self.adapter_menu.pack()

        super().init_base_ui(update_callback)


    def update_local_ip_display(self):
        ip = self.get_selected_adapter_ip()
        self.local_ip_label.config(text=f"Your local IP: {ip}")

    def submit(self):
        selected_ip = self.ip_text.get().strip()
        if not selected_ip:
            messagebox.showwarning("Missing IP address", "Please enter the IP address you want to connect to.")
            return
        try:
            ipaddress.IPv4Address(selected_ip)
        except ipaddress.AddressValueError:
            messagebox.showerror("Not valid IP", f"The address '{selected_ip}' is not in a valid IPv4 format.")
            return
        self.connection_thread = threading.Thread(target=self.attempt_connection, args=(selected_ip,), daemon=True)
        self.connection_thread.start()

    def attempt_connection(self, selected_ip):
        try:
            if self.app.peer.socket_connect(selected_ip, 5001):
                print("Připojení úspěšné, nastavujeme scénu...")
                self.root.after(0, lambda: self.app.set_scene("LoadingGameScene", socket=self.app.peer))
                self.root.after(0, self.on_close)
            else:
                self.root.after(0, lambda: self.show_connection_warning(selected_ip))
        except Exception as e:
            print(f"Chyba ve vlákně připojení: {e}")

    @staticmethod
    def show_connection_warning(selected_ip):
        messagebox.showwarning("Connection failed", f"Unable to connect to {selected_ip}. A connection"
                                                    f" to this address was likely not established.")
