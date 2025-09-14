import threading
import time
import queue
from tkinter import messagebox
from bakalarska_prace.networking.action_manager import ActionManager
from bakalarska_prace.objects.player import Player
from bakalarska_prace.scenes.game_scene import GameScene
from bakalarska_prace.objects.camera import Camera
from bakalarska_prace.settings.globals import *


class MultiplayerScene(GameScene):
    """Herní scéna pro multiplayer. Řeší synchronizaci hráčů v multiplayer režimu."""
    def __init__(self, app, socket):
        super().__init__(app)
        self.my_socket = socket
        if self.my_socket.is_master_peer:  # je peer host?
            self.first_player = Player()
            self.second_player = Player(is_enemy=True)
            self.camera = Camera(0)  # nastavi kameru nalevo
        else:
            self.first_player = Player(is_enemy=True)
            self.second_player = Player()
            self.camera = Camera(SCREENWIDTH + OFFSET_RIGHT_LIMIT - SCREENWIDTH)  # nastavi kameru napravo

        self.action_manager = ActionManager(self.second_player, self.my_socket)
        self._setup_world(self.first_player, self.second_player)
        self.msg = None
        self.tick_accumulator = 0.0  # součet časů - nasčítává čas pro rozhodnutí, kdy synchronizovat
        self.tick = 0  # počítadlo herních cyklů
        self.msg_lock = threading.Lock()  # zámek pro vlákna pro ochranu sdílené proměnné self.msg
        self.synchronize = False  # příznak pro spuštění synchronizace
        threading.Thread(target=self._synchronize_players, daemon=True).start()  # vlákno pro synchronizaci hráče
        threading.Thread(target=self.my_socket.send_keep_alive, daemon=True).start()  # vlákno, které udržuje spojení

    def update(self, delta_time):
        self.world.update(delta_time)
        if self.pause:
            return

        self._update_multiplayer_tick(delta_time)

    def _update_players(self, delta_time):
        self.first_player.update_first()
        self.second_player.update_first()
        self.first_player.update(self.second_player, delta_time)
        self.second_player.update(self.first_player, delta_time)
        self.first_player.check_if_eliminated(self.second_player)
        self.second_player.check_if_eliminated(self.first_player)

    def _update_multiplayer_tick(self, delta_time):
        """Aktualizuje herní stav a rozhoduje, kdy se má spustit synchronizace mezi dvěma hráči.
        :param delta_time: Čas mezi dvěma snímky
        """
        if self.synchronize:  # pokud již synchronizace probíhá
            return
        self.tick_accumulator += delta_time  #
        tick_interval = 0.2  # každých 0.3 sekund se provede synchronizace

        if self.tick_accumulator >= tick_interval:  # lze provést synchronizaci?
            self.tick_accumulator = 0
            self.synchronize = True

        self._update_players(delta_time)  # aktualizace hráčů
        self._check_game_over()  # zkontroluje stav jednotek (tj. jestli jsou zneškodněny) nebo zneškodněna základna

    def _synchronize_players(self):
        """Základní síťová smyčka pro synchronizaci dvou hráčů. Běží ve vlastním vlákně a čeká na
        signál, zda může být provedena synchronizace. (self.synchronize)"""

        while True:  # smyčka běží neustálě ve vlákně
            if not self.synchronize:  # pokud nelze provést synchronizaci, pokdračuj
                time.sleep(0.01)  # aby nezatěžovalo CPU
                continue
            else:  # pokud lze provést synchronizaci

                """Stará se o síťovou syncrhonizaci včetně timeoutu a zpracování přijaté zprávy"""
                self.action_manager.send(self.tick)  # odesílá akci pro aktuální tik

                while True:  # čeká na odpověď
                    with self.msg_lock:
                        if not self.my_socket.connected:  # pokud dojde ke ztrátě připojení, ukončí synchronizaci
                            self.my_socket.socket_close_connection()
                            self.show_connection_error()  # zobrazí chybové okno
                            self.app.set_scene("MenuScene", True)  # vratí se zpět do menu
                            return
                        # zpracování zprávy od druhého hráče
                        if self.msg: # pokud přišla zpráva od druhého hráče
                            msg = self.msg.pop(0)
                            peer_tick = self.action_manager.process(msg)
                            #peer_tick = self.action_manager.process(self.msg[0])  # zpracuje ji a vrátí tik druhého hráče
                            # print(f"tick: {self.tick} - peer_tick{peer_tick}")
                            if peer_tick == self.tick:  # pokud druhé hráč také poslal aktuální nebo vyšší tick
                                # synchronizace úspěšná
                                self.tick += 1
                                break
                    self.synchronize = False  # po dokončení synchronizace se nastaví zpět na False
                #  vlákno pak zase čeká na další signál (z hlavního vlákna)

    @staticmethod
    def show_connection_error():
        messagebox.showerror("Player disconnected", "Player disconnected")
