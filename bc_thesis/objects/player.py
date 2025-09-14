from bakalarska_prace.objects.character import Character
from bakalarska_prace.settings.globals import *
from bakalarska_prace.objects.phase import Phase


class Player:
    def __init__(self, is_enemy=False, coin_amount=300, exp=1000):
        self.coin_amount = coin_amount  # počet mincí hráče
        self.phase = Phase("bugs", "anthill", 200)  # aktuální fáze hráče
        self.exp = exp  # zkušenosti hráče
        self.hero_group = pygame.sprite.Group()  # armáda hráče
        self.tmp_group = pygame.sprite.Group()  #
        self.is_enemy = is_enemy
        self.group_iterator = iter(self.hero_group)  # Iterátor pro skupinu hrdinů
        self.last_coin_time = 0  # Ukládáme čas posledního přidání mincí
        self.coin_interval = 1  # Interval pro přidání mincí (v sekundách)
        self.base = self._create_base()
        self.hero_group.add(self.base)

    def _create_base(self):
        """Vytvoří základnu hráče."""
        position = (0, SCREENHEIGHT - (BLOCK_SIZE + HOUSE_HEIGHT)) if not self.is_enemy else \
            (SCREENWIDTH + OFFSET_RIGHT_LIMIT - HOUSE_WIDTH, SCREENHEIGHT - (BLOCK_SIZE + HOUSE_HEIGHT))

        base = Character(
            groups=self.hero_group,
            animal=self.phase.building_types,
            position=position,
            width=HOUSE_WIDTH)

        if self.is_enemy:
            base.flip_vertically()

        return base

    def initialize_base(self, base):
        """Inicializuje základnu hráče a  přidá do skupiny hrdinů."""
        self.base = base
        self.hero_group.add(base)

    def increase_exp(self, amount):
        """Zvyšuje zkušenosti hráče o zadané množství.  """
        self.exp += amount

    def increase_coin(self, amount):
        """
        Zvyšuje počet mincí hráče o zadané množství"""
        self.coin_amount += amount

    def decrease_coin(self, amount):
        """
        Snižuje počet mincí hráče o zadané množství, pokud má dostatek mincí.

        Args:
            amount (int): Množství, o které se mají snížit mince.
        """
        if self.coin_amount >= amount:
            self.coin_amount -= amount

    def add_hero(self, name, position=(HOUSE_WIDTH, SCREENHEIGHT - (BLOCK_SIZE + ANT_HEIGHT)), speed=-50):
        """
        Přidá nového hrdinu do skupiny hráče, pokud má dostatek mincí.

        Args:
            name (str): Jméno zvířete, na kterém je hrdina založen (z informací o zvířatech).
            position: pozice, na které má být jednotka přidána
            speed: rychlost jednotky
        """
        if self.is_enemy:
            position = ((SCREENWIDTH + OFFSET_RIGHT_LIMIT) - (ANT_WIDTH + HOUSE_WIDTH),
                        SCREENHEIGHT - (BLOCK_SIZE + ANT_HEIGHT))
            speed = speed
        else:
            speed = abs(speed)

        new_char = Character(groups=self.tmp_group, animal=name, position=position, speed=speed)
        if self.is_enemy:
            new_char.flip_vertically()

        if self.coin_amount >= new_char.logic.price:
            self.hero_group.add(new_char)
            self.decrease_coin(new_char.logic.price)
            self.tmp_group.remove(new_char)
            return new_char

    def delete_hero(self, hero):
        """
        Odebere hrdinu ze skupiny hráče a zničí ho.

        Args:
            hero (Character): Hrdina, který má být odstraněn ze skupiny.
        """
        if hero in self.hero_group:
            self.hero_group.remove(hero)
            hero.kill()

    def upgrade_phase(self):
        """
        Vylepšuje fázi hráče, pokud má dostatek zkušeností.

        Returns:
            bool: True, pokud bylo vylepšení fáze úspěšné, jinak False.
        """
        if self.exp >= self.phase.exp_cost and self.coin_amount >= self.phase.coin_cost:
            self.coin_amount -= self.phase.coin_cost
            # pokud bylo vylepšení úspěšné, aktualizuje se základna (stará se odstraní a vytvorí se nová)
            if self.phase.next_phase():
                self.hero_group.remove(self.base)
                self.base = self._create_base()
                self.hero_group.add(self.base)
            return True
        return False

    def check_if_eliminated(self, enemy):
        """
        Kontroluje, zda je některá hráčova hrdinská jednotka zneškodněná, a pokud ano, převede
         mince a zkušenosti nepříteli a odebere tuto jednotku ze skupiny.

        Args:
            enemy (Player): Nepřátelský hráč, který obdrží mince a zkušenosti.
        """
        for unit in list(self.hero_group):
            if unit.logic.is_eliminated():
                enemy.increase_coin(unit.logic.price)
                enemy.increase_exp(unit.logic.exp_price)
                self.delete_hero(unit)

    def get_first(self):
        """
        Vrátí prvního hrdinu ve skupině hráče (ne základnu), nebo základnu, pokud je skupina prázdná.

        Returns:
            Character: První hrdina nebo základna, pokud nejsou žádní hrdinové.
        """
        for unit in self.hero_group:
            if unit != self.base:
                return unit
        return self.base

    def update_first(self):
        """
        Aktualizuje první jednotku ve skupině hrdinů, označí ji jako první.
        """
        first_unit = self.get_first()
        for unit in self.hero_group:
            if unit != first_unit:
                unit.logic.set_first(False)
            else:
                unit.logic.set_first(True)

    def update(self, enemy_player, delta_time):
        """
        Aktualizuje fázi hráče a všechny hráčovi jednotky ve skupině.

        Args:
            enemy_player (Player): Nepřátelský hráč.
            delta_time (float): Čas, který uplynul od poslední aktualizace, používá se pro aktualizaci
             akcí hrdinských jednotek.
        """
        self.last_coin_time += delta_time
        if self.last_coin_time >= self.coin_interval:
            self.increase_coin(1)
            self.last_coin_time = 0  # Resetujeme čas

        for unit in self.hero_group:
            unit.update(enemy_player, self.hero_group, self.is_enemy, delta_time)
