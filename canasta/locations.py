import pygame
import player
import card
import deck
import game
import customappendlist
import canasta_pygame
import time
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Locations():
    def __init__(self):
        self.deck_loc = [910, 540]
        self.discard_pile_loc = [1010, 540]
        self.p1_hand_start_loc = [100, 420]
        self.p2_hand_start_loc = [1110, 420]
        self.p1_melds_start_loc = [100, 820]
        self.p2_melds_start_loc = [1110, 820]
        self.p1_play_cards_start_loc = [100, 510]
        self.p2_play_cards_start_loc = [1110, 510]
        self.top_left_visible = [50, 70]
        self.center = [1010, 610]
        self.card_width_height = [100, 140]
        self.card_group_name_dict = {'deck': deck.MasterDeck.deck, 'discard_pile': deck.MasterDeck.discard_pile, 'P1.hand': player.P1.hand, 'P2.hand': player.P2.hand, 'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds, 'P1.red_3_meld': player.P1.red_3_meld, 'P2.red_3_meld': player.P2.red_3_meld}
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
        print(len(self.card_group_name_dict[card_group_name]))
        self.card_movement(self.card_group_loc_dict[card_group_name], current_card)
        current_card.display_layer = len(self.card_group_name_dict[card_group_name]) + 1
    # -------------------------------------
    # Below Function - Called by funct_dict via keys associated with all meld groups. Handles proper meld and card locations movements for all meld groups.
    def visual_meld_group_update(self, card_group_name, item, meld_num = None, card_num = None):
        print("visual_meld_group_update")
        # -------------------------------------
        # Below Function - Created this function because it is used in two places: for melds AND cards. Detects the length of the melds and determines proper visual placement.
        def card_num_canasta_detect(card_group_name, item, list_loc, meld_num = None, card_num = None):
            # Below Section - For all instances in which the card_num < 6. Visually places the cards in the regular staggered manner.
            if card_num <= 6:
                y_val_increase = card_num * 18
                card_next_loc = [item.list_loc[0], item.list_loc[1] + y_val_increase]
                self.card_movement(card_next_loc, current_card)
            # -------------------------------------
            # Below Line - For all instances in which the cards are part of a 7 or more card canasta.
            if card_num >= 6:
                # Below Section - If current_card is the 7th card (making it a canasta). First places the card in the 7th staggered location, then collapses the previously placed cards into a stack at the starting list_loc.
                if card_num == 6:
                    for preex_card in item[0:card_num + 1]:
                        prior_disp_layer = preex_card.display_layer
                        self.card_movement(item.list_loc, preex_card)
                        preex_card.display_layer = prior_disp_layer
                # -------------------------------------
                # Below Section - For the 8th, 9th, & 10th cards in the meld, if the meld is that big. Places them in the stacked top spot (item.list_loc).
                elif card_num > 6:
                    self.card_movement(item.list_loc, current_card)
                # -------------------------------------
                # Below Section - If current_card is the last card in the meld. Assigns mixed to 0 to be a reference variable to be changed to 1 if the canasta has a wild card in it. Places it in the item.list_loc, then checks through the meld for wild cards to determine whether or not it is a natural or mixed canasta.
                if current_card == item[-1]:
                    mixed = 0
                    for wild_card in deck.MasterDeck.wild_cards:
                        for card in item:
                            if wild_card[0] == card.rank:
                                mixed = 1
                # -------------------------------------
                    # Below Section - If canasta is mixed. Finds a black-faced card to be used as the face-up card for the canasta to distinguish it as mixed.
                    if mixed == 1:
                        reversed_item = item[::-1]
                        for card in reversed_item:
                            if card.suit == 'Spade' or card.suit == 'Club':
                                card.changed_display_layer = 1
                                card.display_layer = card_num + 1
                                game.draw_window()
                                card.changed_display_layer = 0
                                break
                    # -------------------------------------
                    # Below Section - If canasta is mixed. Finds a red-faced card to be used as the face-up card for the canasta to distinguish it as natural.
                    else:
                        reversed_item = item[::-1]
                        for card in reversed_item:
                            if card.suit == 'Heart' or card.suit == 'Diamond':
                                card.changed_display_layer = 1
                                card.display_layer = card_num + 1
                                game.draw_window()
                                card.changed_display_layer = 0
                                break
        # -------------------------------------
        if type(item) == customappendlist.CustomAppendList:
            print("customappendlist.CustomAppendList")
            # Below Section - Sets the x_val_increase to account for the meld_num in the list of melds for proper visual placement, and then assigns the item.list_loc to be the starting meld location for the associated player accounting for the just-calculated x_val_increase.
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            item.list_loc = [self.card_group_loc_dict[card_group_name][0] + x_val_increase, self.card_group_loc_dict[card_group_name][1]]
            # -------------------------------------
            # Below Section - Sets card_num to 0, which will be increased by 1 for each card iteration and begins iteration through the meld.
            card_num = 0
            for current_card in item:
            # -------------------------------------
                card_num_canasta_detect(card_group_name, item, item.list_loc, meld_num = None, card_num = card_num)
                # Below Section - Applies to all cards in the meld. Increases the card.display_layer & card_num by 1 for proper visual locations.
                current_card.display_layer = card_num
                card_num += 1
                pygame.event.wait(2000)
            # -------------------------------------
        elif type(item) == card.Card:
            print("card.Card")
            # Below Section - Handles cards added to melds that are to be placed in the standard, staggered manner. For melds that are NOT canastas.
            x_val_increase = meld_num * (self.card_width_height[0] + 20)
            y_val_increase = card_num * 18
            card_next_loc = [self.card_group_loc_dict[card_group_name][0] + x_val_increase, self.card_group_loc_dict[card_group_name][1] + y_val_increase]
            self.card_movement(card_next_loc, item)
            item.display_layer = card_num
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
