import pygame
import game
import locations
import deck
# -------------------------------------
class Player(): # ****
    def __init__(self, name): # ****
        self._name = name # ****
        self.draw_card = None
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
        self.meld_group_dict = {} # Assigned in customappendlist for proper referencing/updating.
    # -------------------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if self.name == 'Player 1':
            game.game.p1_player_name_text_obj = game.game.font.render(f"Player 1: {val}", True, (255, 255, 255), game.game.dark_blue_color)
            game.game.p1_player_name_text_obj_rect = game.game.p1_player_name_text_obj.get_rect()
            game.game.p1_player_name_text_obj_rect.left = locations.Locate.text_name_loc_dict['p1_player_name_text_loc'][0]
            game.game.p1_player_name_text_obj_rect.top = locations.Locate.text_name_loc_dict['p1_player_name_text_loc'][1]
        else:
            game.game.p2_player_name_text_obj = game.game.font.render(f"Player 2: {val}", True, (255, 255, 255), game.game.dark_blue_color)
            game.game.p2_player_name_text_obj_rect = game.game.p2_player_name_text_obj.get_rect()
            game.game.p2_player_name_text_obj_rect.right = locations.Locate.text_name_loc_dict['p2_player_name_text_loc'][0]
            game.game.p2_player_name_text_obj_rect.top = locations.Locate.text_name_loc_dict['p2_player_name_text_loc'][1]
        # -------------------------------------
        self._name = val
    # -------------------------------------
    @property # ****
    def draw_card_val(self): # ****
        return deck.MasterDeck.draw_ranks.get(self.draw_card.rank) # ****
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
            if (card.rank, card.suit) in deck.Deck().wild_cards: # ****
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
                        if (card.rank, card.suit) in deck.Deck().wild_cards: # ****
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
                            if (card.rank, card.suit) in deck.Deck().wild_cards: # ****
                                wild_card_canasta_check_count += 1 # ****
                            # -------------------------------------
                            round_score += deck.Deck().ranks.get(card.rank) # ****
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
                    round_score -= deck.Deck().ranks.get(card.rank) # ****
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
players = [P1, P2] # ****
