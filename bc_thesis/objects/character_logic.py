import pygame
from bakalarska_prace.objects.animal import AnimalEnum, Damage, Hp, BaseEnum, Price, AnimalExp
from bakalarska_prace.objects.entity import Entity


class CharacterLogic(Entity):
    """
    Třída CharacterLogic spravuje logiku postav - pohyb, útoky, životy a kolize.
    """

    def __init__(self, rect, char_type, character, speed=0):
        """
        Inicializace instance postavy
        :param rect: Obdelník reprezentující pozici a veliksot postavy (pygame.Rect).
        :param char_type: Typ postavy (např. mravenec, beruška).
        :param character: Objekt postavy (graficka/logická reprezentace).

        """

        self.char_type = char_type  # typ postavy
        self.rect = rect  # pygame.Rect reprezentující pozici a velikost postavy
        self.character = character
        self.last_damage_time = pygame.time.get_ticks()
        self.damage_interval = 1000  # Minimální interval mezi útoky (v ms)
        self.speed = speed  # rychlost pohybu postavy
        self.first = False  # značí, zda je postava první (pro útok a kolize)

        self.max_hp_width = 20  # šířka ukazatele zdraví
        self.hp, self.damage, self.price, self.exp_price = self.initialize_attributes(char_type)
        self.max_hp = self.hp  # maximální životy

    @staticmethod
    def initialize_attributes(char_type):
        """
        Vrací základní atributy jednotky na základě jejího typu.
        """
        attributes = {
            AnimalEnum.ANT.value: (
                Hp.ANT_HP.value, Damage.ANT_DMG.value, Price.ANT_PRICE.value, AnimalExp.ANT_EXP.value),
            AnimalEnum.LADYBUG.value: (
                Hp.LADYBUG_HP.value, Damage.LADYBUG_DMG.value, Price.LADYBUG_PRICE.value, AnimalExp.LADYBUG_EXP.value),
            AnimalEnum.SPIDER.value: (
                Hp.SPIDER_HP.value, Damage.SPIDER_DMG.value, Price.SPIDER_PRICE.value, AnimalExp.SPIDER_EXP.value),
            AnimalEnum.BLACKBIRD.value: (
                Hp.BLACKBIRD_HP.value, Damage.BLACKBIRD_DMG.value, Price.BLACKBIRD_PRICE.value,
                AnimalExp.BLACKBIRD_EXP.value),
            AnimalEnum.BLUEBIRD.value: (
                Hp.BLUEBIRD_HP.value, Damage.BLUEBIRD_DMG.value, Price.BLUEBIRD_PRICE.value,
                AnimalExp.BLUEBIRD_EXP.value),
            AnimalEnum.REDBIRD.value: (
                Hp.REDBIRD_HP.value, Damage.REDBIRD_DMG.value, Price.REDBIRD_PRICE.value, AnimalExp.REDBIRD_EXP.value),
            AnimalEnum.TURTLE.value: (
                Hp.TURTLE_HP.value, Damage.TURTLE_DMG.value, Price.TURTLE_PRICE.value, AnimalExp.TURTLE_EXP.value),
            AnimalEnum.LIZARD.value: (
                Hp.LIZARD_HP.value, Damage.LIZARD_DMG.value, Price.LIZARD_PRICE.value, AnimalExp.LIZARD_EXP.value),
            AnimalEnum.SNAKE.value: (
                Hp.SNAKE_HP.value, Damage.SNAKE_DMG.value, Price.SNAKE_PRICE.value, AnimalExp.SNAKE_EXP.value),

            # Základny
            BaseEnum.ANTHILL.value: (Hp.SPIDER_HP.value, 0, 0, 0),
            BaseEnum.STUMP.value: (Hp.ANT_HP.value, 0, 0, 0),
            BaseEnum.STONES.value: (Hp.ANT_HP.value, 0, 0, 0)
        }
        return attributes.get(char_type, (0, 0, 0, 0))

    @staticmethod
    def attack(target, damage):
        """sníží cílové postavě životy o zadané poškození"""
        target.logic.hp -= damage

    @staticmethod
    def modify_width_hp(target):
        """Aktualizuje vizuální délku HP baru na základě aktuálních životů"""
        if target.logic.hp > 0:
            hp_percentage = target.logic.hp / target.logic.max_hp  # výpočet procent HP
            width = hp_percentage * target.logic.max_hp_width  # výpočet nové šířky HP baru
            return width
        return 0

    def set_first(self, value):
        """Nastaví, zda je postava první v řadě."""
        self.first = value

    def set_hp(self, hp):
        """Nastaví počet životů postavy"""
        self.hp = hp

    def set_hp_width(self, width):

        self.character.graphics.rect_hp_width = width

    def handle_attack(self, enemy_player, current_time):
        """Řeší útok na nepřítele, pokud dojde ke kolizi a byl dodržen časový interval"""
        if self.first and enemy_player:
            first_enemy = enemy_player.get_first()  # získá prnví jednotku nepřítele

            if self.rect.colliderect(first_enemy.rect):  # pokud se překrývají a
                if current_time - self.last_damage_time >= self.damage_interval:  # kontrola intervalu
                    self.attack(first_enemy, self.damage)  # provede útok
                    new_width = self.modify_width_hp(first_enemy)  # nová šířka HP baru
                    first_enemy.logic.set_hp_width(new_width)  # aktualizace zobrazení HP baru
                    self.last_damage_time = current_time  # aktualizuje čas posledního útoku
                return True
        return False

    def check_ally_collision(self, allies, is_enemy):
        """zabraňuje pohyb postavy, pokud je před ní spojenec (aby se nepřekrývaly)."""
        direction = 1 if is_enemy else -1
        for ally in allies:
            #Base
            if ally.logic.speed == 0:
                continue
            if self is ally.logic:
                return False
            elif self.rect.colliderect(ally.rect):
                return True
        return True
        #tmp = any(
            #self != ally and self.rect.colliderect(ally.rect) and (self.rect.x - ally.rect.x) * direction < 0
            #for ally in allies
        #)
        #return tmp

    def is_eliminated(self):
        """Vrací true, pokud jsou životy pod nulou (postava je zneškodněná)"""
        if self.hp <= 0:
            return True
        return False

    def update(self, enemies, allies, is_enemy, delta_time):
        """Hlavní update funkce - volá se každý snímek. Nejprve se zkontroluje, zda má jednotka zaútočit. Pokud není
        kolize se spojencem, pohne se dopředu"""
        current_time = pygame.time.get_ticks()

        if self.handle_attack(enemies, current_time):
            return  # pokud došlo k útoku, ukončí update (nepohybuje se dál)

        if not self.check_ally_collision(allies, is_enemy):
            self.move(self.speed, delta_time)  # pohyb, pokud není kolize se spojencem
