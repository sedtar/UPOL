import pygame
from bakalarska_prace.objects.entity import Entity
from bakalarska_prace.settings.globals import padding


class Button(Entity):
    """
       Třída Button reprezentuje grafické tlačítko ve hře. Dědí od třídy Entity.
       Tlačítko může provést akci při kliknutí a změnit svůj vzhled při přejetí myší.

       Atributy:
           action (callable): Funkce, která se spustí při kliknutí na tlačítko.
           original_alpha (int): Výchozí hodnota průhlednosti tlačítka.
           done (bool): Určuje, zda byla akce již provedena (zabraňuje opakovaným kliknutím).
           description (str): Popis tlačítka.

       Metody:
           check_mouse_hover(): Kontroluje, zda je kurzor myši nad tlačítkem, a mění průhlednost.
           check_mouse_click(): Kontroluje události kliknutí myši a spouští akci, pokud bylo tlačítko kliknuto.
       """

    def __init__(self, groups, image=pygame.Surface((50, 50)), position=(0, 0),
                 action=None, description="No description", filled=False):
        """
        Inicializuje tlačítko se zadanou akcí, obrázkem, pozicí a popisem.

        :param groups: Skupiny, do kterých tlačítko patří.
        :param image: Povrch tlačítka (pygame.Surface), výchozí je prázdný povrch 50x50 pixelů.
        :param position: Pozice tlačítka (x, y).
        :param action: Funkce, která se spustí při kliknutí na tlačítko.
        :param description: Popis tlačítka, výchozí je "No description".
        """

        # přidání odsazení
        padded_size = (image.get_width() + 2 * padding, image.get_height() + 2 * padding)
        surface = pygame.Surface(padded_size, pygame.SRCALPHA)

        if filled:
            surface.fill((170, 170, 170))  # vyplnění šedou barvou

        surface.blit(image, (padding, padding))  # vykreslení obrázku s odsazením
        super().__init__(groups, surface, position)  # inicializace jako Entity

        self.original_alpha = self.image.get_alpha()  # Uložení původní průhlednosti
        self.action = action  # akce při kliknutí
        self.description = description  # Popis tlačítka

    def check_mouse_hover(self):
        """
        Změní průhlednost tlačítka při přejetí myši

        :return: True, pokud je kurzor nad tlačítkem, jinak False.
        """
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self.image.set_alpha(128 if hovered else self.original_alpha)
        return hovered

    def check_mouse_click(self, b_event):
        """
        Kontroluje událost pygame.MOUSEBUTTONDOWN pro levé tlačítko myši
        a zda je kurzor nad tlačítkem. Pokud jsou podmínky splněny, provede přiřazenou akci.

        :param b_event: Událost pygame typu pygame.MOUSEBUTTONDOWN.
        """

        # Check if the event corresponds to a left mouse button click
        if b_event.type == pygame.MOUSEBUTTONDOWN and b_event.button == 1:
            mouse_pos = b_event.pos
            if self.rect.collidepoint(mouse_pos):
                pygame.mixer.Sound("res/sounds/click.wav").play()
                if self.action:
                    self.action()  # Executes the action
