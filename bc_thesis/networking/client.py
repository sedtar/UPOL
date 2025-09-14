import json
import socket
import time
import re

import psutil


class Client:
    """Tato třída reprezentuje konkrétního peera v síti peer to peer"""
    def __init__(self, app, is_master_peer: bool,  port=5001):
        self.app = app
        self.is_master_peer = is_master_peer  # boolean
        self.hostname = socket.gethostname()
        self.server_socket = None
        self.client_socket = None
        self.server_address = None
        self.connected = False
        self.client_address = None
        self.local_ip = socket.gethostbyname(self.hostname)
        self.port = port

    @staticmethod
    def is_valid_local_ip(ip):
        """Ověřuje, zda je daná IP adresa platná a použitelná na daném počítači."""
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind((ip, 0))  # Port 0 = libovolný dostupný port, zkouší "připojit" soket k dané IP adrese
            test_socket.close()
            return True
        except OSError:
            return False

    def create_socket(self, ip=None):
        """vytvoří a nastaví serverový soket pro naslouchání"""
        try:
            if self.server_socket:
                self.socket_close_connection()
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bind_ip = ip if ip else self.local_ip
            self.local_ip = bind_ip
            print("lokalni ip je" + str(self.local_ip))
            self.server_socket.bind((bind_ip, self.port))
            self.server_socket.listen(1)
            print(f"Socket vytvořen na {bind_ip}:{self.port}")
            return True
        except OSError as e:
            print(f"Chyba při vytváření socketu: {e}")
            self.socket_close_connection()
            return False

    def socket_wait(self):
        """Čeká na příchozí připojení a akceptuje ho.
         Tato metoda je určena pro serverovou roli. Klient (host), který ji používá, čeká, až se jiný peer
          připojí k němu."""
        if not self.server_socket:
            return False
        try:
            print("Čekám na připojení")
            self.client_socket, self.client_address = self.server_socket.accept()  # blokuje, dokud se nepřipojí klient
            self.server_socket.close()
            self.server_socket = None
            print(f"Připojen klient: {self.client_address}")
            self.connected = True
            return True
        except Exception as e:
            print(f"Chyba při čekání na připojení: {e}")
            return False

    def socket_connect(self, ip, port):
        """Tato metoda je určena pro klientskou roli. Klient, který ji používá, se připojuje k jinému peerovi
          na základě dané IP adresy a port"""
        # Pokud je zadána podsíť, prověříme, zda cílová IP do ní spadá
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # vytvori novy socket,
            # ktery bude pouzivat IPv4
            self.client_socket.settimeout(None)  # timeout pro připojení
            self.client_socket.connect((ip, port))  # # naváže spojení na dané IP adrese a portu
            self.server_address = (ip, port)  # uloží adresu serveru, ke kterému se připojil
            self.connected = True
            print(f"Připjeno k {ip}:{port}")
            return True
        except socket.timeout:
            print(f"Časový limit vypršel při pokusu připojit se na {ip}:{port}")
        except ConnectionRefusedError:
            print(f"Připojení odmítnuto serverem {ip}:{port}")
        except socket.gaierror:
            print(f"Neplatná IP adresa nebo DNS chyba: {ip}")
        except OSError as e:
            print(f"Obecná socket chyba: {e}")
        except Exception as e:
            print(f"Chyba při připojení: {e}")
        self.connected = False
        self.socket_close_connection()
        return False

    def send_message(self, message):
        if not self.connected:
            print("Nejste připojeni k peerovi.")
            return
        try:
            self.client_socket.sendall(message.encode())  # odesíla data přes TCP socket
            print(f"ZPRAVA {message} ODESLANA")
        except Exception as e:
            print(f"Chyba při odesílaní zprávy: {e}")

    def receive_messages(self):
        """Naslouchá zprávy v nekonečné smyčce
        Také zpracovává herní vstupy. Vstupy hráčů se posílají ve formátu
        TICK:<tick_id>;INPUT:<player_id>,<action>
        """
        if not self.connected:
            print("Nejste připojeni k peerovi.")
            return

        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    print("Peer ukončil spojení.")
                    break
                print(data)
                message = data.decode()  # převod bytes na string

                print(f"\nZpráva: {message}")
                if message.startswith("READY:"):
                    peer_ip = message.split(":")[1]
                    print(f"Hráč {peer_ip} je připraven!")
                    self.app.scene.peer_ready = True
                elif message.startswith("START:"):
                    print("START:")
                    self.app.scene.start = True
                elif message.startswith("EXIT:"):
                    print("EXIT:")
                    self.app.set_scene("MenuScene")

                index = message.find("{")
                if index != -1:
                    with self.app.scene.msg_lock:
                        print("message received")
                        self.parse_message(message[index:])
                        print(f"msg: {self.app.scene.msg}")

            except OSError as e:
                print(f"Chyba při příjmu zprávy: {e}")
                break

    def parse_message(self, msg):
        json_objects = re.findall(r'{.*?}', msg)
        if not self.app.scene.msg:
            self.app.scene.msg = []
        # Načteme každý objekt jako JSON
        for obj in json_objects:
            try:
                self.app.scene.msg.append(json.loads(obj))
                print(obj)
            except Exception as e:
                print(f"[ERROR] Nelze vložit do msg: {e}")
        sorted(self.app.scene.msg, key=lambda x: x['tick'])

    @staticmethod
    def is_ip_port_in_use(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((ip, port))
            s.close()
            return False  # bind prošel, adresa + port nejsou používány
        except OSError as e:
            if e.errno == 10048:  # "Address already in use" (Linux/Windows)
                return True

    def get_network_adapters(self):
        """Získa sitove adaptery"""
        adapters = {}
        for name, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and self.is_valid_local_ip(addr.address):
                    adapters[name] = addr.address
        return adapters

    def send_keep_alive(self):
        """Posílá keep-alive zrprávu každé 2 sekundy. Kontroluje, zda je hráč připojen."""
        while self.connected:
            try:
                self.client_socket.sendall(b'')  # prázdná zpráva pro udržení spojení
                time.sleep(2)
            except (OSError, BrokenPipeError):
                print("Chyba při odesílání keep-alive zprávy.")
                self.connected = False
                break

    def socket_close_connection(self):
        """Zavřre bezpečně sokety."""
        # Uzavření klientského soketu
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                if e.winerror != 10057:  # 10057 = socket not connected
                    print(f"Chyba při vypínání klientského socketu: {e}")
            finally:
                try:
                    self.client_socket.close()
                except Exception as e:
                    print(f"Chyba při zavírání klientského socketu: {e}")
                self.client_socket = None

        # Uzavření serverového soketu
        if self.server_socket:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                if e.winerror != 10057:
                    print(f"Chyba při vypínání serverového socketu: {e}")
            finally:
                try:
                    self.server_socket.close()
                except Exception as e:
                    print(f"Chyba při zavírání serverového socketu: {e}")
                self.server_socket = None
