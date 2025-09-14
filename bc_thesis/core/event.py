import sys
import pygame
from bakalarska_prace.objects.enemy import Enemy
from bakalarska_prace.scenes.game_scene import GameScene


class EventHandler:
    """
    Třída EventHandler je zodpovědná za správu a zpracování událostí ve hře. To zahrnuje vstupy uživatele,
    jako jsou stisknutí klávesy, kliknutí myší a jiné interakce s herní scénou a menu.

    Atributy:
        scene (Scene): Aktuální scéna hry, kde se dějí různé akce a události.
        menu (Menu): Hlavní menu hry, které obsahuje různé tlačítka, se kterými může hráč interagovat.

    """

    def __init__(self, scene):
        """
        Inicializuje instanci EventHandler.

        Argumenty:
            scene (Scene): Aktuální scéna, kde se dějí herní události.
            menu (Menu): Hlavní menu hry obsahující tlačítka a interaktivní prvky.
        """
        self.scene = scene

    def handle_events(self):
        """
        Zpracovává všechny vstupy uživatele, jako jsou stisky kláves a kliknutí myší.

        Tato metoda naslouchá různým událostem pomocí `pygame.event.get()` a zpracovává je podle potřeby
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.scene.app.running = False  # Ukončí hlavní smyčku

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and isinstance(self.scene, GameScene):
                    self.scene.toggle_pause()  # Pozastaví nebo znovu spustí hru, když je stisknuta klávesa 'P'.
                if event.key == pygame.K_ESCAPE and isinstance(self.scene, GameScene):
                    self.scene.toggle_pause()  # Pozastaví nebo znovu spustí hru, když je stisknuta klávesa 'P'.

            if hasattr(self.scene, "player_ui") and not self.scene.pause and not self.scene.game_over:
                if hasattr(self.scene.player_ui.graphics, "animal_buttons"):
                    #Kontrola kliknutí myší na tlačítka UI hráče (zvířata a předměty)
                    for button in self.scene.player_ui.graphics.animal_buttons:
                        button.check_mouse_click(event)

                if hasattr(self.scene.player_ui.graphics, "item_buttons"):
                    for button in self.scene.player_ui.graphics.item_buttons:
                        button.check_mouse_click(event)
            elif hasattr(self.scene, "items"):
                for button in self.scene.items:
                    button.check_mouse_click(event)  # Zavolá metodu s událostí jako parametrem.