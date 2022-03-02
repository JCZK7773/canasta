import os
import pygame
import deck
import game
import locations
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Card(pygame.sprite.DirtySprite): # ****
    def __init__(self, rank, suit): # ****
        self.rank = rank # ****
        self.suit = suit # ****
        super().__init__()
    # -------------------------------------
        # Below Line - The card's x-coordinate location (internal reference only as this ultimately becomes self.x via calculated property (for the purpose of updating self.rect.center when set)).
        self._x = locations.Locate.deck_location[0]
        # Below Line - The card's y-coordinate location.
        self._y = locations.Locate.deck_location[1]
    # -------------------------------------
        # Below Line - Internal form of display_layer for editing the card's visual layer via the change_layer() pygame function.
        self._display_layer = 0
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
    # Below Line - For assigning display layer when appending cards to different card groups for proper visuals.
    @property
    def display_layer(self):
        return self._display_layer

    @display_layer.setter
    def display_layer(self, val):
        val = self._display_layer
        game.game.card_group.change_layer(self, val)
    # -------------------------------------
    # Below Section - Modifies the built-in pygame update function for Dirty Sprites, automatically updating the self.dirty value to 1.
    def update(self):
        self.dirty = 1
    # -------------------------------------
    # Below Function - Assigns each Card instance an image & associated card.rect based on c ard.name via comparison with image .png names. Assigns each card to its associated .png as the Card.image.
    def assign_card_images_and_rects(card):
        with os.scandir(os.path.join('Assets')) as asset_path:
            for entry in asset_path:
                entry_str = (str(entry))
                if card.rank.lower() in entry_str:
                    if card.rank != 'Joker':
                        if card.suit.lower() in entry_str:
                            card.image = pygame.transform.scale(pygame.image.load(entry), (100, 140)).convert()
                            card.rect = card.image.get_rect()
                            card.rect.center = locations.Locate.deck_location
                    else:
                        card.image = pygame.transform.scale(pygame.image.load(entry), (100, 140)).convert()
                        card.rect = card.image.get_rect()
                        card.rect.center = locations.Locate.deck_location
