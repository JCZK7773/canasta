# ------------------------------------------
# Things to do:
# 1) Rework temp_melds, etc. from play_2 function so that when leftover_wild_card_handler function runs, it can automatically take in all of that information through calculated properties or something. Either that, or make it so that temp_melds, etc are passed into leftover_wild_card_handler function.
# 2) Implement code for ensuring that the Red 3 meld is treated differently from the rest of the melds, so that it does not show up as an option as a temp_meld when melding new play cards and handling leftover wild cards. I think I need to separate them from player.melds completely.
# 3) Fix the issue wherein after valid_play_check_and_sort the game code, as is, assumes that the player's played cards maintained the same score value prior to being filtered and sorted, meaning that it wrongfully assumes that the player may still exceed the threshold for minimum meld requirements, when indeed after this sorting and filtering, they no longer do exceed this amount, and thus should be rejected completely as a valid play.
# 4) Combine repeated code into logically solid functions.
# 4a) Check for places where above can be done.
# 5) Reworking most logic into the main game run loop?
# 6) Implement canasta recognition function (determines between natural canasta & mixed canastas
# 7) Implement rules for amount of wild cards in each meld, for full canastas & smaller melds. (WHICH IS ALWAYS 4x MAXIMUM PER MELD)
# 8) Implement proper rules for drawing discard pile. Look at rules on Bicycle Canasta rules for reference.
# 9) Fix problem in ?func? that is causing improper functionality when there are more than 1 len_2_melds. Currently not handling all the len_2_melds, but only iterating through once even though there is more opportunities to turn len_2_melds into valid 3 card melds with leftover wild cards.
# 10) Need to implement a system for handling the resetting of values upon a round ending.
# 11) Implement a system for changing cards and melds to a more readable format when used in printed outputs. (i.e. - 10 - Diamonds / 10 of Diamonds / 10 Diamonds, 9 Hearts, 8 Spades)
# 12) Create system for handling frozen discard pile. Pile is frozen whenever a wild card or a black 3 is discarded into it. After this, to draw the pile, player must have 2 natural of matching rank to subsequently placed top discard card in their HAND.
# 13) Fix player.total_score
# ------------------------------------------
import random
# ------------------------------------------
run = 0
# ------------------------------------------
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
# ------------------------------------------
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
        self.round_score_val = 0
        self.total_score_val = 0
        self.red_3_count = 0
        self.going_out = False
    # ------------------------------------------
    @property
    def draw_card(self):
        if len(self.hand) > 0:
            draw_card = self.hand[0]
            return draw_card
        else:
            pass
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
    def round_score(self):
        # Do I need to change this to reflect the fact that Red 3s count as Black 3s if player has no Canasta when the other goes out?
        for meld in self.melds:
            for card in meld:
                self.round_score_val += Deck().ranks.get(card[0])
        if self.going_out == True:
            self.red_3_count == len(self.red_3_meld)
            self.round_score_val += (self.red_3_count * 100)
            if self.red_3_count == 4:
                self.round_score_val += 400
        return self.round_score_val
    # ------------------------------------------
    @property
    def total_score(self):
        # Must fix because Red 3s turn into Black 3s (return negative value) if player goes out with no Canastas.
        for meld in self.melds:
            for card in meld:
                self.total_score_val += Deck().ranks.get(card[0])
        for red_3 in self.red_3_meld:
            self.total_score_val += 100
        return self.total_score_val
# ------------------------------------------
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
# ------------------------------------------
# Below - Creates the players, and gives them starting names for identification at start of game.
P1 = Player("Player 1")
P2 = Player("Player 2")
players = [P1, P2]
# ------------------------------------------
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
# ------------------------------------------
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
# ------------------------------------------
def draw_joker_check(player):
    # Follow up to The_Draw_2 for Game Loop. Checks a player's draw card to ensure it is not a Joker, and if it is, redirects the process back to the_draw_1, to be redone.
    print("draw joker check\n")
    if player.draw_card[0] == "Jo":
        print("Sorry, you picked a Joker, which is not available for use during The Draw! You must choose another card!\n")
        MasterDeck.deck.append(player.hand.pop(0))
        return the_draw_1(player)
# ------------------------------------------
def the_draw_3(player):
    # Follow Up Stem (#2) from The_Draw_1 for Game Loop. Checks whether or not the players have the same draw card, and if they do, redirects the process back to the_draw_1 and places player cards back into the MasterDeck. Also checks to see who wins the draw, and sends off to the_deal after determination.
    print("draw 3\n")
    # ------------------------------------------
    if P1.draw_card == P2.draw_card:
        print("\nYou have the same exact card! You both must pick another card!\n")
        for player in players:
            MasterDeck.deck.append(player.hand.pop(0))
        return the_draw_1()
    elif P1.draw_card_val > P2.draw_card_val:
        for player in players:
            MasterDeck.deck.append(player.hand.pop(0))
        the_deal(P1,P2)
    elif P2.draw_card_val > P1.draw_card_val:
        for player in players:
            MasterDeck.deck.append(player.hand.pop(0))
        the_deal(P2,P1)
    elif P1.draw_card_val == P2.draw_card_val:
        if Deck().draw_suite_ranks.get(P1.draw_card[1]) > Deck().draw_suite_ranks.get(P2.draw_card[1]):
            for player in players:
                MasterDeck.deck.append(player.hand.pop(0))
            the_deal(P1,P2)
        else:
            for player in players:
                MasterDeck.deck.append(player.hand.pop(0))
            the_deal(P2,P1)
# ------------------------------------------
def the_deal(player1, player2):
    # Follow up to Draw_3 for Game Loop. Handles dealing, sorting, printing, red 3 checking each player their cards. Then creates a discard pile from MasterDeck and ensures that top discard is not a wild card. Is that in the rules, though??
    print("the deal\n")
    # ------------------------------------------
    # Below - Deals each player their 11 cards, sorts them, prints them, and checks for Red 3s.
    for player in (player1, player2):
        for card in range(11):
            player.hand.append(MasterDeck.deck.pop(0))
        print("{name} is dealt 11 cards. Your hand consists of:\n".format(name = player.name))
        sort_player_cards(player)
        iterated_and_numbered_list_printer(player.hand)
        red_3_check(player)
    # -----------------------------------------
    # Below - Creates the discard pile from the MasterDeck & ensures that top discard is not a wild card. Is this in the rules, though??
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(0))
    while MasterDeck.face_up_discard[0] in Deck().wild_card_discards:
        MasterDeck.discard_pile.append(MasterDeck.deck.pop(0))
    # ------------------------------------------
    play_1(player1)
# ------------------------------------------
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
# ------------------------------------------
# Miscellaneous function for handling printed lists that I want to be numbered; for the purpose of input game selection via the preceding num.
def iterated_and_numbered_list_printer(passed_list_1, passed_list_2 = None):
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
# ------------------------------------------
def red_3_check(player, drawn = False):
    # Stem (#3) from The_Deal for Game Loop & play_1() after stock_draw(). Handles Red 3s according to game rules.
    print("red 3 check\n")
    red_3_quantity = 0
    # ------------------------------------------
    for red_3 in Deck().red_3s:
        while red_3 in player.hand:
            # ------------------------------------------
            # Below - Handles drawn Red 3s. Removes them from player.hand, replaces it with a newly drawn card from the deck, and prints associated output.
            if drawn == True:
                print("You drew a Red 3! The {red_3} will be placed in your Red 3 meld, and you will automatically draw another card to replace it.".format(red_3 = red_3))
                player.red_3_meld.append(player.hand.pop(-1))
                player.hand.append(MasterDeck.deck.pop(0))
                print("In place of your Red 3, you drew a: {replacement_card}\n".format(replacement_card = player.hand[-1]))
            # ------------------------------------------
            # Below - Handles initial Red 3 check. Appends red_3_meld to player.melds, replaces it with a new card from MasterDeck.deck, & prints out associated output for initial Red 3 distribution.
            elif drawn == False:
                red_3_quantity += 1
                player.red_3_meld.append(player.hand.pop(player.hand.index(red_3)))
                player.hand.append(MasterDeck.deck.pop(0))
    # ------------------------------------------
    if red_3_quantity == 4:
        print("Congratulations! You have 4 Red 3s, therefore you get a bonus of 400 points (granted that when someone goes out, you have at least 1 Canasta)! The rules dictate that all Red 3s must be played down, and you have to withdraw a card from the stock for each one in your hand!\n")
    elif red_3_quantity > 0:
        print("You have {red_3_quantity} Red 3(s) in your hand! The rules dictate that all Red 3s must be played down, and you have to withdraw a card from the stock for each one in your hand!\n".format(red_3_quantity = red_3_quantity))
        red_3_replacements_str = ("In place of your Red 3(s), you drew: " + ', '.join(['%s']*len(player.red_3_meld)) + "\n") % tuple(player.hand[-(len(player.red_3_meld)):])
        print(red_3_replacements_str)
# ------------------------------------------
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
# ------------------------------------------
def stock_draw(player):
    # Stem (#1) from play_1 function. For drawing a card from the stock & giving associated output.
    print("\nstock_draw\n")
    player.hand.append(MasterDeck.deck.pop(0))
    print("\n{name} drew a {card} from the stack.\n".format(name = player.name, card = player.hand[-1]))
# ------------------------------------------
def draw_discard_pile(player):
    # Stem (#2) from play_1 function. For drawing discard pile.
    print("draw_discard_pile\n")

    # Below - First checks if discard pile is frozen. Depending on this, redirects to eligibility determinations based on player's initial meld status, and finalizes determination by either allowing drawing of the discard pile, or denial and subsequent redirection back to play_1.
    if MasterDeck.discard_pile[-1][0] not in Deck().wild_cards and MasterDeck.discard_pile[-1][0] not in Deck().black_3s:
        if player.round_score >= player.meld_requirement:
            for meld in player.melds:
                if MasterDeck.discard_pile[-1][0] == meld[0]:
                    meld.append(MasterDeck.discard_pile.pop(-1))
                    player.play_cards.append(MasterDeck.discard_pile)
                    MasterDeck.discard_pile.clear()
                    print("You successfully drew the discard pile!\n")

            if len(player.play_cards) == 0:
                card_count = 0
                matched_card_list = []
                for card in player.hand[:]:
                    if card[0] == MasterDeck.discard_pile[-1][0]:
                        matched_card_list.append(card)
                        card_count += 1
                if card_count >= 2:
                    temp_meld = []
                    for matched_card in matched_card_list:
                        temp_meld.append(matched_card)
                        player.hand.pop(player.hand.index(matched_card))

                    player.hand.append(MasterDeck.discard_pile.pop(-1))
                    temp_meld.append(player.hand.pop(player.hand[-1]))
                    player.melds.append(temp_meld)
                    print("You successfully drew the discard pile!\n")

                elif card_count == 1:
                    player_hand_wild_cards = []
                    for card in player.hand:
                        if card[0] in Deck().wild_cards:
                            player_hand_wild_cards.append(card)

                    if len(player_hand_wild_cards) > 0:
                        yn = input("Since you only have one of the natural cards that match the top discard pile card, you would have to use a wild card to draw the discard pile. Would you like to do this? (Y/N)\n\n> ")
                        if yn.lower() == "y":
                            temp_meld = []
                            wild_cards_str = ("Which wild card would you like to use? You have these wild cards:\n")
                            iterated_and_numbered_list_printer(player_hand_wild_cards)
                            wild_card_choice = input("> ")
                            temp_meld.append(player.hand.pop(player.hand.index(player_hand_wild_cards[int(wild_card_choice - 1)])))
                            temp_meld.append(player.hand.pop(player.hand.index(matched_card_list[0])))
                            player.melds.append(temp_meld)
                    else:
                        print("Sorry, but you do not meet the requirements to be able to withdraw from the discard pile, because you only had 1 card matching the top discard with no wild card in your hand to be played as part of a meld alongside it.\n")
                        play_1(player)
        # Below - If player_round_score < meld_requirement: Also, this whole else clause is an exact copy and paste of lines 323-358. It checks to see if the player has the required cards within their hand to qualify for the discard pile draw. The code that follows it will check if the subsequent meld from the top discard reaches the meld_requirement.
        else:
            card_count = 0
            matched_card_list = []
            for card in player.hand[:]:
                if card[0] == MasterDeck.discard_pile[-1][0]:
                    matched_card_list.append(card)
                    card_count += 1
            if card_count >= 2:
                temp_meld = []
                for matched_card in matched_card_list:
                    temp_meld.append(matched_card)
                    player.hand.pop(player.hand.index(matched_card))

                player.hand.append(MasterDeck.discard_pile.pop(-1))
                temp_meld.append(player.hand.pop(player.hand[-1]))
                player.melds.append(temp_meld)
                print("You successfully drew the discard pile!\n")

            elif card_count == 1:
                player_hand_wild_cards = []
                for card in player.hand:
                    if card[0] in Deck().wild_cards:
                        player_hand_wild_cards.append(card)

                if len(player_hand_wild_cards) > 0:
                    yn = input("Since you only have one of the natural cards that match the top discard pile card, you would have to use a wild card to draw the discard pile. Would you like to do this? (Y/N)\n\n> ")
                    if yn.lower() == "y":
                        temp_meld = []
                        wild_cards_str = ("Which wild card would you like to use? You have these wild cards:\n")
                        iterated_and_numbered_list_printer(player_hand_wild_cards)
                        wild_card_choice = input("> ")
                        # Below line is different than in above section it was copied from. I needed to pop from player_hand_wild_cards because they may need another wild card from the list if they don't reach the required meld score with the initial meld attempt that follows in this section.
                        temp_meld.append(player.hand.pop(player.hand.index(player_hand_wild_cards.pop(int(wild_card_choice - 1)))))
                        temp_meld.append(player.hand.pop(player.hand.index(matched_card_list[0])))
                        player.melds.append(temp_meld)
                else:
                    print("Sorry, but you do not meet the requirements to be able to withdraw from the discard pile, because you only had 1 card matching the top discard with no wild card in your hand to be played as part of a meld alongside it.\n")
                    play_1(player)
            if meld_check(player) == True:
                print("You successfully drew the discard pile!\n")
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
    # From the top of draw_discard_pile function until this line, I have went through and redone everything, and it should be in working order. I need to make sure I can't make improvements, though, as noted on lines 391 & 412.
    else:
        # Below - Need to complete. Stopped here.
        pass
# ------------------------------------------
def play_2(player):
    # Follow up to Play_1 for Game loop.
    print("play_2\n")
    global int
    # ------------------------------------------
    play_choice = input("{name}, what would you like to do with your turn?\n\n 1) Play Cards\n 2) Discard\n\n> ".format(name = player.name))
    if play_choice == "1":
        print("\n{name}, which cards would you like to play? (Use the ordered number of the card(s) in hand as listed below. i.e. - '1,3,4,8')\n".format(name = player.name))
        iterated_and_numbered_list_printer(player.hand)
        play_cards_input = input("> ")
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        play_cards_list = list(play_cards_input)
        temp_char_holder = []
        index_reference = []
        index_num = 1
        consec_int_counter = 0
        int_counter_reference = 0
        index = -1
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        for char in play_cards_list:
            if char in numbers:
                index += 1
                index_reference.append(int(index))
                temp_char_holder.append(int(char))
                if int_counter_reference > consec_int_counter:
                    int_counter_reference = consec_int_counter
                consec_int_counter += 1
                if consec_int_counter == (int_counter_reference + 2):
                    integer_2 = temp_char_holder.pop(index_reference[-(index_num)])
                    integer_1 = temp_char_holder.pop(index_reference[-(index_num + 1)])
                    index_num += 1
                    concatenated_int = int(str(integer_1) + str(integer_2))
                    temp_char_holder.append(concatenated_int)
            else:
                consec_int_counter = 0
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        for integer in temp_char_holder:
            player.play_cards.append(player.hand[integer - 1])
        # ------------------------------------------
        if valid_play_check_and_sort(player) == True:
            player.play_cards.clear()
            discard(player)
        else:
            player.play_cards.clear()
            play_2(player)
    else:
        discard(player)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Leads to restarting of Game Loop via redirect upon finish to Play_1, unless player went out; in that case, ends round and then redirects.
    went_out_check(player)
# ------------------------------------------
def meld_check(player):
    # Stems from play_2. Checks for player meld requirements. If player hasn't met intial meld, determines if set of play cards reaches the meld_requirement score (does not check for valid play).
    print("meld_check\n")
    # If you are trying to meet initial meld.
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
# ------------------------------------------
def valid_play_check_and_sort(player):
    # Stems (#1) from Play_2. For ensuring that a set of attempted play cards are valid according to game rules.
    print("\nvalid_play_check_and_sort\n")
    # ------------------------------------------
    play_cards_ranks = []
    len_2_temp_melds_list = []
    bad_len_temp_melds_list = []
    play_cards_removed_black_3s = []
    # ------------------------------------------
    initial_played_card_count = player.played_card_count
    # ------------------------------------------
    for card in player.play_cards[:]:
        if card not in Deck().black_3s and card not in Deck().red_3s:
            if card not in Deck().wild_cards and card[0] not in play_cards_ranks:
                play_cards_ranks.append(card[0])
                temp_meld = []
                temp_meld.append(player.play_cards.pop(player.play_cards.index(card)))
                player.play_cards.append(temp_meld)
            elif card in Deck().wild_cards:
                player.play_cards_wild_cards.append(player.play_cards.pop(player.play_cards.index(card)))
            elif card[0] in play_cards_ranks:
                for item in player.play_cards:
                    if type(item) == list:
                        if card[0] == item[0][0]:
                            item.append(player.play_cards.pop(player.play_cards.index(card)))
        else:
            play_cards_removed_black_3s.append(player.play_cards.pop(player.play_cards.index(card)))
    # ------------------------------------------
    # Below - This is simply a test to ensure that my above code is properly removing all the proper cards and that none are left over in here. None should be in here, thus none should be printed.
    for card in player.play_cards[:]:
        if type(card) != list:
            print("valid_play_check_and_sort didn't catch all cards: {card}".format(card = card))
    # ------------------------------------------
    if player.round_score < player.meld_requirement:
        print("player.round_score < meld\n")
        # --------------------------------------
        if len(player.play_cards) < 3:
            print("Sorry, but you must play at least 3 cards for a new meld. Please select a new set of cards to play, or you can choose to discard if you like.\n")
            return False
        # --------------------------------------
        if len(player.play_cards) == 0:
            if len(player.play_cards_wild_cards) < 7:
                print("Sorry, but you cannot play a meld of only wild cards, unless that play consists of a complete Wild Card Canasta.\n")
            else:
                player.play_cards.append(player.play_cards_wild_cards)
                player.play_cards_wild_cards.clear()
        else:
            for temp_meld in player.play_cards[:]:
                if len(temp_meld) < 2:
                    bad_len_temp_melds_list.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
                elif len(temp_meld) == 2:
                    if len(player.play_cards_wild_cards) < 1:
                        bad_len_temp_melds_list.append(player.play_cards.pop(player.play_cards.index(temp_meld)))
                    else:
                        len_2_temp_melds_list.append(temp_meld)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            if len(play_cards_removed_black_3s) > 0:
                print("Sorry, but you cannot play Black 3(s) in this way. Black 3s can only be used to freeze the discard pile. The Black 3(s) that are being removed from your attempted play cards back into your hand are as follows:\n")
                iterated_and_numbered_list_printer(play_cards_removed_black_3s)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            if len(bad_len_temp_melds_list) > 0:
                print("Sorry, but you cannot create a new meld without at least 2 natural cards of that rank, or without a wild card to add to it to reach the 3 card minimum meld requirement. The attempted meld(s) will be removed and placed back in your hand:\n")
                iterated_and_numbered_list_printer(bad_len_temp_melds_list)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # Below - remove the temp_meld from len_2_temp_melds_list OR SOMETHING NEED TO MAKE IT SO THAT THIS LOOP WORKS CORRECTLY. AS IS IT DOES NOT RUN THIS PART AGAIN FOR WHEN WE HAVE 2 len_2 MELDS and 2 WILD CARDS. IT MOVES TO leftover_wild_card_handler INSTEAD ERRANTLY.
            while len(len_2_temp_melds_list) > 0:
                while len(player.play_cards_wild_cards) > 0:
                    player_play_cards_wild_cards_print = ("The below meld(s) from your attempted play cards have only 2 cards in them. Since 3 cards are required for a valid meld, you must add a wild card to them for them to remain in play. It looks as if you have {len_num} wild card(s) in your set of play cards to use for this. The wild card(s) you have available are as follows: ".format(len_num = len(player.play_cards_wild_cards)) + ', '.join(['%s']*len(player.play_cards_wild_cards)) + " Choose a meld from the list below that you would like to add a wild card to.\n") % tuple(player.play_cards_wild_cards)
                    print(player_play_cards_wild_cards_print)
                    iterated_and_numbered_list_printer(len_2_temp_melds_list)
                    num = str(len(len_2_temp_melds_list) + 1)
                    print("{num}) I would rather use the wild card(s) elsewhere, and let the meld(s) be placed back into my hand.\n".format(num = num))
                    len_2_temp_meld_choice = int(input("> ")) - 1
                    if len_2_temp_meld_choice != (num - 1):
                        if len(player.play_cards_wild_cards) > 1:
                            print("\nWhich wild card would you like to add to the selected meld?\n")
                            iterated_and_numbered_list_printer(player.play_cards_wild_cards)
                            wild_card_choice = int(input("\n > ")) - 1
                            len_2_temp_melds_list[len_2_temp_meld_choice].append(player.play_cards_wild_cards.pop(wild_card_choice))
                            # remove the temp_meld from len_2_temp_melds_list OR SOMETHING NEED TO MAKE IT SO THAT THIS LOOP WORKS CORRECTLY. AS IS IT DOES NOT RUN THIS PART AGAIN FOR WHEN WE HAVE 2 len_2 MELDS and 2 WILD CARDS. IT MOVES TO leftover_wild_card_handler INSTEAD ERRANTLY.
                        elif len(player.play_cards_wild_cards) > 0:
                            len_2_temp_melds_list[len_2_temp_meld_choice].append(player.play_cards_wild_cards.pop(0))
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            for temp_meld in player.play_cards[:]:
                if len(temp_meld) == 2:
                    player.play_cards.remove(temp_meld)
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        leftover_wild_card_handler(player)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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
        leftover_wild_card_handler(player)
    # -------------------------------------
    for temp_meld in player.play_cards:
        player.melds.append(temp_meld)
        for card in temp_meld[:]:
            player.hand.remove(card)
    # -------------------------------------
    print("\nfinal play 2 player.melds print\n")
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
            print("Sorry, but you seem to be trying to go out. ")

    if initial_played_card_count == final_played_card_count:
        print("initial_played_card_count == final_played_card_count\n")
        return False
    else:
        print("True - initial_played_card_count != final_played_card_count\n")
        return True
# ------------------------------------------
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
            if int(temp_meld_choice) == int(temp_meld_num - 1):
                break
            elif temp_meld_choice >= (temp_meld_num_at_player_meld_transition - 1):
                player.melds[temp_meld_choice].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card)))
            else:
                player.play_cards[temp_meld_choice].append(player.play_cards_wild_cards.pop(player.play_cards_wild_cards.index(wild_card)))
        else:
            print("You had wild card(s) left in your attempted play cards, but had nowhere to place them, or chose not to use them at this time, after valid play determinations and sorting, so they will be placed back into your hand.")
            player.play_cards_wild_cards.clear()
# ------------------------------------------
def discard(player):
    # Stems (#2) from Play_2. For discarding.
    print("discard\n")
    print("Which card would you like to discard? Your available cards in hand are:\n")
    iterated_and_numbered_list_printer(player.hand)
    discard_input = int(input("\n> ")) - 1
    print("\nYou discarded the {discard}.\n".format(discard = (player.hand[discard_input])))
    MasterDeck.discard_pile.append(player.hand.pop(discard_input))
# ------------------------------------------
def went_out_check(player):
    # Follow up to Play_2. For checking to see if players went out during turn. If not, redirects to beginning of game loop (Play_1). If so, ends round and redirects to The_Draw_1.
    print("went out check\n")
    if len(player.hand) == 0:
        for player in players:
            player.going_out = True
        if player == player1:
            print("{p1} went out!\n\nRound Score:\n{p1}:{p1_round_score}\n{p2}:{p2_round_score}\n".format(p1 = player1.name, p1_round_score = player1.round_score, p2 = player2.name, p2_round_score = player2.round_score))
        else:
            print("{p2} went out!\n\nRound Score:\n{p2}:{p2_round_score}\n{p1}:{p1_round_score}\n".format(p2 = player2.name, p2_round_score = player2.round_score, p1 = player1.name, p1_round_score = player1.round_score))
        for player in (player1, player2):
            player.round_score_val = 0
        win_check()
        the_draw_1()
    else:
        if player == P1:
            play_1(P2)
        else:
            play_1(P1)
# ------------------------------------------
def win_check():
    global run
    for player in players:
        if total_score >= 5000:
            print("Congratulations, {player_name}, you were the first to reach 5,000 points, therefore you are the winner! You are the champion, my friend!!!".format(player_name = player.name))
            run = 0
# ------------------------------------------
def game_run():
    # Main Run loop. Runs game until a player wins.
    global run
    run = 1
    while run == 1:
        print("run\n")
        the_draw_1()
        print("run end\n")
# ------------------------------------------
# Runs the game, until someone wins!
game_run()
