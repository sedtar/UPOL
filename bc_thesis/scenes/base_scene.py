import pygame

from bakalarska_prace.objects.button_actions import ButtonActions
from bakalarska_prace.settings.globals import SCREENWIDTH, SCREENHEIGHT
from bakalarska_prace.utils.textures import load_character_textures


class BaseScene:
    """Základní třída pro všechny herí scény.
        Obsahuje sdílené vlastnosti, jako pozadí, velikost obrazovky, sprity, tlačítka
        Ostatní scény (např. menu, gamescene, ji dědí)
    """
    def __init__(self, app, background_color='lightblue'):
        """
        Inicializace základní scény.

        :param app: Hlavní aplikace
        :param background_color: Výchozí barva pozadí scény.
              """
        self.screen_width = SCREENWIDTH
        self.screen_height = SCREENHEIGHT
        self.app = app
        self.start = False
        self.button_actions = ButtonActions(self)
        self.items = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.background_color = background_color
        self.textures = load_character_textures()

    def update(self, delta_time):
        """Metoda pro aktualizaci scény. Přepíše ji konkrétní scéna."""
        pass

    def draw(self):
        """
            Vykreslí pozadí a všechny prvky scény.
            Prvky (texty i obrázky) jsou iterovány a zobrazeny na obrazovce.
        """
        self.app.screen.fill(self.background_color)
        for item in self.items:
            self.app.screen.blit(item.image, item.rect)
        for text in self.texts:
            text.write()
