import sys
from bakalarska_prace.scenes.connection_scene import ConnectionScene
from bakalarska_prace.scenes.lobby_scene import LoadingGameScene
from bakalarska_prace.scenes.multiplayer_scene import MultiplayerScene
from bakalarska_prace.scenes.single_player_scene import SingleplayerScene
from event import EventHandler
from bakalarska_prace.settings.globals import *
from bakalarska_prace.scenes.menu_scene import MenuScene
from bakalarska_prace.scenes.game_scene import GameScene


class Game:
    """
    Třída Game je hlavní vstupní bod a ovladač pro hru, který zpracovává herní smyčku, správu událostí,
    aktualizaci herních stavů a vykreslování. Řídí přechody mezi menu a hlavní herní scénou.

    Atributy:
        screen (pygame.Surface): Povrch pro zobrazení hry.
        clock (pygame.time.Clock): Hodiny používané k řízení snímkové frekvence hry.
        running (bool): Příznak označující, zda hra běží.
        menu (Menu): Instance třídy Menu pro správu herního menu.
        scene (Scene): Instance třídy Scene pro správu hlavní herní scény.
        handler (EventHandler): Instance třídy EventHandler pro zpracování uživatelského vstupu a událostí.
    """

    def __init__(self):
        """
        Inicializuje hru s potřebnými komponentami, včetně nastavení zobrazení,
        hodin, obsluhy událostí, menu a scény.

        Inicializuje následující atributy:
            screen (pygame.Surface): Obrazovka hry, na které probíhá veškeré vykreslování.
            clock (pygame.time.Clock): Hodiny používané k řízení snímkové frekvence.
            running (bool): Příznak, který řídí, zda hra pokračuje v běhu.
            menu (Menu): Instance třídy Menu.
            scene (Scene): Instance třídy Scene.
            handler (EventHandler): Instance třídy EventHandler zodpovědná za zpracování událostí.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.peer = None
        self.scene = MenuScene(self)
        self.handler = EventHandler(self.scene)
        self.times = 0

    def run(self):
        """
        Hlavní herní smyčka. Neustále zpracovává události, aktualizuje stav hry
        a vykresluje obrazovku, dokud není hra uzavřena.

        Volání:
            handle_events() z třídy EventHandler pro zpracování uživatelského vstupu.
            update() pro obnovu herního stavu.
            pygame.display.update() pro aktualizaci zobrazení.
            pygame.time.Clock.tick() pro udržení snímkové frekvence.
        """
        while self.running:
            self.handler.handle_events()  # Zpracovává události
            self.update(self.clock.get_time()/1000.0)  # Aktualizuje herní stav (delta time v sekundach)
            pygame.display.update()  # Aktualizuje zobrazení
            self.clock.tick(FPS)  # Řídí snímkovou frekvenci hry

        self.close()  # Zavře hru, když smyčka skončí

    def update(self, delta_time):
        """
        Aktualizuje herní stav na základě času, který uplynul od posledního snímku (delta_time).

        Pokud hra není pozastavena a menu není spuštěno, vykreslí menu.
        Jinak aktualizuje herní scénu.

        Args:
            delta_time (float): Čas, který uplynul od posledního snímku (v sekundách).

        Úpravy:
            Pokud delta_time přesáhne 1.0 sekundy, je omezena na 1.0, aby se předešlo velkým skokům v čase.
        """
        # Omezíme maximální delta_time, aby nedocházelo k velkým skokům
        if delta_time > 1.0:
            delta_time = 1.0

        self.scene.update(delta_time)  # Aktualizuje herní scénu
        self.scene.draw()

        self.times += 1
        if self.times < 70:
            return
        self.times = 0
        if self.peer:
            if self.peer.server_socket: #cekam na pripojeni klienta
                print(f"Poslouchám na {self.peer.server_socket}")
            elif self.peer.client_socket: #Spojeni s klientem navazano
                print(
                    f"Spojení na  {self.peer.client_socket} navázáno")
        else:
            print("Socket neexistuje.")

    def set_scene(self, enum, socket=None):
        match enum:
            case "GameScene":
                self.scene = GameScene(self)
                self.handler = EventHandler(self.scene)
            case "ConnectionScene":
                self.scene = ConnectionScene(self)
                self.handler = EventHandler(self.scene)
            case "LoadingGameScene":
                self.scene = LoadingGameScene(self, socket)
                self.handler = EventHandler(self.scene)
            case "MainMenuScene":
                self.scene = MenuScene(self)
                self.handler = EventHandler(self.scene)
            case "SingleplayerScene":
                self.scene = SingleplayerScene(self)
                self.handler = EventHandler(self.scene)
            case "MultiplayerScene":
                self.scene = MultiplayerScene(self, socket)
                self.handler = EventHandler(self.scene)

            case _: #default
                self.scene = MenuScene(self)
                self.handler = EventHandler(self.scene)

    def close(self):

        #if self.peer:
        #    print(f"socket {self.peer.local_ip} zničen.")
        #    self.peer.close_connection()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()