import pygame
from bakalarska_prace.utils.file_manager import FileManager


class Phase:
    """
    Třída představující herní fázi, včetně typů jednotek, základny a nákladů na přechod do další fáze.
    """

    PHASE_SEQUENCE = ["bugs", "birds", "reptiles"]

    def __init__(self, name, building_types, exp_cost=200, coin_cost=200):
        self.name = name
        self.building_types = building_types
        self.exp_cost = exp_cost
        self.coin_cost = coin_cost
        self.file_manager = FileManager()
        self.units = pygame.sprite.Group()
        self.current_index = 0
        self.set_base_building()

    def group_of_animals(self):
        """
        Vrací seznam souborů zvířat na základě aktuální fáze

        Vrací:
            list: Seznam názvů souborů zvířat (bez přípony) z odpovídající složky.
        """

        folder_mapping = {
            "bugs": "./res/animals/bugs",
            "birds": "./res/animals/birds",
            "reptiles": "./res/animals/reptiles"
        }
        folder = folder_mapping.get(self.name)
        if folder:
            return self.file_manager.file_names(folder)
        return []

    def set_base_building(self):
        """
        Nastaví základní typ budovy na základě názvu fáze.
        """
        base_buildings = {
            "bugs": "anthill",
            "birds": "stump",
            "reptiles": "stones"
        }
        self.building_types = base_buildings.get(self.name, "unknown")


    def next_phase(self):
        """
        Nataví hráče do další fáze.

        Argumenty:
            player (Player): Objekt hráče.

        Vrací:
            bool: True, pokud je přechod do další fáze úspěšný, jinak False.
        """

        self.current_index = self.PHASE_SEQUENCE.index(self.name)

        # Pokud je dostupná další fáze, provede upgrade
        if self.current_index < len(self.PHASE_SEQUENCE) - 1:
            self.name = self.PHASE_SEQUENCE[self.current_index + 1]
            # cena se zdvojnásobí
            self.exp_cost *= 2
            self.coin_cost *= 2
            self.set_base_building()  # nastaví novou základnu odpovídající fázi
            return True
        return False
