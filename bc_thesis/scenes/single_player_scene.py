from bakalarska_prace.objects.phase import Phase
from bakalarska_prace.objects.player import Player
from bakalarska_prace.objects.enemy import Enemy
from bakalarska_prace.scenes.game_scene import GameScene
from bakalarska_prace.objects.camera import Camera
import pygame


class SingleplayerScene(GameScene):
    def __init__(self, app):
        super().__init__(app)

        self.camera = Camera(0)
        self.player = Player()
        self.enemy = Enemy(self.player)
        self._setup_world(self.player, self.enemy)


    def update(self, delta_time):
        self.world.update(delta_time)
        if self.pause:
            return

        self.enemy.generate_enemies()
        self.player.update_first()
        self.enemy.update_first()

        self.player.update(self.enemy, delta_time)
        self.enemy.update(self.player, delta_time)

        self.enemy.check_if_eliminated(self.player)
        self.player.check_if_eliminated(self.enemy)

        if not self.player.hero_group or not self.enemy.hero_group:
            self.game_over = True
            if not self.sound_played:
                sound = pygame.mixer.Sound("res/sounds/explosion.wav")
                sound.play()
                self.sound_played = True
