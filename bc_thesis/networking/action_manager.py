import json
import threading

class ActionManager:
    def __init__(self, player, connection):
        """
        Inicializuje správce akcí pro daného hráče. Slouží k ukládání a odesílání akcí hráče v multiplayerovém režimu.
        Zajišťuje odesílání herních dat přes síť.

        :param player: Instance třídy Player, jejíž jednotky a akce bude spravovat.
        :param connection: Síťové spojení pro posílání zrpáv
        """
        self.player = player
        self.connection = connection
        self.data = {} #slovník pro ukládání akcí hráče
        self.data_lock = threading.Lock()

    def buy(self, name):
        """Přidá požadovanou jednotku (name) do seznamu nákupů"""
        if "buy" in self.data: #pokud klíč buy už existuje, přidá jednotku do seznamu
            self.data["buy"].append(name)
        else:
            self.data["buy"] = [name] #jinak vytvoří nový seznam s touto jednotkou


    def upgrade(self):
        """Ukládá požadavek na vylepšení do self.data"""
        with self.data_lock:
            self.data["upgrade"] = True

    def pause(self):
        """Ukládá požadavek na pauzu do self.data"""
        with self.data_lock:
            self.data["pause"] = True

    def send(self, tick):
        """Přidává aktuální časový údaj (tick) do self.data. Převádí data do formátu JSON a posílá ho pomocí
        connection.send_message(json_data"""
        with self.data_lock:
            self.data["tick"] = tick # přidá do slovníku "tick", což je časový údaj pro synchronizaci hráčů
            json_data = json.dumps(self.data) + "\n"
            print(json_data)
            self.connection.send_message(json_data)
            self.data = {}

    def process(self, data):
        """Zprácovává přijatou zrpávu v JSON formátu. """

        self.perform_action(data)
        tick = data["tick"] #uložení ticku
        #resetování slovníku pro další tick
        return tick #vrátí hodnotu ticku

    def perform_action(self, data):
        """
        Provede akci podle názvu akce.

        :param action: Název akce jako string (např. "buy", "upgrade").
       """
        if "buy" in data:
            for animal in data["buy"]:
                self.player.add_hero(animal)
        if "upgrade" in data:
            self.player.upgrade_phase()
        if "pause" in data:
            self.scene.toggle_pause()

