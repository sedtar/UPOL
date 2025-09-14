import pygame
from bakalarska_prace.objects.character_graphic import CharacterGraphics
from bakalarska_prace.objects.character_logic import CharacterLogic
from bakalarska_prace.objects.entity import Entity


class Character(Entity):
    """
    Character třída reprezentuje herní postavu s grafickými a logickými komponenty.
    Dědí z třídy Entity. Kombinuje jak vizuální, tak logickou reprezentaci

    """

    def __init__(self, groups, animal, image=pygame.Surface((50, 50)), position=(0, 0), speed=0, width=50, height=500):
        """
        Inicializuje instanci třídy Character s grafickými a logickými komponenty.

        """
        super().__init__(groups, image, position)
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.rect.topleft = position
        self.graphics = CharacterGraphics(self.rect, self, animal, image, position)
        self.logic = CharacterLogic(rect=self.rect, char_type=animal, character=self, speed=speed)
        self.image = self.graphics.image

    def update(self, enemy_player, allies, is_enemy, delta_time):
        self.graphics.draw()
        self.logic.update(enemy_player, allies, is_enemy, delta_time)

    def flip_vertically(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.graphics.image = self.image
