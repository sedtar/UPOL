import time
from bakalarska_prace.objects.character_logic import CharacterLogic
from bakalarska_prace.settings.globals import ANT_WIDTH, MARGIN, SCREENWIDTH, COOLDOWN_SEC
from bakalarska_prace.ui.player_ui_graphics import PlayerUIGraphics
from bakalarska_prace.objects.button import Button
from bakalarska_prace.utils.textures import load_character_textures


class PlayerUI:
    """Řídí logiku a interaktivní čáti hráčského UI - tlačítka, fáze, akce"""

    def __init__(self, screen, player, scene):
        self.player = player
        self.screen = screen
        self.textures = load_character_textures()
        self.graphics = PlayerUIGraphics(screen, player)
        self.margin_button = 0
        self.player = player
        self.scene = scene
        self.upgraded = False
        self.last_purchase_time = 0  # cas posledniho nakupu
        self._create_buttons()

    def _create_buttons(self):
        """Vytvoří tlačítka pro jednotlivé jendotky a vylepseni do dalsi faze a přiřadí jím
            příslušné akce.
        """
        for name in self.player.phase.group_of_animals():
            self.margin_button += ANT_WIDTH + MARGIN
            _, _, price, _ = CharacterLogic.initialize_attributes(name)

            # tlacitko pro kazdou jednotku
            Button(self.graphics.animal_buttons,
                   self.textures[name], ((SCREENWIDTH // 2) + self.margin_button, 0),
                   lambda n=name: self.buy_button_action(n),
                   f"Add unit {name}  ({price} coins)",
                   filled=True)

        self.margin_button += ANT_WIDTH + MARGIN

        if not self.player.phase.name == "reptiles":
            # tlacitko pro upgrade do dsalsi faze
            Button(self.graphics.item_buttons, self.textures["star"],
                   ((SCREENWIDTH // 2) + self.margin_button, 0),
                   self.upgrade_button_action,
                   "Upgrade to the next stage\n(" + str(self.player.phase.coin_cost) + " coins and " +
                   str(self.player.phase.exp_cost) + "xp)",
                   filled=True)
        else:
            self.graphics.item_buttons.empty()

    def buy_button_action(self, name):
        """Akce pro tlačítko pro koupi postavy. Pokud je herní režim multiplayer, tj. má atribut action_manager, uloži
        se tato infromace o koupi postavy do slovníku.
        :param name: typ (název) postavy - např. mravenec, beruška
        """
        current_time = time.time()
        if current_time - self.last_purchase_time >= 2:  # kontrola intervalu
            self.player.add_hero(name)
            self.last_purchase_time = current_time
            if hasattr(self.scene, "action_manager"):
                self.scene.action_manager.buy(name)

    def upgrade_button_action(self):
        """
        Akce pro tlačítko pro vylepšení do další fáze. Pokud je herní režim multiplayer, tj. má atribut action_manager,
         uloži se tato infromace o vylepšení do další fáze do slovníku.

        """
        if self.player.upgrade_phase():
            self.graphics.animal_buttons.empty()
            self.graphics.item_buttons.empty()
            self.margin_button = 0
            self._create_buttons()
            self.upgraded = True
            if hasattr(self.scene, "action_manager"):
                self.scene.action_manager.upgrade()

    def calculate_cooldown_ratio(self):
        """Vrátí poměr zbývajícího cooldownu mezi 0 a 1."""
        current_time = time.time()
        cooldown_duration = COOLDOWN_SEC

        if current_time - self.last_purchase_time < cooldown_duration:
            ratio = (current_time - self.last_purchase_time) / cooldown_duration
            return ratio
        return 0

    def update(self):
        """
        Aktualizuje jednotlivé prvky uživatelského rozhraní, včetně textů mincí a zkušeností..

        Zpracovává akce při najetí myší na tlačítka a zobrazuje popisy tlačítek.
        """
        self.graphics.coin_text.update_text(str(self.player.coin_amount))
        self.graphics.exp_value.update_text(str(self.player.exp))

        for button in self.graphics.animal_buttons:
            if button.check_mouse_hover():
                self.graphics.button_text(button)
            cooldown_ratio = self.calculate_cooldown_ratio()
            if cooldown_ratio > 0:
                self.graphics.draw_cooldown_bar(button, cooldown_ratio)

        for button in self.graphics.item_buttons:
            if button.check_mouse_hover():
                self.graphics.button_text(button)
