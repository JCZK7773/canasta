import math
import pygame
import time
import player
import card
import deck
import game
import locations
import customappendlist
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Locations():
    def __init__(self):
        self.visible_top = 0
        self.visible_bottom = 1009
        self.visible_left = 0
        self.visible_right = 1919
        # Below Line - [959.5, 504.5] to be exact. HAS TO BE ROUNDED OR WILL CAUSE A B U G!!
        self.visible_center = [round(self.visible_right / 2, 0), round(self.visible_bottom / 2, 0)]
        self.top_left_visible_from_center = [51, 71]
        self.card_width_height = [100, 140]
        self.deck_loc = [self.visible_center[0] - (self.card_width_height[0] / 2) - 10 , self.visible_top + 120]
        self.discard_pile_loc = [self.deck_loc[0] + self.card_width_height[0] + 20, self.deck_loc[1]]
        self.p1_hand_start_loc = [64, 330]
        self.p2_hand_start_loc = [self.visible_center[0] + 64, self.p1_hand_start_loc[1]]
        self.p1_play_cards_start_loc = [80, 540]
        self.p2_play_cards_start_loc = [self.visible_center[0] + 80, self.p1_play_cards_start_loc[1]]
        self.p1_melds_start_loc = [80, 830]
        self.p2_melds_start_loc = [self.visible_center[0] + 80, self.p1_melds_start_loc[1]]
        self.card_group_name_dict = {'deck': deck.MasterDeck.deck,
                                    'discard_pile': deck.MasterDeck.discard_pile,
                                    'P1.hand': player.P1.hand,
                                    'P2.hand': player.P2.hand,
                                    'P1.play_cards': player.P1.play_cards,
                                    'P2.play_cards': player.P2.play_cards,
                                    'P1.melds': player.P1.melds,
                                    'P2.melds': player.P2.melds,
                                    'P1.red_3_meld': player.P1.red_3_meld,
                                    'P2.red_3_meld': player.P2.red_3_meld}
        # Below Line - For whatever reason, this dictionary has to be called in customappendlist.CustomAppendList.append to be updated, or else the locations are not calculated property.
        self.card_group_loc_dict = {'deck': self.deck_loc, 'discard_pile': self.discard_pile_loc, 'P1.hand': self.p1_hand_next_loc, 'P2.hand': self.p2_hand_next_loc, 'P1.play_cards': self.p1_play_cards_start_loc, 'P2.play_cards': self.p2_play_cards_start_loc, 'P1.melds': self.p1_melds_start_loc, 'P2.melds': self.p2_melds_start_loc}
        # Below Line - The number used in self.text_name_loc_dict to adjust how far above a card group the text display is situated.
        self.y_reduce_num = 93
        # Below Dict - The text location dictionary which defines the visual locations for all of the various text displays. Accessed by game.Game.
        self.text_name_loc_dict = {'Deck': [self.deck_loc[0], self.deck_loc[1] - self.y_reduce_num],
                                  'Discard Pile': [self.discard_pile_loc[0], self.discard_pile_loc[1] - self.y_reduce_num],
                                  'p1_hand_text_loc': [self.p1_hand_start_loc[0] + 12, self.p1_hand_start_loc[1] - self.y_reduce_num],
                                  'p2_hand_text_loc': [self.p2_hand_start_loc[0] + 12, self.p2_hand_start_loc[1] - self.y_reduce_num],
                                  'p1_play_cards_text_loc': [self.p1_play_cards_start_loc[0] + 20, self.p1_play_cards_start_loc[1] - self.y_reduce_num],
                                  'p2_play_cards_text_loc': [self.p2_play_cards_start_loc[0] + 20, self.p2_play_cards_start_loc[1] - self.y_reduce_num],
                                  'p1_melds_text_loc': [self.p1_melds_start_loc[0], self.p1_melds_start_loc[1] - self.y_reduce_num],
                                  'p2_melds_text_loc': [self.p2_melds_start_loc[0], self.p2_melds_start_loc[1] - self.y_reduce_num],
                                  'p1_red_3_meld_text_loc': [-100, 0],
                                  'p2_red_3_meld_text_loc': [-100, 0],
                                  # Below Section - Make it so that whenever a value is set for this (through progression.py) make it calculate and assign the rect and it's center based on the size of the rect so that it will always properly display on the screen.
                                  'p1_player_name_text_loc': [10, 10],
                                  'p2_player_name_text_loc': [self.visible_center[0] + 10, 10],
                                  'progression_text_loc': self.visible_center}
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
    # Below Function - Called by card_movement(). Detects the game_state, which is assigned in the various progression.py loops. This determines which version of draw_window() will be called, which renders a different set of Sprites, rects, lines, etc. to conform to the game progress content.
    def draw_window_func(self):
        # print("draw_window_func")
        if game.game.game_state == 'the_draw_1':
            game.game.draw_window_the_draw_1()
        elif game.game.game_state == 'draw_window_the_draw_2':
            game.game.draw_window_the_draw_2()
        elif game.game.game_state == 'main':
            game.game.draw_window_main()
        # Below Line - For test_run.test_run() only. For testing card movements and features.
        elif game.game.game_state == 'test_run':
            game.game.draw_window_main()
        # -------------------------------------
    # Below Function - Dynamically moves a single passed in card from it's current location to the desired location (loc) one unit at a time, using a formula (ratio) to move the card in a straight line. Calls player.P2 at the end of the function, which visually updates the card's on-screen location.
    def card_movement(self, loc, current_card):
        # print("card_movement")
        # Below Section - For testing. Trying to find the cause of inconsistent card movement times.
        prior_time = time.time()
        iter_num = 0
        draw_window_calls_num = 0
        total_distance = round(math.sqrt((loc[0] - current_card.x) ** 2 + (loc[1] - current_card.y) ** 2), 2)
        # -------------------------------------
        # Below Section - Handles the assignment of proper card.image depending on whether or not it is going to the deck or not, and whether or not it already has the proper face_down or face_up image set.
        if loc == self.card_group_loc_dict['deck']:
            # Below Line - I do NOT need to add .get_rect() here. This is NOT required.
            current_card.image = card.Card.face_down_image
        else:
            if current_card.image == card.Card.face_down_image:
                # Below Line - I do NOT need to add .get_rect() here. This is NOT required.
                current_card.image = current_card.face_up_image
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
            ratio = round((y_difference / x_difference), 3)
            while [int(current_card.x), int(current_card.y)] != loc:
                iter_num += 1
                if x_lesser == True and int(current_card.x) != int(loc[0]):
                    current_card.x += 1
                elif x_lesser == False and int(current_card.x) != int(loc[0]):
                    current_card.x -= 1
                if y_lesser == True and int(current_card.y) != int(loc[1]):
                    prior_y = current_card.y
                    current_card.y += ratio
                    current_y = current_card.y
                    if int(prior_y) < int(current_y):
                        draw_window_calls_num += 1
                        self.draw_window_func()
                elif y_lesser == False and int(current_card.y) != int(loc[1]):
                    prior_y = current_card.y
                    current_card.y -= ratio
                    current_y = current_card.y
                    if int(prior_y) > int(current_y):
                        draw_window_calls_num += 1
                        self.draw_window_func()
                elif y_lesser == None:
                    pass
                    ###### Below Line - Bugged for some reason. Can't figure it out. Takes 3 seconds to move the card. Keep disabled.  Added for the instance in which the y-coordinate is == final y-coordinate, but x-coordinate still needs to be changed.
                    # self.draw_window_func()
        # -------------------------------------
        elif int(y_difference) > int(x_difference):
            ratio = round((x_difference / y_difference), 3)
            while [int(current_card.x), int(current_card.y)] != loc:
                iter_num += 1
                if y_lesser == True and int(current_card.y) != int(loc[1]):
                    current_card.y += 1
                elif y_lesser == False and int(current_card.y) != int(loc[1]):
                    current_card.y -= 1
                if x_lesser == True and int(current_card.x) != int(loc[0]):
                    prior_x = current_card.x
                    current_card.x += ratio
                    current_x = current_card.x
                    if int(prior_x) < int(current_x):
                        draw_window_calls_num += 1
                        self.draw_window_func()
                elif x_lesser == False and int(current_card.x) != int(loc[0]):
                    prior_x = current_card.x
                    current_card.x -= ratio
                    current_x = current_card.x
                    if int(prior_x) > int(current_x):
                        draw_window_calls_num += 1
                        self.draw_window_func()
                elif x_lesser == None:
                    pass
                    ###### Below Line - Bugged for some reason. Can't figure it out. Takes 3 seconds to move the card. Keep disabled. Added for the instance in which the y-coordinate is == final y-coordinate, but x-coordinate still needs to be changed.
                    # self.draw_window_func()
        # -------------------------------------
        # Below Section - For the rare instance when both the current x & y coordinates are the same distance from the final location's x & y coordinates.
        elif int(y_difference) == int(x_difference):
            while [int(current_card.x), int(current_card.y)] != loc:
                iter_num += 1
                if x_lesser == True:
                    current_card.x += 1
                else:
                    current_card.x -= 1
                if y_lesser == True:
                    current_card.y += 1
                else:
                    current_card.y -= 1
                draw_window_calls_num += 1
                self.draw_window_func()
        # -------------------------------------
        # Below Section - For testing. Trying to figure out the cause of inconsistent times for card movements.
        current_time = time.time()
        final_time = round(current_time - prior_time, 2)
        if final_time != 0.0:
            print(f"final_time = {final_time}")
            print(f"total_distance / final_time = {round(total_distance / final_time, 2)}")
            print(f"iter_num = {iter_num}")
            print(f"draw_window_calls_num / total_distance = {draw_window_calls_num / total_distance}")
            print(f"ratio = {ratio}")
            print(f"iter_num / final_time = {round(iter_num / final_time, 2)}")
            print(f"ratio / final_time = {round(ratio / final_time, 2)}")
            print("**********************************")
        # First Half of List Iteration
            # Highest Performance Card Info
                # Lowest Time = 0.01
                # Iter_num = 1,000
                # Ratio = .001
                # Iter_num/Final_time = 100,000
            # Lowest Performance Card Info
                # Highest Time = 1.1
                # Iter_num = 288
                # Ratio = .976
                # Iter_num/Final_time = 261
        # Second Half of List Iteration
            # Highest Performance Card Info
                # Lowest Time = 0.01
                # Iter_num = 501
                # Ratio = .002
                # Iter_num/Final_time = 50,100
            # Lowest Performance Card Info
                # Highest Time = 1.71
                # Iter_num = 712
                # Ratio = .608
                # Iter_num/Final_time = 424
        # Conclusions
            # Higher the Ratio = Higher the Total Time
            # Higher the draw_window_calls_num = Higher the Total Time. More calls; more time.
    # -------------------------------------
    # Below Function - Called by func_dict via key 'deck', 'discard_pile', and 'hand' whenever a card is appended to the MasterDeck.deck, MasterDeck.discard_pile, or P1.hand/P2.hand. Calls card_movement() function to visually and digitally move card to the proper location.
    def visual_deck_discard_hand_update(self, card_group_name, current_card):
        # print("visual_deck_discard_hand_update")
        self.card_movement(self.card_group_loc_dict[card_group_name], current_card)
        current_card.display_layer = len(self.card_group_name_dict[card_group_name]) + 1
    # -------------------------------------
    # Below Function - Detects where cards should be placed within a meld, and detects and visually updates the proper visual locations associated with this. Called by visual_meld_update(). Calls canasta_find_face_up_card() at the end of the function. Created this function because it is used in two places: for melds AND cards. Detects the length of the melds and determines proper visual placement.
    def card_num_canasta_detect(self, card_group_name, card, meld, meld_num, card_num):
        print("card_num_canasta_detect")
        # -------------------------------------
        # Below Section - Assigns variables associated with the meld's & cards' location.
        y_val_increase = card_num * 18
        x_val_increase = meld_num * (self.card_width_height[0] + 20)
        meld_group_loc = self.card_group_loc_dict[card_group_name]
        meld_loc = [meld_group_loc[0] + x_val_increase, meld_group_loc[1]]
        # -------------------------------------
        # Below Section - For all instances in which the card_num < 6. Visually places the cards in the regular staggered manner.
        if card_num <= 6:
            card_next_loc = [self.card_group_loc_dict[card_group_name][0] + x_val_increase, self.card_group_loc_dict[card_group_name][1] + y_val_increase]
            self.card_movement(card_next_loc, card)
            card.display_layer = card_num
        # -------------------------------------
        # Below Line - For all instances in which the cards are part of a 7 or more card canasta.
        if card_num >= 6:
            # Below Section - If current_card is the 7th card (making it a canasta). First places the card in the 7th staggered location, then collapses the previously placed cards into a stack at the starting list_loc.
            if card_num == 6:
                for preex_card in meld[0:card_num + 1]:
                    prior_disp_layer = preex_card.display_layer
                    self.card_movement(meld_loc, preex_card)
                    preex_card.display_layer = prior_disp_layer
            # -------------------------------------
            # Below Section - For the 8th, 9th, & 10th cards in the meld, if the meld is that big. Places them in the stacked top spot (item.list_loc).
            elif card_num > 6:
                self.card_movement(meld_loc, card)
            # -------------------------------------
            # Below Section - If current_card is the last card in the meld. Assigns mixed to 0 to be a reference variable to be changed to 1 if the canasta has a wild card in it. Places it in the item.list_loc, then checks through the meld for wild cards to determine whether or not it is a natural or mixed canasta.
            if card == meld[-1]:
                mixed = 0
                for wild_card in deck.MasterDeck.wild_cards:
                    for card in meld:
                        if wild_card[0] == card.rank:
                            mixed = 1
                            break
                    if mixed == 1:
                        break
            # -------------------------------------
                # Below Section - Finds the face-up card for the canasta based on whether or not it is mixed (black-faced) or natural (red-faced).
                suits = ['Heart', 'Diamond']
                if mixed == 1:
                    suits = ['Spade', 'Club']
                reversed_item = meld[::-1]
                for card in reversed_item:
                    if card.suit == suits[0] or card.suit == suits[1]:
                        card.changed_display_layer = 1
                        card.display_layer = card_num + 1
                        game.game.draw_window_main()
                        card.changed_display_layer = 0
                        break
    # -------------------------------------
    # Below Function - Called by funct_dict via keys associated with all meld groups. Handles proper meld and card locations movements for all meld groups.
    def visual_meld_update(self, card_group_name, item, meld_num = None, card_num = None):
        print("visual_meld_update")
        # -------------------------------------
        # Below line - If you are adding from a completed meld.
        if type(item) == customappendlist.CustomAppendList:
            print("customappendlist.CustomAppendList")
            # Below Section - Sets card_num to 0, which will be increased by 1 for each card iteration and begins iteration through the meld.
            card_num = 0
            for cur_card in item:
                self.card_num_canasta_detect(card_group_name, cur_card, item, meld_num, card_num)
                # Below Section - Applies to all cards in the meld. Increases the card.display_layer & card_num by 1 for proper visual locations.
                cur_card.display_layer = card_num
                card_num += 1
                # -------------------------------------
        # Below Line - If you are adding cards to a preexisiting meld.
        elif type(item) == card.Card:
            print("card.Card")
            meld = player.Player.meld_group_dict[card_group_name][meld_num]
            self.card_num_canasta_detect(card_group_name, item, meld, meld_num, card_num)
    # -------------------------------------
    # Below Function - Called by func_dict via key 'red_3_meld' whenever a card is appended to player.P1.red_3_meld. Calls card_movement() function to visually and digitally move card to player.P1.red_3_meld.
    def visual_red_3_meld_update(self, card_group_name, current_card):
        print("visual_red_3_meld_update")
        # -------------------------------------
        # Below Section - Determines the player based on the card_group_name and assigns the associated player's (x, y) starting coordinates.
        cur_player = player.P1
        x_start_loc = self.p1_melds_start_loc[0]
        y_start_loc = self.p1_melds_start_loc[1]
        if 'P2' in card_group_name:
            cur_player = player.P2
            x_start_loc = self.p2_melds_start_loc[0]
            y_start_loc = self.p2_melds_start_loc[1]
        # -------------------------------------
        x_val_increase = len(cur_player.melds) * (self.card_width_height[0] + 20)
        y_val_increase = len(cur_player.red_3_meld) * 18
        red_3_meld_next_loc = [x_start_loc + x_val_increase, y_start_loc - 40 + y_val_increase]
        self.card_movement(red_3_meld_next_loc, current_card)
        current_card.display_layer = len(cur_player.red_3_meld) + 1
    # -------------------------------------
    # Below Function - Called by progression.the_draw_2() to visually lay out all of the cards in the MasterDeck so that the player can pick the card that they want to choose for determining the first player.
    def the_draw_anim(self):
        print("the_draw_anim")
        # -------------------------------------
        prior_time = time.time()
        # -------------------------------------
        next_card_loc = self.top_left_visible_from_center
        # -------------------------------------
        # Below Section - Iterator method. Performance time for function - 135.76 vs generator method performance - 137.33.
        for current_card in deck.MasterDeck.deck:
            self.card_movement(next_card_loc, current_card)
            next_card_loc[0] += 17
            next_card_loc[1] += 10
        # -------------------------------------
        current_time = time.time()
        final_time = round(current_time - prior_time, 2)
        print(f"the_draw_anim() final_time = {final_time}")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Locate = Locations()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - Creates a dictionary attribute for Locations that includes all of the associated functions for updating visuals for the various card groups.
Locations.func_dict = {'deck': Locate.visual_deck_discard_hand_update, 'discard_pile': Locate.visual_deck_discard_hand_update, 'P1.hand': Locate.visual_deck_discard_hand_update, 'P2.hand': Locate.visual_deck_discard_hand_update, 'P1.play_cards': Locate.visual_meld_update, 'P2.play_cards': Locate.visual_meld_update, 'P1.melds': Locate.visual_meld_update, 'P2.melds': Locate.visual_meld_update, 'P1.red_3_meld': Locate.visual_red_3_meld_update, 'P2.red_3_meld': Locate.visual_red_3_meld_update}
