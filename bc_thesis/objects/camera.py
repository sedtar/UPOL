from bakalarska_prace.settings.globals import *  # globální konstanty


class Camera:
    """
     Třída Camera zajišťuje pohyb kamery v herním světě.
    """
    def __init__(self, start_position):
        """
            Inicializuje kameru s počáteční pozicí (odsazením).

            Parametry:
                start_position (int): Počáteční pozice kamery (kolik je posunuta od začátku mapy).
        """
        self.camera_offset = start_position

    def update(self, scroll_speed=10):
        """
        Aktualizuje pozici kamery podle pohybu myši pro horizontální posun.

        Kamera se posouvá doleva, když je kurzor u levého okraje obrazovky a zároveň
        není dosaženo levého limitu posouvání.
        Kamera se posouvá doprava, když je kurzor u pravého okraje obrazovky a zároveň
        není dosaženo pravého limitu posouvání.
        :param scroll_speed: Rychlost posouvání kamery v pixelech.
        :return:
        """
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] < BLOCK_SIZE and self.camera_offset > OFFSET_LEFT_LIMIT:
            self.camera_offset -= scroll_speed
        elif mouse_pos[0] > SCREENWIDTH - BLOCK_SIZE and self.camera_offset < OFFSET_RIGHT_LIMIT:
            self.camera_offset += scroll_speed
