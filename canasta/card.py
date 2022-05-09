import os
import pygame
import deck
import game
import locations
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Card(pygame.sprite.DirtySprite): # ****
    # Below Line - Assigns the face-down 'card backing' file. To be used as the card.image whenever cards are populated into the deck.
    face_down_image_file = os.path.join('assets\8_bit_cards\card back red.png')
    # -------------------------------------
    def __init__(self, rank, suit): # ****
        super().__init__()
        self.rank = rank # ****
        self.suit = suit # ****
        # -------------------------------------
        # Below Line - The card's x-coordinate location (internal reference only as this ultimately becomes self.x via calculated property (for the purpose of updating self.rect.center when set)).
        self._x = locations.Locate.deck_loc[0]
        # Below Line - The card's y-coordinate location. (internal reference only as this ultimately becomes self.y via calculated property (for the purpose of updating self.rect.center when set)).
        self._y = locations.Locate.deck_loc[1]
        # -------------------------------------
        self.prior_x = 0
        self.prior_y = 0
        # -------------------------------------
    # Below Section - Image section.
        # Below Line - Assigned through self.assign_face_down_image() wherever pygame.display, which is required, is initiated. The converted image file for the face-down card backing (red colored) to be assigned as the card's face_down_image.
        self.face_down_image = None
        # Below Line - Assigned through assign_card_images_and_rects(); is the face-up version of each card, as opposed to the face-down version that will be used whenever the card is placed in the deck.
        self.face_up_image = None
        # -------------------------------------
    # Below Section - Highlighting section
        # Below Line - Type: bool. The internal variable used in the self.highlighted calculated property used to determine whether or not game.Game will detect the variable as T/F and highlight the card, or not, accordingly.
        self._highlighted = False
        # Below Line - The yellow highlighted color used for highlighting cards' perimeters.
        self.yellow_highlight_color = (242, 255, 0)
    # -------------------------------------
    # Below Section - Layer section
        # Below Line - Internal form of display_layer (which is a calculated property below) for editing the card's visual layer via the change_layer() pygame function.
        self._display_layer = 0
        # Below Line - To be used in some instances whenever the display_layer of a card is going to be changed but the (x, y) coordinate is not going to be changed; used as a reference to it's prior value to determine if it is ==, or has been altered. (Used specifically in locations.py)
        self.changed_display_layer = 0
    ## -------------------------------------
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
        if [int(self.x), int(self.y)] != [int(self.prior_x), int(self.prior_y)] or self.changed_display_layer == 1:
            self.dirty = 1
        self.prior_x, self.prior_y = self.x, self.y
    # -------------------------------------
    # Below Function - The highlighting rect that will go around cards and melds that, during gameplay, are up for being chosen from an array of options. This will be active or inactive for each card dependent upon the card's status.
    def draw_highlight_rect(self):
        pygame.draw.rect(game.game.screen_surface, self.yellow_highlight_color, self.rect, 2)
    # -------------------------------------
    # Below Function - Calculated property which is either set to True or False. If True, assigns the card's image to include a highlighted perimeter which functions to notify the user that the card is eligible for being clicked.
    @property
    def highlighted(self):
        return self._highlighted
    ###### Below Section - Needs to be completed...
    @highlighted.setter
    def highlighted(self, val):
        self._highlighted = val
        if val == True:
            self.draw_highlight_rect()
    ###### -------------------------------------
    # Below Function - Loads the Card class's face_down_image (one time, instead of many, as it is used for all cards). Called by canasta_pygame.setup() because it requires pygame.display to be initialized. Must be run before assign_card_images_and_rects() because it looks for this to be the card's initial image. Also assigns to card.face_down_image.
    def assign_face_down_image():
        Card.face_down_image = pygame.transform.scale(pygame.image.load(Card.face_down_image_file), (100, 140)).convert()
    # -------------------------------------
    # Below Function - Assigns each Card instance an image & associated card.rect based on card.name via comparison with image .png names. Assigns each card to its associated .png as the Card.image.
    def assign_card_images_and_rects(card):
        with os.scandir(os.path.join('assets\hi_res_cards')) as asset_path:
            for entry in asset_path:
                entry_str = (str(entry))
                if card.rank.lower() in entry_str:
                    if card.rank != 'Joker':
                        if card.suit.lower() in entry_str:
                            card.face_up_image = pygame.transform.scale(pygame.image.load(entry), (100, 140)).convert()
                            card.image = Card.face_down_image
                            card.rect = card.image.get_rect()
                            card.rect.center = locations.Locate.deck_loc
                    else:
                        card.face_up_image = pygame.transform.scale(pygame.image.load(entry), (100, 140)).convert()
                        card.image = Card.face_down_image
                        card.rect = card.image.get_rect()
                        card.rect.center = locations.Locate.deck_loc
    # -------------------------------------
