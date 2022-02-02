# ------------------------------------------

# Things to do
# 1) Need to implement a system for handling the resetting of values upon a round ending.
# 2) Implement a system for changing cards and melds to a more readable format when used in printed outputs. (i.e. - 10 - Diamonds / 10 of Diamonds / 10 Diamonds, 9 Hearts, 8 Spades
# 3) Have to finish section in valid_play_check_and_sort where I am dealing with when the play consists of only wild cards.
# 4) Ensure that there is always a proper hand off between the deck, the player's hand, the play cards, the melds, and the discard piles. Ensure that appends are always connected to pops, etc, unless that particular list is going to be .clear()-ed.
# 4a) Am currently going through valid_play_check_and_sort checking for this.
# 4b) Doing now - Checking all instances of player.hand to ensure proper transfer of cards to and from it. (~60% complete)
# 5) Go through the entire script to look for errors, bad logic, places to improve via a function, altering of loops, etc. '# ***' - denotes that line of code has been inspected and found valid and good.
# 6) Write some thorough tests for the program to go through for finding and fixing hidden bugs.
# 7) "Which card would you like to discard? Your available cards in hand are:" - Following this string output, (after trying to play all cards in the hand), the cards are not printed out. Seems as if the cards are not being placed back into the hand.
# 8) Make sure that meld_check is going off of a set, recorded end-round score, and not a current, ever-changing score pool.
# 9) Implement some tests.
# 10) Go through the entire script to remove all extra comments and test functions, etc.

# -------------------------------------
# ------------------------------------------
# -------------------------------------
import random
# -------------------------------------
# ------------------------------------------
# -------------------------------------
run = 0
# -------------------------------------
# ------------------------------------------
# -------------------------------------
class Deck():
    def __init__(self):
        self.deck = []
        self.draw_ranks = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Ja":11, "Q":12, "K":13, "A":14}
        self.draw_suite_ranks = {"S":4, "H":3, "D":2, "C":1}
        self.ranks = {"Jo":50, "2":50, "3":5, "4":5, "5":5, "6":5, "7":5, "8":10, "9":10, "10":10, "Ja":10, "Q":10, "K":10, "A":20}
        self.suites = ["H", "D", "S", "C"]
        self.discard_pile = [("None", "None")]
        self.discard_pile_is_frozen = False
        self.black_3s = [('3', 'C'), ('3', 'S')]
        self.red_3s = [('3', 'H'), ('3', 'D')]
        self.wild_cards = [('2', 'D'), ('2', 'H'), ('2', 'S'), ('2', 'C'), ('Jo', '')]
        self.wild_card_discards = ["Jo", "2", "3"]

    @property
    def face_up_discard(self):
        return self.discard_pile[-1]

    def create_deck(self):
        for rank in self.ranks:
            if rank != "Jo":
                for suite in self.suites:
                    self.deck.append((rank,suite))
            else:
                for Jo in range(2):
                    self.deck.append((rank,""))
# -------------------------------------
# ------------------------------------------
# -------------------------------------
class Player():
    def __init__(self, start_name = None):
        self.start_name = start_name
        self.name = "Name"
        self.the_draw = None
        self.hand = []
        self.play_cards = []
        self.play_cards_wild_cards = []
        self.red_3_meld = []
        self.melds = []
        self.len_2_temp_melds_list = []
        self.maxed_out_wild_card_melds = []
        self.going_out = None
        self.total_score_value = 0

    # ------------------------------------------

    @property
    def draw_card(self):
        if len(self.hand) > 0:
            draw_card = self.hand[0]
            return draw_card

    # ------------------------------------------

    @property
    def draw_card_val(self):
        return Deck().draw_ranks.get(self.draw_card[0])

    # ------------------------------------------

    @property
    def play_cards_val(self):
        total_value = 0
        for card in play_cards:
            total_value += Deck().ranks.get(card[0])
        return total_value

    # ------------------------------------------

    @property
    def meld_requirement(self):
        meld_requirement = 0
        if self.total_score <= -1:
            meld_requirement = 15
        elif 0 <= self.total_score <= 1495:
            meld_requirement = 50
        elif 1500 <= self.total_score <= 2995:
            meld_requirement = 90
        elif 3000 <= self.total_score:
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

    # ------------------------------------------

    @property
    def has_canasta(self):
        has_canasta = False
        for meld in self.melds:
            if len(meld) >= 7:
                has_canasta = True
        return has_canasta

    # ------------------------------------------

    @property
    def round_score(self):
        wild_card_canasta_check_count = 0
        round_score_val = 0
        for meld in self.melds:
            for card in meld:
                round_score_val += Deck().ranks.get(card[0])
        if self.going_out == True:
            round_score_val += 100
            round_score_val += (self.red_3_count * 100)
            if self.went_out_concealed == True:
                round_score_val += 100
            if self.red_3_count == 4:
                round_score_val += 400
        elif self.going_out == False:
            if self.has_canasta == True:
                round_score_val += (self.red_3_count * 100)
                for meld in self.melds:
                    if len(meld) >= 7:
                        for card in meld:
                            if card in Deck().wild_cards:
                                natural_canasta = False
                                wild_card_canasta_check_count += 1
                        if wild_card_canasta_check_count == 7:
                            if len(meld) == 7:
                                round_score_val +=  1000
                        if natural_canasta == True:
                            round_score_val += 500
                        else:
                            round_score_val += 300
            if player.has_canasta == False:
                self.round_score -= (self.red_3_count * 100)
                if self.red_3_count == 4:
                    round_score_val -= 400
        return round_score_val

    # ------------------------------------------

    @property
    def total_score(self):
        self.total_score_value += self.round_score
        return self.total_score_value
# -------------------------------------
# ------------------------------------------
# -------------------------------------
# Below - Creates the MasterDeck & Deck2, shuffles them, and combines the two together, with MasterDeck becoming the Deck for the game.
MasterDeck = Deck()
Deck2 = Deck()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
MasterDeck.create_deck()
Deck2.create_deck()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
random.shuffle(MasterDeck.deck)
random.shuffle(Deck2.deck)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for card in Deck2.deck:
    MasterDeck.deck.append(card)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
# Below - Creates the players, and gives them starting names for identification at start of game.
P1 = Player("Player 1")
P2 = Player("Player 2")
players = [P1, P2]
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def the_draw_1(player=P1):
    # First Function for Game Loop. Handles logic for sequencing of the_draws for when certain criteria require certain sections to be rerun.
    print("draw 1\n")
    if player == P1:
        for player in players:
            print("draw_1 part 1\n")
            the_draw_2(player)
        for player in players:
            print("draw_1 part 2\n")
            the_draw_3(player)
    else:
        print("draw_1 part 3\n")
        the_draw_2(player)
        the_draw_3(player)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def the_draw_2(player):
    # Follow Up Stem (#1) from The_Draw_1 for Game Loop. Handles name creation, draw card choice (to determine first player), and ensures that if a Joker is drawn during this process, it is reset and redone (Logic for that handled in draw_joker_check).
    print("draw 2")
    if player.name == "Name":
        player.name = input("\n{player}, what is your name? \n\n> ".format(player = player.start_name))
    player.the_draw = int(input("\n{p_name}, Select your card from the stack to determine which player will have the first play. (Pick a card, represented as a number from 1-108)\n\n> ".format(p_name = player.name)))
    player.hand.append(MasterDeck.deck.pop(player.the_draw - 1))
    print("\nYou drew a {p_draw_card}\n".format(p_draw_card = player.draw_card))
    # ------------------------------------------
    draw_joker_check(player)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def draw_joker_check(player):
    # Follow up to The_Draw_2 for Game Loop. Checks a player's draw card to ensure it is not a Joker, and if it is, redirects the process back to the_draw_1, to be redone. # ***
    print("draw joker check\n") # ***
    if player.draw_card[0] == "Jo": # ***
        print("Sorry, you picked a Joker, which is not available for use during The Draw! You must choose another card!\n") # ***
        MasterDeck.deck.append(player.hand.pop(0)) # ***
        return the_draw_1(player) # ***
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def the_draw_3(player):
    # Follow Up Stem (#2) from The_Draw_1 for Game Loop. Checks whether or not the players have the same draw card, and if they do, redirects the process back to the_draw_1 and places player cards back into the MasterDeck. Also checks to see who wins the draw, and sends off to the_deal after determination.
    print("draw 3\n")
    # ------------------------------------------
    if P1.draw_card == P2.draw_card:
        print("\nYou have the same exact card! You both must pick another card!\n")
        # ------------------------------------------
        return_draw_card(players)
        return the_draw_1()
    elif P1.draw_card_val > P2.draw_card_val:
        return_draw_card(players)
        the_deal(P1,P2)
    elif P2.draw_card_val > P1.draw_card_val:
        return_draw_card(players)
        the_deal(P2,P1)
    elif P1.draw_card_val == P2.draw_card_val:
        if Deck().draw_suite_ranks.get(P1.draw_card[1]) > Deck().draw_suite_ranks.get(P2.draw_card[1]):
            return_draw_card(players)
            the_deal(P1,P2)
        else:
            return_draw_card(players)
            the_deal(P2,P1)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def return_draw_card(players):
    # Stem from the_draw_3. Simple function to return the draw card used to determine first play from player.hand back into MasterDeck.deck(). For purpose of reducing amount of repeated code. # ***
    print("return_draw_card\n") # ***
    for player in players: # ***
        MasterDeck.deck.append(player.hand.pop(0)) # ***
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def the_deal(player1, player2): # ***
    # Follow up to Draw_3 for Game Loop. Handles dealing, sorting, printing, red 3 checking each player their cards, then creates a discard pile from MasterDeck. # ***
    print("the deal\n") # ***
    # ------------------------------------------
    # Below - Deals each player their 11 cards, sorts them, prints them, and checks for Red 3s. # ***
    for player in (player1, player2): # ***
        for card in range(11): # ***
            player.hand.append(MasterDeck.deck.pop(0)) # ***
        print("{name} is dealt 11 cards. Your hand consists of:\n".format(name = player.name)) # ***
        sort_player_cards(player) # ***
        iterated_and_numbered_list_printer(player.hand) # ***
        red_3_check(player) # ***
    # -----------------------------------------
    # Below - Creates the discard pile from the MasterDeck # ***.
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(0)) # ***
    # ------------------------------------------
    play_1(player1) # ***
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def sort_player_cards(player):
    # Stem (#1) from The_Deal for Game Loop. Sorts player cards by converting the ranks into a integer value via sorter_key_function, and then running that function through .sort(). Could just create a dict attribute that lists these values as integers instead of doing this.
    print("sort_player_cards\n")
    # ------------------------------------------
    non_num_card_rank_sort_value = {'Ja':11, 'Q':12, 'K':13, 'A':14, 'Jo':15}
    # ------------------------------------------
    def sorter_key_function(card):
        if card[0] in non_num_card_rank_sort_value:
            int_rank = non_num_card_rank_sort_value.get(card[0])
            return int_rank
        else:
            return int(card[0])
    # ------------------------------------------
    player.hand.sort(key=sorter_key_function)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def iterated_and_numbered_list_printer(passed_list_1, passed_list_2 = None):
    # Miscellaneous function for handling printed lists that I want to be numbered; for the purpose of input game selection via the preceding num.
    print("iterated_and_numbered_list_printer\n")
    num = 1
    for item in passed_list_1:
        if item != passed_list_1[-1]:
            print("{num}) {item}".format(num = num, item = item))
        else:
            print("{num}) {item}\n".format(num = num, item = item))
        num += 1
    if passed_list_2 != None:
        for item in passed_list_2:
            if item != passed_list_2[-1]:
                print("{num}) {item}".format(num = num, item = item))
            else:
                print("{num}) {item}\n".format(num = num, item = item))
            num += 1
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def red_3_check(player, drawn = False): # ***
    # Stem (#3) from the_deal() for game_run() & play_1() after stock_draw(). Handles Red 3s according to game rules. # ***
    print("red 3 check\n") # ***
    red_3_quantity = 0 # ***
    # ------------------------------------------
    for red_3 in Deck().red_3s: # ***
        while red_3 in player.hand: # ***
            # ------------------------------------------
            # Below - Handles drawn Red 3s. Removes them from player.hand, replaces it with a newly drawn card from the deck, and prints associated output. # ***
            if drawn == True: # ***
                print("You drew a Red 3! The {red_3} will be placed in your Red 3 meld, and you will automatically draw another card to replace it.".format(red_3 = red_3)) # ***
                player.red_3_meld.append(player.hand.pop(-1)) # ***
                player.hand.append(MasterDeck.deck.pop(0)) # ***
                print("In place of your Red 3, you drew a: {replacement_card}\n".format(replacement_card = player.hand[-1])) # ***
            # ------------------------------------------
            # Below - Handles initial Red 3 check. Appends red_3_meld to player.melds, replaces it with a new card from MasterDeck.deck, & prints out associated output for initial Red 3 distribution. # ***
            elif drawn == False: # ***
                red_3_quantity += 1 # ***
                player.red_3_meld.append(player.hand.pop(player.hand.index(red_3))) # ***
                player.hand.append(MasterDeck.deck.pop(0)) # ***
    # ------------------------------------------
    if red_3_quantity == 4: # ***
        print("Congratulations! You have 4 Red 3s, therefore you get a bonus of 400 points (granted that when the round ends, you have at least 1 Canasta)! The rules dictate that all Red 3s must be played down, and you will withdraw a replacement card from the stock for each one in your hand!\n") # ***
    elif red_3_quantity > 0: # ***
        print("You have {red_3_quantity} Red 3(s) in your hand! The rules dictate that all Red 3s must be played down, and you have to withdraw a card replacement card from the stock for each one in your hand!\n".format(red_3_quantity = red_3_quantity)) # ***
        red_3_replacements_str = ("In place of your Red 3(s), you drew: " + ', '.join(['%s']*len(player.red_3_meld)) + "\n") % tuple(player.hand[-(len(player.red_3_meld)):]) # ***
        print(red_3_replacements_str) # ***
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def play_1(player):
    # Follow up to The_Deal for Game Loop.
    print("play_1\n")
    # ------------------------------------------
    draw_method = input("{name}, which method would you like to use to draw?\n\n1) Draw from Stack\n2) Draw from Discard Pile\n\n> ".format(name = player.name))
    if draw_method == "1":
        # Draw from Stock.
        stock_draw(player)
        red_3_check(player, True)
    else:
        # Draw from Discard Pile.
        draw_discard_pile(player)
    print("{name}, it is your turn to play!\n".format(name = player.name))
    # ------------------------------------------
    play_2(player)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def stock_draw(player): # ***
    # Stem (#1) from play_1 function. For drawing a card from the stock & giving associated output. # ***
    print("\nstock_draw\n") # ***
    player.hand.append(MasterDeck.deck.pop(0)) # ***
    print("{name} drew a {card} from the stack.\n".format(name = player.name, card = player.hand[-1])) # ***
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def draw_discard_pile(player): # ***
    # Stem (#2) from play_1 function. For drawing discard pile. # ***
    print("draw_discard_pile\n") # ***
    # Below - Checking to see if the deck has a wild_card or a black_3 inside of it (if it's internally or topically frozen). # ***
    for card in MasterDeck.discard_pile: # ***
        if card not in Deck().wild_cards and card not in Deck.black_3s: # ***
            MasterDeck.discard_pile_is_frozen = False # ***
        else: # ***
            MasterDeck.discard_pile_is_frozen = True # ***

    # ------------------------------------------

    # Below Section - For discard pile draw attempt when it is not internally or topically frozen. Redirects to eligibility determinations based on player's initial meld status, and finalizes determination by either allowing drawing of the discard pile, or denial and subsequent redirection back to play_1. # ***
    if MasterDeck.discard_pile_is_frozen == False: # ***
        # Below - Checks the player's existing melds to see if they have the top discard rank already melded to be used as a means to withdraw the discard pile.
        for meld in player.melds: # ***
            if MasterDeck.face_up_discard[0] == meld[0][0]: # ***
                meld.append(MasterDeck.discard_pile.pop(-1)) # ***
                for card in MasterDeck.discard_pile[:]: # ***
                    player.hand.append(MasterDeck.discard_pile.pop(MasterDeck.discard_pile.index(card))) # ***
                print("You successfully drew the discard pile!\n") # ***
                return play_2(player) # ***

        # ------------------------------------------

        # Below - Checks the player's hand to see if they have the required cards in their hand (for when they have no melds that match the top discard) as an alternative means to pick up the discard pile. # ***
        hand_check_for_discard_pile_draw(player)
        # Below Section - Checks the player's attempted meld from above (using the face up discard) to see if it reaches the meld_requirement. If it does, player successfully draws discard pile, popping all of the discards from MasterDeck.discard_pile and appending them to player.hand, and also popping the temp_meld from player.play_cards to be appended to player.melds. # ***
        if meld_check(player) == True:
            player.melds.append(player.play_cards.pop(0))
            # Below - Pops each card off of MasterDeck.discard_pile & appends them to player.hand. # ***
            for card in MasterDeck.discard_pile[:]: # ***
                player.hand.append(MasterDeck.discard_pile.pop(MasterDeck.discard_pile.index(card))) # ***
            print("You successfully drew the discard pile!\n")
            return play_2(player)
        else:
            print("You were able to create a valid meld from the top discard, but unfortunately the meld did not meet the minimum meld requirement score.\n")
            if len(player_hand_wild_cards) > 0:
                print("You still have wild card(s) left in your hand that you could use to extend this meld, which may help you reach the minimum meld requirement score. Would you like to try and do this? (Y/N)\n")
                retry_input = ("> ")
                if retry_input.lower() == 'y':
                    print("Okay, the remaining wild cards that you can use are listed below. Which one would you like to use?\n")
                    iterated_and_numbered_list_printer(player_hand_wild_cards)
                    wild_card_choice = input("> ")
                    player.melds[0].append(player.hand.pop(player.hand.index(player_hand_wild_cards.pop(int(wild_card_choice - 1)))))
                    if meld_check(player) == True:
                        print("You successfully drew the discard pile!\n")
                    # HAVE TO GO BACK AND ENSURE THIS ENTIRE draw_discard_pile FUNCTION IS CORRECT. IT IS NOT COMPLETED AS OF YET. STOPPED HERE!
                    # Below - Is a recursive copy of above code: lines 400-411. To reduce repetition, could I just use a while loop? Meaning, while there are wild cards left in the hand, unless that subsequent attempt succeeds, continue to loop through, but if it succeeds, break out of it via break or a function call.
                    else:
                        print("You were able to create a valid meld from the top discard, but unfortunately the meld did not meet the minimum meld requirement score.\n")
                        if len(player_hand_wild_cards) > 0:
                            print("You still have wild card(s) left in your hand that you could use to extend this meld, which may help you reach the minimum meld requirement score. Would you like to try and do this? (Y/N)\n")
                            retry_input = ("> ")
                            if retry_input.lower() == 'y':
                                print("Okay, the remaining wild cards that you can use are listed below. Which one would you like to use?\n")
                                iterated_and_numbered_list_printer(player_hand_wild_cards)
                                wild_card_choice = input("> ")
                                player.melds[0].append(player.hand.pop(player.hand.index(player_hand_wild_cards.pop(int(wild_card_choice - 1)))))
                                if meld_check(player) == True:
                                    print("You successfully drew the discard pile!\n")

    if MasterDeck.discard_pile_is_frozen == True:
        if MasterDeck.face_up_discard[0] not in Deck().wild_cards and MasterDeck.face_up_discard[0] not in Deck().black_3s:
            card_count = 0
            matched_card_list = []
            for card in player.hand[:]:
                if card[0] == MasterDeck.face_up_discard[0]:
                    matched_card_list.append(card)
                    card_count += 1
            if card_count >= 2:
                temp_meld = []
                for matched_card in matched_card_list:
                    temp_meld.append(matched_card)
                    player.hand.pop(player.hand.index(matched_card))

                # ------------------------------------------

                player.hand.append(MasterDeck.discard_pile.pop(-1))
                temp_meld.append(player.hand.pop(player.hand[-1]))
                player.play_cards.append(temp_meld)

                # ------------------------------------------

                if meld_check(player) == True:
                    player.melds.append(temp_meld)
                    MasterDeck.discard_pile
                    print("You successfully drew the discard pile!\n")
                else:
                    MasterDeck.discard_pile.append(player.play_cards.pop(-1))
                    for card in player.play_cards[:]:
                        player.hand.append(player.play_cards.pop(player.play_cards.index(card)))
                    print("Sorry, but you cannot draw the discard pile because you're attempted meld did not reach the minimum meld requirement score. All of the cards from the attempted play will be restored to their original location, and you will have to try another play.\n")
                    return play_1(player)
            else:
                print("Sorry, but you cannot draw the discard pile because you don't have 2 natural matches for the top discard to be used as a meld, which is what is required when the discard pile is frozen.\n")
                return play_1(player)
        else:
            print("Sorry, but you cannot draw the discard pile, as it's face card is either a Black 3 or a Wild Card.\n")
            return play_1(player)
# -------------------------------------# ------------------------------------------
# ------------------------------------------# ------------------------------------------
# -------------------------------------# ------------------------------------------
def hand_check_for_discard_pile_draw(player):
    print("hand_check_for_discard_pile_draw\n")

    # ------------------------------------------

    card_count = 0 # ***
    matched_card_list = [] # ***
    for card in player.hand[:]: # ***
        if card[0] == MasterDeck.face_up_discard[0]: # ***
            matched_card_list.append(card) # ***
            card_count += 1 # ***
    if card_count >= 2: # ***
        temp_meld = [] # ***
        for matched_card in matched_card_list: # ***
            temp_meld.append(matched_card) # ***
            player.hand.pop(player.hand.index(matched_card)) # ***
        temp_meld.append(MasterDeck.discard_pile.pop(-1)) # ***
        player.play_cards.append(temp_meld) # ***

    # ------------------------------------------

    elif card_count == 1: # ***
        player_hand_wild_cards = [] # ***
        for card in player.hand: # ***
            if card in Deck().wild_cards: # ***
                player_hand_wild_cards.append(card) # ***

        # ------------------------------------------

        if len(player_hand_wild_cards) > 0: # ***
            yn = input("Since you only have one of the natural cards that match the face up discard, you would have to use a wild card to draw the discard pile. Would you like to do this? (Y/N)\n\n> ") # ***
            if yn.lower() == "y": # ***
                temp_meld = [] # ***
                wild_cards_str = ("Which wild card would you like to use? You have these wild cards:\n") # ***
                iterated_and_numbered_list_printer(player_hand_wild_cards) # ***
                wild_card_choice = input("> ") # ***
                temp_meld.append(MasterDeck.discard_pile.pop(-1)) # ***
                temp_meld.append(player.hand.pop(player.hand.index(player_hand_wild_cards[int(wild_card_choice - 1)]))) # ***
                temp_meld.append(player.hand.pop(player.hand.index(matched_card_list[0]))) # ***
                player.melds.append(temp_meld) # ***
            else: # ***
                print("Okay, the attempt will be cancelled, and you will be redirected back to the draw method options.\n") # ***
                return play_1(player) # ***

    # ------------------------------------------

    else: # ***
        print("Sorry, but you do not meet the requirements to be able to withdraw from the discard pile because you only had 1 card matching the top discard, with no wild card in your hand to be played as part of a meld alongside it.\n") # ***
        return play_1(player) # ***
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def play_2(player): # ***
    # Follow up to Play_1 for Game loop. # ***
    print("play_2\n") # ***

    # ------------------------------------------

    player.play_cards.clear() # ***
    player.play_cards_wild_cards.clear() # ***
    # ------------------------------------------

    play_choice = input("{name}, what would you like to do with your turn?\n\n 1) Play Cards\n 2) Discard\n\n> ".format(name = player.name)) # ***
    if play_choice == "1": # ***
        print("\n{name}, which cards would you like to play? (Use the ordered number of the card(s) as listed below. (i.e. - '1,3,4,8')\n".format(name = player.name)) # ***
        iterated_and_numbered_list_printer(player.hand) # ***
        play_cards_input = input("> ") # ***

        # ------------------------------------------

        play_cards_list = list(play_cards_input) # ***
        temp_char_holder = {} # ***
        index = -1 # ***
        consec_int_counter = 0 # ***
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # ***

        # ------------------------------------------

        for char in play_cards_list: # ***
            if char in numbers: # ***
                index += 1 # ***
                temp_char_holder[index] = int(char) # ***
                consec_int_counter += 1 # ***
                if consec_int_counter == 2: # ***
                    concatenated_int = int(str(temp_char_holder.pop(index - 1)) + str(temp_char_holder.pop(index))) # ***
                    temp_char_holder[index - 1] = concatenated_int # ***
            else: # ***
                 consec_int_counter = 0 # ***

                 # ------------------------------------------

        temp_char_holder_sorted = sorted(temp_char_holder.values(), reverse = True) # ***

        # ------------------------------------------

        for typed_value in temp_char_holder_sorted: # ***
            player.play_cards.append(player.hand.pop(typed_value - 1)) # ***

            # ------------------------------------------

        if valid_play_check_and_sort(player) == True: # ***
            discard(player) # ***
        else: # ***
            play_2(player) # ***
    else: # ***
        discard(player) # ***

    # ------------------------------------------

    # Leads to restarting of Game Loop via redirect upon finish to Play_1, unless player went out; in that case, ends round and then redirects.
    return went_out_check(player) # ***
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def meld_check(player):
    # Stems from play_2. Checks for player meld requirements. If player hasn't met intial meld, determines if set of play cards reaches the meld_requirement score (does not check for valid play). # ***
    print("meld_check\n") # ***
    # Below - If you are trying to meet initial meld. # ***
    if player.round_score < player.meld_requirement:
        meld_score = 0
        for temp_meld in player.play_cards:
            for card in temp_meld:
                value = Deck().ranks.get(card[0])
                meld_score += value
        if meld_score >= player.meld_requirement:
            return True
        else:
            return False
    # If you have already initially melded, and want to add, or add to, a meld.
    else:
        return True
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def valid_play_check_and_sort(player): # ***
    # Stems (#1) from Play_2. For ensuring that a set of attempted play cards are valid according to game rules. # ***
    print("\nvalid_play_check_and_sort\n") # ***

    # ------------------------------------------

    play_cards_new_ranks = [] # ***
    bad_len_temp_melds_list_print = [] # ***
    play_cards_removed_black_3s_print = [] # ***

    # ------------------------------------------

    initial_played_card_count = player.played_card_count # ***

    # ------------------------------------------

    for card in player.play_cards[:]: # ***
        # Below - If card is a valid, non-wild card that is the first of it's rank iterated through in the group of play cards. Creates a new temp_meld for it to be placed into, and the temp_meld is then placed back into player.play_cards, which is where other cards of the same rank will be placed.
        if card not in Deck().black_3s and card not in Deck().wild_cards and card[0] not in play_cards_new_ranks: # ***
            play_cards_new_ranks.append(card[0]) # ***
            temp_meld = [] # ***
            temp_meld.append(player.play_cards.pop(player.play_cards.index(card))) # ***
            player.play_cards.append(temp_meld) # ***
        # Below - If card is a wild card. Puts them all in their own special meld/list.
        elif card in Deck().wild_cards: # ***
            player.play_cards_wild_cards.append(player.play_cards.pop(player.play_cards.index(card))) # ***
        # Below - If card's rank exists in play_cards_new_ranks. Sorts the card into the temp_meld that matches the card's rank. For grouping cards of the same rank together.
        elif card[0] in play_cards_new_ranks: # ***
            for item in player.play_cards: # ***
                if type(item) == list: # ***
                    if card[0] == item[0][0]: # ***
                        item.append(player.play_cards.pop(player.play_cards.index(card))) # ***
        # Below - If card is a Black 3. Appends it to play_cards_removed_black_3s_print, which is used to print out all of these instances later on, and removes it from player.play_cards because Black 3s are never valid play cards.
        else: # ***
            play_cards_removed_black_3s_print.append(player.play_cards.pop(player.play_cards.index(card))) # ***

            # ------------------------------------------

    # Below - This is simply a test to ensure that my above code is properly removing all the correct cards and that none are left over in here. None should be in here, thus none should be printed. If it prints a card, that means the above section did not properly sort it or remove it. # ***
    for card in player.play_cards[:]: # ***
        if type(card) != list: # ***
            print("valid_play_check_and_sort didn't catch all cards: {card}".format(card = card)) # ***

            # ------------------------------------------
    # Below - Checks to see if the player has NOT met the initial meld requirements. If so, valid plays are different than if they had met the requirement, thus puts different restrictions on what a valid play is.
    if player.round_score < player.meld_requirement: # ***
        print("player.round_score < meld\n") # ***

        # --------------------------------------

        if len(player.play_cards) < 3:
            print("Sorry, but you must play at least 3 cards for a new meld. Please select a new set of cards to play, or you can choose to discard if you like.\n")
            for card in player.play_cards:
                player.hand.append(card)
            return False

            # --------------------------------------

        if len(play_cards_removed_black_3s_print) > 0:
            print("Sorry, but you cannot play Black 3(s) in this way. Black 3s can only be used to freeze the discard pile. The Black 3(s) that are being removed from your attempted play cards back into your hand are as follows:\n")
            iterated_and_numbered_list_printer(play_cards_removed_black_3s_print)
            for card in play_cards_removed_black_3s_print:
                player.hand.append(play_cards_removed_black_3s_print.pop(play_cards_removed_black_3s_print.index(card)))

            # --------------------------------------
        # Below - This is in the incorrect spot. This list has not been addressed yet at this point.
        if len(bad_len_temp_melds_list_print) > 0:
            print("Sorry, but you cannot create a new meld without at least 2 natural cards of that rank, or without a wild card to add to it to reach the 3 card minimum meld requirement. The attempted meld(s) will be removed and placed back in your hand:\n")
            iterated_and_numbered_list_printer(bad_len_temp_melds_list_print)
            for card in bad_len_temp_melds_list_print:
                player.hand.append(bad_len_temp_melds_list_print.pop(bad_len_temp_melds_list_print.index(card)))

            # --------------------------------------

        if len(player.play_cards) == 0:
            if len(player.play_cards_wild_cards) < 7:
                print("Sorry, but you cannot play a meld of only wild cards, unless that play consists of a complete Wild Card Canasta.\n")
                for card in player.play_cards_wild_cards:
                    player.hand.append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(card)))
            else:
                player.play_cards.append(player.play_cards_wild_cards)
                player.play_cards_wild_cards.clear()

                # --------------------------------------

        else:
            for temp_meld in player.play_cards[:]:
                if len(temp_meld) < 2:
                    for card in temp_meld:
                        player.hand.append(card)
                    bad_len_temp_melds_list_print.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
                elif len(temp_meld) == 2:
                    if len(player.play_cards_wild_cards) < 1:
                        for card in temp_meld:
                            player.hand.append(card)
                        bad_len_temp_melds_list_print.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
                    else:
                        # Below - Can I just nix len_2_temp_melds_list and just operate on the player.melds list instead? From this else clause.
                        player.len_2_temp_melds_list.append(player.play_cards.pop(player.play_cards.index(temp_meld)))

                        # --------------------------------------

            # Below - remove the temp_meld from player.len_2_temp_melds_list OR SOMETHING NEED TO MAKE IT SO THAT THIS LOOP WORKS CORRECTLY. AS IS IT DOES NOT RUN THIS PART AGAIN FOR WHEN WE HAVE 2 len_2 MELDS and 2 WILD CARDS. IT MOVES TO leftover_wild_card_handler INSTEAD ERRANTLY.

            while len(player.len_2_temp_melds_list) > 0: # ***
                if len(player.play_cards_wild_cards) > 0: # ***
                    print("The below meld(s) from your attempted play cards have only 2 cards in them. Since 3 cards are required for a valid meld, you must add a wild card to them for them to remain in play. It looks as if you have {len_num} wild card(s) in your set of play cards to use for this. Choose a meld from the list below that you would like to add a wild card to.\n".format(len_num = len(player.play_cards_wild_cards))) # ***
                    iterated_and_numbered_list_printer(player.len_2_temp_melds_list) # ***
                    num = str(len(player.len_2_temp_melds_list) + 1) # ***
                    print("{num}) I would rather use the wild card(s) elsewhere, and let the meld(s) be placed back into my hand.\n".format(num = num)) # ***
                    len_2_temp_meld_choice = int(input("> ")) - 1 # ***
                    if len_2_temp_meld_choice != int(num) - 1: # ***
                        print("\nWhich wild card would you like to add to the selected meld? Choose from the below choices.\n") # ***
                        iterated_and_numbered_list_printer(player.play_cards_wild_cards) # ***
                        wild_card_choice = int(input("> ")) - 1 # ***
                        print("\nYou successfully added the {wild_card} to your meld.\n".format(wild_card = player.play_cards_wild_cards[wild_card_choice])) # ***
                        player.len_2_temp_melds_list[len_2_temp_meld_choice].append(player.play_cards_wild_cards.pop(wild_card_choice)) # ***
                        player.play_cards.append(player.len_2_temp_melds_list.pop(len_2_temp_meld_choice)) # ***

                        # -------------------------------------

                    # Below - If the player chooses to place the meld(s) back into their hand, leaving the wild cards in play cards. # ***
                    else: # ***
                        print("\nOkay, the meld(s) will be put back into your hand, while the wild card(s) will continue to remain in your group of played cards. \n") # ***
                        for temp_meld in len_2_temp_melds_list:
                            for card in temp_meld:
                                player.hand.append(card)
                        player.len_2_temp_melds_list.clear() # ***

                        # -------------------------------------

                elif len(player.play_cards_wild_cards) == 0: # ***
                    for temp_meld in len_2_temp_melds_list:
                        for card in temp_meld:
                            player.hand.append(card)
                    player.len_2_temp_melds_list.clear() # ***

                    # -------------------------------------

            for temp_meld in player.play_cards[:]: # ***
                if len(temp_meld) == 2: # ***
                    player.play_cards.remove(temp_meld) # ***

                    # --------------------------------------

        leftover_wild_card_handler(player) # ***

        # --------------------------------------

        if meld_check(player) != True:
            print("Sorry, but the value of your play cards after filtering and sorting is not enough to meet the minimum meld requirement of {player_meld_requirement}\n".format(player_meld_requirement = player.meld_requirement))
            return False

            # ------------------------------------------

    # If player.round_score > meld_requirement:

    else:
        print("player_round_score > meld\n")
        for temp_meld in player.play_cards[:]:
            for meld in player.melds:
                if temp_meld[0][0] == meld[0][0]:
                    for card in temp_meld:
                        meld.append(card)
                    player.play_cards.remove(temp_meld)

                    # ------------------------------------------

            if len(temp_meld) < 2:
                print("Sorry, but you cannot create a new meld without having at least 2 natural cards of that rank in the initial meld. This attempted meld: {temp_meld} will unfortunately be removed and placed back in your hand.\n".format(temp_meld = temp_meld))
                player.play_cards.remove(temp_meld)
            elif len(temp_meld) == 2:
                if len(player.play_cards_wild_cards) > 0:
                    if len(player.play_cards_wild_cards) > 1:
                        print("Which wild card would you like to place in this meld: {temp_meld}?\n".format(temp_meld = temp_meld))
                        iterated_and_numbered_list_printer(player.play_cards_wild_cards)
                        wild_card_choice = int(input('\n > ')) - 1
                        temp_meld.append(player.play_cards_wild_cards.pop(wild_card_choice))
                    elif len(player.play_cards_wild_cards) == 1:
                        temp_meld.append(player.play_cards_wild_cards[0])
                else:
                    print("Sorry, but you only have 2 cards in this meld: {temp_meld}, and you don't have any wild cards to add on to it to reach the 3 card minimum meld requirement. This attempted meld will unfortunately be removed and placed back in your hand.\n".format(temp_meld = temp_meld))
                    player.play_cards.remove(temp_meld)

                    # -------------------------------------

        # Below - Checking to see if this play is only comprised of wild cards. If so, will determine where to place them, whether that be in a meld or replaced back into the hand. Methodology utilizes the first element/wild_card in play_cards_wild_cards without iterating through the list.
        if len(player.play_cards) == 0 and len(player.play_cards_wild_cards) > 0:
            if len(player.melds) > 0:
                while len(player.play_cards_wild_cards) > 0:
                    wild_card_only_play(player)
            else:
                print("Sorry, but there are no melds played by you, currently. Therefore there is nowhere to place your wild card(s) from your attempted play, so they will be placed back into your hand and you will have to choose another play.\n")
                return False

                # -------------------------------------

        leftover_wild_card_handler(player)

    # -------------------------------------

    for temp_meld in player.play_cards:
        player.melds.append(temp_meld)

    # -------------------------------------

    print("final play 2 player.melds print\n")
    iterated_and_numbered_list_printer(player.melds)

    # -------------------------------------

    final_played_card_count = player.played_card_count

    # -------------------------------------

    if len(player.hand) == 0:
        for temp_meld in player.play_cards:
            if len(temp_meld) >= 7:
                player.has_canasta = True
        if player.has_canasta == True:
            pass
        else:
            print("Sorry, but you seem to be trying to go out. \n")

            # -------------------------------------

    if initial_played_card_count == final_played_card_count:
        print("initial_played_card_count == final_played_card_count\n")
        return False
    else:
        print("True - initial_played_card_count != final_played_card_count\n")
        return True
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def wild_card_only_play(player):
    # Below Section - Altered copy of lines 743-766.
    print("Which meld from the list below would you like to add the {wild_card} to?\n".format(wild_card = play_cards_wild_cards[0]))
    iterated_and_numbered_list_printer(player.melds)
    temp_meld_num = str(len(player.melds) + 1)
    print("{temp_meld_num}) I would not like to use this wild card, and would rather have it be replaced back into my hand.\n".format(temp_meld_num = temp_meld_num))
    temp_meld_choice = int(input('\n')) - 1

    # -------------------------------------

    # Below - If player chooses not to use the wild card in the meld, it is popped from play_cards_wild_cards, to be placed back into the player's hand.

    if temp_meld_choice == int(temp_meld_num) - 1:
        print("Okay, the wild card will be placed back into your hand.\n")
        player.hand.append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card)))

    # -------------------------------------

    # Below - If player chooses to play the wild card to the chosen meld. Ensures that the meld is not in maxed_out_wild_card_melds, and if not appends the wild card to the meld, removing it from play_cards_wild_cards.

    else:
        maximum_wild_card_amount_check(player, player.melds)
        if player.melds[temp_meld_choice] not in player.maxed_out_wild_card_melds:
            print("You successfully added the {wild_card} to your meld.\n".format(wild_card = player.play_cards_wild_cards[player.play_cards_wild_cards.index(wild_card)]))
            player.melds[temp_meld_choice].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card)))
        else:
            print("Sorry, but this meld currently has the maximum amount of wild cards (4) that you can have in a meld. You must choose a different meld to add this card to.\n")
            return wild_card_only_play(player)
# -------------------------------------
# -------------------------------------
# -------------------------------------
def maximum_wild_card_amount_check(player, passed_meld_list):
    wild_card_count = 0
    for meld in passed_meld_list:
        for card in meld:
            if card in Deck().wild_cards:
                wild_card_count += 1
    if wild_card_count >= 4:
        player.maxed_out_wild_card_melds.append(meld)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def leftover_wild_card_handler(player):
    # Stems from valid_play_check_and_sort function. For handling leftover wild cards in attempted play cards. Currently code is in aforementioned func with note. Need to transfer code from there to here.
    print("leftover_wild_card_handler\n")

    # ------------------------------------------

    while len(player.play_cards_wild_cards) > 0:
        if len(player.play_cards) > 0 or len(player.melds) > 0:
            print("It looks as if you had a/some wild card(s) left over after your play cards were sorted and validated. Below are the remaining wild card(s) in your set of played cards.\n")
            iterated_and_numbered_list_printer(player.play_cards_wild_cards)
            print("Which meld from the list below would you like to add a leftover wild card to?\n")
            iterated_and_numbered_list_printer(player.play_cards, player.melds)
            temp_meld_num = str(len(player.play_cards) + len(player.melds) + 1)
            print("{temp_meld_num}) I would not like to use any of my leftover wild cards, and would rather have them be replaced back into my hand.".format(temp_meld_num = temp_meld_num))
            temp_meld_choice = int(input('\n')) - 1
            if int(temp_meld_choice) == int(temp_meld_num) - 1:
                break
            elif temp_meld_choice >= (temp_meld_num_at_player_meld_transition - 1):
                maximum_wild_card_amount_check(player, player.melds)
                if player.melds[temp_meld_choice] not in player.maxed_out_wild_card_melds:
                    player.melds[temp_meld_choice].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card)))
                else:
                    print("Sorry, but this meld currently has the maximum amount of wild cards (4) that you can have in a meld. You must choose a different meld to add this card to.\n")
            else:
                maximum_wild_card_amount_check(player, player.play_cards)
                if player.play_cards[temp_meld_choice] not in player.maxed_out_wild_card_melds:
                    player.play_cards[temp_meld_choice].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card)))
                else:
                    print("Sorry, but this meld currently has the maximum amount of wild cards (4) that you can have in a meld. You must choose a different meld to add this card to.\n")
        else:
            print("You had wild card(s) left in your attempted play cards, but had nowhere to place them, or chose not to use them at this time, after valid play determinations and sorting, so they will be placed back into your hand.")
            player.play_cards_wild_cards.clear()
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def discard(player):
    # Stems (#2) from Play_2. For discarding.
    print("discard\n")

    print("Which card would you like to discard? Your available cards in hand are:\n")
    iterated_and_numbered_list_printer(player.hand)
    discard_input = int(input("\n> ")) - 1
    print("\nYou discarded the {discard}.\n".format(discard = (player.hand[discard_input])))
    MasterDeck.discard_pile.append(player.hand.pop(discard_input))
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def went_out_check(player):
    # Follow up to Play_2. For checking to see if players went out during turn. If not, redirects to beginning of game loop (Play_1). If so, ends round and redirects to The_Draw_1.
    print("went out check\n")

    if len(player.hand) == 0:
        player.going_out = True
        if player == player1:
            player2.going_out = False
            print("{p1} went out!\n\nRound Score:\n{p1}:{p1_round_score}\n{p2}:{p2_round_score}\n".format(p1 = player1.name, p1_round_score = player1.round_score, p2 = player2.name, p2_round_score = player2.round_score))
        else:
            player1.going_out = False
            print("{p2} went out!\n\nRound Score:\n{p2}:{p2_round_score}\n{p1}:{p1_round_score}\n".format(p2 = player2.name, p2_round_score = player2.round_score, p1 = player1.name, p1_round_score = player1.round_score))
        win_check()
        for player in (player1, player2):
            player.round_score_val = 0
        the_draw_1()
    else:
        if player == P1:
            play_1(P2)
        else:
            play_1(P1)
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def win_check():
    global run
    for player in players:
        if player.total_score >= 5000:
            print("Congratulations, {player_name}, you were the first to reach 5,000 points, therefore you are the winner! You are the champion, my friend!!!".format(player_name = player.name))
            run = 0
# -------------------------------------
# ------------------------------------------
# -------------------------------------
def game_run():
    # Main Run loop. Runs game until a player wins.

    global run
    run = 1
    while run == 1:
        print("run\n")
        the_draw_1()
        print("run end\n")
# -------------------------------------
# ------------------------------------------
# -------------------------------------
# Runs the game, until someone wins!
game_run()
