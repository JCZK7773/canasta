import os
import pygame
import deck
import game
import locations
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Card(pygame.sprite.DirtySprite): # ****
    def __init__(self, rank, suit): # ****
        # Below Section - Non-parent class attributes.
        self.rank = rank # ****
        self.suit = suit # ****
        self.prior_x = None
        self.prior_y = None
        # -------------------------------------
        # Below Line - Initializes pygame.sprite.DirtySprite parent class.
        super().__init__()
        # -------------------------------------
        # Below Section - Parent class attributes.
        # Below Line - The card's x-coordinate location (internal reference only as this ultimately becomes self.x via calculated property (for the purpose of updating self.rect.center when set)).
        self._x = locations.Locate.deck_loc[0]
        # Below Line - The card's y-coordinate location. (internal reference only as this ultimately becomes self.y via calculated property (for the purpose of updating self.rect.center when set)).
        self._y = locations.Locate.deck_loc[1]
        # -------------------------------------
        # Below Line - Internal form of display_layer (which is a calculated property below) for editing the card's visual layer via the change_layer() pygame function.
        self._display_layer = 0
        # Below Line - To be used in some instances whenever the display_layer of a card is going to be changed but the (x, y) coordinate is not going to be changed; used as a reference to it's prior value to determine if it is ==, or has been altered. (Used specifically in locations.py)
        self.changed_display_layer = 0
    # -------------------------------------
    def __str__(self): # ****
        return f"{self.rank}{deck.Deck().suits_symbols.get(self.suit)}" # ****

    def __repr__(self): # ****
        return self.__str__() # ****
    # -------------------------------------
    # Below Section - x functions as the card's x-coordinate. Changed it to be this way so that self.rect.center is updated every time x or y coordinate is updated.
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val
        self.rect.center = [self._x, self._y]
    # -------------------------------------
    # Below Section - y functions as the card's y-coordinate. Changed it to be this way so that self.rect.center is updated every time x or y coordinate is updated.
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val
        self.rect.center = [self._x, self._y]
    # -------------------------------------
    # Below Section - For assigning display layer when appending cards to different card groups for proper visuals.
    @property
    def display_layer(self):
        return self._display_layer

    @display_layer.setter
    def display_layer(self, val):
        self._display_layer = val
        game.game.card_group.change_layer(self, val)
    # -------------------------------------
    # Below Section - Modifies the built-in pygame update function for Dirty Sprites, automatically updating the self.dirty value to 1.
    def update(self):
        if [self.x, self.y] != [self.prior_x, self.prior_y] or self.changed_display_layer == 1:
            self.dirty = 1
        self.prior_x, self.prior_y = self.x, self.y
    # -------------------------------------
    # Below Function - Assigns each Card instance an image & associated card.rect based on c ard.name via comparison with image .png names. Assigns each card to its associated .png as the Card.image.
    def assign_card_images_and_rects(card):
        with os.scandir(os.path.join('assets\8_bit_cards')) as asset_path:
            for entry in asset_path:
                entry_str = (str(entry))
                if card.rank.lower() in entry_str:
                    if card.rank != 'Joker':
                        if card.suit.lower() in entry_str:
                            card.image = pygame.transform.scale(pygame.image.load(entry), (100, 140)).convert()
                            card.rect = card.image.get_rect()
                            card.rect.center = locations.Locate.deck_loc
                    else:
                        card.image = pygame.transform.scale(pygame.image.load(entry), (100, 140)).convert()
                        card.rect = card.image.get_rect()
                        card.rect.center = locations.Locate.deck_loc
