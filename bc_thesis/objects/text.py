import pygame


class Text(pygame.sprite.Sprite):
    """Třída pro vykreslování textu na obrazovku, dědí do pygame.sprite.Sprite"""
    def __init__(self, screen, text, position=(0, 0), color='black', size=21, bold=False):
        """Kontstruktor třídy Text, který inicializuje objekt pro zobrazení textu
         :param screen: Obrazovka (pygame.Surface), na které bude text vykreslen.
        :param text: Text, který má být zobrazen.
        :param position: Počáteční pozice textu na obrazovce (výchozí je (0, 0)).
        :param color: Barva textu (výchozí je černá).
        :param size: Velikost textu (výchozí je 21).
        :param bold: Určuje, zda má být text tučný (výchozí je False)
        """
        super().__init__()  # zavolá konstruktor třídy Sprite
        self.font_obj = pygame.font.Font('res/open-sans.light.ttf', size)  # Vytvoří objekt písma
        if bold:  # pokud je bold True, text bude tučný
            self.font_obj.set_bold(True)
        self.text = text  # Text, který bude zobrazen
        self.color = color  # Barva textu
        self.screen = screen  # Obrazovka, na které bude text vykreslen
        self.position = position  # Pozice textu na obrazovce
        self._update_surface()  # Metoda pro aktualizaci textového povrchu při inicializaci

    def set_text(self, text):
        self.text = text
        self._update_surface()

    def _update_surface(self):
        """
            Vytvoří nový povrch (surface) pro text, který bude vykreslen.
            Vytvoří také obdélník, který umožňuje správné umístění textu na obrazovce.
            """
        self.text_surf_obj = self.font_obj.render(self.text, True, self.color)  # Render the text
        self.text_rect_obj = self.text_surf_obj.get_rect(topleft=self.position)  # Get the rectangle for positioning

    def write(self):
        """Vykreslí text na obrazovku
        Tato metoda použije obdélník a povrch textu a vykreslí ho na obrazovku.
        """
        self.screen.blit(self.text_surf_obj, self.text_rect_obj)

    def width(self):
        """Vrátí šířku textu, což je šířka obdelníku, který obklopuje text"""
        return self.text_rect_obj.width

    def height(self):
        """Vrátí výšku textu, což je výška obdelníku, který obklopuje text"""
        return self.text_rect_obj.height

    def set_position(self, x, y):
        """Umožňuje změnit pozici textu na obrazovce
            :param x: Nová x-ová souřadnice
            :param y: Nová y-ová souřadnice
        """
        self.position = (x, y)  # nová pozice
        self.text_rect_obj.topleft = self.position  # nastaví pozici obdelníku, který obsahuje text

    def update_text(self, new_text):

        self.text = new_text  # Nastaví nový text
        self._update_surface()  # aktualizuje povrch textu na základě nového textu
        