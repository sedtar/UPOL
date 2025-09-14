from bakalarska_prace.ai.behaviour_tree import Selector, Sequence, Condition, Action
from bakalarska_prace.objects.character import Character
from bakalarska_prace.objects.character_logic import CharacterLogic
import random


class BTAction:
    """
      Třída BTAction slouží k definici chování nepřítele pomocí behaviorálního stromu.

      Tato třída obsahuje metody pro vytváření stromu chování, definici podmínek
      a akcí, které určují logiku rozhodování nepřítele během hry.

      Atributy:
          player (Player): Reference na hráče (např. AI nebo lidský hráč).
          enemy (Player): Reference na nepřítele (AI hráče).
      """

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def build_behavior_tree(self):
        """
        Vytvoří behaviour tree pro nepřítele.

        Návratová hodnota:
            Selector: Kořen behaviour tree, který obsahuje logiku chování.
        """
        return Selector([  # root
            Sequence([
                # První sekvence: Pokud má hráč dostatek zkušeností, koupí vylepšení.
                Condition(self.has_money),
                Condition(self.has_experience),
                Action(self.buy_upgrade)
            ]),
            Sequence([
                # Druhá sekvence: Pokud je hráčova základna v ohrožení, postaví ochranu základny.
                Condition(self.is_under_attack),
                Action(self.buy_turret)
            ]),
            Selector([
                Sequence([
                    Selector([
                        Condition(self.has_nothing),
                        Condition(lambda: self.player.coin_amount <= self.get_unit_price())
                    ]),
                    Action(lambda: self.add_hero(0, speed=-50))
                ]),
                Selector([
                    Sequence([
                        Condition(lambda: self.has_char(0) is True or self.has_char(1) is True
                                  or self.has_char(2) is True),  # pokud ma souper jakoukoliv postavu na bojišti
                        Condition(self.is_stronger_than_enemy),  # hrač je silnějsi nez souper
                        Action(lambda: self.add_hero(0, speed=-50))
                    ]),
                    Sequence([
                        Condition(lambda: self.has_char(0) is True or self.has_char(1) is True
                                  or self.has_char(2) is True),  # pokud ma souper jakoukoliv postavu na bojišti
                        Condition(lambda: not self.is_stronger_than_enemy()),  # hrac je slabsi jak soupeř
                        Action(lambda: self.add_hero(random.randint(1, 2), speed=-50))
                    ]),
                ]),

            ])
        ])

    def get_unit_price(self):
        group = self.player.phase.group_of_animals()
        _, _, price, _ = CharacterLogic.initialize_attributes(group[1])
        return price

    # podminky stromu

    def is_under_attack(self):
        """
        Podmínka pro behaviour tree: Kontroluje, zda má hráč dostatek zkušeností.
        bool: True, pokud má hráč dostatek zkušeností pro vylepšení, jinak False.
        """
        pass

    def is_stronger_than_enemy(self):
        """
        Podmínka pro behaviour tree: Kontroluje, zda je hráč silnější než nepřítel.

        Návratová hodnota:
            bool: True, pokud je hráč silnější než nepřítel, jinak False.
        """
        # Síla je kombinace počtu hrdinů a životů základny
        my_power = len(self.player.hero_group) * 10 + self.player.base.logic.hp
        enemy_power = len(self.enemy.hero_group) * 10 + self.enemy.base.logic.hp

        print("my_power: " + str(my_power))
        print("enemy_power: " + str(enemy_power))
        return my_power >= enemy_power

    def has_experience(self):
        """
        Podmínka pro behaviour tree: Kontroluje, zda má hráč dostatek zkušeností.
        bool: True, pokud má hráč dostatek mincí pro vylepšení, jinak False.
        """
        return self.player.exp >= self.player.phase.exp_cost

    def has_money(self):
        """
        Podmínka pro behaviour tree: Kontroluje, zda má hráč finanční rezervu po vylepšení do další áze .
        bool: True, pokud má hráč rezervu po vylepšení, jinak False.
        """
        return self.player.coin_amount >= self.player.phase.coin_cost + self.has_money_reserve()

    def has_money_reserve(self):
        """
        Podmínka pro behaviour tree: Kontroluje, zda má hráč finanční rezervu po vylepšení do další fáze.
        :return: bool: True, pokud má hráč rezervu po vylepšení, jinak False.
        """
        group = self.enemy.phase.group_of_animals()
        sum_price_amount = 0
        for unit in group:
            _, _, price, _ = CharacterLogic.initialize_attributes(unit)
            sum_price_amount += price
        print("finanční rezerva: " + str(sum_price_amount))
        return sum_price_amount

    def has_nothing(self):
        """
        Podmínka pro behaviour tree: Kontroluje, zda hráč nemá žádné hrdiny.

        Návratová hodnota:
            bool: True, pokud hráč nemá žádné hrdiny, jinak False.
        """
        if len(self.enemy.hero_group) == 1:
            return True

    def has_char(self, char_position):
        """
        Kontroluje, zda hráč má hrdinu na specifické pozici.

        Args:
            char_position (int): Index pozice hrdiny k ověření.

        Návratová hodnota:
            bool: True, pokud má hráč hrdinu na zadané pozici, jinak False.
        """
        group = self.enemy.phase.group_of_animals()
        for unit in group:
            print(unit)
        # Kontrola, zda je pozice validní
        if char_position < 0 or char_position >= len(group):
            return False

        for unit in self.enemy.hero_group:

            if isinstance(unit, Character) and unit.logic.char_type == group[char_position]:
                return True
        return False

    # akce stromu

    def add_hero(self, char_position, speed):
        """
        Bezpečně přidá hrdinu a zajistí jeho správnou orientaci.

        Args:
            char_position (int): Pozice hrdiny ve skupině zvířat.
            speed (int): Rychlost pohybu hrdiny.
        """
        group = self.player.phase.group_of_animals()
        # Přidá hrdinu na zadanou pozici a rychlost.
        self.player.add_hero(group[char_position], position=self.player.position, speed=speed)

    def buy_turret(self):
        pass

    # Zakoupení vylepšení.
    def buy_upgrade(self):
        """
            Akce pro behaviour tree: Koupí vylepšení fáze hráče.
        """
        print("Enemy: Buying upgrade.")
        self.player.upgrade_phase()
