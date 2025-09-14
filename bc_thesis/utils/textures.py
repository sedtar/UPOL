from bakalarska_prace.settings.globals import *

# Pomocné konstanty pro opakující se velikosti
CHAR_SIZE = (ANT_WIDTH, ANT_HEIGHT)
HOUSE_SIZE = (HOUSE_WIDTH, HOUSE_HEIGHT)
COIN_SIZE = (COIN_WIDTH, COIN_HEIGHT)
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
SCREEN_SIZE = (SCREENWIDTH, SCREENHEIGHT)


def make_texture(type_, filepath, size):
    return {'type': type_, 'filepath': filepath, 'size': size}


# Konfigurace textur
texture_data = {
    # Zvířata
    'ant': make_texture('character', 'res/animals/bugs/ant.png', CHAR_SIZE),
    'ladybug': make_texture('character', 'res/animals/bugs/ladybug.png', CHAR_SIZE),
    'spider': make_texture('character', 'res/animals/bugs/spider.png', CHAR_SIZE),
    'blackbird': make_texture('character', 'res/animals/birds/blackbird.png', CHAR_SIZE),
    'bluebird': make_texture('character', 'res/animals/birds/bluebird.png', CHAR_SIZE),
    'redbird': make_texture('character', 'res/animals/birds/redbird.png', CHAR_SIZE),
    'turtle': make_texture('character', 'res/animals/reptiles/turtle.png', CHAR_SIZE),
    'lizard': make_texture('character', 'res/animals/reptiles/lizard.png', CHAR_SIZE),
    'snake': make_texture('character', 'res/animals/reptiles/snake.png', CHAR_SIZE),

    # Předměty
    'coin': make_texture('item', 'res/coin.png', COIN_SIZE),
    'star': make_texture('item', 'res/star.png', COIN_SIZE),
    'background': make_texture('item', 'res/background.png', SCREEN_SIZE),
    'cloud': make_texture('item', 'res/cloud.png', (90, 70)),

    # Tlačítka
    'start': make_texture('item', 'res/buttons/start.png', BUTTON_SIZE),
    'exit': make_texture('item', 'res/buttons/exit.png', BUTTON_SIZE),
    'host': make_texture('item', 'res/buttons/host.png', BUTTON_SIZE),
    'join': make_texture('item', 'res/buttons/join.png', BUTTON_SIZE),
    'back': make_texture('item', 'res/buttons/back.png', BUTTON_SIZE),
    '1920x1080': make_texture('item', 'res/buttons/1920x1080.png', BUTTON_SIZE),
    '1280x720': make_texture('item', 'res/buttons/1280x720.png', BUTTON_SIZE),
    'singleplayer': make_texture('item', 'res/buttons/singleplayer.png', BUTTON_SIZE),
    'multiplayer': make_texture('item', 'res/buttons/multiplayer.png', BUTTON_SIZE),
    'ready': make_texture('item', 'res/buttons/ready.png', BUTTON_SIZE),

    # Základny
    'anthill': make_texture('house', 'res/houses/anthill.png', HOUSE_SIZE),
    'stump': make_texture('house', 'res/houses/stump.png', HOUSE_SIZE),
    'stones': make_texture('house', 'res/houses/stones.png', HOUSE_SIZE)
}

# Atlas textury
atlas_texture_data = {
    'dirt': {
        'type': 'block',
        'size': (BLOCK_SIZE, BLOCK_SIZE),
        'position': (0, 0)
    }
}


# Načtení textur
def load_character_textures():
    return {
        name: pygame.transform.scale(
            pygame.image.load(data['filepath']).convert_alpha(),
            data['size']
        )
        for name, data in texture_data.items()
    }


def load_block_textures(filepath):
    atlas_img = pygame.transform.scale(
        pygame.image.load(filepath).convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE)
    )
    return {
        name: pygame.Surface.subsurface(atlas_img, pygame.Rect(data['position'], data['size']))
        for name, data in atlas_texture_data.items()
    }
