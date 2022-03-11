import player
import card
import deck
import game
import time
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Locations():
    def __init__(self):
        self.deck_location = [910, 540]
        self.discard_pile_location = [1010, 540]
        self.p1_hand_start_location = [100, 420]
        self.p2_hand_start_location = [1110, 420]
        self.p1_melds_start_location = [100, 800]
        self.p2_melds_start_location = [1110, 800]
        self.p1_play_cards_start_location = [100, 510]
        self.p2_play_cards_start_location = [1110, 510]
        self.top_left_visible = [50, 70]
        self.center = [1010, 610]
        self.card_width_height = [100, 140]
    # -------------------------------------
    # Below Function - Dynamically assigns player.P1's hand location.
    @property
    def p1_hand_next_location(self):
        if len(player.P1.hand) == 0:
            return self.p1_hand_start_location
        else:
            x_val_increase = len(player.P1.hand) * 20
            p1_hand_next_location = [self.p1_hand_start_location[0] + x_val_increase, self.p1_hand_start_location[1]]
            return p1_hand_next_location
    # -------------------------------------
    # Below Function - Dynamically assigns player.P2's hand location.
    @property
    def p2_hand_next_location(self):
        if len(player.P2.hand) == 0:
            return self.p2_hand_start_location
        else:
            x_val_increase = len(player.P2.hand) * 20
            p2_hand_next_location = [self.p2_hand_start_location[0] + x_val_increase, self.p2_hand_start_location[1]]
            return p2_hand_next_location
    # -------------------------------------
    # Below Function - Dynamically moves a single passed in card from it's current location to the desired location (loc) one unit at a time, using a formula (ratio) to move the card in a straight line. Calls player.P2 at the end of the function, which visually updates the card's on-screen location.
    def card_movement(self, loc, current_card):
        current_card.display_layer = 9999
        # -------------------------------------
        x_difference = 0
        y_difference = 0
        # -------------------------------------
        y_lesser = None
        x_lesser = None
        # -------------------------------------
        if current_card.x < loc[0]:
            x_difference = loc[0] - current_card.x
            x_lesser = True
        elif current_card.x > loc[0]:
            x_difference = current_card.x - loc[0]
            x_lesser = False
        if current_card.y < loc[1]:
            y_difference = loc[1] - current_card.y
            y_lesser = True
        elif current_card.y > loc[1]:
            y_difference = current_card.y - loc[1]
            y_lesser = False
        # -------------------------------------
        if x_difference > y_difference:
            ratio = (y_difference / x_difference)
            while [int(current_card.x), int(current_card.y)] != [int(loc[0]), int(loc[1])]:
                if x_lesser == True and int(current_card.x) != int(loc[0]):
                    current_card.x += 1
                elif x_lesser == False and int(current_card.x) != int(loc[0]):
                    current_card.x -= 1
                if y_lesser == True and int(current_card.y) != int(loc[1]):
                    prior_y = current_card.y
                    current_card.y += ratio
                    current_y = current_card.y
                    if int(prior_y) < int(current_y):
                        game.draw_window()
                elif y_lesser == False and int(current_card.y) != int(loc[1]):
                    prior_y = current_card.y
                    current_card.y -= ratio
                    current_y = current_card.y
                    if int(prior_y) > int(current_y):
                        game.draw_window()
                if y_lesser == None:
                    # Below Line -  Added for the instance in which the y-coordinate is == final y-coordinate, but x-coordinate still needs to be changed.
                    game.draw_window()
        # -------------------------------------
        elif int(y_difference) > int(x_difference):
            ratio = (x_difference / y_difference)
            while [int(current_card.x), int(current_card.y)] != [int(loc[0]), int(loc[1])]:
                if y_lesser == True and int(current_card.y) != int(loc[1]):
                    current_card.y += 1
                elif y_lesser == False and int(current_card.y) != int(loc[1]):
                    current_card.y -= 1
                if x_lesser == True and int(current_card.x) != int(loc[0]):
                    prior_x = current_card.x
                    current_card.x += ratio
                    current_x = current_card.x
                    if int(prior_x) < int(current_x):
                        game.draw_window()
                elif x_lesser == False and int(current_card.x) != int(loc[0]):
                    prior_x = current_card.x
                    current_card.x -= ratio
                    current_x = current_card.x
                    if int(prior_x) > int(current_x):
                        game.draw_window()
                if x_lesser == None:
                    # Below Line - Added for the instance in which the y-coordinate is == final y-coordinate, but x-coordinate still needs to be changed.
                    game.draw_window()
        # -------------------------------------
        # Below Section - For the rare instance when both the current x & y coordinates are the same distance from the final location's x & y coordinates.
        elif int(y_difference) == int(x_difference):
            while [int(current_card.x), int(current_card.y)] != [int(loc[0]), int(loc[1])]:
                current_card.x += 1
                current_card.y += 1
                game.draw_window()
    # -------------------------------------
    # Below Function - Called by func_dict via key 'deck' whenever a card is appended to the MasterDeck.deck. Calls card_movement() function to visually and digitally move card to the deck.
    def visual_deck_update(self, current_card, card_num = None, list_location = None):
        self.card_movement(self.deck_location, current_card)
        current_card.display_layer = len(deck.MasterDeck.deck) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'discard_pile' whenever a card is appended to the MasterDeck.discard_pile. Calls card_movement() function to visually and digitally move card to the discard pile.
    def visual_discard_pile_update(self, current_card, card_num = None, list_location = None):
        self.card_movement(self.discard_pile_location, current_card)
        current_card.display_layer = len(deck.MasterDeck.discard_pile) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p1_hand' whenever a card is appended to the player.P1.hand. Calls card_movement() function to visually and digitally move card to player.P1.hand.
    def visual_p1_hand_update(self, current_card, card_num = None, list_location = None):
        self.card_movement(self.p1_hand_next_location, current_card)
        current_card.display_layer = len(player.P1.hand) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p2_hand' whenever a card is appended to the player.P2.hand. Calls card_movement() function to visually and digitally move card to player.P2.hand.
    def visual_p2_hand_update(self, current_card, card_num = None, list_location = None):
        self.card_movement(self.p2_hand_next_location, current_card)
        current_card.display_layer = len(player.P2.hand) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p1_play_cards' whenever a card is appended to the player.P1.hand. Calls card_movement() function to visually and digitally move card to player.P1.play_cards.
    def visual_p1_play_cards_update(self, item, card_num = None, list_location = None):
        if type(item) == list:
            # Below Line - FOR NEW METHOD OF GIVING EACH LIST/MELD A SPECIFIED LOCATION FOR REFERENCE WHENEVER ADDING CARDS TO THEM FOR WHEN ITEM == CARDS.
            meld_num = len(player.P1.play_cards)
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            item.list_location = [self.p1_play_cards_start_location[0] + x_val_increase, self.p1_play_cards_start_location[1]]
            card_num = 0
            for current_card in item:
                prior_time = time.time()
                y_val_increase = card_num * 20
                p1_play_cards_next_location = [self.p1_play_cards_start_location[0] + x_val_increase, self.p1_play_cards_start_location[1] + y_val_increase]
                self.card_movement(p1_play_cards_next_location, current_card)
                current_card.display_layer = card_num + 1
                card_num += 1
                current_time = time.time()
                print("p1_play_cards list", current_time - prior_time)
        elif type(item) == card.Card:
            prior_time = time.time()
            y_val_increase = card_num * 20
            p1_play_cards_next_location = [list_location[0], list_location[1] + y_val_increase]
            self.card_movement(p1_play_cards_next_location, item)
            item.display_layer = card_num + 1
            current_time = time.time()
            print("p1_play_cards cards", current_time - prior_time)
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p1_play_cards' whenever a card is appended to player.P2.play_cards. Calls card_movement() function to visually and digitally move card to the player.P2.play_cards.
    def visual_p2_play_cards_update(self, item):
        if type(item) == list:
            meld_num = len(player.P2.play_cards)
            card_num = 0
            for current_card in item:
                prior_time = time.time()
                x_val_increase = meld_num * (self.card_width_height[0] + 20)
                y_val_increase = card_num * 20
                p2_play_cards_next_location = [self.p2_play_cards_start_location[0] + x_val_increase, self.p2_play_cards_start_location[1] + y_val_increase]
                self.card_movement(p2_play_cards_next_location, current_card)
                current_card.display_layer = card_num + 1
                card_num += 1
                current_time = time.time()
                print("p2_play_cards list", current_time - prior_time)
        elif type(item) == card.Card:
            prior_time = time.time()
            meld_num = len(player.P2.play_cards)
            card_num = 0
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            y_val_increase = card_num * 20
            p2_play_cards_next_location = [self.p2_play_cards_start_location[0] + x_val_increase, self.p2_play_cards_start_location[1] + y_val_increase]
            self.card_movement(p2_play_cards_next_location, item)
            item.display_layer = len(player.P2.play_cards) + 1
            card_num += 1
            current_time = time.time()
            print("p2_play_cards cards", current_time - prior_time)
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p1_melds' whenever a card is appended to player.P1.melds. Calls card_movement() function to visually and digitally move card to the player.P1.melds.
    def visual_p1_melds_update(self, item):
        if type(item) == list:
            meld_num = len(player.P1.melds)
            card_num = 0
            for current_card in item:
                prior_time = time.time()
                x_val_increase = meld_num * (self.card_width_height[0] + 20)
                y_val_increase = card_num * 20
                p1_melds_next_location = [self.p1_melds_start_location[0] + x_val_increase, self.p1_melds_start_location[1] + y_val_increase]
                self.card_movement(p1_melds_next_location, current_card)
                current_card.display_layer = card_num + 1
                card_num += 1
                current_time = time.time()
                print("p1_melds list", current_time - prior_time)
        elif type(item) == card.Card:
            prior_time = time.time()
            meld_num = len(player.P1.melds)
            card_num = 0
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            y_val_increase = card_num * 20
            p1_melds_next_location = [self.p1_melds_start_location[0] + x_val_increase, self.p1_melds_start_location[1] + y_val_increase]
            self.card_movement(p1_melds_next_location, item)
            item.display_layer = len(player.P1.melds) + 1
            card_num += 1
            current_time = time.time()
            print("p1_melds card", current_time - prior_time)
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p2_melds' whenever a card is appended to player.P2.melds. Calls card_movement() function to visually and digitally move card to the player.P2.melds.
    def visual_p2_melds_update(self, item):
        if type(item) == list:
            meld_num = len(player.P2.melds)
            card_num = 0
            for current_card in item:
                prior_time = time.time()
                x_val_increase = meld_num * (self.card_width_height[0] + 20)
                y_val_increase = card_num * 20
                p2_melds_next_location = [self.p2_melds_start_location[0] + x_val_increase, self.p2_melds_start_location[1] + y_val_increase]
                self.card_movement(p2_melds_next_location, current_card)
                current_card.display_layer = card_num + 1
                card_num += 1
                current_time = time.time()
                print("p2_melds list", current_time - prior_time)
        elif type(item) == card.Card:
            prior_time = time.time()
            meld_num = len(player.P2.melds)
            card_num = 0
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            y_val_increase = card_num * 20
            p2_melds_next_location = [self.p2_melds_start_location[0] + x_val_increase, self.p2_melds_start_location[1] + y_val_increase]
            self.card_movement(p2_melds_next_location, item)
            item.display_layer = len(player.P2.melds) + 1
            card_num += 1
            current_time = time.time()
            print("p2_melds card", current_time - prior_time)
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p1_red_3_meld' whenever a card is appended to player.P1.red_3_meld. Calls card_movement() function to visually and digitally move card to player.P1.red_3_meld.
    def visual_p1_red_3_meld_update(self, current_card):
        x_val_increase = len(player.P1.melds) * (self.card_width_height[0] + 20)
        y_val_increase = len(player.P1.red_3_meld) * 20
        red_3_meld_next_location = [self.p1_melds_start_location[0] + x_val_increase, self.p1_melds_start_location[1] - 10 + y_val_increase]
        self.card_movement(red_3_meld_next_location, current_card)
        current_card.display_layer = len(player.P1.red_3_meld) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p2_red_3_meld' whenever a card is appended to player.P2.red_3_meld. Calls card_movement() function to visually and digitally move card to player.P2.red_3_meld.
    def visual_p2_red_3_meld_update(self, current_card):
        x_val_increase = len(player.P2.melds) * (self.card_width_height[0] + 20)
        y_val_increase = len(player.P2.red_3_meld) * 20
        red_3_meld_next_location = [self.p2_melds_start_location[0] + x_val_increase, self.p2_melds_start_location[1] - 10 + y_val_increase]
        self.card_movement(red_3_meld_next_location, current_card)
        current_card.display_layer = len(player.P2.red_3_meld) + 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Locate = Locations()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - Creates a dictionary attribute for Locations that includes all of the associated functions for updating visuals for the various card groups.
Locations.func_dict = {'deck': Locate.visual_deck_update, 'discard_pile': Locate.visual_discard_pile_update, 'p1_hand': Locate.visual_p1_hand_update, 'p2_hand': Locate.visual_p2_hand_update, 'p1_play_cards': Locate.visual_p1_play_cards_update, 'p2_play_cards': Locate.visual_p2_play_cards_update, 'p1_melds': Locate.visual_p1_melds_update, 'p2_melds': Locate.visual_p2_melds_update, 'p1_red_3_meld': Locate.visual_p1_red_3_meld_update, 'p2_red_3_meld': Locate.visual_p2_red_3_meld_update}
