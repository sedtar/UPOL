from bakalarska_prace.utils.file_manager import FileManager
from bakalarska_prace.objects.player import Player
from bakalarska_prace.ai.bt_action import BTAction
from bakalarska_prace.settings.globals import *


class Enemy(Player):
    """
    Třída Enemy (Nepřítel) dědí od třídy Player a přidává AI logiku pro řízení chování nepřítele.

    Atributy:
        last_spawn_time (int): Časový záznam posledního spawnu nepřítele, slouží pro řízení časování spawnu.
        speed (int): Rychlost pohybu nepřátelské postavy.
        spawn_delay (int): Zpoždění v milisekundách mezi spawnováním nepřátel.
        filenames (list): Seznam názvů souborů představujících dostupné typy nepřátel (např. obrázky nebo datové soubory pro různé nepřátele).
    """

    def __init__(self, enemy):
        """
              Inicializuje objekt Enemy – nastaví výchozí zdroje, fázi a připraví strom chování.

              :param enemy: Objekt nebo strategie, kterou AI používá (např. typ soupeře).

        """
        super().__init__(is_enemy=True, coin_amount=300, exp=0)
        self.last_spawn_time = 0
        self.spawn_delay = 2000
        self.enemy = enemy
        self.position = (SCREENWIDTH + OFFSET_RIGHT_LIMIT) - (ANT_WIDTH + HOUSE_WIDTH), SCREENHEIGHT - (BLOCK_SIZE +
                                                                                                        ANT_HEIGHT)
        self.bt_action = BTAction(self, self.enemy)
        self.behavior_tree = self.bt_action.build_behavior_tree()

    def generate_enemies(self):
        current_time = pygame.time.get_ticks()
        # Spustí strom chování každé 2 sekundy
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.behavior_tree.execute()
            self.last_spawn_time = current_time  # Aktualizuje časovač pro strom chování
