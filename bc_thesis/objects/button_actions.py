import pygame


class ButtonActions:
    def __init__(self, scene):
        self.scene = scene

    def start_game(self):
        self.scene.start = True
        message = f"START:{self.scene.my_socket.local_ip}"
        self.scene.my_socket.send_message(message)

    def sp_start_game(self):
        """Spustí hru pro rezim singleplayer."""
        self.scene.start = True
        self.scene.app.set_scene("SingleplayerScene")

    def close_app(self):
        """Ukončí aplikaci."""
        self.scene.app.running = False

    def show_scene(self, scene):
        self.scene.app.set_scene(scene)

    def change_resolution(self, screen_width, screen_height):

        self.scene.screen_width = screen_width
        self.scene.screen_height = screen_height
        self.scene.app.screen = pygame.display.set_mode((self.scene.screen_width, self.scene.screen_height))
        self.scene.recalculate_layout()

