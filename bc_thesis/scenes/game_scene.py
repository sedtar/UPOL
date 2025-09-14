from bakalarska_prace.scenes.base_scene import BaseScene
from bakalarska_prace.objects.button import Button
from bakalarska_prace.objects.text import Text
from bakalarska_prace.ui.playerui import PlayerUI
from bakalarska_prace.objects.world import World
from bakalarska_prace.settings.globals import *


class GameScene(BaseScene):
    """
    Třída reprezentující herní scénu.
    Poskytuje logiku pro herní režim včetně pauzy, konce hry a ovládacích prvků.
    """

    def __init__(self, app):
        super().__init__(app)
        self.pause = False
        self.game_over = False
        self.sound_played = False
        self._create_overlay_buttons()

    def _create_overlay_buttons(self):
        """Vytváří tlačítka pro restart a návrat do hlavního menu."""
        self.restart_button = self._create_button(
            texture_key="start",
            callback=lambda: self.button_actions.show_scene("SingleplayerScene"),
            label="Restart Button"
        )
        self.exit_button = self._create_button(
            texture_key="exit",
            callback=lambda: self.button_actions.show_scene("MainMenuScene")
        )
        self.items.add(self.restart_button)
        self.items.add(self.exit_button)

    def _create_button(self, texture_key, callback, label=None):
        """
        Pomocná metoda pro vytvoření tlačítka se sdílenou pozicí."""
        return Button(
            self.items,
            self.textures[texture_key],
            (SCREENWIDTH // 2 - BUTTON_WIDTH // 2,
             (SCREENHEIGHT // 2 - BUTTON_HEIGHT) + (2 * BUTTON_HEIGHT)),
            callback,
            label
        )

    def _setup_world(self, player, enemy):
        """Inicializuje herní svět a uživatelské rozhraní hráče."""
        self.world = World(self, player, enemy)
        self.player_ui = PlayerUI(self.app.screen, player, self)

    def _check_game_over(self):
        """Zkontroluje, zda nenastal konec hry (hráč nebo nepřítel nemá žádnou postavu)."""
        if not self.first_player.hero_group or not self.second_player.hero_group:
            self.game_over = True
            self.start = False

    def toggle_pause(self):
        """Přepne stav pauzy."""
        self.pause = not self.pause

    def draw_overlay(self, text):
        """
        Vykreslí průhledný overlay (pauza nebo konec hry) s příslušnými tlačítky a textem.

        Args:
            text (str): Text k zobrazení (např. "Pause", "Game Over").
        """
        overlay = pygame.Surface((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.app.screen.blit(overlay, (0, 0))

        self.items.empty()

        if text == "Game Over":
            self.items.add(self.restart_button)
            self.app.screen.blit(self.restart_button.image, self.restart_button.rect)
        elif text == "Pause":
            self.items.add(self.exit_button)
            self.app.screen.blit(self.exit_button.image, self.exit_button.rect)

        overlay_text = Text(self.app.screen, text=text, color="white")
        overlay_text.text_rect_obj.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)
        overlay_text.write()

    def draw(self):
        """Vykreslí herní scénu, UI a overlay podle aktuálního stavu."""
        super().draw()
        self.world.draw(self.app.screen, self.camera.camera_offset)
        self.player_ui.graphics.draw()

        if self.game_over:
            self.start = False
            self.draw_overlay("Game Over")
        elif self.pause:
            self.draw_overlay("Pause")
        else:
            self.camera.update()
            self.player_ui.update()

    def save_full_screenshot(self, filename="screenshot.png"):
        """
        Uloží screenshot celého herního světa bez ohledu na posun kamery.
        """
        full_surface = pygame.Surface((SCREENWIDTH + OFFSET_RIGHT_LIMIT, SCREENHEIGHT))
        self.world.draw(full_surface, 0)

        line_thickness = 3
        black = (0, 0, 0)

        pygame.draw.rect(full_surface, black, (0, 0, SCREENWIDTH + OFFSET_RIGHT_LIMIT, SCREENHEIGHT), line_thickness)
        pygame.draw.line(full_surface, black, (SCREENWIDTH, 0), (SCREENWIDTH, SCREENHEIGHT), line_thickness)

        pygame.image.save(full_surface, filename)
