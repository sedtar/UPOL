import threading
import tkinter as tk
from bakalarska_prace.form.connection_form import ConnectionForm
from bakalarska_prace.form.game_host_form import GameHostForm
from bakalarska_prace.objects.text import Text
from bakalarska_prace.scenes.base_scene import BaseScene
from bakalarska_prace.objects.button import Button
from bakalarska_prace.settings.globals import SCREENWIDTH, SCREENHEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT
import bakalarska_prace.settings.globals as g


class ConnectionScene(BaseScene):
    """Scéna pro výběr připojení v multiplayer režimu (Host / Join)."""
    def __init__(self, app):
        super().__init__(app, 'lightblue')
        self.tkinter_thread = None
        self.root = None
        self._create_text()
        self._create_buttons()  # Vytvori tlacitka

    def _create_text(self):
        text = Text(self.app.screen, "MULTIPLAYER", ((SCREENWIDTH // 2) - 55, (SCREENHEIGHT // 2) -
                                                     (5 * BUTTON_HEIGHT)), size=42, color='black', bold=True)
        text.set_position((SCREENWIDTH // 2) - (text.width() // 2), (SCREENHEIGHT // 2) - (5 * BUTTON_HEIGHT))
        self.texts.add(text)

    def _create_buttons(self):
        """Vytvoří tlačítka a přidá je do skupiny sprite objektů."""
        # tlačítko "Host" - spustí vlákno s otevřením formuláře pro hostitele hry
        Button(self.items, self.textures["host"],
               ((self.app.scene.screen_width // 2) - (BUTTON_WIDTH // 2), (self.app.scene.screen_height // 2) -
                (2 * BUTTON_HEIGHT)),
               lambda: self._start_thread(lambda: self.open_form(GameHostForm)))
        # tlačítko "Join" - spustí vlákno s otevřením formuláře pro připojení ke hře
        Button(self.items, self.textures["join"],
               ((self.app.scene.screen_width // 2) - (g.BUTTON_WIDTH // 2), self.app.scene.screen_height // 2),
               lambda: self._start_thread(lambda: self.open_form(ConnectionForm)))
        # tlačítko "Back" - vrátí zpět do hlavního menu
        Button(self.items, self.textures["back"], (0, 0), lambda: self.button_actions.show_scene("MainMenuScene"))

    def _start_thread(self, target_function):
        """Spustí nové vlákno pro danou funkci, pokud žádné již neběží."""
        # Pokud už vlákno existuje a je aktivní, nic neděláme
        if hasattr(self, "tkinter_thread") and self.tkinter_thread is not None and self.tkinter_thread.is_alive():
            return
        self.tkinter_thread = threading.Thread(target=target_function, daemon=True)
        self.tkinter_thread.start()

    def open_form(self, form_class):
        """Otevře formulář v novém tkinter okně."""
        root = tk.Tk()
        form_class(self.app, root, self.tkinter_thread)

    def draw(self):
        """Vykreslí scénu."""
        super().draw()
