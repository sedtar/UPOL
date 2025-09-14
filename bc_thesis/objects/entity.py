import pygame.sprite
from bakalarska_prace.settings.globals import *


class Entity(pygame.sprite.Sprite):
    """Základní herní ojekt. Můžou z něho dědit další herní třídy (např. postavy, tlačítka). Je součástí sprite skupin,
     které Pygame umí hromadně vykreslovat a aktualizovat.
    :param groups: seznam sprite skupin, do kterých má být instance přidána
    :param image: Pygame surface, tedy obrázek/plocha, která se bude zobrazovat
    :param position: počáteční pozice objektu na obrazovce
    """
    def __init__(self, groups, image=pygame.Surface((50, 50)), position=(0, 0)):

        super().__init__(groups)
        self.image = image
        self.position = list(position)  # Převedeme tuple na list, aby byl mutabilní
        # vytvoří obdelník (pygame.Rect) odpovídajícím rozměrům obrázku a nastaví jeho pozici
        self.rect = self.image.get_rect()
        self.rect.topleft = position  # vykreslí se

    def draw_border(self):
        """Nakreslí okraj (černý rámeček) kolem objektu"""
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 2)

    def move(self, speed, delta_time):
        """Posune entitu o danou rychlost v závislosti na čase (delta_time)"""

        self.rect.x += speed * delta_time
