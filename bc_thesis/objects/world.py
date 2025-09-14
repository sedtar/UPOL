from bakalarska_prace.objects.entity import Entity
from bakalarska_prace.utils.textures import *
import random


class World:
    def __init__(self, scene, player, enemy):
        """Inicializuje svět včetně textur, objektů a bloků"""
        self.block_textures = load_block_textures('res/grass.png')

        self.sprites = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.base_texture = load_character_textures()
        self.player = player
        self.enemy = enemy
        self.scene = scene

        self.num_of_dirt_block = self.count_block(BLOCK_SIZE)
        self.num_of_background_block = self.count_block(SCREENWIDTH)
        # Generate the world blocks
        self._create_blocks(self.num_of_background_block, SCREENWIDTH, position_y=0,
                            texture=self.base_texture['background'])
        self._create_clouds()
        self._create_blocks(self.num_of_dirt_block, BLOCK_SIZE, SCREENHEIGHT - BLOCK_SIZE,  self.block_textures['dirt'])

    def count_block(self, block_size):
        return (self.scene.screen_width + OFFSET_RIGHT_LIMIT) / block_size

    def _create_clouds(self):
        """Vytváří mraky v náhodných pozicích na obrazovce"""
        num_of_clouds = NUM_OF_CLOUDS  # pocet mraků
        shuffled_indices = list(range(num_of_clouds))  # vytvori seznam cisel pro mraky
        random.shuffle(shuffled_indices)  # zamíchá seznam, aby byly pozice mraků náhodné
        for cloud_index in range(num_of_clouds):
            # pocatecní pozice mraku na základě indexu
            cloud_x = (SCREENWIDTH + OFFSET_RIGHT_LIMIT) / num_of_clouds * cloud_index
            cloud_y = (SCREENHEIGHT - BLOCK_SIZE * 4) / num_of_clouds * shuffled_indices[cloud_index]
            position = (cloud_x, cloud_y)
            # vytvori entitu pro kazdy mrak a prda ji do skupiny clouds
            Entity(self.clouds, self.base_texture['cloud'], position)

    def _create_blocks(self, num_of_blocks, block_size, position_y, texture):
        """Vytváří bloky na základě počtu bloků, velikosti a textury
            :param num_of_blocks: Počet bloků k vytvoření
            :param block_size: Velikost každého bloku
            :param position_y: Y pozice, na které se bloky umístí
            :param texture: Textura, kterou bloky budou mít
        """
        full_blocks = int(num_of_blocks)  # celkový počet plných bloků
        remainder = num_of_blocks - full_blocks  # zbytek, pokud počet bloků není celé číslo
        x = 0  # počáteční x pozice pro bloky

        # vytváří plné bloky (celé jednotky velikosti bloku)
        for _ in range(full_blocks):
            position = (x * block_size, position_y)  # vypocita pozici
            Entity(self.sprites, texture, position)  # vytvori entitu s danou texturou
            x += 1  # posune X pozici pro další blok

        if remainder > 0:  # pokud je nějaký zbytek (část bloku), vykreslí zbytek bloku
            new_width = int(block_size * remainder)  # vypočíta šířku zbytku
            texture_width = texture.get_width()  # získá šírku textury
            new_width = min(new_width, texture_width)  # omezí šírku, aby nevyčnivala z textury
            position = (x * block_size, position_y)
            # vytvoří nový povrch pro zbytek bloku
            new_image = pygame.Surface((new_width, block_size), pygame.SRCALPHA)
            new_image.blit(texture, (0, 0), (0, 0, new_width, block_size))  # překreslí texturu
            Entity(self.sprites, new_image, position)  # vytvoří entitu pro zbytek bloku

    @staticmethod
    def _draw_entities(screen, camera_offset, group):
        """Vykreslí všechny entity ve skupině na obrazovku
            :param screen: Pygame obrazovka, na kterou se vykresluje
            :param camera_offset: Posun kamery (pro zajištění pohybu)
            :param group: Skupina entit, které mají být vykresleny
        """
        for entity in group:
            offset_pos = (entity.rect.left - camera_offset, entity.rect.top)
            screen.blit(entity.image, offset_pos)

    def update(self, delta_time):
        """Aktualizuje stav světa
        :param delta_time: Čas mezi snímky
        """
        for cloud in self.clouds:
            if cloud.rect.x > SCREENWIDTH + OFFSET_RIGHT_LIMIT:
                cloud.rect.x = -BLOCK_SIZE  # Také aktualizujeme obdélník
            else:

                cloud.move(20, delta_time)

    def draw(self, screen, camera_offset):
        """Vykresluje svět na obrazovku
        :param screen: Pygame obrazovka
        :param camera_offset: Posun kamery pro zajištění pohybu
        """
        screen.fill('lightblue')  # Fill the screen with a light blue color as background

        # Vykreslí všechny entity (bloky a další objekty)
        self._draw_entities(screen, camera_offset, self.sprites)
        self._draw_entities(screen, camera_offset, self.clouds)

        # Vykreslí postavy hráče a nepřítele
        self._draw_entities(screen, camera_offset, self.player.hero_group)
        self._draw_entities(screen, camera_offset, self.enemy.hero_group)
        