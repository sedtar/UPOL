# Importuje knihovnu enum, která umožňuje vytvořit výčtové typy (enums) pro přehledné definování konstant.
import enum


# Definuje výčtový typ AnimalEnum, který obsahuje seznam zvířat.
class AnimalEnum(enum.Enum):
    ANT = "ant"
    SPIDER = "spider"
    LADYBUG = "ladybug"
    BLACKBIRD = "blackbird"
    BLUEBIRD = "bluebird"
    REDBIRD = "redbird"
    TURTLE = "turtle"
    LIZARD = "lizard"
    SNAKE = "snake"


# Definuje třídu BaseEnum jako výčtový typ, který obsahuje různé typy základen.
class BaseEnum(enum.Enum):
    ANTHILL = "anthill"
    STUMP = "stump"
    STONES = "stones"


# Definuje třídu AnimalExp jako výčtový typ, který udává hodnoty zkušeností (exp) pro každé zvíře.
class AnimalExp(enum.Enum):
    ANT_EXP = 30
    SPIDER_EXP = 45
    LADYBUG_EXP = 40
    BLACKBIRD_EXP = 50
    BLUEBIRD_EXP = 55
    REDBIRD_EXP = 60
    TURTLE_EXP = 70
    LIZARD_EXP = 75
    SNAKE_EXP = 80


# Definuje třídu Damage jako výčtový typ pro různé úrovně poškození.
class Damage(enum.Enum):
    ANT_DMG = 1
    LADYBUG_DMG = 3
    SPIDER_DMG = 5
    BLACKBIRD_DMG = 7
    BLUEBIRD_DMG = 9
    REDBIRD_DMG = 11
    TURTLE_DMG = 13
    LIZARD_DMG = 15
    SNAKE_DMG = 17


# Definuje třídu Hp jako výčtový typ, který uvádí počet životů pro různá zvířata.
class Hp(enum.Enum):
    ANT_HP = 10
    LADYBUG_HP = 15
    SPIDER_HP = 20
    BLACKBIRD_HP = 25
    BLUEBIRD_HP = 30
    REDBIRD_HP = 35
    TURTLE_HP = 40
    LIZARD_HP = 45
    SNAKE_HP = 50


# Definuje třídu Price jako výčtový typ, který obsahuje ceny pro různá zvířata.
class Price(enum.Enum):
    ANT_PRICE = 10
    LADYBUG_PRICE = 15
    SPIDER_PRICE = 20
    BLACKBIRD_PRICE = 30
    BLUEBIRD_PRICE = 35
    REDBIRD_PRICE = 40
    TURTLE_PRICE = 50
    LIZARD_PRICE = 55
    SNAKE_PRICE = 60
