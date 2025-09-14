import pygame

from bakalarska_prace.objects.animal import AnimalEnum, BaseEnum
from bakalarska_prace.utils.textures import load_character_textures

from bakalarska_prace.settings.globals import RED


class CharacterGraphics:
    """Grafická reprezentace herní jednotky - stará se o texturu a vykreslování HP baru
        :param rect: obdélníkový tvar postavy
        :param char: samotný objekt herní postavy (incstance Character)
        :param animal: název zvířete např. "ant"
        :param image
        :param position: počáteční pozice na obrazovce
    """
    def __init__(self, rect, char, animal, image=pygame.Surface((50, 50), pygame.SRCALPHA), position=(0, 0)):
        self.char_texture = load_character_textures()
        self.rect = rect
        self.image = image
        self.position = position
        self.char = char
        self.rect_hp_width = 20  # výchozí šířka ukazatele životů
        self.rect_hp = pygame.Rect(20, 0, self.rect_hp_width, 2)  # Plochý obdelník pro HP bar
        self._set_textures(animal)

    def set_width(self, width):

        self.rect_hp.width = width

    def _set_textures(self, animal):
        """Kontroluje, zda je animal typ str. Pokud ano, přiřazuje správnou texturu z dictionary na záklladě hodnoty
        Enumu. Pokud se hodnota nenajde, vyvolá ValueError."""
        if isinstance(animal, str):
            animal_textures = {
                AnimalEnum.LADYBUG.value: self.char_texture['ladybug'],
                AnimalEnum.ANT.value: self.char_texture['ant'],
                AnimalEnum.SPIDER.value: self.char_texture['spider'],
                AnimalEnum.BLUEBIRD.value: self.char_texture['bluebird'],
                AnimalEnum.BLACKBIRD.value: self.char_texture['blackbird'],
                AnimalEnum.REDBIRD.value: self.char_texture['redbird'],
                AnimalEnum.TURTLE.value: self.char_texture['turtle'],
                AnimalEnum.LIZARD.value: self.char_texture['lizard'],
                AnimalEnum.SNAKE.value: self.char_texture['snake'],
                BaseEnum.ANTHILL.value: self.char_texture['anthill'],
                BaseEnum.STUMP.value: self.char_texture['stump'],
                BaseEnum.STONES.value: self.char_texture['stones']
            }
            try:
                self.image = animal_textures[animal]
            except KeyError:
                raise ValueError("Unknown animal type!")

    def clear_hp(self):
        """Vymaže předchozí HP bar z obrázku (nakreslí průhledný obdelník)"""
        pygame.draw.rect(self.image, (0, 0, 0, 0), self.rect_hp)

    def draw_hp(self, color=RED):
        self.clear_hp()
        self.rect_hp.width = self.rect_hp_width  # nastaví šířku životů podle hodnoty
        pygame.draw.rect(self.image, color, self.rect_hp)

    def draw(self):
        self.draw_hp()