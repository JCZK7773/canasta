# Things to do
# 1) Write and run some thorough tests for the program to go through for finding and fixing hidden bugs.
# 2) Go through the entire script to remove all extra comments and test functions, etc.
# 3) Post on web so others can check for bugs as well.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import random # ***
import sys # ***
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{Deck().suits_symbols.get(self.suit)}"

    def __repr__(self):
        return self.__str__()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Deck():
    def __init__(self):
        self.deck = []
        self.draw_ranks = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        self.draw_suit_ranks = {'S':4, 'H':3, 'D':2, 'C':1}
        self.ranks = {'Jo':50, '2':20, '3':100, '4':5, '5':5, '6':5, '7':5, '8':10, '9':10, '10':10, 'J':10, 'Q':10, 'K':10, 'A':20}
        self.suits = ['H', 'D', 'S', 'C']
        self.suits_symbols = {'H': '♥', 'D': '♦', 'S': '♠', 'C': '♣', None: '🃟'}
        self.discard_pile = []
        self.red_3s = [('3', 'D'), ('3', 'H')]
        self.black_3s = [('3', 'C'), ('3', 'S')]
        self.wild_cards = [('2', 'D'), ('2', 'H'), ('2', 'S'), ('2', 'C'), ('Jo', None)]
        self.wild_card_discards = ['Jo', '2', '3']
         # -------------------------------------
    @property
    def face_up_discard(self):
        return self.discard_pile[-1]
    # -------------------------------------
    @property
    def discard_pile_is_frozen(self):
        for card in MasterDeck.discard_pile: # ****
            if (card.rank, card.suit) not in MasterDeck.wild_cards or (card.rank, card.suit) not in MasterDeck.black_3s: # ****
                discard_pile_is_frozen = False # ****
            else: # ****
                discard_pile_is_frozen = True # ****
        return discard_pile_is_frozen
    # -------------------------------------
    def create_deck(self):
        for rank in self.ranks:
            if rank != 'Jo':
                for suit in self.suits:
                    card = Card(rank, suit)
                    self.deck.append(card)
            else:
                for Joker in range(2):
                    card = Card(rank, None)
                    self.deck.append(card)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Player():
    def __init__(self, start_name = None):
        self.start_name = start_name
        self.name = 'Name'
        self.the_draw = None
        self.hand = []
        self.play_cards = []
        self.play_cards_wild_cards = []
        self.initial_played_card_count = 0
        self.final_played_card_count = 0
        self.red_3_meld = []
        self.black_3_meld = []
        self.melds = []
        self.len_2_temp_melds_list = []
        self.going_out = None
        self.went_out_concealed = False
        self.finished_rounds_scores = []
    # -------------------------------------
    @property
    def draw_card(self):
        if len(self.hand) > 0:
            draw_card = self.hand[0]
            return draw_card
    # -------------------------------------
    @property
    def draw_card_val(self):
        return MasterDeck.draw_ranks.get(self.draw_card.rank)
    # ------------------------------------------
    @property
    def meld_requirement(self):
        meld_requirement = 0
        if self.total_score < 0:
            meld_requirement = 15
        elif 0 <= self.total_score < 1500:
            meld_requirement = 50
        elif 1500 <= self.total_score < 3000:
            meld_requirement = 90
        elif self.total_score >= 3000:
            meld_requirement = 120
        return meld_requirement
    # ------------------------------------------
    @property
    def played_card_count(self):
        played_card_count = 0
        for meld in self.melds:
            played_card_count += len(meld)
        return played_card_count
    # ------------------------------------------
    @property
    def red_3_count(self):
        return len(self.red_3_meld)
    # -------------------------------------
    @property
    def hand_wild_cards_reference_list(self):
        hand_wild_cards = []
        for card in player.hand:
            if (card.rank, card.suit) in Deck().wild_cards:
                hand_wild_cards.append(card)
        return hand_wild_cards
    # -------------------------------------
    @property
    def non_maxed_out_melds(self):
        non_maxed_out_melds = []
        # -------------------------------------
        for meld_group in [self.play_cards, self.melds]:
            for item in meld_group:
                if type(item) == list:
                    wild_card_count = 0
                    for card in item:
                        if (card.rank, card.suit) in Deck().wild_cards:
                            wild_card_count += 1
                    if wild_card_count < 3:
                        non_maxed_out_melds.append(item)
                        # -------------------------------------
        return non_maxed_out_melds
    # -------------------------------------
    @property
    def has_canasta(self):
        for meld in self.melds:
            if len(meld) >= 7:
                return True
    # -------------------------------------
    @property
    def round_score(self):
        round_score = 0
        # -------------------------------------
        for meld_group in [self.play_cards, self.melds]:
            for item in meld_group:
                wild_card_canasta_check_count = 0
                if type(item) == list:
                    for card in item:
              	    # -------------------------------------
                        if (card.rank, card.suit) in Deck().wild_cards:
                            wild_card_canasta_check_count += 1
                        # -------------------------------------
                        round_score += Deck().ranks.get(card.rank)
                    # -------------------------------------
                    if len(item) >= 7:
                        if wild_card_canasta_check_count == 7:
                            round_score += 1000
                        elif wild_card_canasta_check_count == 0:
                            round_score += 500
                        elif wild_card_canasta_check_count > 0:
                            round_score += 300
                            # -------------------------------------
        if self.going_out == True:
            round_score += 100
            if self.went_out_concealed == True:
                round_score += 100
            round_score += (self.red_3_count * 100)
            if self.red_3_count == 4:
                round_score += 400
                # -------------------------------------
        elif self.going_out == False:
            if self.has_canasta == True:
                round_score += (self.red_3_count * 100)
                if self.red_3_count == 4:
                    round_score += 400
            else:
                round_score -= (self.red_3_count * 100)
                if self.red_3_count == 4:
                    round_score -= 400
                    # -------------------------------------
            if len(self.hand) > 0:
                for card in self.hand:
                    if (card.rank, card.suit) in Deck().black_3s:
                        round_score -= Deck().ranks.get(card.rank)
                        # -------------------------------------
        return round_score
    # -------------------------------------
    @property
    def total_score(self):
        return sum(self.finished_rounds_scores)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below - Creates the MasterDeck & Deck2, shuffles them, and combines the two together, with MasterDeck becoming the Deck for the game.
MasterDeck = Deck()
Deck2 = Deck()
# -------------------------------------
MasterDeck.create_deck()
Deck2.create_deck()
# -------------------------------------
random.shuffle(MasterDeck.deck)
random.shuffle(Deck2.deck)
# -------------------------------------
for card in Deck2.deck:
    MasterDeck.deck.append(card)
del Deck2
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below - Creates the players, and gives them starting names for identification at start of game.
P1 = Player('Player 1')
P2 = Player('Player 2')
players = [P1, P2]
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def the_draw_1(player=P1):
    # First Function for Game Loop. Handles logic for sequencing of the_draws for when certain criteria require certain sections to be rerun.
    print("draw 1\n")
    if player == P1:
        for player in players:
            print("draw_1 part 1\n")
            the_draw_2(player)
        print("draw_1 part 2\n")
        the_draw_3(player)
    else:
        print("draw_1 part 3\n")
        the_draw_2(player)
        the_draw_3(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def the_draw_2(player):
    # Follow Up Stem (#1) from The_Draw_1 for Game Loop. Handles name creation, draw card choice (to determine first player), and ensures that if a Joker is drawn during this process, it is reset and redone (Logic for that handled in draw_joker_check).
    print("draw 2")
    if player.name == "Name":
        while True:
            try:
                player.name = input(f"\n{player.start_name}, what is your name? \n\n> ")
                if len(player.name) < 1:
                    raise ValueError
                break
            except ValueError:
                print("\nSorry, but your name must be at least one character long. It looks as if your input was blank.\n")
    while True:
        try:
            player.the_draw = int(input(f"\n{player.name}, Select your card from the stack to determine which player will have the first play. (Pick a card, represented as a number from 1-108)\n\n> "))
            player.hand.append(MasterDeck.deck.pop(player.the_draw - 1))
            break
        except (ValueError, IndexError):
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is a number between 1-108.")
    print(f"\n{player.name} drew a {player.draw_card}\n")
    # -------------------------------------
    draw_joker_check(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def draw_joker_check(player):
    # Follow up to The_Draw_2 for Game Loop. Checks a player's draw card to ensure it is not a Joker, and if it is, redirects the process back to the_draw_1, to be redone. # ***
    print("draw joker check\n") # ***
    if player.draw_card.rank == 'Jo': # ***
        print(f"Sorry, {player.name}, you picked a Joker, which is not available for use during The Draw! You must choose another card!\n") # ***
        MasterDeck.deck.append(player.hand.pop(0)) # ***
        the_draw_1(player) # ***
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def the_draw_3(player):
    # Follow Up Stem (#2) from The_Draw_1 for Game Loop. Checks whether or not the players have the same draw card, and if they do, redirects the process back to the_draw_1 and places player cards back into the MasterDeck. Also checks to see who wins the draw, and sends off to the_deal after determination.
    print("draw 3\n")
    # -------------------------------------
    # ****** Below - Have to update this method and this code to reflect the changes I made to cards, namely that they are now a class, with each card being an individual object. I have to reference the card rank and suit.
    if P1.draw_card == P2.draw_card:
        print("\nYou have the same exact card! You both must pick another card!\n")
        # -------------------------------------
        return_draw_card(players)
        the_draw_1()
    elif P1.draw_card_val > P2.draw_card_val:
        return_draw_card(players)
        the_deal(P1,P2)
    elif P2.draw_card_val > P1.draw_card_val:
        return_draw_card(players)
        the_deal(P2,P1)
    elif P1.draw_card_val == P2.draw_card_val:
        if MasterDeck.draw_suit_ranks.get(P1.draw_card.suit) > MasterDeck.draw_suit_ranks.get(P2.draw_card.suit):
            return_draw_card(players)
            the_deal(P1,P2)
        else:
            return_draw_card(players)
            the_deal(P2,P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def return_draw_card(players):
    # Stem from the_draw_3. Simple function to return the draw card used to determine first play from player.hand back into MasterDeck.deck(). For purpose of reducing amount of repeated code. # ***
    print("return_draw_card\n") # ***
    for player in players: # ***
        MasterDeck.deck.append(player.hand.pop(0)) # ***
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def the_deal(player1, player2): # ***
    # Follow up to Draw_3 for Game Loop. Handles dealing, sorting, printing, red 3 checK each player their cards, then creates a discard pile from MasterDeck. # ***
    print("the deal\n") # ***
    # -------------------------------------
    # Below - Deals each player their 11 cards, sorts them, prints them, and checks for Red 3s. # ***
    for player in (player1, player2): # ***
        for card in range(11): # ***
            player.hand.append(MasterDeck.deck.pop(0)) # ***
        print(f"{player.name} is dealt 11 cards. Your hand consists of:\n") # ***
        sorted_and_numbered_list_printer(player.hand) # ***
        red_3_check(player) # ***
    # -------------------------------------
    # Below - Creates the discard pile from the MasterDeck # ***.
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(0)) # ***
    # -------------------------------------
    play_1(player1) # ***
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Miscellaneous function for handling printed lists that I want to be sorted and then numbered; for the purpose of input choice selection via the preceding num.
def sorted_and_numbered_list_printer(passed_list_1, passed_list_2 = None):
    print("sorted_and_numbered_list_printer\n")
    # -------------------------------------
    non_num_card_rank_sort_value = {'J':11, 'Q':12, 'K':13, 'A':14, "Jo":15}
    # -------------------------------------
    # Below Function - The sorter function which orders the cards in ascending order based on card rank.
    def sorter_key_function(item):
        # Below - If item is a card (tuple).
        if type(item) != list:
            if item.rank in non_num_card_rank_sort_value:
                int_rank = non_num_card_rank_sort_value.get(item.rank)
                return int_rank
            else:
                return int(item.rank)
        # Below - If item is a meld (list).
        else:
            if item[0].rank in non_num_card_rank_sort_value:
                int_rank = non_num_card_rank_sort_value.get(item[0].rank)
                return int_rank
            else:
                return int(item[0].rank)
                # -------------------------------------
    num = 1
    passed_list_1.sort(key=sorter_key_function)
    for item in passed_list_1:
        if item != passed_list_1[-1]:
            print(f"{num}) {item}")
        else:
            print(f"{num}) {item}\n")
        num += 1
        # -------------------------------------
    if passed_list_2 != None:
        passed_list_2.sort(key=sorter_key_function)
        for item in passed_list_2:
            if item != passed_list_2[-1]:
                print(f"{num}) {item}")
            else:
                print(f"{num}) {item}\n")
            num += 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def red_3_check(player, drawn = False): # ***
    # Stem # Below - Handles drawn Red 3s. Removes them from player.hand, replaces it with a newly drawn card from the deck, and prints associated output. # ****
    print("red 3 check\n") # ****
    red_3_quantity = 0 # ****
    # -------------------------------------
    for card in player.hand: # ****
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
    if red_3_quantity == 4: # ***
        print(f"Congratulations, {player.name}! You have 4 Red 3s, therefore you get a bonus of 400 points (granted that when the round ends, you have at least 1 Canasta)! The rules dictate that all Red 3s must be played down, and you will withdraw a replacement card from the stock for each one in your hand!\n") # ***
    elif red_3_quantity > 0: # ***
        print(f"{player.name}, you have {red_3_quantity} Red 3(s) in your hand! The rules dictate that all Red 3s must be played down, and you have to withdraw a replacement card from the stock for each one in your hand!\n\n{player.name}, in place of your Red 3(s), you drew a " + ', '.join(['%s']*len(player.red_3_meld)) % tuple(player.hand[-(len(player.red_3_meld)):]) + "\n") # ***
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def play_1(player):
    # Follow up to The_Deal for Game Loop.
    print("play_1\n")
    # -------------------------------------
    while True:
        try:
            draw_method = input(f"{player.name}, which method would you like to use to draw?\n\n1) Draw from Stack\n2) Draw from Discard Pile - The face up discard is {MasterDeck.face_up_discard}.\n\n> ")
            if draw_method not in ('1', '2'):
                raise ValueError
            break
        except ValueError:
            print("\nSorry, but there was a problem with your input. Please try again. Make sure to use only either '1' or '2' as your input.\n")
    if len(player.melds) > 0:
        print("Your current melds are as follows.\n")
        sorted_and_numbered_list_printer(player.melds)
    if draw_method == '1':
        stock_draw(player)
    else:
        draw_discard_pile_attempt(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - For drawing a card from the stock & giving associated output. If stock is empty, redirects to draw_discard_pile_attempt. # ****
def stock_draw(player): # ****
    print("stock_draw\n") # ****
    # -------------------------------------
    if len(MasterDeck.deck) > 0: # ****
        player.hand.append(MasterDeck.deck.pop(0)) # ****
        print(f"{player.name} drew a {player.hand[-1]} from the stack.\n") # ****
        red_3_check(player) # ****
        play_2(player) # ****
    else: # ****
        print("There are no cards left in the stock pile. If you have a meld that matches the rank of the face up discard, you are required to draw the discard pile's face up discard (or the entire discard pile), per the rules. This rule will continue until no player has a matching meld for the face up discard; at that point the round will end.\n") # ****
        draw_discard_pile_attempt(player, True) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - For attempting to draw the discard pile. If the stock_depleted parameter is true, checks to see if the discard pile is depleted; if not, checks for a matching meld for the face up discard, but if so, ends the round, per the rules. # ****
def draw_discard_pile_attempt(player, stock_depleted = False): # ****
    print("\ndraw_discard_pile_attempt\n") # ****
    # -------------------------------------
    # Below Section - Checks to see if the player can draw the discard pile in the case that the stock_depleted parameter is True. If so, attempts to draw the discard pile. If there is a matching meld, successfully draws the discard pile. If not, the round ends, per the rules. # ****
    if stock_depleted == True: # ****
        if len(MasterDeck.discard_pile) == 0: # ****
            print("It looks as if the discard pile is depleted as well. Per the rules, this means the round is ended since there is no means by which you can draw another card.") # ****
            round_reset() # ****
            # -------------------------------------
        else: # ****
            # Below Section - Checks to see if player has a meld that matches the rank of the face up discard. If so, appends the face up discard to the matching meld, and if the player chooses to, also appends the discard pile into their hand, and returns back to play_2. If not, round ends, as there is no means for them to draw a card, per the rules. # ****
            draw_discard_pile_attempt_check_meld_match(player, True)
            # -------------------------------------
    # Below - For discard pile draw attempt when it is not internally or topically frozen. Redirects to eligibility determinations based on player's initial meld status, and finalizes determination by either allowing drawing of the discard pile, or denial and subsequent redirection back to play_1. # ***
    if MasterDeck.discard_pile_is_frozen == False: # ****
        # Below - prints are for testing purposes only to ensure that code is working properly.
        print("discard_pile_is_frozen == False\n")
        # Below - Checks the player's existing melds to see if they have a match for the top discard to be used as a means to withdraw the discard pile. If so, draws the discard pile and creates a meld from the face up discard, and returns True. If not, continues to check the hand for an alternate route to draw the discard pile. # ****
        draw_discard_pile_attempt_check_meld_match(player)
    # Below - For when the discard_pile_is_frozen is either True or False, and if draw_discard_pile_attempt_check_meld_match did not succeed. Checks the player's hand to see if they have matching cards in their hand (for when they have no melds that match the top discard) as an alternative means to pick up the discard pile. If so, draws the discard pile and creates a meld from the face up discard, and returns True, If not... # ****
    draw_discard_pile_attempt_check_hand_match(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def draw_discard_pile_attempt_check_meld_match(player, stock_depleted = False): # ****
    for meld in player.melds: # ****
        if MasterDeck.face_up_discard.suit == meld[0].rank: # ****
            meld.append(MasterDeck.discard_pile.pop(-1)) # ****
            # Below - In the case that the player is trying to draw from the discard pile because the stock is depleted. Per the rules, in this instance, only the face up discard is withdrawn, unless the player chooses otherwise.
            if stock_depleted == True:
                while True:
                    try:
                        draw_rest_of_discard_pile_input = input(f"{player.name}, you successfully withdrew the face up discard from the discard pile, as you had a matching meld! Per the rules, you have the choice to either pick up the entire discard pile, or to take just the face up discard. Would you like to take the rest of the pile as well? (Y/N)\n\n> ")
                        if draw_rest_of_discard_pile_input.lower() not in ('y', 'n'):
                            raise ValueError
                        break
                    except ValueError:
                        print("Sorry, but there was an issue with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n")
                if draw_rest_of_discard_pile_input.lower() == 'n':
                    return play_2(player)
                    # -------------------------------------
            draw_discard_pile(player)
            # -------------------------------------
    if stock_depleted == True:
        print(f"{player.name}, unfortunately, you were unable to draw the discard pile because you did not have a matching meld. Therefore, since you have no means to draw a card, the round is over, per the rules.\n")
        round_reset() # ****
        # -------------------------------------
    print(f"{player.name}, unfortunately, you were unable to draw the discard pile because you did not have a matching meld. You will instead draw from the stock.\n")
    stock_draw(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Stems from draw_discard_pile_attempt.
def draw_discard_pile_attempt_check_hand_match(player): # ****
    print("draw_discard_pile_attempt_check_hand_match\n") # ****
    # -------------------------------------
    card_count = 0 # ****
    matched_card_list = [] # ****
    for card in player.hand: # ****
        if card.rank == MasterDeck.face_up_discard.rank: # ****
            matched_card_list.append(card) # ****
            card_count += 1 # ****
            # -------------------------------------
    if len(matched_card_list) > 0:
        # Below - Creates a new meld in player.melds for the matched cards to be subsequently appended to. # ****
        player.melds.append([])
        # Below - Pops and appends each matching card from the player's hand as well as the face up discard.
        for matched_card in matched_card_list: # ****
            player.melds[-1].append(player.hand.pop(player.hand.index(matched_card))) # ****
        player.melds[-1].append(MasterDeck.discard_pile.pop(-1)) # ****
        # -------------------------------------
        # Below - If the meld consists of at least 2 natural cards from the hand and the face up discard; checks that the player has met meld requirement; if so, proceeds to draw the discard pile into their hand, popping and appending each card from the discard pile. If they have not met the meld requirement, checks to see if they have a wild card that they can add to the attempted meld to reach the requirement. If so, successfully draws the discard pile. If not,   # ****
        if len(player.melds[-1]) >= 3:
            if player.round_score > player.meld_requirement:
                draw_discard_pile(player)
                # -------------------------------------
        # Below Section - If the meld only consists of 1 natural card from the hand and the face up discard; if discard_pile_is_frozen == True, reroutes the player to stock_draw.
        elif len(player.melds[-1]) <= 2:
            if MasterDeck.discard_pile_is_frozen == True:
                print(f"Sorry, {player.name}, but you don't have 2 natural cards of the face up discard's rank in your hand, which is required to pick up the discard pile when it is frozen, which it currently is. Therefore you will have to withdraw from the stock pile.\n")
                # -------------------------------------
                # Below - Replaces the face up discard back into the discard pile and replaces the matched cards from the player.meld back to the player.hand.
                MasterDeck.discard_pile.append(player.melds[-1][-1])
                for matched_card in matched_card_list:
                    player.hand.append(player.melds[-1].pop(player.melds[-1].index(matched_card)))
                player.melds.pop(-1)
                stock_draw(player)
                # -------------------------------------
            else:
                if len(player.hand_wild_cards_reference_list) > 0: # ****
                    while True:
                        try:
                            use_wild_card_for_discard_pile = input(f"{player.name}, you only have one card that matches the face up discard, so you would have to use a wild card to draw the discard pile. You have {len(player.hand_wild_cards_reference_list)} Would you like to do this? (Y/N)\n\n> ") # ****
                            if use_wild_card_for_discard_pile.lower() not in ('y', 'n'):
                                raise ValueError
                            break
                        except ValueError:
                            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n")
                    if use_wild_card_for_discard_pile.lower() == "y": # ****
                        draw_discard_pile_attempt_temp_meld_wild_card_addition(player)
                        # -------------------------------------
                        # Below Section - Checks the player's attempted meld from above (using the face up discard) to see if it reaches the meld_requirement. If it does, player successfully draws discard pile, popping all of the discards from MasterDeck.discard_pile and appending them to player.hand, and also popping the temp_meld from player.play_cards to be appended to player.melds. # ****
                        if player.round_score > player.meld_requirement: # ****
                            # Below - Pops each card off of MasterDeck.discard_pile & appends them to player.hand, then prints a successful draw output, and finally returns play_2(player). # **** # ***
                            draw_discard_pile(player)
                            play_2(player)
                            # -------------------------------------
                        else:
                            print(f"{player.name}, you were able to create a valid meld from the top discard, but unfortunately the meld did not meet the minimum meld requirement score.\n")
                            if len(player.hand_wild_cards_reference_list) > 0:
                                while True:
                                    try:
                                        add_more_wild_cards = input(f"{player.name}, you still have {len(player.hand_wild_cards_reference_list)} wild card(s) available to add to your attempted meld. Would you like to add another one to the meld to see if it will help you to reach your meld requirement? Your meld requirement is {player.meld_requirement}, and the current meld value is {player.round_score}.\n\n > ")
                                        if add_more_wild_cards.lower() not in ('y', 'n'):
                                            raise ValueError
                                        break
                                    except ValueError:
                                        print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n")
                                if add_more_wild_cards.lower() == 'y':
                                    draw_discard_pile_attempt_temp_meld_wild_card_addition(player)
                                else:
                                    print("Okay, the cards from your attempted meld will be placed back into your hand.")
                                    MasterDeck.discard_pile.append(player.melds[-1][-1])
                                    for matched_card in matched_card_list:
                                        player.hand.append(player.melds[-1].pop(player.melds[-1].index(matched_card)))
                    else: # ****
                        print("Okay, the attempt will be cancelled, and you will be redirected back to the draw method options.\n") # ****
                        play_1(player) # ****
                        # -------------------------------------
                else: # # ****
                    print(f"Sorry, {player.name}, but you do not meet the requirements to be able to withdraw from the discard pile because you only had 1 card matching the top discard, with no wild card in your hand to be played as part of a meld alongside it.\n") # ****
                    play_1(player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Stems from draw_discard_pile_attempt. Pops and appends each card from the discard pile to the player's hand.
def draw_discard_pile(player):
    print("draw_discard_pile\n")
    for card in MasterDeck.discard_pile: # ****
        player.hand.append(MasterDeck.discard_pile.pop(-1)) # ***
    print(f"{player.name}, you successfully drew the discard pile!\n") # ***
    red_3_check(player)
    play_2(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def draw_discard_pile_attempt_temp_meld_wild_card_addition(player):
    wild_cards_str = (f"{player.name}, which wild card would you like to use? You have these wild cards:\n") # ****
    sorted_and_numbered_list_printer(player.hand_wild_cards_reference_list) # ****
    while True:
        try:
            wild_card_choice = input("> ") # ****
            player.melds[0].append(player.hand.pop(player.hand.index(player.hand_wild_cards_reference_list[int(wild_card_choice - 1)]))) # ****
            break
        except (ValueError, IndexError):
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is one of the numbers preceding the card you would like to use.\n")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def play_2(player): # ***
    # Follow up to Play_1 for Game loop. # ***
    print("play_2\n") # ***
    # -------------------------------------
    player.play_cards.clear() # ***
    # -------------------------------------
    print(f"{player.name}, it is your turn to play!\n")
    if len(player.melds) > 0:
        print(f"Your existing melds are as follows:\n")
        sorted_and_numbered_list_printer(player.melds)
    while True:
        try:
            play_choice = input(f"{player.name}, what would you like to do with your turn?\n\n 1) Play Cards\n 2) Discard\n\n> ") # ***
            if play_choice not in ('1', '2'):
                raise ValueError
            break
        except ValueError:
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either '1' or '2' (Play Cards or Discard).\n")
    # -------------------------------------
    if play_choice == "1": # ***
        print(f"\n{player.name}, which cards would you like to play? (Use the ordered number of the card(s) as listed below. (i.e. - '1,3,4,8')\n") # ***
        sorted_and_numbered_list_printer(player.hand) # ***
        multiple_choices_input_filter_and_transfer(player, player.play_cards, player.hand)
        # -------------------------------------
        if len(player.hand) == 0:
            if player.has_canasta == False:
                print(f"Sorry, {player.name}, but you seem to be trying to go out. Unfortunately, you do not have a Canasta in your set of melds, which is required for a player to be eligible to go out. You must keep at least 1 card in your hand until you are eligible to go out. Please choose from the list of play cards below a card that you would like to take back into your hand.\n")
                sorted_and_numbered_list_printer(player.play_cards)
                multiple_choices_input_filter_and_transfer(player, player.hand, player.play_cards)
        # -------------------------------------
        valid_play_check_and_sort(player)
    else: # ***
        discard(player) # ***
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def multiple_choices_input_filter_and_transfer(player, append_list, pop_list):
    while True:
        try:
            input_str = input("> ")
            input_str = list(input_str) # ***
            temp_char_holder = {} # ***
            index = -1 # ***
            consec_int_counter = 0 # ***
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # ***
            # -------------------------------------
            for char in input_str: # ***
                if char in numbers: # ***
                    index += 1 # ***
                    temp_char_holder[index] = int(char) # ***
                    consec_int_counter += 1 # ***
                    if consec_int_counter == 2: # ***
                        concatenated_int = int(str(temp_char_holder.pop(index - 1)) + str(temp_char_holder.pop(index))) # ***
                        temp_char_holder[index - 1] = concatenated_int # ***
                else: # ***
                     consec_int_counter = 0 # ***
                     # -------------------------------------
            temp_char_holder = sorted(temp_char_holder.values(), reverse = True) # ***
            # -------------------------------------
            for typed_value in temp_char_holder: # ***
                append_list.append(pop_list.pop(typed_value - 1)) # ***
            break
        except (ValueError, IndexError):
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your choices match the number that precedes the card(s) you are trying to choose.\n")
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def valid_play_check_and_sort(player): # ***
    # Stems (#1) from Play_2. For ensuring that a set of attempted play cards are valid according to game rules. # ***
    print("\nvalid_play_check_and_sort\n") # ***
    # -------------------------------------
    play_cards_new_ranks = [] # ***
    bad_len_temp_melds_list_print = [] # ***
    play_cards_removed_black_3s_print = [] # ***
    # -------------------------------------
    player.initial_played_card_count = player.played_card_count # ***
    # -------------------------------------
    # Below - Checks to see if the player has NOT met the initial meld requirements. If so, valid plays are different than if they had met the requirement, thus puts different restrictions on what a valid play is.
    if player.round_score < player.meld_requirement: # ***
        print("player.round_score < meld\n") # ***
        # -------------------------------------
        if len(player.play_cards) < 3:
            print(f"Sorry, {player.name}, but you must play at least 3 cards for a new meld. Please select a new set of cards to play, or you can choose to discard if you like.\n")
            for card in player.play_cards:
                player.hand.append(card)
            player.play_cards.clear()
            return play_2(player)
            # -------------------------------------
    # - Below Section - Sorts all of the individual play cards, putting them either in matching melds, or creating temp_melds and putting those back into play_cards to be further sorted. Also places all played wild cards into play_cards_wild_cards and removes any played Black 3s. # ****
    for card in player.play_cards[:]: # ****
        # Below - Checks to see if the player already has existing melds. If so, checks to see if card rank is already in a preexisting meld. If so, pops the card from player.play_cards and appends it to the meld. # ****
        card_found_in_meld = False
        if len(player.melds) > 0: # ****
            for meld in player.melds: # ****
                if card.rank == meld[0].rank: # ****
                    meld.append(player.play_cards.pop(player.play_cards.index(card))) # ****
                    # Below - Changes the variable card_found_in_meld to True in the case that it is matched and subsequently popped from the list, so that if it also meets another parameter later on in the loop, it will not be recognized again and attempted to be handled again, which caused errors wherein it was trying to place the card in two different locations.
                    card_found_in_meld = True
                    # ------------------------------------- # ****
        if card_found_in_meld == False:
            # Below - If card is a Black 3 and the player does not meet the requirements to be able to play a Black 3 meld (above). Appends it to play_cards_removed_black_3s_print, which is used to print out all of these instances later on to inform the player, and removes it from player.play_cards, placing it back into player.hand. # ****
            if (card.rank, card.suit) in Deck().black_3s: # ****
                if len(player.hand) <= 1 and player.has_canasta == True: # ****
                    player.black_3_meld.append(card) # ****
                else:
                    play_cards_removed_black_3s_print.append(player.play_cards.pop(player.play_cards.index(card))) # ***
                    # -------------------------------------
            # Below - If card is a Wild Card; appends it to play_cards_wild_cards, popping it from player.play_cards, for the purpose of segregation so that later on when meld lengths are determined, they are not convoluted by having individual wild cards mixed in.
            elif (card.rank, card.suit) in Deck().wild_cards:
                player.play_cards_wild_cards.append(player.play_cards.pop(player.play_cards.index(card)))
                # -------------------------------------
            # Below - If card is a valid, non-wild card that is the first of it's rank iterated through in the group of play cards. Creates a new temp_meld for it to be placed into, and the temp_meld is then placed back into player.play_cards, which is where other cards of the same rank will be placed.
            elif card.rank not in play_cards_new_ranks: # ***
                play_cards_new_ranks.append(card.rank) # ***
                temp_meld = [] # ***
                temp_meld.append(player.play_cards.pop(player.play_cards.index(card))) # ***
                player.play_cards.append(temp_meld) # ***
            # Below - If card's rank exists in play_cards_new_ranks. Sorts the card into the temp_meld that matches the card's rank. For grouping cards of the same rank together.
            elif card.rank in play_cards_new_ranks: # ***
                for item in player.play_cards: # ***
                    if type(item) == list:
                        if card.rank == item[0].rank: # ***
                            item.append(player.play_cards.pop(player.play_cards.index(card))) # ***
                            # -------------------------------------
    # Below - If the player only had 1 or 0 cards left in his hand for this play, then they are able to meld Black 3s. If they did, then this meld will be appended to their list of play cards, and player.black_3_meld will be .clear()ed.
    if len(player.black_3_meld) > 0:
        player.play_cards.append(player.black_3_meld)
        player.black_3_meld.clear()
        # -------------------------------------
    # Below - Checks to see if there are any Black 3s that were removed from the play cards, and if so, prints them out and informs the player of their removal.
    if len(play_cards_removed_black_3s_print) > 0:
        print(f"Sorry, {player.name}, but you cannot play Black 3(s) in this way. Black 3s can only be used to freeze the discard pile. The Black 3(s) that are being removed from your attempted play cards back into your hand are as follows:\n")
        sorted_and_numbered_list_printer(play_cards_removed_black_3s_print)
        for card in play_cards_removed_black_3s_print:
            player.hand.append(play_cards_removed_black_3s_print.pop(play_cards_removed_black_3s_print.index(card)))
            # -------------------------------------
    for temp_meld in player.play_cards[:]:
        if len(temp_meld) < 2:
            bad_len_temp_melds_list_print.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
            # -------------------------------------
        elif len(temp_meld) == 2:
            if len(player.play_cards_wild_cards) < 1:
                bad_len_temp_melds_list_print.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
            else:
                player.len_2_temp_melds_list.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
                # -------------------------------------
    # Below - ...
    while len(player.len_2_temp_melds_list) > 0: # ***
        if len(player.play_cards_wild_cards) > 0: # ***
            print(f"{player.name}, the below meld(s) from your attempted play cards have only 2 cards in them. Since 3 cards are required for a valid meld, you must add a wild card to them for them to remain in play. It looks as if you have {len(player.play_cards_wild_cards)} wild card(s) in your set of play cards to use for this. Choose a meld from the list below that you would like to add a wild card to.\n") # ***
            sorted_and_numbered_list_printer(player.len_2_temp_melds_list) # ***
            num = str(len(player.len_2_temp_melds_list) + 1) # ***
            print(f"{num}) I would rather use the wild card elsewhere, and let the meld(s) be placed back into my hand.\n") # ***
            while True:
                try:
                    len_2_temp_meld_choice = int(input("> ")) - 1 # ***
                    if len_2_temp_meld_choice + 1 != int(num) and player.len_2_temp_melds_list[len_2_temp_meld_choice] not in player.len_2_temp_melds_list:
                        raise IndexError
                    break
                except (ValueError, IndexError):
                    print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is a number that precedes one of the meld groups above, or is the number that precedes the option to not use the wild card.\n")
            if len_2_temp_meld_choice != int(num) - 1: # ***
                if len(player.play_cards_wild_cards) > 1:
                    print(f"\nWhich wild card would you like to add to the following meld? - {player.len_2_temp_melds_list[len_2_temp_meld_choice]} - Choose from the below choices.\n") # ***
                    sorted_and_numbered_list_printer(player.play_cards_wild_cards) # ***
                    while True:
                        try:
                            wild_card_choice = int(input("> ")) - 1 # ***
                            print(f"\nYou successfully added the {player.play_cards_wild_cards[wild_card_choice]} to your meld.\n") # ***
                            player.len_2_temp_melds_list[len_2_temp_meld_choice].append(player.play_cards_wild_cards.pop(wild_card_choice)) # ***
                            player.play_cards.append(player.len_2_temp_melds_list.pop(len_2_temp_meld_choice)) # ***
                            break
                        except (ValueError, IndexError):
                            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is a number that precedes the card you are trying to choose.\n")
                else:
                    print(f"\nYou successfully added the {player.play_cards_wild_cards[0]} to your meld.\n") # ***
                    player.len_2_temp_melds_list[len_2_temp_meld_choice].append(player.play_cards_wild_cards.pop(0)) # ***
                    player.play_cards.append(player.len_2_temp_melds_list.pop(len_2_temp_meld_choice)) # ***
                    # -------------------------------------
            # Below - If the player chooses not to use the available wild card(s); places the len_2_temp_melds_list melds into bad_len_temp_melds_list_print, leaving the wild cards in play cards to be handled with wild_card_handler. # ***
            else: # ***
                print("\nOkay, the meld will be put back into your hand, while the wild card will continue to remain in your group of played cards with the option of being used later in any of your attempted melds or your existing melds. \n") # ***
                for temp_meld in player.len_2_temp_melds_list[:]: # ***
                    bad_len_temp_melds_list_print.append(player.len_2_temp_melds_list.pop(player.len_2_temp_melds_list.index(temp_meld))) # ***
                # -------------------------------------
        elif len(player.play_cards_wild_cards) == 0: # ***
            for temp_meld in player.len_2_temp_melds_list[:]: # ***
                bad_len_temp_melds_list_print.append(player.len_2_temp_melds_list.pop(player.len_2_temp_melds_list.index(temp_meld))) # ***
            # -------------------------------------
    # Below - ...
    if len(bad_len_temp_melds_list_print) > 0:
        print(f"{player.name}, you have some attemped melds that do not pass the rule requirements. You cannot create a new meld without at least 2 natural cards of the same rank, or without a wild card to add to it to reach the 3 card minimum meld requirement. The attempted meld(s) will be removed and placed back in your hand:\n")
        # -------------------------------------
        sorted_and_numbered_list_printer(bad_len_temp_melds_list_print)
        for bad_len_meld in bad_len_temp_melds_list_print[:]:
            for card in bad_len_meld[:]:
                player.hand.append(bad_len_meld.pop(bad_len_meld.index(card)))
                # -------------------------------------
    # Below - ...
    if len(player.play_cards_wild_cards) > 0:
        wild_card_handler(player) # ***
    # -------------------------------------
    if player.round_score < player.meld_requirement:
        print(f"Sorry, {player.name}, but the value of your play cards: ({player.round_score}) - after filtering and sorting your attempted melds: (" + ', '.join(['%s']*len(player.play_cards)) % tuple(player.play_cards) + f") is not enough to meet the minimum meld requirement of {player.meld_requirement}. Your play cards will be placed back into your hand.\n")
        # -------------------------------------
        for meld in player.play_cards:
            for card in meld[:]:
                player.hand.append(meld.pop(-1))
        player.play_cards.clear()
        # -------------------------------------
        return play_2(player)
        # -------------------------------------
    if len(player.play_cards) > 0:
        print(f"{player.name}, you successfully melded the cards below!\n")
        sorted_and_numbered_list_printer(player.play_cards)
        # -------------------------------------
    for temp_meld in player.play_cards[:]:
        player.melds.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
        # -------------------------------------
    player.final_played_card_count = player.played_card_count
    # -------------------------------------
    if player.initial_played_card_count == player.final_played_card_count:
        print("initial_played_card_count == final_played_card_count\n")
        print("It looks as if you were unable to succeed in playing any of your attempted play cards. Therefore you will have to choose another set of play cards, or opt to discard instead if you have no valid plays to make.\n")
        play_2(player)
    else:
        print("initial_played_card_count != final_played_card_count\n")
        # Below - Checks to see if the player has any cards left in their hand. If they do not, runs went_out_check() to determine whether or not they are eligible to go out. If they still have cards in their hand, redirects to discard().
        if len(player.hand) == 0:
            went_out_check(player)
        else:
            discard(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below - Handles all played wild cards (after len_2_temp_melds_list sorting and placement of played wild cards), prompting the player to determine their placement. Also determines whether or not a Wild Card Canasta is being played. Any unplayed wild cards are placed back into the player's hand. # ****
def wild_card_handler(player): # ****
    # Below Section - Checks via prompt to see if player is trying to play a Wild Card Canasta. If so, character chooses which 7 wild cards they want in the canasta and appends them to player.play_cards, popping them from player.play_cards_wild_cards.  # ****
    if len(player.play_cards_wild_cards) >= 7: # ****
        while True:
            try:
                wild_card_canasta_check_input = input(f"{player.name}, are you trying to play a Wild Card Canasta? (Y/N)\n\n> ") # ****
                if wild_card_canasta_check_input.lower() not in ('y', 'n'):
                    raise ValueError
                break
            except ValueError:
                print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n")
        if wild_card_canasta_check_input.lower() == 'y': # ****
            # Below - Checks if the amount of wild cards in player.play_cards_wild_cards is exactly 7 cards, in which case the entire list will simply be appended to player.play_cards, then clearing player.play_cards_wild_cards. # ****
            if len(player.play_cards_wild_cards) == 7: # ****
                player.play_cards.append(player.play_cards_wild_cards) # ****
                player.play_cards_wild_cards.clear() # ****
                print(f"{player.name}, you successfully played a Wild Card Canasta! Congratulations!\n") # ****
                # ------------------------------------- # ****
            # Below - If the amount of wild cards being played is greater than 7; player is prompted to choose which wild cards they want to use in the canasta. The non-chosen wild cards will remain in play to be distributed later in the function, unless this is the player's first meld. In this case, appends left over wild cards back into player.hand, and returns None. # ****
            else: # ****
                print(f"{player.name}, choose 7 wild cards from the list below that you want to use for your Wild Card Canasta. Use the numbers that prefix each wild card ( 1), 2), 3), 4), etc. ) in the list to choose those that you want. (i.e. - 1, 3, 5, 7, etc.) \n") # ****
                sorted_and_numbered_list_printer(player.play_cards_wild_cards) # ****
                multiple_choices_input_filter_and_transfer(player, player.play_cards, player.play_cards_wild_cards) # ****
                if player.round_score < player.meld_requirement: # ****
                    print(f"{player.name}, since you only have the Wild Card Canasta in your available melds and extra wild cards left over, they will be placed back into your hand as there is currently no other place to put them.\n") # ****
                    for wild_card in player.play_cards_wild_cards: # ****
                        player.hand.append(player.play_card_wilds_cards.pop(-1)) # ****
                    return None # ****
                    # ------------------------------------- # ****
    # Below - Runs if the player has less than 7 wild cards in play_cards_wild_cards OR if they have 7 or more wild cards but chose not to create a wild card canasta with them, and if the player has at least 1 meld in player.play_cards or player.melds that do not contain the max amount of wild cards to add the wild cards to; iterates through each wild card in player.play_cards_wild_cards and prompts the player to choose a destination for each card. # ****
    if len(player.play_cards) > 0 or len(player.melds) > 0: # ****
        if len(player.non_maxed_out_melds) > 0: # ****
            for wild_card in player.play_cards_wild_cards[:]: # ****
                meld_choice_index = wild_card_meld_choice_prompt(player, wild_card) # ****
                # ------------------------------------- # ****
                # Below - If player chooses not to use the wild card, it is popped from play_cards_wild_cards and appended back into the player's hand. # ****
                if meld_choice_index > len(player.non_maxed_out_melds) - 1: # ****
                    print("\nOkay, the wild card will be placed back into your hand.\n") # ****
                    player.hand.append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card))) # ****
                    # ------------------------------------- # ****
                # Below - If player chooses to place the wild card into a meld; determines which meld group (player.play_cards or player.melds) they chose, and appends the wild card to that meld, popping it from play_cards_wild_cards. # ****
                elif meld_choice_index <= len(player.play_cards) - 1: # ****
                    print(f"{player.name}, you successfully added the {player.play_cards_wild_cards[player.play_cards_wild_cards.index(wild_card)]} to your meld.\n") # ****
                    player.play_cards[meld_choice_index].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card))) # ****
                elif meld_choice_index <= len(player.non_maxed_out_melds) - 1: # ****
                    print(f"{player.name}, you successfully added the {player.play_cards_wild_cards[player.play_cards_wild_cards.index(wild_card)]} to your meld.\n") # ****
                    player.melds[meld_choice_index - len(player.play_cards)].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card))) # ****
                    # ------------------------------------- # ****
        else: # ****
            print(f"{player.name}, it looks as if every meld in your play cards and/or in your melds have the maximum amount of wild cards possible. Therefore the remaining wild cards in play will be placed back into your hand.\n") # ****
            for wild_card in player.play_cards_wild_cards[:]: # ****
                player.hand.append(player.play_cards_wild_cards.pop(-1)) # ****
            return None # ****
            # ------------------------------------- # ****
    # Below - If a player who has no play_card melds or player.meld melds tried to play some wild cards. Since there is nowhere to put them, places the cards back into the player's hand. # ****
    else: # ****
        print(f"It looks as if you have some wild cards leftover in your group of play cards, {player.name}, but there is nowhere to place them, since you have no existing melds. The cards will be placed back into your hand.\n") # ****
        for wild_card in player.play_cards_wild_cards[:]: # ****
            player.hand.append(player.play_cards_wild_cards.pop(-1)) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def wild_card_meld_choice_prompt(player, wild_card):
    print(f"{player.name}, which meld from the list below would you like to add the {player.play_cards_wild_cards[player.play_cards_wild_cards.index(wild_card)]} to?\n")
    sorted_and_numbered_list_printer(player.play_cards, player.melds)
    meld_num = str(len(player.play_cards) + len(player.melds) + 1)
    print(f"{meld_num}) I would not like to use this wild card, and would rather have it be replaced back into my hand.\n")
    while True:
        try:
            meld_choice_index = int(input('> ')) - 1
            if meld_choice_index + 1 != int(meld_num):
                if player.play_cards[meld_choice_index] not in player.play_cards and player.melds[meld_choice_index] not in player.melds:
                    raise ValueError
            break
        except (ValueError, IndexError):
            print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either a number that precedes the meld you are choosing or the option to not use the wild card.\n")
    return meld_choice_index
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def maximum_wild_card_amount_check(player, passed_meld_list_1, passed_meld_list_2):
    wild_card_count = 0
    for meld in passed_meld_list_1, passed_meld_list_2:
        for card in meld:
            if (card.rank, card.suit) in Deck().wild_cards:
                wild_card_count += 1
        if wild_card_count >= 3:
            player.maxed_out_wild_card_melds.append(meld)
        wild_card_count = 0
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def discard(player):
    # Stems (#2) from Play_2. For discarding.
    print("discard\n")
    # -------------------------------------
    print(f"{player.name}, which card would you like to discard? Your available cards in hand are:\n")
    sorted_and_numbered_list_printer(player.hand)
    while True:
        try:
            discard_input = int(input("> ")) - 1
            break
        except (ValueError, IndexError):
            print("\nSorry, but there was a problem with your input. Please try again. Make sure your input is a number preceding the card you would like to discard.\n")
    print(f"\n{player.name}, you discarded the {player.hand[discard_input]}.\n")
    MasterDeck.discard_pile.append(player.hand.pop(discard_input))
    # -------------------------------------
    went_out_check(player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def went_out_check(player):
    # Follow up to Play_2. For checking to see if players are eligible to go out, and whether or not they went out during their last turn. If they are not trying to go out, redirects to beginning of the player turn loop via (play_1()). If so, ends round via round_reset().
    print("went out check\n")
    # -------------------------------------
    if len(player.hand) == 0:
        if player.has_canasta == True:
            player.going_out = True
            if player.initial_played_card_count == 0:
                player.went_out_concealed = True
            # -------------------------------------
            if player == P1:
                P2.going_out = False
                print(f"{P1.name} went out!\n\nRound Score:\n{P1.name}:{P1.round_score}\n{P2.name}:{P2.round_score}\n")
            else:
                P1.going_out = False
                print(f"{P2.name} went out!\n\nRound Score:\n{P2.name}:{P2.round_score}\n{P1.name}:{P1.round_score}\n")
                # -------------------------------------
            round_reset()
            # -------------------------------------
    if player == P1:
        play_1(P2)
    else:
        play_1(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def round_reset():
    for player in (P1, P2):
        player.finished_rounds_scores.append(player.round_score)
        player.name = 'Name'
        player.the_draw = None
        player.hand.clear()
        player.play_cards.clear()
        player.play_cards_wild_cards.clear()
        player.initial_played_card_count = 0
        player.final_played_card_count = 0
        player.red_3_meld.clear()
        player.black_3_meld.clear()
        player.melds.clear()
        player.len_2_temp_melds_list.clear()
        player.going_out = None
        player.went_out_concealed = False
        player.finished_rounds_scores.clear()
        # -------------------------------------
    win_check()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def win_check():
    for player in players:
        if player.total_score >= 5000:
            print(f"Congratulations, {player.name}, you were the first to reach 5,000 points, therefore you are the winner! You are the champion, my friend!!!")
            # -------------------------------------
            p1_game_summary_string = (f"{P1.name}'s Game Summary! :\n\nRound Scores :\n" + '\n'.join(['%s']*len(player.finished_rounds_scores)) % tuple(player.finished_rounds_scores) + "\n")
            p2_game_summary_string = (f"{P2.name}'s Game Summary! :\n\nRound Scores :\n" + '\n'.join(['%s']*len(player.finished_rounds_scores)) % tuple(player.finished_rounds_scores) + "\n")
            # -------------------------------------
            while True:
                try:
                    play_again_input = input("Would you like to play again?\n\n> ")
                    if play_again_input.lower() not in ('y', 'n'):
                        raise ValueError
                    break
                except ValueError:
                    print("\nSorry, but there was a problem with your input. Please try again. Make sure that your input is either 'Y' or 'N' (Yes or No).\n)
            if play_again_input.lower() == 'y':
                return the_draw_1()
            sys.exit()
            # -------------------------------------
    the_draw_1()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Main Run loop. Runs game until a player wins.
def game_run():
    print("game_run\n")
    # -------------------------------------
    run = 1
    while run == 1:
        print("run\n")
        the_draw_1()
        print("run end\n")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Runs the game, until someone wins!
game_run()
