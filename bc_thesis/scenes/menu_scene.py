from bakalarska_prace.objects.text import Text
from bakalarska_prace.scenes.base_scene import BaseScene
from bakalarska_prace.objects.button import Button
from bakalarska_prace.settings.globals import SCREENWIDTH, SCREENHEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT
from bakalarska_prace.utils.textures import load_character_textures


class MenuScene(BaseScene):
    """"Tato třída reprezentuje scenu """
    def __init__(self, app):
        super().__init__(app)
        self.start = False
        self.app = app
        self.background_color = 'lightblue'
        self.textures = load_character_textures()
        self._create_buttons()
        self._create_text()

    def _create_text(self):
        text = Text(self.app.screen, "MENU",  ((self.screen_width // 2) - 55, (self.screen_height // 2)
                                               - (5 * BUTTON_HEIGHT)), size=42, color='black', bold=True)
        text.set_position((self.screen_width // 2) - (text.width() // 2), (self.screen_height // 2) - (5 * BUTTON_HEIGHT))
        self.texts.add(text)

    def start_game(self):
        """Spustí hru"""
        self.start = True
        self.app.set_scene("SinglelayerScene")

    def _create_buttons(self):
        """Vytvoří tlačítka a přidá je do skupiny sprite objektů."""

        Button(self.items, self.textures["singleplayer"],
               ((SCREENWIDTH // 2) - (BUTTON_WIDTH // 2), (SCREENHEIGHT // 2) - (3 * BUTTON_HEIGHT)),
               lambda: self.button_actions.show_scene("SingleplayerScene"))
        Button(self.items, self.textures["multiplayer"],
               ((SCREENWIDTH // 2) - (BUTTON_WIDTH // 2), SCREENHEIGHT // 2 - BUTTON_HEIGHT),
               lambda: self.button_actions.show_scene("ConnectionScene"))

        Button(self.items, self.textures["exit"],
               (SCREENWIDTH // 2 - BUTTON_WIDTH // 2, (SCREENHEIGHT // 2) + BUTTON_HEIGHT),
               self.button_actions.close_app)

    def draw(self):
        """Pokud hra nezačala, vykreslí menu."""
        if not self.start:
            super().draw()

