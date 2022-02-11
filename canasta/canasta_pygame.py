# D E B U G
    # Error code goes here in this section; for debugging.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# N O T E S #
    # ...
    # TO BE PASTED TO DEVLOG - 02/??/22 - 02/??/22 - Completed implementation of card movement system by creating various methods, each associated with one of the various card lists, inside of the Locate instance which are to be called by CustomAppendList whenever they are appended to. Needs to be tested to work out bugs.
    # 02/08/22 - Began conversion of text-based inputs to be text display rects on the game screen.

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  T H I N G S  T O  D O  #
    # Have to fix func_dict in a way that allows for proper function calling. As it is, the functions being a method do not work because the dict calls them as if they are an attribute, and the attribute does not exist. I could change the methods to be calculated properties? Or I could make it so that the dictionary is actually a list of tuples?? But then I'm not sure how to pass the card item to the function....USE GETATTR? https://stackoverflow.com/questions/26663032/calling-python-dictionary-of-function-from-class
    # 1) Convert inputs to text rects on display.
    # 2) Test implemented card movement system.
    # 2) Post on web so others can check for bugs as well.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import sys # ****
import logging # ****
import random # ****
import copy
import pygame
import os
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - For the purpose of testing. Is used to store the cards passed through sorted_and_numbered_list_printer so that they can be tested to ensure they are in the proper ascending order according to card rank/suit combination value.
testing_register_list = []
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Logger setup. # ****
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s" # ****
logging.basicConfig(filename = "J:\\Programming\\Projects\\Canasta\\canasta\\Canasta_log.log", level = logging.DEBUG, format = LOG_FORMAT, filemode = 'a') # ****
logger = logging.getLogger() # ****
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Card(pygame.sprite.Sprite): # ****
    def __init__(self, rank, suit): # ****
        self.rank = rank # ****
        self.suit = suit # ****
        super().__init__()
        # Below Line - Assigned via matching .png image file name with card.rank & card.suit via self. assign_card_images_and_rects.
        self.image = None
        # Below Line - The card's x-coordinate location (internal reference only as this ultimately becomes self.x via calculated property (for the purpose of updating self.rect.center when set)).
        self._x = 50
        # Below Line - The card's y-coordinate location.
        self._y = 70
        # Below Line - Assigned when self.image is assigned via self.assign_card_images_and_rects.
        self.rect = None
    # -------------------------------------
    def __str__(self): # ****
        return f"{self.rank}{Deck().suits_symbols.get(self.suit)}" # ****

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
        self.rect.center = [val, self._y]
    # -------------------------------------
    # Below Section - y functions as the card's y-coordinate. Changed it to be this way so that self.rect.center is updated every time x or y coordinate is updated.
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val
        self.rect.center = [self._x, val]
    # -------------------------------------
    # Below Function - Assigns each Card instance an image & associated card.rect based on c ard.name via comparison with image .png names. Assigns each card to its associated .png as the Card.image.
    def assign_card_images_and_rects():
        for card in MasterDeck.deck:
            with os.scandir(os.path.join('Assets')) as asset_path:
                for entry in asset_path:
                    entry_str = (str(entry))
                    if card.rank.lower() in entry_str:
                        if card.rank != 'Joker':
                            if card.suit.lower() in entry_str:
                                card.image = pygame.transform.scale(pygame.image.load(entry), (100, 140))
                                card.rect = card.image.get_rect()
                        else:
                            card.image = pygame.transform.scale(pygame.image.load(entry), (100, 140))
                            card.rect = card.image.get_rect()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Locations():
    def __init__(self):
        self.deck_location = [910, 540]
        self.discard_pile_location = [1010, 540]
        self.p1_hand_start_location = [100, 420]
        self.p2_hand_start_location = [1110, 420]
        self.p1_melds_start_location = [100, 800]
        self.p2_melds_start_location = [1110, 800]
        self.p1_play_cards_start_location = [100, 610]
        self.p2_play_cards_location = [1110, 610]
        self.top_left_visible = [50, 70]
        self.center = [1010, 610]
        self.card_width_height = [100, 140]
        self.text_rect_center = [self.center[0], 300] # Calculate y-coordinate based on rect size? So that if it is a larger text box, it still shows all of the text as opposed to text being off of the screen. ???
    # -------------------------------------
        # Below Function - Dynamically assigns P1's red_3_meld_location.
        @property
        def p1_red_3_meld_location():
            return ((len(p1.melds) + 1) * (self.card_width_height[0] + 20))
        # -------------------------------------
        # Below Function - Dynamically assigns P2's red_3_meld_location.
        @property
        def p2_red_3_meld_location():
            return ((len(p2.melds) + 1) * (self.card_width_height[0] + 20))
        # -------------------------------------
        # Below Function - Dynamically assigns P1's hand location.
        @property
        def p1_hand_next_location():
            if len(P1.hand) == 0:
                return self.p1_hand_start_location
            else:
                x_val_increase = len(P1.hand) * 20
                p1_hand_next_location = [self.p1_hand_start_location[0] + x_val_increase, self.p1_hand_start_location[1]]
                return p1_hand_next_location
        # -------------------------------------
        # Below Function - Dynamically assigns P2's hand location.
        @property
        def p2_hand_next_location():
            if len(P2.hand) == 0:
                return self.p2_hand_start_location
            else:
                x_val_increase = len(P2.hand) * 20
                p2_hand_next_location = [self.p2_hand_start_location[0] + x_val_increase, self.p2_hand_start_location[1]]
                return p2_hand_next_location
        # -------------------------------------
        # Below Function - Dynamically
        def card_movement(loc):
            if card.x < Locate.loc[0]:
                x_difference = Locate.loc[0] - card.x
                x_lesser = True
            elif card.x > Locate.loc[0]:
                x_difference = card.x - Locate.loc[0]
                x_lesser = False
            if card.y < Locate.loc[1]:
                y_difference = Locate.loc[1] - card.y
                y_lesser = True
            elif card.y > Locate.loc[1]:
                y_difference = card.y - Locate.loc[1]
                y_lesser = False
            if x_difference > y_difference:
                ratio = y_difference / x_difference
                while [card.x, card.y] != Locate.loc:
                    if x_lesser == True:
                        card.x += 1
                    else:
                        card_x -= 1
                    if y_lesser == True:
                        card.y += ratio
                    else:
                        card_y -= ratio
            elif y_difference > x_difference:
                ratio = x_difference / y_difference
                while [card.x, card.y] != Locate.loc:
                    if x_lesser == True:
                        card.x += ratio
                    else:
                        card_x -= ratio
                    if y_lesser == True:
                        card.y += 1
                    else:
                        card_y -= 1
        # -------------------------------------
        # Below Function - ...
        def visual_deck_update(card):
            card_movement(self.deck_location)
        # -------------------------------------
        # Below Function - ...
        def visual_discard_pile_update(card):
            card_movement(self.discard_pile_location)
        # -------------------------------------
        # Below Function - ...
        def visual_p1_hand_update(card):
            card_movement(self.p1_hand_next_location)
        # -------------------------------------
        # Below Function - ...
        def visual_p2_hand_update(card):
            card_movement(self.p2_hand_next_location)
        # -------------------------------------
        # Below Function - ...
        def visual_p1_play_cards_update(item):
            if type(item) == list:
                meld_num = len(p1.play_cards)
                card_num = 0
                for card in item:
                    x_val_increase = meld_num * (self.card_width_height[0] + 20)
                    y_val_increase = card_num * 20
                    p1_play_cards_next_location = [self.p1_play_cards_start_location[0] + x_val_increase, self.p1_play_cards_start_location[1] + y_val_increase]
                    card_movement(p1_play_cards_next_location)
                    card_num += 1
            elif type(item) == Card:
                meld_num = len(p1.play_cards)
                card_num = 0
                x_val_increase = meld_num * (self.card_width_height[0] + 20)
                y_val_increase = card_num * 20
                p1_play_cards_next_location = [self.p1_play_cards_start_location[0] + x_val_increase, self.p1_play_cards_start_location[1] + y_val_increase]
                card_movement(p1_play_cards_next_location)
                card_num += 1
        # -------------------------------------
        # Below Function - ...
        def visual_p2_play_cards_update(item):
            if type(item) == list:
                meld_num = len(p2.play_cards)
                card_num = 0
                for card in item:
                    x_val_increase = meld_num * (self.card_width_height[0] + 20)
                    y_val_increase = card_num * 20
                    p2_play_cards_next_location = [self.p2_play_cards_start_location[0] + x_val_increase, self.p2_play_cards_start_location[1] + y_val_increase]
                    card_movement(p2_play_cards_next_location)
                    card_num += 1
            elif type(item) == Card:
                meld_num = len(p2.play_cards)
                card_num = 0
                x_val_increase = meld_num * (self.card_width_height[0] + 20)
                y_val_increase = card_num * 20
                p2_play_cards_next_location = [self.p2_play_cards_start_location[0] + x_val_increase, self.p2_play_cards_start_location[1] + y_val_increase]
                card_movement(p2_play_cards_next_location)
                card_num += 1
        # -------------------------------------
        # Below Function - ...
        def visual_p1_melds_update(item):
            meld_num = len(p1.play_cards)
            card_num = 0
            for card in item:
                x_val_increase = meld_num * (self.card_width_height[0] + 20)
                y_val_increase = card_num * 20
                p1_play_cards_next_location = [self.p1_play_cards_start_location[0] + x_val_increase, self.p1_play_cards_start_location[1] + y_val_increase]
                card_movement(p1_play_cards_next_location)
                card_num += 1
        # -------------------------------------
        # Below Function - ...
        def visual_p2_melds_update(item):
            meld_num = len(p2.play_cards)
            card_num = 0
            for card in item:
                x_val_increase = meld_num * (self.card_width_height[0] + 20)
                y_val_increase = card_num * 20
                p2_play_cards_next_location = [self.p2_play_cards_start_location[0] + x_val_increase, self.p2_play_cards_start_location[1] + y_val_increase]
                card_movement(p2_play_cards_next_location)
                card_num += 1
        # -------------------------------------
        # Below Function - ...
        def visual_p1_red_3_meld_update(card):
            y_val_increase = len(P1.red_3_meld) * 20
            red_3_meld_next_location = [self.p1_red_3_meld_location[0], self.p1_red_3_meld_location[1] + y_val_increase]
            card_movement(red_3_meld_next_location)
        # -------------------------------------
        # Below Function - ...
        def visual_p2_red_3_meld_update(card):
            y_val_increase = len(P2.red_3_meld) * 20
            red_3_meld_next_location = [self.p2_red_3_meld_location[0], self.p2_red_3_meld_location[1] + y_val_increase]
            card_movement(red_3_meld_next_location)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Locate = Locations()
# Below Line - ...
Locations.func_dict = {'deck': Locate.visual_deck_update, 'discard_pile': 'Locate().visual_discard_pile_update', 'p1_hand': 'Locations.visual_p1_hand_update', 'p2_hand': 'Locations.visual_p2_hand_update', 'p1_play_cards': 'Locations.visual_p1_play_cards_update', 'p2_play_cards': 'Locations.visual_p2_play_cards_update', 'p1_melds': 'Locations.visual_p1_melds_update', 'p2_melds': 'Locations.visual_p2_melds_update', 'p1_red_3_meld': 'Locations.visual_p1_red_3_meld_update', 'p2_red_3_meld': 'Locations.visual_p2_red_3_meld_update'}
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Class - Customized list class which is used to call a particular function whenever the sub-classed list .append method is called, for the purpose of visually updating card locations by updating the card coordinate via the function call.
class CustomAppendList(list):
    def __init__(self, name):
        self.name = name
    # -------------------------------------
    def append(self, item):
        Locations.func_dict[(self.name)](item)
        # Locate.func_dict[exec(self.name)](item) # Haven't tested this yet. May have to move execute to be before func_dict...so that it is called on the returned item.
        super(CustomAppendList, self).append(item)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Deck(): # ****
    def __init__(self): # ****
        self.deck = CustomAppendList('deck') # ****
        self.original_deck = [] # ****
        self.draw_ranks = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}
        self.draw_suit_ranks = {'Joker': 0, 'Club': 1, 'Diamond': 2, 'Heart': 3, 'Spade': 4} # ****
        self.ranks = {'Joker':50, '2':20, '3':100, '4':5, '5':5, '6':5, '7':5, '8':10, '9':10, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':20}
        self.suits = ['Club', 'Diamond', 'Heart', 'Spade'] # ****
        self.suits_symbols = {'Heart': '♥', 'Diamond': '♦', 'Spade': '♠', 'Club': '♣', 'Joker': '🃟'} # ****
        self.discard_pile = CustomAppendList('discard_pile')
        self.red_3s = [('3', 'Diamond'), ('3', 'Heart')] # ****
        self.black_3s = [('3', 'Club'), ('3', 'Spade')] # ****
        self.wild_cards = [('2', 'Diamond'), ('2', 'Heart'), ('2', 'Spade'), ('2', 'Club'), ('Joker', 'Joker')] # ****
    # -------------------------------------
    @property # ****
    def face_up_discard(self): # ****
        return self.discard_pile[-1] # ****
    # -------------------------------------
    @property # ****
    def discard_pile_is_frozen(self): # ****
        discard_pile_is_frozen = False
        for card in MasterDeck.discard_pile: # ****
            if (card.rank, card.suit) in MasterDeck.wild_cards or (card.rank, card.suit) in MasterDeck.black_3s : # ****
                discard_pile_is_frozen = True # ****
        return discard_pile_is_frozen # ****
    # -------------------------------------
    def create_deck(self): # ****
        for rank in self.ranks: # ****
            if rank != 'Joker': # ****
                for suit in self.suits: # ****
                    card = Card(rank, suit) # ****
                    self.deck.append(card) # ****
            else: # ****
                for Joker in range(2): # ****
                    card = Card(rank, 'Joker') # ****
                    self.deck.append(card) # ****
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Creates the MasterDeck & Deck2 instances so that the can later be combined into the one MasterDeck. # ****
MasterDeck = Deck() # ****
Deck2 = Deck() # ****
# -------------------------------------
# Below Section - Creates the actual decks via class method create_deck.
MasterDeck.create_deck() # ****
Deck2.create_deck() # ****
# -------------------------------------
# Below Section - Appends Deck2.deck to the MasterDeck.deck to create the required doubledeck.
for card in Deck2.deck: # ****
    MasterDeck.deck.append(card) # ****
# -------------------------------------
# Below Section - Shuffles the MasterDeck & assigns MasterDeck.original_deck == the newly created doubledeck MasterDeck.deck.
random.shuffle(MasterDeck.deck) # ****
MasterDeck.original_deck = copy.copy(MasterDeck.deck[:])
# -------------------------------------
# Below Line - Calls card.assign_card_images_and_rects to set up each card to have an associated sprite that is ready for display.
Card.assign_card_images_and_rects()
# -------------------------------------
# Below Section - Creates the card_group Sprite Group and appends each card from the deck into the group so that the entire group location can be updated with only one line instead of coding movement updates of each card inidividually.
card_group = pygame.sprite.Group()
for card in MasterDeck.deck:
    card_group.add(card)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Player(): # ****
    def __init__(self, name): # ****
        self.name = name # ****
        self.the_draw = None # ****
        self.hand = [] # ****
        self.play_cards = [] # ****
        self.play_cards_wild_cards = [] # ****
        self.initial_played_cards = [] # ****
        self.final_played_cards = 0
        self.last_set_played_cards = [] # ****
        self.red_3_meld = [] # ****
        self.black_3_meld = [] # ****
        self.melds = [] # ****
        self.len_2_temp_melds_list = [] # ****
        self.matched_card_list = []
        self.going_out = None # ****
        self.went_out_concealed = False # ****
        self.finished_rounds_scores = [] # ****
        self.total_score_over_5000 = False
        self.special_case_cant_draw = False
    # -------------------------------------
    @property # ****
    def draw_card(self): # ****
        draw_card = self.hand[0] # ****
        return draw_card # ****
    # -------------------------------------
    @property # ****
    def draw_card_val(self): # ****
        return MasterDeck.draw_ranks.get(self.draw_card.rank) # ****
    # ------------------------------------------
    @property # ****
    def meld_requirement(self): # ****
        meld_requirement = 0 # ****
        if self.total_score < 0: # ****
            meld_requirement = 15 # ****
        elif 0 <= self.total_score < 1500: # ****
            meld_requirement = 50 # ****
        elif 1500 <= self.total_score < 3000: # ****
            meld_requirement = 90 # ****
        elif self.total_score >= 3000: # ****
            meld_requirement = 120 # ****
        return meld_requirement # ****
    # ------------------------------------------
    @property # ****
    def red_3_count(self): # ****
        return len(self.red_3_meld) # ****
    # -------------------------------------
    @property # ****
    def hand_wild_cards_reference_list(self): # ****
        hand_wild_cards = [] # ****
        for card in self.hand: # ****
            if (card.rank, card.suit) in Deck().wild_cards: # ****
                hand_wild_cards.append(card) # ****
        return hand_wild_cards # ****
    # -------------------------------------
    @property # ****
    def non_maxed_out_melds(self): # ****
        non_maxed_out_melds = [] # ****
        # -------------------------------------
        for meld_group in [self.play_cards, self.melds]: # ****
            for item in meld_group: # ****
                if type(item) == list: # ****
                    wild_card_count = 0 # ****
                    for card in item: # ****
                        if (card.rank, card.suit) in Deck().wild_cards: # ****
                            wild_card_count += 1 # ****
                    if 7 <= wild_card_count or wild_card_count < 3: # ****
                        non_maxed_out_melds.append(item) # ****
                        # -------------------------------------
        return non_maxed_out_melds # ****
    # -------------------------------------
    @property # ****
    def has_canasta(self): # ****
        for meld_group in [self.melds, self.play_cards]: # ****
            if len(meld_group) > 0:
                for meld in meld_group:
                    if len(meld) >= 7: # ****
                        return True # ****
    # -------------------------------------
    @property # ****
    def round_score(self): # ****
        round_score = 0 # ****
        # -------------------------------------
        for meld_group in [self.play_cards, self.melds]: # ****
            if len(meld_group) > 0: # ****
                for item in meld_group: # ****
                    wild_card_canasta_check_count = 0 # ****
                    if type(item) == list: # ****
                        for card in item: # ****
                        # -------------------------------------
                            if (card.rank, card.suit) in Deck().wild_cards: # ****
                                wild_card_canasta_check_count += 1 # ****
                            # -------------------------------------
                            round_score += Deck().ranks.get(card.rank) # ****
                        # -------------------------------------
                        if len(item) >= 7: # ****
                            if wild_card_canasta_check_count == 7: # ****
                                round_score += 1000 # ****
                            elif wild_card_canasta_check_count == 0: # ****
                                round_score += 500 # ****
                            elif wild_card_canasta_check_count > 0: # ****
                                round_score += 300 # ****
                        # -------------------------------------
        if self.going_out == True: # ****
            round_score += 100 # ****
            if self.went_out_concealed == True: # ****
                round_score += 100 # ****
            round_score += (self.red_3_count * 100) # ****
            if self.red_3_count == 4: # ****
                round_score += 400 # ****
                # -------------------------------------
        elif self.going_out == False: # ****
            if self.has_canasta == True: # ****
                round_score += (self.red_3_count * 100) # ****
                if self.red_3_count == 4: # ****
                    round_score += 400 # ****
            else: # ****
                round_score -= (self.red_3_count * 100) # ****
                if self.red_3_count == 4:# ****
                    round_score -= 400 # ****
                    # -------------------------------------
            if len(self.hand) > 0: # ****
                for card in self.hand: # ****
                    round_score -= Deck().ranks.get(card.rank) # ****
                    # -------------------------------------
        return round_score # ****
    # -------------------------------------
    @property # ****
    def total_score(self): # ****
        return sum(self.finished_rounds_scores) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Creates the players, and gives them placeholder names for identification at start of game. # ****
P1 = Player('Player 1') # ****
P2 = Player('Player 2') # ****
# -------------------------------------
# Below Section - Assigns each player's card groups that will be visually displayed on the pygame screen to be an instance of CustomAppendList, giving each a name associated with the card group name to be used for when cards are appended to these card groups. The dictionary func_dict has the names as the keys , and a function name which updates the card coordinates of the appended card group is the dict value, so that whenever a card is appended to one of these groups, through a modified append method, the function is called before the card is appended to the card group, for the purpose of automation and simplicity.
P1.hand = CustomAppendList('p1_hand') # ****
P2.hand = CustomAppendList('p2_hand') # ****
P1.play_cards = CustomAppendList('p1_play_cards') # ****
P2.play_cards = CustomAppendList('p2_play_cards') # ****
P1.red_3_meld = CustomAppendList('p1_red_3_meld') # ****
P2.red_3_meld = CustomAppendList('p2_red_3_meld') # ****
P1.melds = CustomAppendList('p1_melds') # ***
P2.melds = CustomAppendList('p2_melds') # ***
# -------------------------------------
players = [P1, P2] # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Test section to verify proper movement of card-screen locations.
P1.melds.append(MasterDeck.deck[0:7])
P1.melds.append(MasterDeck.deck[8:15])
P1.melds.append(MasterDeck.deck[16:19])
P1.melds.append(MasterDeck.deck[19:23])
# -------------------------------------
# Below Section - Sets up the pygame window size and assigns a title caption for the game window.
screen = pygame.display.set_mode((1920, 1020))
pygame.display.set_caption("Canasta")
# -------------------------------------
# Below Section - ...
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('GeeksForGeeks', True, green, blue)
textRect = text.get_rect()
textRect.center = Locations.text_rect_center
# -------------------------------------
# Below Function - Called by main(). Handles screen background assignment, card_group draw updating, and the pygame.display updates.
def draw_window():
    screen.fill((0,40,0))
    card_group.draw(screen)
    screen.draw(text)
    pygame.display.update()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by module when opened, if __name__ == "__main__". The main pygame loop. Handles FPS, pygame.event handling, and calls draw_window() for screen updating.
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - First Function for run loop. Handles logic for sequencing of the_draw functions for when certain criteria require certain sections to be rerun. # ****
def the_draw_1(player=P1, testing = False): # ****
    logger.debug("the_draw_1\n") # ****
    if player == P1: # ****
        logger.debug("player == P1") # ****
        if testing == True:
            return "player == P1"
        for player in players: # ****
            the_draw_2(player) # ****
        return the_draw_3() # ****
    else: # ****
        logger.debug("player != P1") # ****
        if testing == True:
            return "player == P2"
        the_draw_2(player) # ****
        return the_draw_3() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_1() function. Handles name creation, draw card choice (to determine first player), and ensures that if a Joker is drawn during this process, it is reset and redone (Logic for that handled in draw_joker_check). # ****
def the_draw_2(player, testing = False): # ****
    logger.debug("the_draw_2") # ****
    if player.name == 'Player 1' or player.name == 'Player 2': # ****
        while True: # ****
            try: # ****
                player.name = input(f"\n{player.name}, what is your name? \n\n> ") # ****
                if len(player.name) < 1: # ****
                    raise ValueError # ****
                break # ****
            except ValueError: # ****
                print("\nSorry, but your name must be at least one character long. It looks as if your input was blank.\n") # ****
    while True: # ****
        try: # ****
            player.the_draw = int(input(f"\n{player.name}, Select your card from the stack to determine which player will have the first play. (Pick a card, represented as a number from 1-{len(MasterDeck.deck)})\n\n> ")) # ****
            player.hand.append(MasterDeck.deck.pop(player.the_draw - 1)) # ****
            break # ****
        except (ValueError, IndexError): # ****
            print(f"\nSorry, but there was a problem with your input. Please try again. Make sure that your input is a number between 1-{len(MasterDeck.deck)}.") # ****
    print(f"\n{player.name} drew a {player.draw_card}\n") # ****
    # -------------------------------------
    if testing == True:
        return "draw_joker_check(player)"
    draw_joker_check(player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_2() for Game Loop. Checks a player's draw card to ensure it is not a Joker, and if it is, redirects the process back to the_draw_1, to be redone. # ****
def draw_joker_check(player, testing = False): # ****
    logger.debug("draw_joker_check\n") # ****
    if player.draw_card.rank == 'Joker': # ****
        if testing == True:
            return "player.draw_card.rank == \'Joker\'"
        print(f"Sorry, {player.name}, you picked a Joker, which is not available for use during The Draw! You must choose another card!\n") # ****
        MasterDeck.deck.append(player.hand.pop(0)) # ****
        the_draw_1(player) # ****
    else:
        if testing == True:
            return "player.draw_card.rank != \'Joker\'"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_1() function. Checks whether or not the players have the same draw card, and if they do, redirects the process back to the_draw_1 and places player cards back into the MasterDeck. Also checks to see who wins the draw, and redirects to the_deal() after determination. # ****
def the_draw_3(testing = False): # ****
    logger.debug("the_draw_3\n") # ****
    # ------------------------------------- # ****
    if (P1.draw_card.rank, P1.draw_card.suit) == (P2.draw_card.rank, P2.draw_card.suit): # ****
        if testing == True:
            return "\nYou have the same exact card! You both must pick another card!\n" # ****
        print("\nYou have the same exact card! You both must pick another card!\n") # ****
        # -------------------------------------
        return_draw_card(players) # ****
        return the_draw_1(P1) # ****
    elif P1.draw_card_val > P2.draw_card_val: # ****
        if testing == True:
            return "the_deal(P1,P2)"
        return_draw_card(players) # ****
        return the_deal(P1,P2) # ****
    elif P2.draw_card_val > P1.draw_card_val: # ****
        if testing == True:
            return "the_deal(P2,P1)"
        return_draw_card(players) # ****
        return the_deal(P2,P1) # ****
    elif P1.draw_card_val == P2.draw_card_val: # ****
        if MasterDeck.draw_suit_ranks.get(P1.draw_card.suit) > MasterDeck.draw_suit_ranks.get(P2.draw_card.suit): # ****
            if testing == True:
                return "the_deal(P1,P2)"
            return_draw_card(players) # ****
            return the_deal(P1,P2) # ****
        else: # ****
            if testing == True:
                return "the_deal(P2,P1)"
            return_draw_card(players) # ****
            return the_deal(P2,P1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_3() function. Simple function to return the draw card used to determine first play from player.hand back into MasterDeck.deck(). For purpose of reducing amount of repeated code. # ***
def return_draw_card(players): # ****
    logger.debug("return_draw_card\n") # ****
    for player in players: # ****
        MasterDeck.deck.append(player.hand.pop(0)) # ****
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_3() function. Handles dealing, sorting, printing; red 3 checks each player's cards, creates a discard pile from MasterDeck, and directs to play_1(). # ****
def the_deal(player1, player2): # ****
    logger.debug("the_deal\n") # ****
    # -------------------------------------
    # Below - Deals each player their 11 cards, sorts them, prints them, and checks for Red 3s. # ****
    for player in (player1, player2): # ****
        for card in range(11): # ****
            player.hand.append(MasterDeck.deck.pop(0)) # ****
        print(f"{player.name} is dealt 11 cards. Your hand consists of:\n") # ****
        sorted_and_numbered_list_printer(player.hand) # ****
        red_3_check(player) # ****
    # -------------------------------------
    # Below - Creates the discard pile from the MasterDeck # ****
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(0)) # ****
    # -------------------------------------
    return play_1(player1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by sorted_and_numbered_list_printer(). To be used as a sorter key function which orders the cards in ascending order based on card rank. # ****
def sorter_key_function(item): # ****
    # Below - If item is a Card (not a list or tuple). # ****
    if type(item) != list: # ****
        int_suit = MasterDeck.draw_suit_ranks.get(item.suit)
        if item.rank != 'Joker': # ****
            int_rank = MasterDeck.draw_ranks.get(item.rank) # ****
            final_value = int(str(int_rank) + str(int_suit)) # ****
            return final_value # ****
        else: # ****
            final_value = int(str(1) + str(int_suit)) # ****
            return final_value # ****
    # Below - If item is a meld (list). # ****
    else: # ****
        if item[0].rank != 'Joker': # ****
            int_rank = MasterDeck.draw_ranks.get(item[0].rank) # ****
            return int_rank # ****
        else: # ****
            return int(1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_1(), draw_discard_pile_attempt_temp_meld_wild_card_addition(), play_2(), valid_play_check_and_sort(), wild_card_meld_choice_prompt(), discard(), went_out_check() functions. Miscellaneous function for handling printed lists that I want to be sorted and then numbered; for the purpose of input choice selection via the preceding num. # ****
def sorted_and_numbered_list_printer(passed_list_1, passed_list_2 = None): # ****
    logger.debug("sorted_and_numbered_list_printer\n") # ****
    # -------------------------------------
    passed_list_1.sort(key=sorter_key_function) # ****
    # -------------------------------------
    num = 1 # ****
    for item in passed_list_1: # ****
        # -------------------------------------
        # Below Line - Strictly for the purpose of testing.
        testing_register_list.append(item)
        # -------------------------------------
        if item != passed_list_1[-1]: # ****
            print(f"{num}) {item}") # ****
        else: # ****
            print(f"{num}) {item}\n") # ****
        num += 1 # ****
        # -------------------------------------
    if passed_list_2 != None: # ****
        passed_list_2.sort(key=sorter_key_function) # ****
        for item in passed_list_2: # ****
            if item != passed_list_2[-1]: # ****
                print(f"{num}) {item}") # ****
            else: # ****
                print(f"{num}) {item}\n") # ****
            num += 1 # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Handles initially dealt and drawn Red 3s. Removes them from player.hand, replaces it with a newly drawn card from the deck, and prints associated output. # ****
def red_3_check(player, drawn = False): # ****
    logger.debug("red_3_check\n") # ****
    red_3_quantity = 0 # ****
    # -------------------------------------
    for card in player.hand[:]: # ****
        if (card.rank, card.suit) in Deck().red_3s: # ****
            if drawn == True: # ****
                print(f"{player.name}, you drew a Red 3! The {card} will be placed in your Red 3 meld, and you will automatically draw another card to replace it\n.") # ****
                player.red_3_meld.append(player.hand.pop(-1)) # ****
                player.hand.append(MasterDeck.deck.pop(0)) # ****
                print(f"In place of your Red 3, you drew a: {player.hand[-1]}\n") # ****
                # -------------------------------------
            # Below - Handles initial Red 3 check. Appends red_3_meld to player.melds, replaces it with a new card from MasterDeck.deck, & prints out associated output for initial Red 3 distribution. # ****
            elif drawn == False: # ****
                red_3_quantity += 1 # ****
                player.red_3_meld.append(player.hand.pop(player.hand.index(card))) # ****
                player.hand.append(MasterDeck.deck.pop(0)) # ****
    # -------------------------------------
    if red_3_quantity == 4: # ****
        print(f"Congratulations, {player.name}! You have 4 Red 3s, therefore you get a bonus of 400 points (Granted that when the round ends, you have at least 1 Canasta. Otherwise you will deducted 400 points!)! The rules dictate that all Red 3s must be played down, and you will withdraw a replacement card from the stock for each one!\n") # ****
    elif red_3_quantity > 0: # ****
        print(f"{player.name}, you have {red_3_quantity} Red 3(s) in your hand! The rules dictate that all Red 3s must be played down, and you have to withdraw a replacement card from the stock for each one!\n\n{player.name}, in place of your Red 3(s), you drew a " + ', '.join(['%s']*len(player.red_3_meld)) % tuple(player.hand[-(len(player.red_3_meld)):]) + "\n") # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by went_out_check(), the_deal() functions. Gives the player the option to either draw from the deck or to attempt a draw from the discard pile. Also prints out all preexisting melds for reference as it is important for choosing between the draw options. # ****
def play_1(player): # ****
    logger.debug("play_1\n") # ****
    # -------------------------------------
    while True: # ****
        try: # ****
            draw_method = input(f"{player.name}, which method would you like to use to draw?\n\n1) Draw from Stack\n2) Draw from Discard Pile - The face up discard is {MasterDeck.face_up_discard}.\n\n> ") # ****
            if draw_method not in ('1', '2'): # ****
                raise ValueError # ****
            break # ****
        except ValueError: # ****
            print("\nSorry, but there was a problem with your input. Please try again. Make sure to enter either '1' or '2' as your input.\n") # ****
    if len(player.melds) > 0: # ****
        print("\nYour current melds are as follows.\n") # ****
        sorted_and_numbered_list_printer(player.melds) # ****
    if draw_method == '1': # ****
        stock_draw(player) # ****
    else: # ****
        draw_discard_pile_attempt(player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_1(), draw_discard_pile_attempt_check_meld_match(), draw_discard_pile_attempt_check_hand_match(), replace_discard_pile_temp_meld() functions. For drawing a card from the stock & giving associated output. If stock is empty, redirects to draw_discard_pile_attempt(). # ****
def stock_draw(player, from_draw_discard_pile_attempt_no_canasta_fail = False): # ****
    logger.debug("stock_draw\n") # ****
    # -------------------------------------
    if len(MasterDeck.deck) > 0: # ****
        player.hand.append(MasterDeck.deck.pop(0)) # ****
        print(f"{player.name} drew a {player.hand[-1]} from the stack.\n") # ****
        red_3_check(player) # ****
        play_2(player) # ****
    else: # ****
        if from_draw_discard_pile_attempt_no_canasta_fail == False:
            print("There are no cards left in the stock pile. If you have a meld that matches the rank of the face up discard, you are required to draw the discard pile's face up discard (or the entire discard pile), per the rules. This rule will continue until no player has a matching meld for the face up discard; at that point the round will end.\n") # ****
            draw_discard_pile_attempt(player, True) # ****
        else:
            print("It looks as if there are no cards in the stock pile for you to draw from, and since you cannot draw from the discard pile, your turn is forfeited and the opposing player will be allowed a chance at playing.\n")
            if player == P1:
                return play_1(P2)
            else:
                return play_1(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_1(), stock_draw() functions. For attempting to draw the discard pile. If the stock_depleted parameter is true, checks to see if the discard pile is depleted; if not, checks for a matching meld for the face up discard, but if so, ends the round per the rules. # ****
def draw_discard_pile_attempt(player, stock_depleted = False): # ****
    logger.debug("\ndraw_discard_pile_attempt\n") # ****
    # -------------------------------------
    # Below Section - Checks to see if the player can draw the discard pile in the case that the stock_depleted parameter is True. If so, attempts to draw the discard pile. If there is a matching meld, successfully draws the discard pile. If not, the round ends, per the rules. # ****
    if stock_depleted == True: # ****
        if len(MasterDeck.discard_pile) == 0: # ****
            print("It looks as if the discard pile is depleted as well. Per the rules, this means the round is ended since there is no means by which you can draw another card.") # ****
            return round_reset() # ****
    # -------------------------------------
    # Below Section - In the case that a player attempts to draw the discard pile whenever the face up discard is a Wild Card or a Black 3. Outputs an informative prompt and returns stock_draw(), unless the stock_depleted == True, in which case round_reset() is called because there is no means by which anybody can draw a card.
    if (MasterDeck.face_up_discard.rank, MasterDeck.face_up_discard.suit) in MasterDeck.wild_cards or (MasterDeck.face_up_discard.rank, MasterDeck.face_up_discard.suit) in MasterDeck.black_3s:
        if stock_depleted == False:
            print("\nSorry, but you cannot draw the discard pile whenever the face up discard is a Wild Card or a Black 3. You will instead have to draw from the Stock.\n")
            return stock_draw(player)
        else:
            print("It looks as if the stock is depleted and the discard pile is topically frozen, which means nobody has a means by which to draw a card. Therefore the round is over!\n")
            return round_reset()
    # -------------------------------------
    # Below Section - For discard pile draw attempt when it is not internally or topically frozen. Redirects to eligibility determinations based on player's initial meld status, and finalizes determination by either allowing drawing of the discard pile, or denial and subsequent redirection back to play_1. # ****
    if MasterDeck.discard_pile_is_frozen == False: # ****
        logger.debug("discard_pile_is_frozen == False\n") # ****
        if stock_depleted == True:
            draw_discard_pile_attempt_check_meld_match(player, True) # ****
        else:
            # Below Line - Checks the player's existing melds to see if they have a match for the top discard to be used as a means to withdraw the discard pile. If so, draws the discard pile and creates a meld from the face up discard, and returns True. If not, continues to check the hand for an alternate route to draw the discard pile. # ****
            draw_discard_pile_attempt_check_meld_match(player) # ****
    elif MasterDeck.discard_pile_is_frozen == True: # ****
        logger.debug("discard_pile_is_frozen == True\n") # ****
        print("\nIt looks as if the discard pile is frozen, which means that you cannot pick up the pile using a preexisting meld. You instead have to have matches to the face up discard in your hand, or a match and a Wild Card in certain circumstances.\n")
    # -------------------------------------
    # Below Line - For when the discard_pile_is_frozen is either True or False, and if draw_discard_pile_attempt_check_meld_match did not succeed. Checks the player's hand to see if they have matching cards in their hand (for when they have no melds that match the top discard) as an alternative means to pick up the discard pile. If so, draws the discard pile and creates a meld from the face up discard, and returns True, If not... # ****
    draw_discard_pile_attempt_check_hand_match(player) # ****
    # Below Section - Since the player was unable to draw the discard pile after attempting all of the possible methods, they must instead draw from the stock; calls stock_draw(player), unless the stock is depleted, in which case the player is given the opportunity to make a play via play_2(). In the latter case, player.special_case_cant_draw is changed to = True. If both players have went through this process, meaning both players' .special_case_cant_draw == True, then round_reset() is called as the round is functionally over since nobody can draw a card and both players have had the opportunity to make a final play.
    print("It looks as if you were unable to draw the discard pile after attempting all of the possible methods.\n")
    if stock_depleted == False:
        print("You will draw from the stock instead.\n")
        stock_draw(player)
    else:
        player.special_case_cant_draw = True
        if P1.special_case_cant_draw == True and P2.special_case_cant_draw == True:
            print("Since both players have had a final opportunity to draw a card and have both been unsuccessful, and since both players have had a final opportunity to play their remaining plays, and since the round is functionally gridlocked, the round is over!\n")
            round_reset()
        else:
            print("Since the stock is depleted and you were unable to draw from the discard pile, you will not draw any card, and will instead move to your play, if you have one planned.\n")
            play_2(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt(). Checks player's existing melds to see if they have a meld match for the face up discard, for the purpose of drawing the discard pile. # ****
def draw_discard_pile_attempt_check_meld_match(player, stock_depleted = False): # ****
    logger.debug("draw_discard_pile_attempt_check_meld_match")
    for meld in player.melds: # ****
        if MasterDeck.face_up_discard.rank == meld[0].rank: # ****
            meld.append(MasterDeck.discard_pile.pop(-1)) # ****
            # Below - In the case that the player is trying to draw from the discard pile because the stock is depleted. Per the rules, in this instance, only the face up discard is withdrawn, unless the player chooses otherwise. # ****
            if stock_depleted == True: # ****
                while True: # ****
                    try: # ****
                        draw_rest_of_discard_pile_input = input(f"{player.name}, you successfully withdrew the face up discard from the discard pile, as you had a matching meld! Per the rules, you have the choice to either pick up the entire discard pile, or to take just the face up discard. Would you like to take the rest of the pile as well? (Y/N)\n\n> ") # ****
                        if draw_rest_of_discard_pile_input.lower() not in ('y', 'n'): # ****
                            raise ValueError # ****
                        break # ****
                    except ValueError: # ****
                        print("Sorry, but there was an issue with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n") # ****
                if draw_rest_of_discard_pile_input.lower() == 'n': # ****
                    return play_2(player) # ****
                    # -------------------------------------
            # If draw_rest_of_discard_pile_input was 'Y'. Or if stock_depleted was not True and a face_up_discard match was found. # ****
            return draw_discard_pile(player) # ****
            # -------------------------------------
    # Below - When stock_depleted == True and the player cannot draw the pile because of the above section not detecting a match for the face up discard. # ****
    if stock_depleted == True: # ****
        print(f"{player.name}, unfortunately, you were unable to draw the discard pile because you did not have a matching meld. Therefore, since you have no means to draw a card, the round is over, per the rules.\n") # ****
        round_reset() # ****
        # -------------------------------------
    if len(player.melds) > 0:
        print(f"\nYou were unable to draw the discard pile using a matching meld.\n") # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt(). Checks the player's hand to see if they have a qualifying set of matching cards for the purpose of drawing the discard pile. # ****
def draw_discard_pile_attempt_check_hand_match(player): # ****
    logger.debug("draw_discard_pile_attempt_check_hand_match\n") # ****
    # -------------------------------------
    # Below Line - Clears player.matched_card_list so that whenever it has been previously appended to or modified, it is reset back to an empty list upon the start of this function so as to not mix up cards from previous play attempts.
    player.matched_card_list.clear()
    # Below Section - Checks each card in player.hand[:] to see if there is a match to the face_up_discard. If so, appends that card to player.matched_card_list and pops it from player.hand.
    for card in player.hand[:]: # ****
        if card.rank == MasterDeck.face_up_discard.rank: # ****
            player.matched_card_list.append(player.hand.pop(player.hand.index(card))) # ****
    # -------------------------------------
    if len(player.matched_card_list) == 0: # ****
        print("Sorry, but you did not have any matches to the face up discard.\n")
        return None
    # -------------------------------------
    # Below Section - Copies the player.matched_card_list so as to create a fixed, static rank value, as the variable player_matched_card_list_copy. Next the player_matched_card_list_copy is appended to player.melds, and finally appends the face_up_discard to that meld, popping the cards from their original locations. Also gives an informative prompt and returns None so as not to continue on errantly to remainder of function code. # ****
    else:
        player_matched_card_list_copy = copy.copy(player.matched_card_list)
        player.melds.append(player_matched_card_list_copy) # ****
        player.melds[-1].append(MasterDeck.discard_pile.pop(-1)) # ****
        # Below Section - If the player has 2 natural matches for the face up discard, (plus the face_up_discard in player.melds[-1]). Checks that the player has met meld requirement. If so, draws discard pile successfully. If not, attempts to use additional wild cards within the hand to reach the meld requirement via draw_discard_pile_wild_card_prompt. # ****
        if len(player.melds[-1]) >= 3: # ****
            if player.round_score >= player.meld_requirement: # ****
                if len(player.hand) < 1:
                    if player.has_canasta == True:
                        went_out_check(player, going_out_from_discard_draw = True)
                    else:
                        print("It looks as if you are attempting to go out, but do not have a Canasta, which is against the rules. This means the drawing of the discard pile attempt must be cancelled. All of the cards that would have been used in the meld, along with the face up discard, will be replaced to their proper locations. You will instead have to draw from the stock.")
                        replace_discard_pile_temp_meld(player)
                print("You successfully created a valid meld from the face up discard and met the meld requirements!\n")
                return draw_discard_pile(player) # ****
            else: # ****
                draw_discard_pile_wild_card_prompt(player) # ****
        # -------------------------------------
        # Below Section - If the meld consists of only 1 natural card from the hand and the face up discard; if the discard_pile_is_frozen == True, reroutes the player to replace_discard_pile_temp_meld (which redirects to stock_draw()). If discard_pile_is_frozen == False, checks to see if the player has any wild cards to help them reach the meld length requirement. If so, attempts this via draw_discard_pile_wild_card_prompt(). Otherwise, redirects to replace_discard_pile_temp_meld(). # ****
        elif len(player.melds[-1]) == 2: # ****
            if MasterDeck.discard_pile_is_frozen == True: # ****
                print(f"\nSorry, {player.name}, but you don't have 2 natural cards of the face up discard's rank in your hand, which is required to pick up the discard pile when it is frozen, which it currently is. Therefore you will have to withdraw from the stock pile.\n") # ****
                replace_discard_pile_temp_meld(player)
            elif MasterDeck.discard_pile_is_frozen == False: # ****
                if len(player.hand_wild_cards_reference_list) > 0: # ****
                    draw_discard_pile_wild_card_prompt(player) # ****
                else: # ****
                    print("Sorry, but you only had 1 natural card to match the face up discard's rank, with no wild cards to use to help reach the 3 card minimum for a valid meld. Therefore your meld and the face up discard will be placed back into the hand and discard pile respectively and you will instead have to draw from the stock.\n") # ****
                    replace_discard_pile_temp_meld(player)
        # -------------------------------------
        # Below Section - If the player did not have any matching cards to the face up discard in their hand; redirects player to stock_draw. # ****
        else: # ****
            print("\nYou did not have enough matches to the face up discard in your hand to draw the discard pile using cards in your hand.\n") # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_wild_card_prompt(), draw_discard_pile_attempt_check_meld_match(), draw_discard_pile_attempt_check_hand_match() functions. Pops and appends each card from the discard pile to the player's hand. # ****
def draw_discard_pile(player): # ****
    logger.debug("draw_discard_pile\n") # ****
    # -------------------------------------
    for card in MasterDeck.discard_pile[:]: # ****
        player.hand.append(MasterDeck.discard_pile.pop(-1)) # ****
    print(f"{player.name}, you successfully drew the discard pile!\n") # ****
    red_3_check(player) # ****
    play_2(player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_wild_card_prompt() function. Prompts the player to choose which wild card they would like to use to add to their temp_meld for use in attempting to draw the discard pile. # ****
def draw_discard_pile_attempt_temp_meld_wild_card_addition(player): # ****
    logger.debug("draw_discard_pile_attempt_temp_meld_wild_card_addition")
    print(f"\n{player.name}, which wild card would you like to use? You have these wild cards:\n") # ****
    sorted_and_numbered_list_printer(player.hand_wild_cards_reference_list) # ****
    while True: # ****
        try: # ****
            wild_card_choice = int(input("> ")) # ****
            player.melds[-1].append(player.hand.pop(player.hand.index(player.hand_wild_cards_reference_list[wild_card_choice - 1]))) # ****
            break # ****
        except (ValueError, IndexError): # ****
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is one of the numbers preceding the card you would like to use.\n") # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt_check_meld_match(), draw_discard_pile_attempt_check_hand_match() functions. Prompts the player to choose which wild card they would like to use to help them in withdrawing the discard pile. # ****
def draw_discard_pile_wild_card_prompt(player):
    logger.debug("draw_discard_pile_wild_card_prompt")
    while len(player.hand_wild_cards_reference_list) > 0: # ****
        while True: # ****
            try: # ****
                use_wild_card_input = input(f"\nYour attempted meld using the face up discard did not meet the meld requirement, therefore you would have to add a/some wild card(s) to the meld to see if that would help you to reach the score requirement. It looks as if you have {len(player.hand_wild_cards_reference_list)} wild card(s) to use for this: {player.hand_wild_cards_reference_list} Would you like to do this? (Y/N)\n\n> ") # ****
                if use_wild_card_input.lower() not in ('y', 'n'): # ****
                    raise ValueError # ****
                break # ****
            except ValueError: # ****
                print("\nSorry, but there was a problem with your input. Please try again, making sure that your input is either 'Y' or 'N' (Yes or No).\n") # ****
                # -------------------------------------
        if use_wild_card_input.lower() == 'y': # ****
            draw_discard_pile_attempt_temp_meld_wild_card_addition(player) # ****
            if player.round_score >= player.meld_requirement: # ****
                print("\nYou successfully created a valid meld from the face up discard and met the meld requirements!\n") # ****
                return draw_discard_pile(player) # ****
        else: # ****
            print("Okay, the attempted meld will be placed back into your hand, and the face up discard will be placed back on top of the discard pile. You will also draw from the stock pile instead.\n") # ****
            return replace_discard_pile_temp_meld(player) # ****
            # -------------------------------------
    print("Unfortunately your attempted meld using the face up discard did not meet the meld requirement, and you do not have any wild cards to add to it to help reach the required score. Your attempted meld will be placed back in your hand, and the face up discard will be placed back into the discard pile. You will instead draw from the stock pile.\n") # ****
    return replace_discard_pile_temp_meld(player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_wild_card_prompt() function. Replaces the face up discard back into the discard pile and replaces the matched cards from the player.meld back into the player.hand. # ****
def replace_discard_pile_temp_meld(player): # ****
    logger.debug("replace_discard_pile_temp_meld")
    MasterDeck.discard_pile.append(player.melds[-1].pop(-1)) # ****
    for matched_card in player.matched_card_list[:]: # ****
        player.hand.append(player.melds[-1].pop(-1)) # ****
    player.melds.pop(-1) # ****
    player.matched_card_list.clear()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt_check_meld_match(), stock_draw(), draw_discard_pile(), and valid_play_check_and_sort() functions. Prompts the player to choose between either playing a set of cards or discarding instead. If player chooses to play cards, then the player is prompted to choose a set of cards to play and is then  # ****
def play_2(player): # ****
    logger.debug("play_2\n") # ****
    # -------------------------------------
    # Below Line - For when valid_play_check_and_sort(), etc. functions do not successfully lead to a valid complete play and reroute back here mid-play. Instead of doing this each time an attempt is unsuccessful & redirects back here, it is done here once, for all instances. # ****
    player.play_cards.clear() # ****
    # -------------------------------------
    print(f"{player.name}, it is your turn to play!\n") # ****
    if len(player.melds) > 0: # ****
        print("Your existing melds are as follows:\n") # ****
        sorted_and_numbered_list_printer(player.melds) # ****
    while True: # ****
        try: # ****
            play_choice = input(f"{player.name}, what would you like to do with your turn?\n\n 1) Play Cards\n 2) Discard\n\n> ") # ****
            if play_choice not in ('1', '2'): # ****
                raise ValueError # ****
            break # ****
        except ValueError: # ****
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either '1' or '2' (Play Cards or Discard).\n") # ****
    # -------------------------------------
    if play_choice == "1": # ****
        print(f"\n{player.name}, which cards would you like to play? (Use the ordered number of the card(s) as listed below for choosing associated card(s) for play.)\n") # ****
        sorted_and_numbered_list_printer(player.hand) # ****
        multiple_choices_input_filter_and_transfer(player, player.play_cards, player.hand) # ****
        valid_play_check_and_sort(player) # ****
    else: # ****
        discard(player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by wild_card_handler(), play_2() functions. For transferring cards from one list to another. # ****
def multiple_choices_input_filter_and_transfer(player, append_list, pop_list): # ****
    logger.debug("multiple_choices_input_filter_and_transfer")
    while True: # ****
        try: # ****
            input_str = input("> ") # ****
            input_str = list(input_str) # ****
            temp_char_holder = {} # ****
            index = -1 # ****
            consec_int_counter = 0 # ****
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # ****
            # -------------------------------------
            for char in input_str: # ****
                if char in numbers: # ****
                    index += 1 # ****
                    temp_char_holder[index] = int(char) # ****
                    consec_int_counter += 1 # ****
                    if consec_int_counter == 2: # ****
                        concatenated_int = int(str(temp_char_holder.pop(index - 1)) + str(temp_char_holder.pop(index))) # ****
                        temp_char_holder[index - 1] = concatenated_int # ****
                elif char in [',', ' ']: # ****
                    consec_int_counter = 0 # ****
                else:
                    raise ValueError
                    # -------------------------------------
            temp_char_holder = sorted(temp_char_holder.values(), reverse = True) # ****
            # -------------------------------------
            for typed_value in temp_char_holder: # ****
                append_list.append(pop_list.pop(typed_value - 1)) # ****
            break # ****
        except (ValueError, IndexError): # ****
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your choices match the number that precedes the card(s) you are trying to choose.\n") # ****
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_2() function. For ensuring that a set of attempted play cards are valid according to game rules. # ****
def valid_play_check_and_sort(player): # ****
    logger.debug("\nvalid_play_check_and_sort\n") # ****
    # -------------------------------------
    play_cards_new_ranks = [] # ****
    bad_len_temp_melds_list_print = [] # ****
    play_cards_removed_black_3s = [] # ****
    # -------------------------------------
    # Below Section - Clears player.initial_played_cards and iterates through player.melds, appending each existing meld to initial_played_cards so that initial_played_cards == player.melds at this point in time. For the purpose of comparing player.initial_played_cards against player.melds later on to see if any cards/melds were successfully added to player.melds throughout the play after sorting and validation. # ****
    player.initial_played_cards.clear()
    player.initial_played_cards = copy.deepcopy(player.melds) # ****
    # -------------------------------------
    # Below Section - Checks to see if the player has NOT met the initial meld requirements. If so, valid plays are different than if they had met the requirement, thus puts different restrictions on what a valid play is. # ****
    if player.round_score < player.meld_requirement: # ****
        logger.debug("player.round_score < player.meld_requirement\n") # ****
        # -------------------------------------
        if len(player.play_cards) < 3: # ****
            print(f"\nSorry, {player.name}, but you must play at least 3 cards for a new meld. Please select a new set of cards to play, or you can choose to discard if you like.\n") # ****
            for card in player.play_cards[:]: # ****
                player.hand.append(card) # ****
            player.play_cards.clear() # ****
            return play_2(player) # ****
    # -------------------------------------
    # Below Extended Section - Sorts all of the individual play cards, putting them either in matching melds, or creating temp_melds and putting those back into play_cards to be further sorted. Also places all played wild cards into play_cards_wild_cards and removes any played Black 3s unless special requirements are met. # ****
    for card in player.play_cards[:]: # ****
        # Below Section - Checks to see if the player already has existing melds. If so, checks to see if card rank is already in a preexisting meld. If so, pops the card from player.play_cards and appends it to the meld. # ****
        card_found_in_meld = False # ****
        if len(player.melds) > 0: # ****
            for meld in player.melds: # ****
                if card.rank == meld[0].rank: # ****
                    meld.append(player.play_cards.pop(player.play_cards.index(card))) # ****
                    # Below Line - Changes the variable card_found_in_meld to True in the case that it is matched and subsequently popped from the list, so that if it also meets another parameter later on in the loop, it will not be recognized again and attempted to be handled again, which caused errors wherein it was trying to place the card in two different locations in the past. # ****
                    card_found_in_meld = True # ****
        # -------------------------------------
        # Below Extended Section - Handles all cards that were not found in a preexisting meld. Handles black_3s, wild cards, new melds, and cards that match the rank of new melds so that they can all be properly sorted and later validated. # ****
        if card_found_in_meld == False: # ****
            # Below Section - Checks if card is a Black 3 and whether the player meets the card count requirements to be able to play a Black 3 meld. If not, appends it to play_cards_removed_black_3s, which is used to print out all of these instances later on to inform the player, and removes it from player.play_cards, placing it back into player.hand. If so, appends the Black 3s into player.black_3_meld. # ****
            if (card.rank, card.suit) in Deck().black_3s: # ****
                if len(player.hand) <= 1: # ****
                    player.black_3_meld.append(player.play_cards.pop(player.play_cards.index(card))) # ****
                else: # ****
                    play_cards_removed_black_3s.append(player.play_cards.pop(player.play_cards.index(card))) # ****
            # -------------------------------------
            # Below Section - If card is a Wild Card; appends it to play_cards_wild_cards, popping it from player.play_cards, for the purpose of segregation so that later on when meld lengths are determined, they are not convoluted by having individual wild cards mixed in. # ****
            elif (card.rank, card.suit) in Deck().wild_cards: # ****
                player.play_cards_wild_cards.append(player.play_cards.pop(player.play_cards.index(card))) # ****
            # -------------------------------------
            # Below Section - If card is a valid, non-wild card that is the first of it's rank iterated through in the group of play cards. Creates a new temp_meld for it to be placed into, and the temp_meld is then placed back into player.play_cards, which is where other cards of the same rank will be placed. # ****
            elif card.rank not in play_cards_new_ranks: # ****
                play_cards_new_ranks.append(card.rank) # ****
                temp_meld = [] # ****
                temp_meld.append(player.play_cards.pop(player.play_cards.index(card))) # ****
                player.play_cards.append(temp_meld) # ****
            # -------------------------------------
            # Below Section - If card's rank exists in play_cards_new_ranks. Sorts the card into the temp_meld that matches the card's rank. For grouping cards of the same rank together. # ****
            elif card.rank in play_cards_new_ranks: # ****
                for item in player.play_cards: # ****
                    if type(item) == list: # ****
                        if card.rank == item[0].rank: # ****
                            item.append(player.play_cards.pop(player.play_cards.index(card))) # ****
        # -------------------------------------
    # -------------------------------------
    # Below Section - Handles temp_melds that are too small or that require a wild card to be able to meet the 3 card minimum requirement. If the melds consist of only 1 card, they are appended to bad_len_temp_melds_list_print for later output and removal from player.play_cards back into player.hand, and the melds that require a wild card (consisting of 2 cards) are put in len_2_temp_melds_list, given that there is at least one card in play_cards_wild_cards so that the player can later choose which meld he would like to add the wild card(s) to. If there is nothing in play_cards_wild_cards, those melds are also added to bad_len_temp_melds_list_print for later removal back into the player.hand. # ****
    for temp_meld in player.play_cards[:]: # ****
        if type(temp_meld) != Card:
            if len(temp_meld) < 2: # ****
                bad_len_temp_melds_list_print.append(player.play_cards.pop(player.play_cards.index(temp_meld))) # ****
            elif len(temp_meld) == 2: # ****
                if len(player.play_cards_wild_cards) < 1: # ****
                    bad_len_temp_melds_list_print.append(player.play_cards.pop(player.play_cards.index(temp_meld))) # ****
                else: # ****
                    player.len_2_temp_melds_list.append(player.play_cards.pop(player.play_cards.index(temp_meld))) # ****
        else:
            logger.debug(f"{temp_meld} is in the list of play_cards after all sorting, which means somewhere the code is wrong. Only melds should be here, no single cards: melds of one card should exist, but not single cards outside of a meld. If this is showing, a Card type is the object being handled.")
    # -------------------------------------
    # Below Section - For adding available played wild cards to melds consisting of 2 cards (len_2_temp_melds_list) so that they will meet the 3 card minimum requirement. # ****
    while len(player.len_2_temp_melds_list) > 0: # ****
        if len(player.play_cards_wild_cards) > 0: # ****
            print(f"\n{player.name}, the below meld(s) from your attempted play cards have only 2 cards in them. Since 3 cards are required for a valid meld, you must add a wild card to them for them to remain in play. It looks as if you have {len(player.play_cards_wild_cards)} wild card(s): {(player.play_cards_wild_cards)} in your set of play cards to use for this. Choose a meld from the list below that you would like to add a wild card to.\n") # ****
            sorted_and_numbered_list_printer(player.len_2_temp_melds_list) # ****
            num = str(len(player.len_2_temp_melds_list) + 1) # ****
            print(f"{num}) I would rather use the wild card elsewhere, and let the meld(s) be placed back into my hand.\n") # ****
            while True: # ****
                try: # ****
                    len_2_temp_meld_choice = int(input("> ")) - 1 # ****
                    if len_2_temp_meld_choice + 1 != int(num) and player.len_2_temp_melds_list[len_2_temp_meld_choice] not in player.len_2_temp_melds_list: # ****
                        raise IndexError # ****
                    break # ****
                except (ValueError, IndexError): # ****
                    print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is a number that precedes one of the meld groups above, or is the number that precedes the option to not use the wild card.\n") # ****
            if len_2_temp_meld_choice != int(num) - 1: # ****
                if len(player.play_cards_wild_cards) > 1: # ****
                    print(f"\nWhich wild card would you like to add to the following meld? - {player.len_2_temp_melds_list[len_2_temp_meld_choice]} - Choose from the below choices.\n") # ****
                    sorted_and_numbered_list_printer(player.play_cards_wild_cards) # ****
                    while True: # ****
                        try: # ****
                            wild_card_choice = int(input("> ")) - 1 # ****
                            print(f"\nYou successfully added the {player.play_cards_wild_cards[wild_card_choice]} to your meld.\n") # ****
                            player.len_2_temp_melds_list[len_2_temp_meld_choice].append(player.play_cards_wild_cards.pop(wild_card_choice)) # ****
                            player.play_cards.append(player.len_2_temp_melds_list.pop(len_2_temp_meld_choice)) # ****
                            break # ****
                        except (ValueError, IndexError): # ****
                            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is a number that precedes the card you are trying to choose.\n") # ****
                else: # ****
                    print(f"\nYou successfully added the {player.play_cards_wild_cards[0]} to your meld.\n") # ****
                    player.len_2_temp_melds_list[len_2_temp_meld_choice].append(player.play_cards_wild_cards.pop(0)) # ****
                    player.play_cards.append(player.len_2_temp_melds_list.pop(len_2_temp_meld_choice)) # ****
    # -------------------------------------
            # Below Section - If the player chooses not to use the available wild card(s); places the len_2_temp_melds_list melds into bad_len_temp_melds_list_print, leaving the wild cards in play cards to be handled with wild_card_handler. # ****
            else: # ****
                print("\nOkay, the meld(s) will be put back into your hand, while the wild card will continue to remain in your group of played cards with the option of being used later in any of your attempted melds or your existing melds. \n") # ****
                for temp_meld in player.len_2_temp_melds_list[:]: # ****
                    bad_len_temp_melds_list_print.append(player.len_2_temp_melds_list.pop(player.len_2_temp_melds_list.index(temp_meld))) # ****
            # -------------------------------------
        # Below Section - If player does not have any wild cards left to use for appending to the short melds. Appends the melds to bad_len_temp_melds_list_print for placement back into the player.hand # ****
        elif len(player.play_cards_wild_cards) == 0: # ****
            for temp_meld in player.len_2_temp_melds_list[:]: # ****
                bad_len_temp_melds_list_print.append(player.len_2_temp_melds_list.pop(player.len_2_temp_melds_list.index(temp_meld))) # ****
        # -------------------------------------
    # Below  Section - Handles the informative output for melds of bad length & removal of said melds back into the player.hand. # ****
    if len(bad_len_temp_melds_list_print) > 0: # ****
        print(f"\n{player.name}, you have some attemped melds that do not pass the rule requirements. You cannot create a new meld without at least 2 natural cards of the same rank, or without a wild card to add to it to reach the 3 card minimum meld requirement. The attempted meld(s) will be removed and placed back in your hand:\n") # ****
        sorted_and_numbered_list_printer(bad_len_temp_melds_list_print) # ****
        for bad_len_meld in bad_len_temp_melds_list_print[:]: # ****
            for card in bad_len_meld[:]: # ****
                player.hand.append(bad_len_meld.pop(bad_len_meld.index(card))) # ****
    # -------------------------------------
    # Below Section - Checks to see if player.play_cards_wild_cards is populated, and if so, calls wild_card_handler to distribute them. # ****
    if len(player.play_cards_wild_cards) > 0: # ****
        wild_card_handler(player) # ****
    # -------------------------------------
    # Below Section - If the player had 1 or 0 cards left in his hand for this play, then Black 3s were segregated into player.black_3_meld until their played cards were sorted and validated (this point). If they have a Canasta at this point, then the black_3_meld will be appended to their list of play cards, and player.black_3_meld will be .clear()ed. If not, the cards in the black_3_meld will be placed back into their hand. # ****
    if len(player.black_3_meld) >= 3:
        if player.has_canasta == True:
            player.play_cards.append(player.black_3_meld[:]) # ****
            player.black_3_meld.clear() # ****
    elif len(player.black_3_meld) > 0:
        print(f"Sorry, {player.name}, but your attempted Black 3 meld (made possible because you played them with 1 or 0 cards left in your hand) did not succeed because you must have at least 1 Canasta to be eligible for this play. Therefore, your Black 3(s) will be placed back into your hand.\n")
        for card in player.black_3_meld[:]:
            player.hand.append(player.black_3_meld.pop(-1))
    # -------------------------------------
    # Below Section - Checks to see if there are any Black 3s that were removed from the play cards, and if so, prints them out and informs the player of their removal. # ****
    if len(play_cards_removed_black_3s) > 0:  # ****
        print(f"Sorry, {player.name}, but you cannot play your Black 3(s) in this way, unless you are going out this play. Black 3s can otherwise only be used to freeze the discard pile. The Black 3(s) that are being removed from your attempted play cards back into your hand are as follows:\n") # ****
        sorted_and_numbered_list_printer(play_cards_removed_black_3s) # ****
        for card in play_cards_removed_black_3s[:]: # ****
            player.hand.append(play_cards_removed_black_3s.pop(play_cards_removed_black_3s.index(card))) # ****
    # -------------------------------------
    # Below Section - Checks to ensure that after all the sorting and validation the player's melds meet their minimum meld requirement score, in the case that they have no established melds/have not already met the meld requirement. If, so, cards are kept in player.play_cards, but if not, they are transferred back into player.hand. # ****
    if len(player.melds) == 0:
        if player.round_score < player.meld_requirement: # ****
            if len(player.play_cards) > 0:
                print(f"Sorry, {player.name}, but the value of your play cards: ({player.round_score}) - after filtering and sorting your attempted melds: (" + ', '.join(['%s']*len(player.play_cards)) % tuple(player.play_cards) + f") is not enough to meet the minimum meld requirement of {player.meld_requirement}. Your play cards will be placed back into your hand and you will be redirected to make another play attempt.\n") # ****
            else:
                print(f"Sorry, {player.name}, but the value of your play cards: (0) - after filtering and sorting your attempted melds, is not enough to meet the minimum meld requirement of {player.meld_requirement}. Your play cards will be placed back into your hand and you will be redirected to make another play attempt.\n") # ****
            # -------------------------------------
            for meld in player.play_cards[:]: # ****
                for card in meld[:]: # ****
                    player.hand.append(meld.pop(-1)) # ****
            player.play_cards.clear() # ****
            # -------------------------------------
            return play_2(player) # ****
            # -------------------------------------
        else:
            print(f"You succeeded in meeting your minimum meld score requirement of {player.meld_requirement}!\n")
    # -------------------------------------
    # Below Section - Prints out the successfully played cards, transfers the played cards to player.melds (granted there were successfully played cards), and directs the player to either went_out_check() or discard() depending on the amount of cards in the player's hand. If no cards were played, prints an informative message, and reroutes the player to make a new play attempt via play_2(). # ****
    if len(player.play_cards) > 0: # ****
        print(f"{player.name}, you successfully created the meld(s) below!\n") # ****
        sorted_and_numbered_list_printer(player.play_cards) # ****
        # -------------------------------------
    for temp_meld in player.play_cards[:]: # ****
        player.melds.append(player.play_cards.pop(player.play_cards.index(temp_meld))) # ****
        # -------------------------------------
    # Below Section - Creates 2 variables, total_melds_len & total_initial_played_cards_len, with values of 0, then gets the sum of all meld lens in player.melds & player.initial_played_cards, then compares them to one another to determine if any cards were successfully played during the current play.
    total_melds_len = 0
    total_initial_played_cards_len = 0
    for meld in player.melds:
        total_melds_len += len(meld)
    for meld in player.initial_played_cards:
        total_initial_played_cards_len += len(meld)
    if total_initial_played_cards_len == total_melds_len: # ****
        print("It looks as if you were unable to succeed in playing any of your attempted play cards. Therefore you will have to choose another set of play cards, or opt to discard instead if you have no valid plays to make.\n") # ****
        play_2(player) # ****
    else: # ****
        logger.debug("total_initial_played_cards_len != total_melds_len\n") # ****
        player.final_played_cards = 1
    # -------------------------------------
        if len(player.hand) <= 1: # ****
            went_out_check(player) # ****
        else: # ****
            discard(player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below - Called by valid_play_check_and_sort() function. Handles all played wild cards (after len_2_temp_melds_list sorting and placement of played wild cards), prompting the player to determine their placement. Also determines whether or not a Wild Card Canasta is being played. Any unplayed wild cards are placed back into the player's hand. # ****
def wild_card_handler(player): # ****
    logger.debug("wild_card_handler") # ****
    # Below Section - In the case that player plays 7 or more wild cards, checks via prompt to see if player is trying to play a Wild Card Canasta. # ****
    if len(player.play_cards_wild_cards) >= 7: # ****
        while True: # ****
            try: # ****
                wild_card_canasta_check_input = input(f"{player.name}, are you trying to play a Wild Card Canasta? (Y/N)\n\n> ") # ****
                if wild_card_canasta_check_input.lower() not in ('y', 'n'): # ****
                    raise ValueError # ****
                break # ****
            except ValueError: # ****
                print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n") # ****
        if wild_card_canasta_check_input.lower() == 'y': # ****
    # ------------------------------------- ****
            # Below Section - Checks if the amount of wild cards in player.play_cards_wild_cards is exactly 7 cards, in which case the entire list will be appended to player.play_cards, then player.play_cards_wild_cards will be cleared. Finally, returns None. # ****
            if len(player.play_cards_wild_cards) == 7: # ****
                player.play_cards.append(player.play_cards_wild_cards[:]) # ****
                player.play_cards_wild_cards.clear() # ****
                print(f"{player.name}, you successfully played a Wild Card Canasta! Congratulations!\n") # ****
                return None
            # ------------------------------------- ****
            # Below Section - If the amount of wild cards being played is greater than 7; player is prompted to choose which wild cards they want to use in the canasta. The non-chosen wild cards will remain in play to be distributed later in the function, unless this is the player's first meld. In this case, appends left over wild cards back into player.hand, and returns None. # ****
            else: # ****
                print(f"{player.name}, choose 7 wild cards from the list below that you want to use for your Wild Card Canasta. Use the numbers that prefix each wild card ( 1), 2), 3), 4), etc. ) in the list to choose those that you want. (i.e. - 1, 3, 5, 7, etc.) \n") # ****
                sorted_and_numbered_list_printer(player.play_cards_wild_cards) # ****
                wild_card_canasta_meld = []
                multiple_choices_input_filter_and_transfer(player, wild_card_canasta_meld, player.play_cards_wild_cards) # ****
                player.play_cards.append(wild_card_canasta_meld)
                if player.round_score < player.meld_requirement: # ****
                    print(f"\n{player.name}, since you only have the Wild Card Canasta in your available melds and extra wild cards left over, they will be placed back into your hand as there is currently no other place to put them.\n") # ****
                    for wild_card in player.play_cards_wild_cards[:]: # ****
                        player.hand.append(player.play_cards_wild_cards.pop(-1)) # ****
                    return None # ****
            # ------------------------------------- ****
    # Below Section - Runs if the player has less than 7 wild cards in player.play_cards_wild_cards OR if they have/had 7 or more wild cards but chose not to create a wild card canasta/had leftover wild cards after creating a wild card canasta with them, and if the player has at least 1 meld in player.play_cards or player.melds that does not contain the max amount of wild cards; iterates through each wild card in player.play_cards_wild_cards and prompts the player to choose a destination for each card. # ****
    if len(player.play_cards) > 0 or len(player.melds) > 0: # ****
        for wild_card in player.play_cards_wild_cards[:]: # ****
            if len(player.non_maxed_out_melds) > 0: # ****
                meld_choice_index = wild_card_meld_choice_prompt(player, wild_card) # ****
    # -------------------------------------
                # Below Section - If player chooses not to use the wild card, it is popped from play_cards_wild_cards and appended back into the player's hand. # ****
                if meld_choice_index > (len(player.non_maxed_out_melds) - 1): # ****
                    print("\nOkay, the wild card will be placed back into your hand.\n") # ****
                    player.hand.append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card))) # ****
                # -------------------------------------
                # Below Section - If player chooses to place the wild card into a meld; determines which meld group (player.play_cards or player.melds) they chose, and appends the wild card to that meld, popping it from play_cards_wild_cards. # ****
                elif player.non_maxed_out_melds[meld_choice_index] in player.play_cards: # ****
                    print(f"\n{player.name}, you successfully added the {player.play_cards_wild_cards[player.play_cards_wild_cards.index(wild_card)]} to your meld.\n") # ****
                    player.play_cards[player.play_cards.index(player.non_maxed_out_melds[meld_choice_index])].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card))) # ****
                elif player.non_maxed_out_melds[meld_choice_index] in player.melds: # ****
                    print(f"\n{player.name}, you successfully added the {player.play_cards_wild_cards[player.play_cards_wild_cards.index(wild_card)]} to your meld.\n") # ****
                    player.melds[player.melds.index(player.non_maxed_out_melds[meld_choice_index])].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card))) # ****
                # -------------------------------------
            # Below Section - For the case whenever the player has nowhere to place the wild card. Places all of the remaining wild cards back into the player's hand after an informative message. # ****
            else: # ****
                print(f"{player.name}, it looks as if every meld in your play cards and/or in your melds have the maximum amount of wild cards possible. Therefore the remaining wild cards in play will be placed back into your hand.\n") # ****
                for wild_card in player.play_cards_wild_cards[:]: # ****
                    player.hand.append(player.play_cards_wild_cards.pop(-1)) # ****
                return None # ****
            # ------------------------------------- # ****
    # Below Section - If a player who has no play_card melds or player.meld melds tried to play some wild cards. Since there is nowhere to put them, places the cards back into the player's hand. # ****
    else: # ****
        print(f"It looks as if you have some wild cards leftover in your group of play cards, {player.name}, but there is nowhere to place them, since you have no existing melds. The cards will be placed back into your hand.\n") # ****
        for wild_card in player.play_cards_wild_cards[:]: # ****
            player.hand.append(player.play_cards_wild_cards.pop(-1)) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by wild_card_handler() function. Prompts the player to choose a meld to add the wild_card to, or to opt to not use the wild card at all in this manner. Ensures that the input is valid, and returns the choice. # ****
def wild_card_meld_choice_prompt(player, wild_card): # ****
    logger.debug("wild_card_meld_choice_prompt")
    print(f"\n{player.name}, which meld from the list below would you like to add the {player.play_cards_wild_cards[player.play_cards_wild_cards.index(wild_card)]} to?\n") # ****
    sorted_and_numbered_list_printer(player.non_maxed_out_melds) # ****
    meld_num = str(len(player.non_maxed_out_melds) + 1) # ****
    print(f"{meld_num}) I would not like to use this wild card, and would rather have it be replaced back into my hand.\n") # ****
    while True: # ****
        try: # ****
            meld_choice_index = int(input('> ')) - 1 # ****
            if (meld_choice_index + 1) != int(meld_num): # ****
                if (0 > meld_choice_index) or ((meld_choice_index + 1) > int(meld_num)): # ****
                    raise IndexError # ****
            break # ****
        except (ValueError, IndexError): # ****
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either a number that precedes the meld you are choosing or the number associated with the option to not use the wild card.\n") # ****
    return meld_choice_index # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_2(), valid_play_check_and_sort(), went_out_check() functions. For discarding; prompts the player to choose a card from their hand to be placed into the discard pile. # ****
def discard(player): # ****
    logger.debug("discard\n") # ****
    # -------------------------------------
    print(f"\n{player.name}, which card would you like to discard? Your available cards in hand are:\n") # ****
    sorted_and_numbered_list_printer(player.hand) # ****
    while True: # ****
        try: # ****
            discard_input = int(input("> ")) - 1 # ****
            break # ****
        except (ValueError, IndexError): # ****
            print("\nSorry, but there was a problem with your input. Please try again. Make sure your input is a number preceding the card you would like to discard.\n") # ****
    print(f"\n{player.name}, you discarded the {player.hand[discard_input]}.\n") # ****
    MasterDeck.discard_pile.append(player.hand.pop(discard_input)) # ****
    # -------------------------------------
    if len(player.hand) == 0: # ****
        went_out_check(player) # ****
    else:
        if player == P1: # ****
            play_1(P2) # ****
        else: # ****
            play_1(P1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by valid_play_check_and_sort(), discard() functions. Checks to see if player is eligible to go out, and whether or not they went out during their last turn. If they are not trying to go out, redirects to beginning of the player turn loop via play_1() function. If so, ends round via round_reset(). # ****
def went_out_check(player, going_out_from_discard_draw = False): # ****
    logger.debug("went out check\n") # ****
    # -------------------------------------
    if player.has_canasta == True: # ****
        player.going_out = True # ****
        if going_out_from_discard_draw == False:
            if len(player.initial_played_cards) == 0: # ****
                player.went_out_concealed = True # ****
                # -------------------------------------
        else:
            if len(player.final_played_cards) == 0:
                player.went_out_concealed = True # ****
                # -------------------------------------
        if player == P1: # ****
            P2.going_out = False # ****
            print(f"{P1.name}, you successfully went out!\n\nRound Score:\n\n{P1.name}: {P1.round_score}\n{P2.name}: {P2.round_score}\n") # ****
        else: # ****
            P1.going_out = False # ****
            print(f"{P2.name}, you successfully went out!\n\nRound Score:\n\n{P2.name}: {P2.round_score}\n{P1.name}: {P1.round_score}\n") # ****
            # -------------------------------------
        round_reset() # ****
        # -------------------------------------
    # Below Extended Section - In the case that a player is attempting to go out (has 0 cards in their hand) but does not have the required canasta to do so. Gives the player an informative message and prompts them to choose 2 cards to take back into their hand from the available melds to use as a discard and a required card to be kept in their hand. # ****
    else: # ****
        print("It looks as if you are attempting to go out, but you do not have a Canasta, which is required. Since you cannot go out, you must keep at least 1 card in your hand to use as a required discard and 1 more card to keep in your hand. Therefore, you must choose 2 cards from the set of your most recently played cards to take back into your hand. Choose 2 cards from the list of cards below to use for this. (Use the preceding ordered number associated with each card to choose one.)\n") # ****
        # Below Section - Checks player.melds against player.initial_played_cards to create a list of each card that was just played and its associated meld. # ****
        for meld_index in range(len(player.melds)): # ****
            # Below Line - Checks for melds that were preexisting before current play. # ****
            if (meld_index + 1) <= len(player.initial_played_cards):
                if len(player.melds[meld_index]) > len(player.initial_played_cards[meld_index]): # ****
                    meld_len_difference = len(player.melds[meld_index]) - len(player.initial_played_cards[meld_index]) # ****
                    for card in player.melds[meld_index][-meld_len_difference:]: # ****
                        player.last_set_played_cards.append([card, player.melds[meld_index]]) # ****
            # Below Line - For melds that were created during current play. # ****
            else: # ****
                for card in player.melds[meld_index]: # ****
                    player.last_set_played_cards.append([card, player.melds[meld_index]]) # ****
        # -------------------------------------
        # Below Section - Creates a variable prior_hand_len to reference the len(player.hand) before running went_out_check_replacement_card() so that it can be determined whether or not the function needs to be run twice instead of once for the instance in which only one card was removed from a meld, as opposed to multiple cards being removed from a meld due to entire meld disbandment, resulting in the 2 card replacement requirement having already been met with a single function call. Finally, clears player.last_set_played_cards so that the next time this is called it does not have the previous set of played cards included. # ****
        print("The cards that were used last play are listed below, followed by their associated melds for reference in helping to determine which card to take back into your hand. In the case that a card from the affected/created meld consists of less than 4 cards, the card's meld you choose will be completely disbanded and replaced back into your hand. If it is found that after the card or meld is replaced back into your hand you no longer meet the meld requirement, all of your played cards will be placed back into your hand and you will have to make another play attempt. You have to choose 2 cards to be placed back (1 for keeping in the hand and 1 for discarding). In the case that you choose a card from a meld that has to be disbanded, you will only have to make this selection one time since the 2 card replacement will have been met via the meld replacement.\n") # ****
        prior_hand_len = copy.copy(len(player.hand))
        went_out_check_replacement_card(player) # ****
        if len(player.hand) < 2:
            went_out_check_replacement_card(player) # ****
        player.last_set_played_cards.clear()
        # -------------------------------------
        # Below Section - Checks to ensure that after alteration of existing melds the player still reaches their meld requirement. If not, gives the player an informative message, replaces all of the cards in their melds back into their hand, and reroutes them back to a new play attempt. If so, directs the player to discard. # ****
        if player.round_score < player.meld_requirement: # ****
            for meld in player.melds[:]: # ****
                for card in meld[:]: # ****
                    player.hand.append(meld.pop(-1)) # ****
            player.melds.clear() # ****
            print("It looks as if you no longer reach the meld reqiurement after alteration of your melds. Therefore all cards have been placed back into your hand from your melds and you will be redirected to make another play attempt.\n") # ****
            return play_2(player) # ****
        else: # ****
            return discard(player) # ****
    # -------------------------------------
    if player == P1: # ****
        return play_1(P2) # ****
    else: # ****
        return play_1(P1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 # Below Function - Called by went_out_check() function. Prints all of the last played cards and their associated melds for reference when choosing a card to be replaced back into the hand. Prompts the player to choose which card they would like to place back into their hand from the available melds. Determines whether or not the card's removal would require the associated meld to be disbanded. If not, places all of their melds back into their hand and redirects them back to make another play attempt. If so, redirects the player to the discard() function. # ****
def went_out_check_replacement_card(player): # ****
    logger.debug("went_out_check_replacement_card")
    num = 0
    while True: # ****
        try: # ****
            if num == 0:
                sorted_and_numbered_list_printer(player.last_set_played_cards) # ****
            else:
                print("")
                sorted_and_numbered_list_printer(player.last_set_played_cards) # ****
            replacement_choice = int(input("Which card from the list above would you like to place back into your hand? Remember that if it is from a meld with less than 4 cards, the entire meld will be disbanded and placed back into your hand. Use the preceding ordered number associated with each card to make a choice.\n\n> ")) # ****
            if len(player.melds[player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])]) > 3: # ****
                print(f"\nYou removed the {player.last_set_played_cards[replacement_choice - 1][0]} from it's meld back into your hand.\n") # ****
                # Below Line - Appends the chosen card to the player.hand, popping from player.meld. # ****
                player.hand.append(player.melds[player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])].pop(player.melds[player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])].index(player.last_set_played_cards[replacement_choice - 1][0]))) # ****
                # Below Line - Pops the listed card_and_meld from player.last_set_played_cards because since only 1 card is removed here, a 2nd function call is required. Ensures that this card choice is not available again, since it no longer actually exists in the meld.
                player.last_set_played_cards.pop(replacement_choice - 1)
                break
            else: # ****
                # Below Section - Checks to see if the player has any melds with more than 3 cards in them, since they chose to disband a meld of 3 or less cards. If they do have one of these melds, presents the player with an informative message and asks for verification of their choice. # ****
                melds_len_over_3 = False # ****
                for card_and_meld in player.last_set_played_cards: # ****
                    if len(card_and_meld[1]) > 3: # ****
                        melds_len_over_3 = True # ****
                if melds_len_over_3 == True: # ****
                    while True: # ****
                        try: # ****
                            meld_verify_input = input("\nThis meld has 3 cards, which means the entire meld would have to be disbanded if you were to remove this card. It looks like you have a meld in your list of choices that has more than 3 cards, which means it would not have to be completely disbanded. Are you sure that you want to disband this meld instead? (Y/N)\n\n> ") # ****
                            if meld_verify_input.lower() not in ('y', 'n'): # ****
                                raise ValueError # ****
                            break # ****
                        except ValueError: # ****
                            print("\nSorry, but there was a problem with your input. Please try again, making sure that your input is either 'Y' or 'N' (Yes or No).\n") # ****
                    if meld_verify_input.lower() == 'y': # ****
                        print("Okay, the meld will be disbanded and placed back into your hand.\n") # ****
                        for card in player.melds[player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])][:]: # ****
                            player.hand.append(player.melds[player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])].pop(-1)) # ****
                        # Below Line - Pops the emptied meld from player.melds.
                        player.melds.pop(player.melds.index(player.last_set_played_cards[replacement_choice - 1][1]))
                        # Below Line - Breaks out of while loop unless the meld_verify_input != 'y', in which case it reroutes back to the beginning of the loop so that the player can choose a different card. # ****
                        break # ****
                    # Below Section - References the num variable created at the beginning of the function, and changes it to 1 so that there is proper spacing when sorted_and_numbered_list_printer() is printed.
                    else:
                        num = 1
                else: # ****
                    print("\nThe meld associated with this card consists of 3 cards, so the entire meld will be disbanded and placed back into your hand, as that is the least amount of cards allowed in a valid meld.\n") # ****
                    for card in player.melds[player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])][:]: # ****
                        player.hand.append(player.melds[player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])].pop(-1)) # ****
                    # Below Line - Pops the emptied meld from player.melds. # ****
                    player.melds.pop(player.melds.index(player.last_set_played_cards[replacement_choice - 1][1])) # ****
                    # Below Line - Breaks out of the while loop, thus the function. # ****
                    break # ****
                # -------------------------------------
        except (ValueError, IndexError): # ****
            print("\nSorry, but there was a problem with your input. Try again, making sure that your input is the number that precedes the card you wish to choose.\n") # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt(), draw_discard_pile_attempt_check_meld_match(), went_out_check() functions. Resets all settable attributes and values back to default/starting conditions to start a new round. Also prints an informative output showing the players' scores, and who won the round. # ****
def round_reset(): # ****
    logger.debug("round_reset")
    for player in (P1, P2): # ****
        player.finished_rounds_scores.append(player.round_score) # ****
        player.the_draw = None # ****
        player.hand.clear() # ****
        player.play_cards.clear() # ****
        player.play_cards_wild_cards.clear() # ****
        player.initial_played_cards.clear() # ****
        player.final_played_cards = 0
        player.last_set_played_cards.clear() # ****
        player.red_3_meld.clear() # ****
        player.black_3_meld.clear() # ****
        player.melds.clear() # ****
        player.len_2_temp_melds_list.clear() # ****
        player.matched_card_list.clear() # ****
        player.going_out = None # ****
        player.went_out_concealed = False # ****
        player.total_score_over_5000 = False
        player.special_case_cant_draw = False
    # --------------------------------------
    print(f"The round is over! {P1.name}'s final round score was {P1.finished_rounds_scores[-1]}, and {P2.name}'s final round score was {P2.finished_rounds_scores[-1]}.\n")
    if P1.finished_rounds_scores[-1] > P2.finished_rounds_scores[-1]:
        print(f"{P1.name} was the winner of the round!\n")
    elif P1.finished_rounds_scores[-1] == P2.finished_rounds_scores[-1]:
        print(f"Both players had the same score! The round was a tie!\n")
    elif P2.finished_rounds_scores[-1] > P1.finished_rounds_scores[-1]:
        print(f"{P2.name} was the winner of the round!\n")
    # --------------------------------------
    MasterDeck.discard_pile.clear()
    MasterDeck.deck.clear()
    MasterDeck.deck = MasterDeck.original_deck[:]
    # --------------------------------------
    win_check() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by round_reset() function. Checks a winning value (5000) against each player's score to determine whether or not someone has won. If so, calls check_total_score_winner() function to determine the winner. If not, begins a new round via the_draw_1() function. # ****
def win_check(): # ****
    logger.debug("win_check") # ****
    for player in (P1, P2): # ****
        other_player = None
        if player == P1:
            other_player = P2
        else:
            other_player = P1
        if player.total_score >= 5000: # ****
            return check_total_score_winner(player, other_player)
     # -------------------------------------
    # Below Line - In the case that nobody has won yet, restarts a new round. # ****
    the_draw_1() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by win_check() function. In the case that one player has reached 5000 points, checks player & other_player's player.total_score to determine the input for the winner_output() function. If the players have an equal score, (player, True) is passed into winner_output() function so that the tie game output is processed. Otherwise, the winning player is passed in; either player or other_player.
def check_total_score_winner(player, other_player):
    if player.total_score > other_player.total_score: # ****
        return winner_output(player) # ****
    elif player.total_score == other_player.total_score: # ****
        winner_output(player, True) # ****
    elif player.total_score < other_player.total_score: # ****
        return winner_output(other_player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by win_check() function. Prints outputs for the winner (unless it was a draw) and a game summary including all of the players' round scores. Also prompts the user on whether or not they would like to play again. # ****
def winner_output(player, tie_game = False): # ****
    logger.debug("winner_output") # ****
    if tie_game == False: # ****
        print(f"Congratulations, {player.name}, you are the winner! You are the champion, my friend!!\n") # ****
    else: # ****
        print("You both had the same score over 5,000 which means it is a tie game!\n") # ****
    # -------------------------------------
    p1_game_summary_string = (f"{P1.name}'s Game Summary:\n\nRound Scores:\n\n" + '\n'.join(['%s']*len(player.finished_rounds_scores)) % tuple(player.finished_rounds_scores) + "\n") # ****
    p2_game_summary_string = (f"{P2.name}'s Game Summary:\n\nRound Scores:\n\n" + '\n'.join(['%s']*len(player.finished_rounds_scores)) % tuple(player.finished_rounds_scores) + "\n") # ****
    # -------------------------------------
    while True: # ****
        try: # ****
            play_again_input = input("Would you like to play again?\n\n> ") # ****
            if play_again_input.lower() not in ('y', 'n'): # ****
                raise ValueError # ****
            break # ****
        except ValueError: # ****:
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n") # ****
    if play_again_input.lower() == 'y': # ****
        for player in (P1, P2):
            player.finished_rounds_scores.clear()
            if player == P1:
                player.name = 'Player 1'
            else:
                player.name = 'Player 2'
        return the_draw_1() # ****
    else: # ****
        sys.exit() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called at the end of the file. Main run loop. Runs game until a player wins. # ****
def game_run(): # ****
    logger.debug("game_run\n") # ****
    # -------------------------------------
    run = 1 # ****
    while run == 1: # ****
        logger.debug("run start\n") # ****
        the_draw_1() # ****
        return None
        logger.debug("run end\n") # ****
# -----------------------------------------------------------------------------  the_draw_1() # ****
        return None
        logger.debug("run end\n") # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - Runs the game, until someone wins! # ****
if __name__ == "__main__":
    if input("Start Game?\n\n> ") != "":
        game_run() # ****
    else:
        print("\nTESTING\n")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
