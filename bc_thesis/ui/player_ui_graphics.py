import pygame
from bakalarska_prace.objects.entity import Entity
from bakalarska_prace.settings.globals import MARGIN, COIN_HEIGHT, BLOCK_SIZE, RED, SCREENWIDTH, SCREENHEIGHT
from bakalarska_prace.objects.text import Text
from bakalarska_prace.utils.textures import load_character_textures


class PlayerUIGraphics:
    """
    Třída zodpovědná za vykreslování hračova UI - mince, zkušenosti, tlačítka.
    Obsahuje metody pro vykreslování jednotlivých částí UI a správu jejich zobrazení

    """

    def __init__(self, screen, player):

        self.screen = screen
        self.player = player

        self.textures = load_character_textures()

        # Skupiny sprajtů pro různé typy UI prvků
        self.sprites = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.animal_buttons = pygame.sprite.Group()
        self.item_buttons = pygame.sprite.Group()

        # Vytvoření sprajtů pro minci v levém horním rohu
        Entity([self.sprites], self.textures['coin'], (MARGIN, MARGIN))

        # Textové objekty pro zobrazení počtu mincí a zkušeností hráče
        self.coin_text = Text(screen, str(self.player.coin_amount), (MARGIN + BLOCK_SIZE, MARGIN))
        self.exp_text = Text(screen, "EXP", (MARGIN * 2, MARGIN + COIN_HEIGHT), color=RED)
        self.exp_value = Text(screen, str(self.player.exp), (MARGIN + BLOCK_SIZE, MARGIN + self.coin_text.height()))

    def write_texts(self):
        """
        Zapíše texty mincí a zkušeností na obrazovku.
        """
        self.coin_text.write()
        self.exp_text.write()
        self.exp_value.write()

    def button_text(self, button):
        """
        Vykreslí popis tlačítka na obrazovku. Pokud popis obsahuje znak pro nový
        řádek ('/n'), je text rozdělen na více řádků a každý je vykreslen pod sebe.

        :param button: Instance tlačítka, jehož popis  (description) se má vykrelit.
        """

        # Výpočet výchozí X a Y pozice pro text (vedle textu s počtem mincí)
        x = 2 * self.coin_text.position[0] + self.coin_text.width()
        y = MARGIN

        # Rozdělení textu podle znaků nového řádku ('\n')
        lines = button.description.split('\n')

        # Iterace přes jednotlivé řádky textu a jejich vykreslení pod sebe
        for i, line in enumerate(lines):
            text = Text(self.screen, line, position=(x, y + i * 20), size=14)
            text.write()

    def draw_group(self, group):
        """
        Vykreslí skupinu sprajtů na obrazovku.

        Args:
            group: Skupina, která má být vykreslena.
        """
        for item in group:
            self.screen.blit(item.image, item.rect)
            if group is self.animal_buttons or group is self.item_buttons:
                item.draw_border()

    def draw(self):
        """
        Draws all UI elements (sprites, buttons, texts) to the screen.
        """
        self.draw_group(self.item_buttons)
        self.draw_group(self.sprites)
        self.draw_group(self.items)
        self.draw_group(self.animal_buttons)
        self.write_texts()

    def draw_cooldown_bar(self, button, ratio):
        """Vykreslí vizuální indikátor cooldownu pod tlačítkem."""
        bar_x = button.rect.x
        bar_y = button.rect.bottom + 5  # těsně pod tlačítkem
        bar_width = button.rect.width
        bar_height = 6

        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))  # pozadí je šedé
        pygame.draw.rect(self.screen, (0, 120, 255), (bar_x, bar_y, bar_width * ratio, bar_height))  # vyplněná část


