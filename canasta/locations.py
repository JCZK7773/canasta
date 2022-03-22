import player
import card
import deck
import game
import customappendlist
import time
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Locations():
    def __init__(self):
        self.deck_loc = [910, 540]
        self.discard_pile_loc = [1010, 540]
        self.p1_hand_start_loc = [100, 420]
        self.p2_hand_start_loc = [1110, 420]
        self.p1_melds_start_loc = [100, 800]
        self.p2_melds_start_loc = [1110, 800]
        self.p1_play_cards_start_loc = [100, 510]
        self.p2_play_cards_start_loc = [1110, 510]
        self.top_left_visible = [50, 70]
        self.center = [1010, 610]
        self.card_width_height = [100, 140]
        self.card_group_name_dict = {'deck': deck.MasterDeck.deck, 'discard_pile': deck.MasterDeck.discard_pile, 'P1.hand': player.P1.hand, 'P2.hand': player.P2.hand, 'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds, 'P1.red_3_meld': player.P1.red_3_meld, 'P2.red_3_meld': player.P2.red_3_meld}
        self.meld_group_dict = {'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds, 'P1.red_3_meld': player.P1.red_3_meld, 'P2.red_3_meld': player.P2.red_3_meld}
        self.card_group_loc_dict = {'P1.hand': self.p1_hand_next_loc, 'P2.hand': self.p2_hand_next_loc, 'P1.play_cards': self.p1_play_cards_start_loc, 'P2.play_cards': self.p2_play_cards_start_loc, 'P1.melds': self.p1_melds_start_loc, 'P2.melds': self.p2_melds_start_loc}
    # -------------------------------------
    # Below Function - Dynamically assigns player.P1's hand location.
    @property
    def p1_hand_next_loc(self):
        if len(player.P1.hand) == 0:
            return self.p1_hand_start_loc
        else:
            x_val_increase = len(player.P1.hand) * 20
            p1_hand_next_loc = [self.p1_hand_start_loc[0] + x_val_increase, self.p1_hand_start_loc[1]]
            return p1_hand_next_loc
    # -------------------------------------
    # Below Function - Dynamically assigns player.P2's hand location.
    @property
    def p2_hand_next_loc(self):
        if len(player.P2.hand) == 0:
            return self.p2_hand_start_loc
        else:
            x_val_increase = len(player.P2.hand) * 20
            p2_hand_next_loc = [self.p2_hand_start_loc[0] + x_val_increase, self.p2_hand_start_loc[1]]
            return p2_hand_next_loc
    # -------------------------------------
    # Below Function - Dynamically moves a single passed in card from it's current location to the desired location (loc) one unit at a time, using a formula (ratio) to move the card in a straight line. Calls player.P2 at the end of the function, which visually updates the card's on-screen location.
    def card_movement(self, loc, current_card):
        print("card_movement")
        # Below Section - For testing. Trying to find the cause of inconsistent card movement times.
        prior_time = time.time()
        # -------------------------------------
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
            ratio = round((y_difference / x_difference), 2)
            while [int(current_card.x), int(current_card.y)] != loc:
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
            ratio = round((x_difference / y_difference), 2)
            while [int(current_card.x), int(current_card.y)] != loc:
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
            while [int(current_card.x), int(current_card.y)] != loc:
                current_card.x += 1
                current_card.y += 1
                game.draw_window()
        # -------------------------------------
        # Below Section - For testing. Trying to figure out the cause of inconsistent times for card movements.
        current_time = time.time()
        print(round(current_time - prior_time, 2))
    # -------------------------------------
    # Below Function - Called by func_dict via key 'deck' whenever a card is appended to the MasterDeck.deck. Calls card_movement() function to visually and digitally move card to the deck.
    def visual_deck_update(self, current_card):
        print("visual_deck_update")
        self.card_movement(self.deck_loc, current_card)
        current_card.display_layer = len(deck.MasterDeck.deck) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'discard_pile' whenever a card is appended to the MasterDeck.discard_pile. Calls card_movement() function to visually and digitally move card to the discard pile.
    def visual_discard_pile_update(self, current_card):
        print("visual_discard_pile_update")
        self.card_movement(self.discard_pile_loc, current_card)
        current_card.display_layer = len(deck.MasterDeck.discard_pile) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'hand' whenever a card is appended to a player's hand. Calls card_movement() function to visually and digitally move card to associated player's hand.
    def visual_hand_update(self, card_group_name, current_card):
        print("visual_hand_update")
        self.card_movement(self.card_group_loc_dict[card_group_name], current_card)
        current_card.display_layer = len(self.card_group_name_dict[card_group_name]) + 1
    # -------------------------------------
    # Below Function - Called by funct_dict via keys associated with all meld groups. Handles proper meld and card locations movements for all meld groups.
    def visual_meld_group_update(self, card_group_name, item, meld_num = None, card_num = None):
        print("visual_meld_group_update")
        if type(item) == customappendlist.CustomAppendList:
            print("customappendlist.CustomAppendList")
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            item.list_loc = [self.card_group_loc_dict[card_group_name][0] + x_val_increase, self.card_group_loc_dict[card_group_name][1]]
            card_num = 0
            for current_card in item:
                y_val_increase = card_num * 18
                card_next_loc = [item.list_loc[0], item.list_loc[1] + y_val_increase]
                self.card_movement(card_next_loc, current_card)
                current_card.display_layer = card_num + 1
                card_num += 1
        elif type(item) == card.Card:
            print("card.Card")
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            y_val_increase = card_num * 18
            card_next_loc = [self.card_group_loc_dict[card_group_name][0] + x_val_increase, self.card_group_loc_dict[card_group_name][1] + y_val_increase]
            self.card_movement(card_next_loc, item)
            item.display_layer = card_num + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p1_red_3_meld' whenever a card is appended to player.P1.red_3_meld. Calls card_movement() function to visually and digitally move card to player.P1.red_3_meld.
    def visual_p1_red_3_meld_update(self, current_card):
        print("visual_p1_red_3_meld_update")
        x_val_increase = len(player.P1.melds) * (self.card_width_height[0] + 20)
        y_val_increase = len(player.P1.red_3_meld) * 18
        red_3_meld_next_loc = [self.p1_melds_start_loc[0] + x_val_increase, self.p1_melds_start_loc[1] - 10 + y_val_increase]
        self.card_movement(red_3_meld_next_loc, current_card)
        current_card.display_layer = len(player.P1.red_3_meld) + 1
    # -------------------------------------
    # Below Function - Called by func_dict via key 'p2_red_3_meld' whenever a card is appended to player.P2.red_3_meld. Calls card_movement() function to visually and digitally move card to player.P2.red_3_meld.
    def visual_p2_red_3_meld_update(self, current_card):
        print("visual_p2_red_3_meld_update")
        x_val_increase = len(player.P2.melds) * (self.card_width_height[0] + 20)
        y_val_increase = len(player.P2.red_3_meld) * 18
        red_3_meld_next_loc = [self.p2_melds_start_loc[0] + x_val_increase, self.p2_melds_start_loc[1] - 10 + y_val_increase]
        self.card_movement(red_3_meld_next_loc, current_card)
        current_card.display_layer = len(player.P2.red_3_meld) + 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Locate = Locations()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - Creates a dictionary attribute for Locations that includes all of the associated functions for updating visuals for the various card groups.
Locations.func_dict = {'deck': Locate.visual_deck_update, 'discard_pile': Locate.visual_discard_pile_update, 'P1.hand': Locate.visual_hand_update, 'P2.hand': Locate.visual_hand_update, 'P1.play_cards': Locate.visual_meld_group_update, 'P2.play_cards': Locate.visual_meld_group_update, 'P1.melds': Locate.visual_meld_group_update, 'P2.melds': Locate.visual_meld_group_update, 'P1.red_3_meld': Locate.visual_p1_red_3_meld_update, 'P2.red_3_meld': Locate.visual_p2_red_3_meld_update}
