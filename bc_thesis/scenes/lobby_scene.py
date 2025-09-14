import threading
from bakalarska_prace.objects.button import Button
from bakalarska_prace.objects.text import Text
from bakalarska_prace.scenes.base_scene import BaseScene
from bakalarska_prace.settings.globals import SCREENWIDTH, SCREENHEIGHT, FONT_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT


class LoadingGameScene(BaseScene):
    """
    Scéna pro lobby před multiplayer hrou.
    Umožňuje hráčům označit, že jsou připraveni, a sleduje připravenost spoluhráče.
    """

    def __init__(self, app, socket=None):
        super().__init__(app)
        self.app = app
        self.my_socket = socket

        self.ready = False
        self.peer_ready = False
        self.msg = None

        # Texty o připravenosti hráčů (vytvořeny jednou a pouze se mění jejich text)
        self.master_peer_ready_text = Text(self.app.screen, text="", size=int(FONT_SIZE))
        self.second_peer_ready_text = Text(self.app.screen, text="", size=int(FONT_SIZE))
        self.second_peer_ready_text.set_position(0, self.master_peer_ready_text.height())

        self._create_buttons()
        self._create_text()

        if self.my_socket:
            # Vlákno pro příjem zpráv
            self.message_thread = threading.Thread(target=self.my_socket.receive_messages, daemon=True)
            self.message_thread.start()

            # Vlákno pro keep-alive zprávy
            keep_alive_thread = threading.Thread(target=self.my_socket.send_keep_alive, daemon=True)
            keep_alive_thread.start()

    def _create_buttons(self):
        """Vytvoří tlačítko READY."""
        Button(
            self.items,
            self.textures["ready"],
            (SCREENWIDTH // 2 - BUTTON_WIDTH // 2, SCREENHEIGHT // 2 - BUTTON_HEIGHT),
            self.ready_for_game
        )

    def _create_text(self):
        """Vytvoří úvodní text 'LOBBY'."""
        lobby_text = Text(
            self.app.screen,
            "LOBBY",
            size=42,
            color='black',
            bold=True
        )
        lobby_text.set_position((SCREENWIDTH // 2) - (lobby_text.width() // 2), (SCREENHEIGHT // 2) - (5 * BUTTON_HEIGHT))
        self.texts.add(lobby_text)

    def ready_for_game(self):
        """
        Označí tohoto hráče jako připraveného a odešle zprávu peerovi.
        """
        self.ready = True
        if not self.my_socket:
            print("Chyba: Socket není k dispozici.")
            return

        message = f"READY:{self.my_socket.local_ip}"
        try:
            self.my_socket.send_message(message)
        except Exception as e:
            print(f"Chyba při odesílání zprávy o připravenosti: {e}")

        self._update_ready_text(self.my_socket.local_ip, is_self=True)

    def _update_ready_text(self, ip_address, is_self=False):
        """Pomocná metoda pro nastavení textu o připravenosti."""
        text = f"Player {ip_address} is ready."
        if self.my_socket.is_master_peer:
            if is_self:
                self.master_peer_ready_text.set_text(text)
            else:
                self.second_peer_ready_text.set_text(text)
        else:
            if is_self:
                self.second_peer_ready_text.set_text(text)
            else:
                self.master_peer_ready_text.set_text(text)

    def update(self, delta_time):
        """
        Pravidelně kontroluje stav připojení, připravenost peeru a případně spouští hru.
        """
        if not self.my_socket or not self.my_socket.connected:
            self.app.set_scene("MenuScene", True)
            return

        # Aktualizace připravenosti peeru
        if self.peer_ready:
            peer_ip = self.my_socket.client_address[0] if self.my_socket.is_master_peer else self.my_socket.server_address[0]
            self._update_ready_text(peer_ip, is_self=False)

        # Pokud jsou oba připraveni (a je to master peer), zobrazí se tlačítko START
        if self.my_socket.is_master_peer and self.ready and self.peer_ready:
            Button(
                self.items,
                self.textures["start"],
                (SCREENWIDTH // 2 - BUTTON_WIDTH // 2, (SCREENHEIGHT // 2 - BUTTON_HEIGHT) + (2 * BUTTON_HEIGHT)),
                self.button_actions.start_game
            )

        if self.start:
            self.app.set_scene("MultiplayerScene", self.my_socket)

    def draw(self):
        """Vykreslí scénu – pozadí, tlačítka a texty o připravenosti hráčů."""
        super().draw()
        self.master_peer_ready_text.write()
        self.second_peer_ready_text.write()
