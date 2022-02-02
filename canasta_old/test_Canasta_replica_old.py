# Bugs --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  # None Currently. Debugging Completed.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Imports
from Canasta_replica_FINAL import *
from unittest.mock import patch, PropertyMock, call
import pytest
import random
import copy
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Creates an original_deck that is composed of all of the cards from the MasterDeck.deck & Deck2.deck when they were initially created and combined, before it was edited in any way, for the purpose of being used as a reference deck when resetting the deck back to original form when setting up and tearing down for tests.
original_deck = MasterDeck.deck[:]
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - Creates the deck_tionary dictionary to be used for assigning a 'card_string_name' to each card via the assemble_decktionary() function. Each card will be assigned a name, such as 'joker_none_1 & three_spade_1', for the purpose of simplifying finding a particular card so that when testing is done the tester can easily manipulate which cards will be tested, etc.
decktionary = {}
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - ...
p1_premade_hand_1 = ['joker_none_1', 'two_club_1', 'three_spade_1', 'four_heart_1', 'five_diamond_1', 'six_diamond_1', 'seven_heart_1', 'eight_spade_1', 'nine_club_1', 'ten_spade_1', 'jack_club_1']
p2_premade_hand_1 = ['queen_club_1', 'king_spade_1', 'ace_heart_1', 'ace_heart_2', 'king_spade_2', 'queen_club_2', 'seven_heart_2', 'eight_spade_2', 'nine_club_2', 'ten_spade_2', 'jack_club_2']

p1_premade_hand_2 = ['joker_none_1', 'joker_none_2', 'two_club_1', 'two_spade_1', 'two_heart_1', 'two_diamond_1', 'two_club_2', 'two_spade_2', 'two_heart_2', 'two_diamond_2', 'three_club_1']
p2_premade_hand_2 = ['four_club_1', 'four_spade_1', 'five_heart_1', 'five_diamond_1', 'six_club_1', 'six_heart_1', 'seven_club_1', 'seven_diamond_1', 'eight_spade_1', 'eight_diamond_1', 'nine_heart_1']
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def p1_p2_premade_hand_1(p1_premade_hand_1, p2_premade_hand_1):
    """Creates a couple of premade hands for each player so that they can be used
    during later tests."""
    for card_string_name in p1_premade_hand_1:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card_string_name])))
    for card_string_name in p2_premade_hand_1:
        P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card_string_name])))

def p1_p2_premade_hand_2(p1_premade_hand_2, p2_premade_hand_2):
    for card_string_name in p1_premade_hand:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card_string_name])))
    for card_string_name in p2_premade_hand:
        P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card_string_name])))
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def sorter(passed_list): # ****
    # -------------------------------------
    """Orders a passed list of cards based on card.rank & card.draw_suit_ranks in
    ascending order."""
    # Below Function - The sorter KEY function which orders the cards in ascending order based on card rank and card suit rank. # ****
    def sorter_key_function(item): # ****
        int_suit = MasterDeck.draw_suit_ranks.get(item.suit)
        if item.rank == 'Jo': # ****
            int_rank = 1
        else:
            int_rank = MasterDeck.draw_ranks.get(item.rank)
        return int(str(int_rank) + str(int_suit)) # ****
    # -------------------------------------
    # Below Line - Orders the MasterDeck.deck in ascending order (Joker - Ace / Club - Spade)
    return sorted(passed_list, key = sorter_key_function) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def assemble_decktionary(decktionary, ordered_deck):
    """Passes in decktionary and the ordered_deck, then creates two reference
    dictionaries: one assigned with references to each deck_card's card.rank, and
    one assigned with references to each card.suit. Then uses these two
    dictionaries to create a 'string_name' for each deck_card based on those two
    parameters suffixed by a number of the occurrences of that
    card.rank/card.suit combination (1, 2, 3, or 4). Finally appends the
    (string_name: deck_card) as the (key: value)."""
    # -------------------------------------
    card_rank_string_dict = {'Jo': 'joker', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten', 'J': 'jack', 'Q': 'queen', 'K': 'king', 'A': 'ace'}
    card_suit_string_dict = {'Jo': 'none', 'C': 'club', 'S': 'spade', 'H': 'heart', 'D': 'diamond'}
    # -------------------------------------
    for deck_card in ordered_deck:
        occurrence_num = 1
        while (card_rank_string_dict.get(deck_card.rank) + "_" + card_suit_string_dict.get(deck_card.suit) + "_" + str(occurrence_num)) in decktionary:
            occurrence_num += 1
        string_name = (card_rank_string_dict.get(deck_card.rank) + "_" + card_suit_string_dict.get(deck_card.suit) + "_" + str(occurrence_num))
        decktionary[string_name] = deck_card
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def setup():
    """Simple setup function that automatically runs before each test. Prints an
    informative output."""
    # -------------------------------------
    MasterDeck.deck = original_deck[:]
    random.shuffle(MasterDeck.deck) # ****
    # -------------------------------------
    # Below Line - Creates the variable ordered_Masterdeck to be passed into sorter() to return a sorted reference starter deck for use during setup() and teardown() to reset the deck back to it's original state each time a test is run. For consistency in test results.
    ordered_Masterdeck = sorter(MasterDeck.deck)
    # Below Line - Passes the decktionary and the ordered_Masterdeck to assemble_decktionary() function so that the decktionary will be compiled, giving a key to each card that is an easily associated and memorable 'string_name'.
    assemble_decktionary(decktionary, ordered_Masterdeck)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def teardown():
    """Simple teardown function that automatically runs after each test. Prints
    an informative output, clears both players' hands, clears the MasterDeck.deck,
    and then 'resets' the deck to its original state by appending each card from
    original_deck to MasterDeck.deck. Also creates the sorter()
    ordered_Masterdeck and assembles the decktionary for easy reference to each
    Card() object in MasterDeck.deck."""
    # -------------------------------------
    MasterDeck.discard_pile.clear()
    MasterDeck.deck.clear()
    # -------------------------------------
    for player in (P1, P2): # ****
        player.finished_rounds_scores.clear()
        player.the_draw = None # ****
        player.hand.clear() # ****
        player.play_cards.clear() # ****
        player.play_cards_wild_cards.clear() # ****
        player.initial_played_cards.clear() # ****
        player.last_set_played_cards.clear() # ****
        player.red_3_meld.clear() # ****
        player.black_3_meld.clear() # ****
        player.melds.clear() # ****
        player.len_2_temp_melds_list.clear() # ****
        player.matched_card_list.clear()
        player.going_out = None # ****
        player.went_out_concealed = False # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_create_master_deck():
    print("\n# 1\n")
    # -------------------------------------
    """Tests the length of the MasterDeck.deck to ensure that it is of proper
    length."""
    # -------------------------------------
    assert len(MasterDeck.deck) == 108
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_the_draw_1():
    print("\n# 2\n")

    """Tests the_draw_1() function to ensure it has proper output when input
    parameter is (P1, True) is P1."""

    assert the_draw_1(P1, True) == "player == P1"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_2_the_draw_1():
    print("\n# 3\n")

    """Tests the_draw_1() function to ensure it has proper output when input
    parameter is P2."""
    assert the_draw_1(P2, True) == "player == P2"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_the_draw_2():
    print("\n# 4\n")

    """Tests the_draw_2() function to ensure it has proper output when input
    parameter is P2. Checks for proper length of P2.hand and MasterDeck.deck
    after appends and pops were supposed to have been made. Does this for both
    P1 & P2."""

    assert the_draw_2(P2, True) == "draw_joker_check(player)"
    assert len(P2.hand) == 1
    assert len(MasterDeck.deck) == 107 # 108 - 1 for P2.hand's card
    assert the_draw_2(P1, True) == "draw_joker_check(player)"
    assert len(P1.hand) == 1
    assert len(MasterDeck.deck) == 106 # 108 - 2 for P1.hand's card & P2.hand's card
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_draw_joker_check():
    print("\n# 5\n")

    """Tests the draw_joker_check() function to ensure it has proper output."""

    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['joker_none_1'])))
    assert draw_joker_check(P1, True) == "player.draw_card.rank == \'Jo\'"
    assert len(MasterDeck.deck) == 107
    assert len(P1.hand) == 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_2_draw_joker_check():
    print("\n# 6\n")

    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_heart_1'])))
    assert len(MasterDeck.deck) == 107
    assert len(P1.hand) == 1
    assert draw_joker_check(P1, True) == "player.draw_card.rank != \'Jo\'"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_the_draw_3():
    print("\n# 7\n")

    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_heart_1'])))
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_heart_2'])))
    assert len(MasterDeck.deck) == 106
    assert len(P1.hand) == 1
    assert len(P2.hand) == 1
    assert the_draw_3(True) == "\nYou have the same exact card! You both must pick another card!\n"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_2_the_draw_3():
    print("\n# 8\n")

    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_heart_1'])))
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_club_1'])))
    assert len(MasterDeck.deck) == 106
    assert len(P1.hand) == 1
    assert len(P2.hand) == 1
    assert the_draw_3(True) == "the_deal(P1,P2)"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_3_the_draw_3():
    print("\n# 9\n")

    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_club_1'])))
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_heart_1'])))
    assert len(MasterDeck.deck) == 106
    assert len(P1.hand) == 1
    assert len(P2.hand) == 1
    assert the_draw_3(True) == "the_deal(P2,P1)"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_return_draw_card():
    print("\n# 10\n")

    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_heart_1'])))
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_club_1'])))
    return_draw_card(players)
    assert (MasterDeck.deck[-1].rank, MasterDeck.deck[-1].suit) == (decktionary['two_club_1'].rank, decktionary['two_club_1'].suit)
    assert (MasterDeck.deck[-2].rank, MasterDeck.deck[-2].suit) == (decktionary['two_heart_1'].rank, decktionary['two_heart_1'].suit)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_1', autospec = True, return_value = 1)
def test_the_deal(mock_play_1):
    print("\n# 11\n")

    the_deal(P1, P2)
    assert len(P1.hand) == 11
    assert len(P2.hand) == 11
    assert len(MasterDeck.discard_pile) == 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_1', autospec = True, return_value = 1)
def test_2_the_deal(mock_play_1):
    print("\n# 12\n")
    the_deal(P2, P1)
    assert len(P1.hand) == 11
    assert len(P2.hand) == 11
    assert len(MasterDeck.discard_pile) == 1
    assert len(MasterDeck.deck) == (108 - (11 + 11 + 1) - (len(P1.red_3_meld) + len(P2.red_3_meld))) # 11 cards per player, plus 1 for the face up discard, plus any redraws accounting for red_3.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_1_sorted_and_numbered_list_printer():
    print("\n# 13\n")

    p1_p2_premade_hand_1(p1_premade_hand_1, p2_premade_hand_1)

    testing_register_list.clear()
    sorted_and_numbered_list_printer(P1.hand, P2.hand)

    non_num_card_rank_sort_value = {'Jo':1, 'J':11, 'Q':12, 'K':13, 'A':14} # ****
    previous_item = None
    previous_item_value = None

    for item in testing_register_list:
        int_suit = MasterDeck.draw_suit_ranks.get(item.suit)
        if item.rank in non_num_card_rank_sort_value: # ****
            int_rank = non_num_card_rank_sort_value.get(item.rank) # ****
            final_value = int(str(int_rank) + str(int_suit)) # ****
        else: # ****
            final_value = int(str(item.rank) + str(int_suit)) # ****

        if item == testing_register_list[0]:
            previous_item = item
            previous_item_value = final_value
        else:
            assert (final_value > previous_item_value)
            previous_item = item
            previous_item_value = final_value

    assert len(P1.hand) == 11
    assert len(P2.hand) == 11
    assert len(MasterDeck.deck) == (108 - (11 + 11) - (len(P1.red_3_meld) + len(P2.red_3_meld))) # 11 cards per player, plus any redraws accounting for red_3.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_2_sorted_and_numbered_list_printer():
    print("\n# 14\n")

    p1_p2_premade_hand_1(p1_premade_hand_2, p2_premade_hand_2)

    testing_register_list.clear()
    sorted_and_numbered_list_printer(P1.hand, P2.hand)

    non_num_card_rank_sort_value = {'Jo':1, 'J':11, 'Q':12, 'K':13, 'A':14} # ****
    previous_item = None
    previous_item_value = None

    for item in testing_register_list:
        int_suit = MasterDeck.draw_suit_ranks.get(item.suit)
        if item.rank in non_num_card_rank_sort_value: # ****
            int_rank = non_num_card_rank_sort_value.get(item.rank) # ****
            final_value = int(str(int_rank) + str(int_suit)) # ****
        else: # ****
            final_value = int(str(item.rank) + str(int_suit)) # ****

        if item == testing_register_list[0]:
            previous_item = item
            previous_item_value = final_value
        else:
            assert (final_value >= previous_item_value)
            previous_item = item
            previous_item_value = final_value

    assert len(P1.hand) == 11
    assert len(P2.hand) == 11
    assert len(MasterDeck.deck) == (108 - (11 + 11) - (len(P1.red_3_meld) + len(P2.red_3_meld))) # 11 cards per player, plus any redraws accounting for red_3.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_red_3_check():
    print("\n# 15\n")

    # Test Section #1
    premade_hand_red_3 = ['three_heart_1', 'four_club_1']
    for card in premade_hand_red_3:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    red_3_check(P1)
    assert len(P1.red_3_meld) == 1
    assert len(P1.hand) == 2 # 2 (starting len) - 1 (popped from hand to red_3_meld) + 1 (appended from deck for red_3 replacement)
    assert len(MasterDeck.deck) == 105 # 108 (total original len) - 2 (from appends to hand) - 1 (from deck for red_3 replacement)
    teardown()
    setup()

    # Test Section #2
    premade_hand_red_3.append('three_heart_2')
    for card in premade_hand_red_3:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    red_3_check(P1)
    assert len(P1.red_3_meld) == 2
    assert len(P1.hand) == 3 # 3 (starting len) - 2 (popped from hand to red_3_meld) + 2 (appended from deck for red_3 replacement)
    assert len(MasterDeck.deck) == 103 # 108 (total original len) - 3 (from appends to hand) - 2 (from deck for red_3 replacement)
    teardown()
    setup()

    # Test Section #3
    premade_hand_red_3.append('three_diamond_1')
    for card in premade_hand_red_3:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    red_3_check(P1)
    assert len(P1.red_3_meld) == 3
    assert len(P1.hand) == 4 # 4 (starting len) - 3 (popped from hand to red_3_meld) + 3 (appended from deck for red_3 replacement)
    assert len(MasterDeck.deck) == 101 # 108 (total original len) - 4 (from deck to hand) - 3 (from deck for red_3 replacement)
    teardown()
    setup()

    # Test Section #4
    premade_hand_red_3.append('three_diamond_2')
    for card in premade_hand_red_3:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    red_3_check(P1)
    assert len(P1.red_3_meld) == 4
    assert len(P1.hand) == 5 # 5 (starting len) - 4 (popped from hand to red_3_meld) + 4 (appended from deck for red_3 replacement)
    assert len(MasterDeck.deck) == 99 # 108 (total original len) - 5 (from deck to hand) - 4 (from deck for red_3 replacement)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.stock_draw', autospec = True, return_value = None)
@patch('Canasta_replica.draw_discard_pile_attempt', autospec = True, return_value = None)
def test_play_1(mock_draw_discard_pile_attempt, mock_stock_draw):
    print("\n# 16\n")
    # -------------------------------------
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(-1))
    print("\nINPUT: 1\n")
    assert play_1(P1) == None
    mock_stock_draw.assert_called_with(P1)
    print("\nINPUT: 2\n")
    assert play_1(P2) == None
    mock_draw_discard_pile_attempt.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
@patch('Canasta_replica.draw_discard_pile_attempt', autospec = True, return_value = None)
@patch('Canasta_replica.red_3_check', autospec = True, return_value = None)
def test_stock_draw(mock_red_3_check, mock_draw_discard_pile_attempt, mock_play_2):
    print("\n# 17\n")
    # -------------------------------------
    # Below Section - Tests the 'if' clause to ensure that it calls red_3_check(), play_2(), and that the player successfully drew a card.
    assert stock_draw(P1) == None
    mock_red_3_check.assert_called_with(P1)
    mock_play_2.assert_called_with(P1)
    assert len(P1.hand) == 1
    assert len(MasterDeck.deck) == 107
    teardown()
    # -------------------------------------
    # Below Section - Tests the 'else' clause to ensure that it calls draw_discard_pile_attempt().
    MasterDeck.deck.clear()
    assert stock_draw(P2) == None
    mock_draw_discard_pile_attempt.assert_called_with(P2, True)
    assert len(P2.hand) == 0
    assert len(MasterDeck.deck) == 0
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.round_reset', autospec = True, return_value = None)
def test_draw_discard_pile_attempt(mock_round_reset):
    print("\n# 18\n")
    # -------------------------------------
    """Tests to ensure that when the stock_depleted == True and the discard pile
    are empty the function returns round_reset()"""
    # Arrange -------------------------------------
    MasterDeck.deck.clear()
    MasterDeck.discard_pile.clear()
    # Act -------------------------------------
    draw_discard_pile_attempt(P1, True)
    # Assert -------------------------------------
    mock_round_reset.assert_called()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.draw_discard_pile_attempt_check_hand_match', autospec = True, return_value = None)
@patch('Canasta_replica.draw_discard_pile_attempt_check_meld_match', autospec = True, return_value = None)
@patch('Canasta_replica.Deck.discard_pile_is_frozen', new_callable = PropertyMock, return_Value = False)
def test_2_draw_discard_pile_attempt(mock_discard_pile_is_frozen, mock_draw_discard_pile_attempt_check_meld_match, mock_draw_discard_pile_attempt_check_hand_match):
    print("\n# 19\n")
    # Arrange ---------------------------------
    """Tests to ensure that when the stock is depleted, but the discard pile is
    not, the function returns draw_discard_pile_attempt(player, True)."""
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(-1))
    MasterDeck.deck.clear()
    mock_discard_pile_is_frozen.return_value = False
    # Act -------------------------------------
    draw_discard_pile_attempt(P2, True)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 0
    assert len(MasterDeck.discard_pile) == 1
    mock_discard_pile_is_frozen.assert_called()
    mock_draw_discard_pile_attempt_check_meld_match.assert_has_calls([call(P2, True), call(P2)])
    mock_draw_discard_pile_attempt_check_hand_match.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.draw_discard_pile_attempt_check_hand_match', autospec = True, return_value = None)
@patch('Canasta_replica.draw_discard_pile_attempt_check_meld_match', autospec = True, return_value = None)
@patch('Canasta_replica.Deck.discard_pile_is_frozen', new_callable = PropertyMock, return_Value = False)
def test_3_draw_discard_pile_attempt(mock_discard_pile_is_frozen, mock_draw_discard_pile_attempt_check_meld_match, mock_draw_discard_pile_attempt_check_hand_match):
    print("\n# 20\n")
    # -------------------------------------
    """Tests to ensure that when stock is not depleted, and
    discard_pile_is_frozen == False, calls correct things."""
    # Arrange ---------------------------------
    mock_discard_pile_is_frozen.return_value = False
    # Act -------------------------------------
    draw_discard_pile_attempt(P1)
    # Assert ----------------------------------
    assert MasterDeck.discard_pile_is_frozen == False
    mock_discard_pile_is_frozen.assert_called()
    mock_draw_discard_pile_attempt_check_meld_match.assert_called_with(P1)
    mock_draw_discard_pile_attempt_check_hand_match.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.draw_discard_pile_attempt_check_hand_match', autospec = True, return_value = None)
@patch('Canasta_replica.draw_discard_pile_attempt_check_meld_match', autospec = True, return_value = None)
@patch('Canasta_replica.Deck.discard_pile_is_frozen', new_callable = PropertyMock, return_Value = False)
def test_4_draw_discard_pile_attempt(mock_discard_pile_is_frozen, mock_draw_discard_pile_attempt_check_meld_match, mock_draw_discard_pile_attempt_check_hand_match):
    print("\n# 21\n")
    # -------------------------------------
    """Tests to ensure that when stock is not depleted, and
    discard_pile_is_frozen == True, calls correct things."""
    # Arrange ---------------------------------
    mock_discard_pile_is_frozen.return_value = True
    # Act -------------------------------------
    draw_discard_pile_attempt(P2)
    # Assert ----------------------------------
    assert MasterDeck.discard_pile_is_frozen == True
    mock_discard_pile_is_frozen.assert_called()
    mock_draw_discard_pile_attempt_check_meld_match.assert_not_called()
    mock_draw_discard_pile_attempt_check_hand_match.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.stock_draw', autospec = True, return_value = None)
@patch('Canasta_replica.draw_discard_pile', autospec = True, return_value = None)
def test_draw_discard_pile_attempt_check_meld_match(mock_draw_discard_pile, mock_stock_draw):
    print("\n# 22\n")
    # -------------------------------------
    """Tests to verify that whenever player has an existing meld matching the
    face_up_discard the function properly (#1 appends the face_up_discard to the
    matching meld, popping it from the discard_pile). Also checks to ensure
    (#2 draw_discard_pile is called) and (#3 stock_draw is called). Does not
    check 'if stock_depleted' clause."""
    # Arrange ---------------------------------
    P1.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['four_club_1']))])
    P1.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['five_heart_1']))])
    P1.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['six_club_1']))])
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['five_club_2'])))
    # Act -------------------------------------
    draw_discard_pile_attempt_check_meld_match(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 0
    assert len(MasterDeck.deck) == 104
    assert len(P1.melds) == 3
    assert len(P1.melds[1]) == 2
    mock_draw_discard_pile.assert_called_with(P1)
    mock_stock_draw.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
def test_2_draw_discard_pile_attempt_check_meld_match(mock_play_2):
    print("\n# 23")
    # -------------------------------------
    """Tests 'if stock_depleted' clause logic works correctly by passing in
    stock_depleted=True, if draw_rest_of_discard_pile_input input operates
    correctly in the case where player chooses 'n', and finally ensures that
    play_2 is returned."""
    # Arrange ---------------------------------
    P1.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['four_club_1']))])
    P1.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['five_heart_1']))])
    P1.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['six_club_1']))])
    for card in ['seven_club_2', 'eight_club_2', 'five_club_2']:
        MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT: N\n")
    draw_discard_pile_attempt_check_meld_match(P1, True)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 2
    assert len(MasterDeck.deck) == 102
    assert len(P1.melds) == 3
    assert len(P1.melds[0]) == 1
    assert len(P1.melds[1]) == 2
    assert len(P1.melds[2]) == 1
    mock_play_2.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.draw_discard_pile', autospec = True, return_value = None)
def test_draw_discard_pile_attempt_check_hand_match(mock_draw_discard_pile):
    print("\n# 24\n")
    # -------------------------------------
    """Tests to ensure (#1 draw_discard_pile() is called when
    len(player.melds[-1]) >= 3 & player.round_score > player.meld_requirement)
    and (#2 lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['king_club_1', 'king_heart_1', 'king_diamond_1', 'king_club_2']:
        P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_2'])))
    # Act -------------------------------------
    draw_discard_pile_attempt_check_hand_match(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 0
    assert len(MasterDeck.deck) == 103
    assert len(P2.hand) == 0
    assert len(P2.matched_card_list) == 4
    assert len(P2.melds) == 1
    assert len(P2.melds[0]) == 5
    mock_draw_discard_pile.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.Deck.discard_pile_is_frozen', new_callable = PropertyMock, return_Value = True)
@patch('Canasta_replica.replace_discard_pile_temp_meld', autospec = True, return_value = None)
def test_2_draw_discard_pile_attempt_check_hand_match(mock_replace_discard_pile_temp_meld, mock_discard_pile_is_frozen):
    print("\n# 25\n")
    # -------------------------------------
    """Tests to ensure (#1 replace_discard_pile_temp_meld() is called when
    len(player.melds[-1]) == 2 & MasterDeck.discard_pile_is_frozen == True) and
    ensures correct (#2 lens of associated lists)."""
    # Arrange ---------------------------------
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_1'])))
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_2'])))
    mock_discard_pile_is_frozen.return_value = True
    # Act -------------------------------------
    draw_discard_pile_attempt_check_hand_match(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 0
    assert len(MasterDeck.deck) == 106
    assert len(P2.hand) == 0
    assert len(P2.matched_card_list) == 1
    assert len(P2.melds) == 1
    assert len(P2.melds[0]) == 2
    assert MasterDeck.discard_pile_is_frozen == True
    mock_replace_discard_pile_temp_meld.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.Deck.discard_pile_is_frozen', new_callable = PropertyMock, return_Value = True)
@patch('Canasta_replica.draw_discard_pile_wild_card_prompt', autospec = True, return_value = None)
def test_3_draw_discard_pile_attempt_check_hand_match(mock_draw_discard_pile_wild_card_prompt, mock_discard_pile_is_frozen):
    print("\n# 26\n")
    # -------------------------------------
    """Tests to ensure (#1 draw_discard_pile_wild_card_prompt() is called when
    len(player.melds[-1]) == 2 & MasterDeck.discard_pile_is_frozen == False &
    len(player.hand_wild_cards_reference_list) > 0) and (#2 lens of associated
    lists)."""
    # Arrange ---------------------------------
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_1'])))
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['joker_none_1'])))
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_2'])))
    mock_discard_pile_is_frozen.return_value = False
    # Act -------------------------------------
    draw_discard_pile_attempt_check_hand_match(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 0
    assert len(MasterDeck.deck) == 105
    assert len(P2.hand) == 1
    assert len(P2.matched_card_list) == 1
    assert len(P2.melds) == 1
    assert len(P2.melds[0]) == 2
    assert MasterDeck.discard_pile_is_frozen == False
    assert len(P2.hand_wild_cards_reference_list) == 1
    mock_draw_discard_pile_wild_card_prompt.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.Deck.discard_pile_is_frozen', new_callable = PropertyMock, return_Value = True)
@patch('Canasta_replica.replace_discard_pile_temp_meld', autospec = True, return_value = None)
def test_4_draw_discard_pile_attempt_check_hand_match(mock_replace_discard_pile_temp_meld, mock_discard_pile_is_frozen):
    print("\n# 27\n")
    # -------------------------------------
    """Tests to ensure (#1 replace_discard_pile_temp_meld() is called when
    len(player.melds[-1]) == 2 & MasterDeck.discard_pile_is_frozen == False &
    len(player.hand_wild_cards_reference_list) == 0) and validates expected (#2
    lens of associated lists)."""
    # Arrange ---------------------------------
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_1'])))
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_2'])))
    mock_discard_pile_is_frozen.return_value = False
    # Act -------------------------------------
    draw_discard_pile_attempt_check_hand_match(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 0
    assert len(MasterDeck.deck) == 106
    assert len(P2.hand) == 0
    assert len(P2.matched_card_list) == 1
    assert len(P2.melds) == 1
    assert len(P2.melds[0]) == 2
    assert MasterDeck.discard_pile_is_frozen == False
    assert len(P2.hand_wild_cards_reference_list) == 0
    mock_replace_discard_pile_temp_meld.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.stock_draw', autospec = True, return_value = None)
def test_5_draw_discard_pile_attempt_check_hand_match(mock_stock_draw):
    print("\n# 28\n")
    # -------------------------------------
    """Tests to ensure (#1 stock_draw() is called when
    len(player.matched_card_list == 0) and validates expected (#2 lens of
    associated lists)."""
    # Arrange ---------------------------------
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_club_1'])))
    MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_2'])))
    # Act -------------------------------------
    draw_discard_pile_attempt_check_hand_match(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 1
    assert len(MasterDeck.deck) == 106
    assert len(P2.hand) == 1
    assert len(P2.matched_card_list) == 0
    assert len(P2.melds) == 0
    mock_stock_draw.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
def test_draw_discard_pile(mock_play_2):
    print("\n# 29\n")
    # -------------------------------------
    """Tests to ensure (#1 red_3_check() is called), (#2 play_2() is called),
    and validates expected (#3 for proper lens of affected lists)"""
    # Arrange ---------------------------------
    for card in ['king_diamond_1', 'king_diamond_2', 'king_club_1', 'king_club_2', 'king_heart_1', 'king_heart_2', 'king_spade_1', 'king_spade_2', 'three_heart_1', 'three_diamond_2']:
            MasterDeck.discard_pile.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    draw_discard_pile(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.discard_pile) == 0
    assert len(MasterDeck.deck) == 96
    assert len(P1.hand) == 10
    assert len(P1.red_3_meld) == 2
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_draw_discard_pile_attempt_temp_meld_wild_card_addition():
    print("\n# 30\n")
    # -------------------------------------
    """Tests to ensure (#1 player.melds[-1] has the correct amount of cards after
    function has ran), and (#2 for proper lens of affected lists)"""
    # Arrange ---------------------------------
    for card in ['king_club_1', 'joker_none_1', 'two_club_2']:
        P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['four_heart_2']))])
    # Act -------------------------------------
    print("\nINPUT: 1 OR 2\n")
    draw_discard_pile_attempt_temp_meld_wild_card_addition(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 104
    assert len(P2.hand) == 2
    assert len(P2.melds[-1]) == 2
    assert len(P2.hand_wild_cards_reference_list) == 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.draw_discard_pile', autospec = True, return_value = None)
def test_draw_discard_pile_wild_card_prompt(mock_draw_discard_pile):
    print("\n# 31\n")
    # -------------------------------------
    """Tests to ensure (#1 draw_discard_pile() is returned when
    player.hand_wild_cards_reference_list > 0, use_wild_card_input == 'y', &
    player.round_score > player.meld_requirement), and (#2 validates proper lens
    of associated lists)."""
    # Arrange ---------------------------------
    for card in ['king_club_1', 'king_club_2', 'king_diamond_1', 'king_diamond_2']:
        P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    meld = []
    for card in P2.hand[:]:
        meld.append(P2.hand.pop(P2.hand.index(card)))
    P2.melds.append(meld)
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_diamond_2'])))
    # Act -------------------------------------
    print("\nINPUT #1: Y\nINPUT #2: 1\n")
    draw_discard_pile_wild_card_prompt(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 103
    assert len(P2.hand) == 0
    assert len(P2.melds) == 1
    assert len(P2.melds[-1]) == 5
    assert len(P2.hand_wild_cards_reference_list) == 0
    assert P2.round_score >= P2.meld_requirement
    mock_draw_discard_pile.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.replace_discard_pile_temp_meld', autospec = True, return_value = None)
def test_2_draw_discard_pile_wild_card_prompt(mock_replace_discard_pile_temp_meld):
    print("\n# 32\n")
    # -------------------------------------
    """Tests to ensure (#1 replace_discard_pile_temp_meld() is returned when
    player.hand_wild_cards_reference_list > 0, use_wild_card_input == 'n', &
    player.round_score > player.meld_requirement), and (#2 validates proper lens
    of associated lists)."""
    # Arrange ---------------------------------
    for card in ['king_club_1', 'king_club_2', 'king_diamond_1', 'king_diamond_2']:
        P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    meld = []
    for card in P2.hand[:]:
        meld.append(P2.hand.pop(P2.hand.index(card)))
    P2.melds.append(meld)
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['two_diamond_2'])))
    # Act -------------------------------------
    print("\nINPUT: N\n")
    draw_discard_pile_wild_card_prompt(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 103
    assert len(P2.hand) == 1
    assert len(P2.melds) == 1
    assert len(P2.melds[-1]) == 4
    assert len(P2.hand_wild_cards_reference_list) == 1
    assert P2.round_score < P2.meld_requirement
    mock_replace_discard_pile_temp_meld.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.replace_discard_pile_temp_meld', autospec = True, return_value = None)
def test_3_draw_discard_pile_wild_card_prompt(mock_replace_discard_pile_temp_meld):
    print("\n# 33\n")
    # -------------------------------------
    """Tests to ensure (#1 replace_discard_pile_temp_meld() is returned when
    player.hand_wild_cards_reference_list == 0), and (#2 validates proper lens
    of associated lists)."""
    # Arrange ---------------------------------
    for card in ['king_club_1', 'king_club_2', 'king_diamond_1', 'king_diamond_2']:
        P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    meld = []
    for card in P2.hand[:]:
        meld.append(P2.hand.pop(P2.hand.index(card)))
    P2.melds.append(meld)
    # Act -------------------------------------
    draw_discard_pile_wild_card_prompt(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 104
    assert len(P2.hand) == 0
    assert len(P2.melds) == 1
    assert len(P2.melds[-1]) == 4
    assert len(P2.hand_wild_cards_reference_list) == 0
    assert P2.round_score < P2.meld_requirement
    mock_replace_discard_pile_temp_meld.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.stock_draw', autospec = True, return_value = None)
def test_replace_discard_pile_temp_meld(mock_stock_draw):
    print("\n# 34\n")
    # -------------------------------------
    """Tests to ensure (#1 stock_draw() is called at the end of function), and
    (#2 validates correct lens of associated lists)."""
    # Arrange ---------------------------------
    meld = []
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_1'])))
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_1'])))
    meld_copy = copy.copy(meld)
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_2'])))
    P1.melds.append(meld)
    for card in meld_copy:
        P1.matched_card_list.append(card)
    # Act -------------------------------------
    replace_discard_pile_temp_meld(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 105
    assert len(P1.hand) == 2
    assert len(P1.melds) == 0
    assert len(P1.matched_card_list) == 0
    assert len(MasterDeck.discard_pile) == 1
    mock_stock_draw.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.valid_play_check_and_sort', autospec = True, return_value = None)
def test_play_2(mock_valid_play_check_and_sort):
    print("\n# 35\n")
    # -------------------------------------
    """Tests ensures (#1 valid_play_check_and_sort(P1) is called when play_choice
    == 1)"""
    # Arrange ---------------------------------
    meld = []
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_1'])))
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_1'])))
    P1.melds.append(meld)
    for card in ['jack_club_2', 'jack_diamond_2', 'ten_club_1']:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT #1: 1\nINPUT #2: 1,2,3\n")
    play_2(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 103
    assert len(MasterDeck.discard_pile) == 0
    assert len(P1.hand) == 0
    assert len(P1.play_cards) == 3
    assert len(P1.melds) == 1
    assert len(P1.melds[0]) == 2
    mock_valid_play_check_and_sort.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.discard', autospec = True, return_value = None)
def test_2_play_2(mock_discard):
    print("\n# 36\n")
    # -------------------------------------
    """Tests ensures (#1 discard(P1) is called when play_choice == 2)"""
    # Arrange ---------------------------------
    meld = []
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_1'])))
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_1'])))
    P1.melds.append(meld)
    # Act -------------------------------------
    print("\nINPUT: 2\n")
    play_2(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 106
    assert len(MasterDeck.discard_pile) == 0
    assert len(P1.hand) == 0
    assert len(P1.play_cards) == 0
    assert len(P1.melds) == 1
    mock_discard.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_multiple_choices_input_filter_and_transfer():
    print("\n# 37\n")
    # -------------------------------------
    """Tests to ensure (#1 append_list & pop_list have the correct values after
    function has run)."""
    # Arrange ---------------------------------
    meld = []
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_1'])))
    meld.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_1'])))
    P1.melds.append(meld)
    for card in ['king_club_2', 'king_diamond_2', 'king_spade_2']:
        P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT: 1,2,3\n")
    multiple_choices_input_filter_and_transfer(P1, P1.melds[0], P1.hand)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 103
    assert len(MasterDeck.discard_pile) == 0
    assert len(P1.hand) == 0
    assert len(P1.melds) == 1
    assert len(P1.melds[0]) == 5
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
def test_valid_play_check_and_sort(mock_play_2):
    print("\n# 38\n")
    # -------------------------------------
    """Tests to ensure (#1 player_2(P2) is returned when P2.round_score <
    P2.meld_requirement & len(P2.play_cards) < 3)."""
    # Arrange ---------------------------------
    P2.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_club_2'])))
    P2.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['king_diamond_2'])))
    # Act -------------------------------------
    valid_play_check_and_sort(P2)
    # Assert ----------------------------------
    assert P2.round_score < P2.meld_requirement
    assert len(MasterDeck.deck) == 106
    assert len(P2.hand) == 2
    assert len(P2.play_cards) == 0
    mock_play_2.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
def test_2_valid_play_check_and_sort(mock_play_2):
    print("\n# 39\n")
    # -------------------------------------
    """Tests to ensure (#1 when player.score < player.meld_requirement, all lens
    of player.play_cards temp_melds are < 2 or == 2, and when there are no wild
    cards to use for adding to those melds, that the test function returns no
    valid melds), (#2 that the play cards are properly returned to their original
    location), and (#3 validates lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['ace_diamond_2', 'jack_club_2', 'jack_spade_1', 'four_heart_1', 'four_club_1', 'king_club_2', 'king_club_1']:
        P2.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    valid_play_check_and_sort(P2)
    # Assert ----------------------------------
    assert P2.round_score < P2.meld_requirement
    assert len(MasterDeck.deck) == 101
    assert len(P2.hand) == 7
    assert len(P2.play_cards) == 0
    assert len(P2.melds) == 0
    assert len(P2.play_cards_wild_cards) == 0
    mock_play_2.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
def test_3_valid_play_check_and_sort(mock_play_2):
    print("\n# 40\n")
    # -------------------------------------
    """Tests to ensure (#1 cards from player.play_cards that match a preexisting
    meld are added to the proper melds), and (#2 validates lens of associated
    lists)."""
    # Arrange ---------------------------------
    for card in ['ace_diamond_2', 'jack_club_2', 'jack_spade_1', 'four_heart_1', 'four_club_1', 'king_club_2', 'king_club_1']:
        P2.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['ace_club_1', 'ace_club_2', 'ace_heart_1']:
        P2.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['jack_club_1', 'jack_diamond_1', 'jack_diamond_2']:
        P2.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['four_club_2', 'four_diamond_1', 'four_diamond_2']:
        P2.melds[2].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['king_spade_1', 'king_diamond_1', 'king_heart_2']:
        P2.melds[3].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    valid_play_check_and_sort(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 89
    assert len(P2.hand) == 0
    assert len(P2.play_cards) == 0
    assert len(P2.melds) == 4
    assert len(P2.melds[0]) == 4
    assert len(P2.melds[1]) == 5
    assert len(P2.melds[2]) == 5
    assert len(P2.melds[3]) == 5
    assert len(P2.play_cards_wild_cards) == 0
    mock_play_2.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
@patch('Canasta_replica.Player.meld_requirement', new_callable = PropertyMock, return_Value = 9999)
def test_4_valid_play_check_and_sort(mock_meld_requirement, mock_play_2):
    print("\n# 41\n")
    # -------------------------------------
    """Tests to ensure (#1 when player.score < player.meld_requirement, all lens
    of player.play_cards temp_melds are < 2 or == 2, and when there are wild cards
    to use for adding to those melds, but even with those wild card additions the
    attempted melds still do not reach the player.meld_requirement, the test
    function returns play_2(P2)), (#2 that the play cards are properly returned
    to their original location), and (#3 validates expected lens of associated
    lists)."""
    # Arrange ---------------------------------
    mock_meld_requirement.return_value = 9999 # I want to see if this will work without me calling the mock, having set return_value above.
    for card in ['ace_diamond_2', 'jack_club_2', 'jack_spade_1', 'four_heart_1', 'four_club_1', 'king_club_2', 'king_club_1', 'joker_none_1']:
        P2.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("INPUT: 1,2, or 3, but not 4\n")
    valid_play_check_and_sort(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 100
    assert len(P2.hand) == 8
    assert len(P2.play_cards) == 0
    assert len(P2.melds) == 0
    assert len(P2.play_cards_wild_cards) == 0
    mock_meld_requirement.assert_called()
    mock_play_2.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
def test_5_valid_play_check_and_sort(mock_play_2):
    print("\n# 42\n")
    # -------------------------------------
    """Tests to (#1 ensure black_3s are removed from player.play_cards whenever
    len(player.hand) > 1), and (#2 validates expected lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['three_spade_1', 'three_spade_2', 'three_club_1', 'three_club_2']:
        P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['four_club_2'])))
    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['five_club_2'])))
    # Act -------------------------------------
    valid_play_check_and_sort(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 102
    assert len(P1.hand) == 6
    assert len(P1.play_cards) == 0
    assert len(P1.melds) == 0
    assert P1.round_score == 0
    mock_play_2.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.Player.has_canasta', new_callable = PropertyMock, return_Value = True )
@patch('Canasta_replica.Player.meld_requirement', new_callable = PropertyMock, return_Value = 0)
@patch('Canasta_replica.went_out_check', autospec = True, return_value = None)
def test_6_valid_play_check_and_sort(mock_went_out_check, mock_meld_requirement, mock_has_canasta):
    print("\n# 43\n")
    # -------------------------------------
    """Tests to (#1 ensure black_3_meld is created and validly played whenever
    len(player.hand) <= 1 & player.meld_requirement is met), (#2 validates
    expected lens of associated lists)."""
    # Arrange ---------------------------------
    mock_meld_requirement.return_value = 0
    mock_has_canasta.return_value = True
    for card in ['three_spade_1', 'three_spade_2', 'three_club_1', 'three_club_2']:
        P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    valid_play_check_and_sort(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 104
    assert len(P1.hand) == 0
    assert len(P1.play_cards) == 0
    assert len(P1.melds) == 1
    assert len(P1.melds[0]) == 4
    assert P1.round_score == 400
    mock_went_out_check.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.discard', autospec = True, return_value = None)
def test_7_valid_play_check_and_sort(mock_discard):
    print("\n# 44\n")
    # -------------------------------------
    """Tests using a large, diverse set of play cards to ensure proper
    functionality for the entire function, ultimately checking for proper
    transfer of cards and validating expected lengths of associated lists. This
    test tests almost every single possible scenario, and is purposefully large
    so as to ensure proper interaction between all internal systems when various
    situations are combined. This function call should return discard(P1)"""
    # Arrange ---------------------------------
    # Below Section -  The two Jokers below are to be appended to two of the three 2 length melds that exist in the play cards group. The 2 is to be removed from the list of play cards, i.e. input should be 'N' when asked if you would like to use it to be the 3rd card in the last length 2 attempted meld.
    for card in ['joker_none_2', 'joker_none_1', 'two_diamond_1']:
        P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card]))) # Value = 100
    # -------------------------------------
    # Below Section - This attempted meld is to be the black_3_meld that is validated as meld #1 / player.melds[0].
    for card in ['three_spade_1', 'three_spade_2', 'three_club_1']:
        P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card]))) # Value = 300 (400)
    # -------------------------------------
    # Below Section - This attempted meld is to be validated as meld #2 / player.melds[1].
    for card in ['four_club_1', 'four_diamond_2', 'four_spade_1', 'four_spade_2', 'four_heart_1', 'four_club_2', 'four_heart_2']:
        P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card]))) # Value = 35 + 500 = (935)
    # -------------------------------------
    # Below Section - This attempted meld 2 length meld is to be validated via wild card addition as meld #3 / player.melds[2].
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['five_diamond_1']))) # Value = 5 (940)
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['five_heart_1']))) # Value = 5 (945)
    # -------------------------------------
    # Below Section - This attempted 2 length meld is to be validated via wild card addition as meld #4 / player.melds[3].
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['six_heart_1']))) # Value = 5 (950)
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['six_club_2']))) # Value = 5 (955)
    # -------------------------------------
    # Below Section - This attempted 2 length meld should be rejected as the meld that the user rejects to add the last wild card to.
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['seven_heart_1'])))
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['seven_club_2'])))
    # -------------------------------------
    # Below Card - This card is to be rejected as a bad_len_meld.
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_spade_1'])))
    # Below Card - This card is to be rejected as a bad_len_meld.
    P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['queen_spade_1'])))
    # Below Section - This attempted meld is to be validated as meld #5 / player.meld[4].
    for card in ['king_spade_1', 'king_spade_2', 'king_diamond_2', 'king_diamond_1']:
        P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card]))) # Value = 40 (995)
    # -------------------------------------
    # Below Section - This attemped meld is to be validated as meld #6 / player.melds[5].
    for card in ['ace_spade_1', 'ace_club_1', 'ace_diamond_2', 'ace_diamond_1']:
        P1.play_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card]))) # Value = 80 (1075)
    # Act -------------------------------------
    print("\nINPUT #1: 1\nINPUT #2: 1\nINPUT #3: 1\nINPUT #4: 1\nINPUT #5: 2\nINPUT #6: 6\n")
    valid_play_check_and_sort(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 79 # 29
    assert len(MasterDeck.discard_pile) == 0
    assert len(P1.hand) == 5
    assert len(P1.play_cards) == 0
    assert len(P1.black_3_meld) == 0
    assert len(P1.melds) == 6
    assert len(P1.melds[0]) == 3
    assert len(P1.melds[1]) == 7
    assert len(P1.melds[2]) == 3
    assert len(P1.melds[3]) == 3
    assert len(P1.melds[4]) == 4
    assert len(P1.melds[5]) == 4
    assert P1.round_score == 1075
    mock_discard.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_wild_card_handler():
    print("\n# 45\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever the player plays exactly 7 wild cards
    that they are properly placed into a Wild Card Canasta when input == 'Y'),
    and (#2 validates expected lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['joker_none_1', 'joker_none_2', 'joker_none_3', 'joker_none_4', 'two_heart_1', 'two_heart_2', 'two_club_1']:
        P2.play_cards_wild_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT: Y\n")
    wild_card_handler(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 101
    assert len(MasterDeck.discard_pile) == 0
    assert len(P2.hand) == 0
    assert len(P2.play_cards) == 1
    assert len(P2.play_cards[0]) == 7
    assert len(P2.play_cards_wild_cards) == 0
    assert len(P2.melds) == 0
    assert (P2.has_canasta) == True
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_2_wild_card_handler():
    print("\n# 46\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever the player plays more than 7 wild cards
    that 7 of them are properly placed into a Wild Card Canasta when input ==
    'Y'), (#2 that the leftover wild cards are added to the wild card canasta
    whenever the player opts to use them there), and (#3 validates expected lens
    of associated lists)."""
    # Arrange ---------------------------------
    for card in ['joker_none_1', 'joker_none_2', 'joker_none_3', 'joker_none_4', 'two_heart_1', 'two_heart_2', 'two_club_1', 'two_club_2', 'two_diamond_1']:
        P2.play_cards_wild_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("INPUT #1: Y\nINPUT #2: 1,2,3,4,5,6,7\nINPUT #3: 1\nINPUT #4: 1")
    wild_card_handler(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 99
    assert len(MasterDeck.discard_pile) == 0
    assert len(P2.hand) == 0
    assert len(P2.play_cards) == 1
    assert len(P2.play_cards[0]) == 9
    assert len(P2.play_cards_wild_cards) == 0
    assert len(P2.melds) == 0
    assert (P2.has_canasta) == True
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_3_wild_card_handler():
    print("\n# 47\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever the player plays more than 7 wild cards
    that 7 of them are properly placed into a Wild Card Canasta when input ==
    'Y'), (#2 that the leftover wild cards are properly transferred into the
    chosen meld), and (#3 validates expected lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['joker_none_1', 'joker_none_2', 'joker_none_3', 'joker_none_4', 'two_heart_1', 'two_heart_2', 'two_club_1', 'two_club_2', 'two_diamond_1']:
        P2.play_cards_wild_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['four_diamond_1', 'four_diamond_2', 'four_heart_2']:
        P2.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT #1: Y\nINPUT #2: 1,2,3,4,5,6,7\nINPUT #3: 2\nINPUT #4: 2")
    wild_card_handler(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 96
    assert len(MasterDeck.discard_pile) == 0
    assert len(P2.hand) == 0
    assert len(P2.play_cards) == 1
    assert len(P2.play_cards[0]) == 7
    assert len(P2.play_cards_wild_cards) == 0
    assert len(P2.melds) == 1
    assert len(P2.melds[0]) == 5
    assert (P2.has_canasta) == True
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_4_wild_card_handler():
    print("\n# 48\n")
    # -------------------------------------
    """Tests to ensure (#1 that whenever there are a few attempted melds in
    player.play_cards and player.melds, along with a few wild cards being played,
    and when the wild cards are placed in various different places, that the
    cards end up being properly placed), (#2 that whenever a leftover wild card
    is opted to be placed back into the hand, it is properly placed), and (#3
    ensures validity of expected lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['joker_none_1', 'joker_none_2', 'joker_none_3', 'joker_none_4', 'two_heart_1']:
        P2.play_cards_wild_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['four_diamond_1', 'four_diamond_2', 'four_heart_2']:
        P2.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['five_diamond_1', 'five_diamond_2', 'five_club_1']:
        P2.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.play_cards.append([])
    for card in ['jack_club_1', 'jack_club_2', 'jack_spade_1']:
        P2.play_cards[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.play_cards.append([])
    for card in ['ace_club_1', 'ace_club_2', 'ace_spade_1']:
        P2.play_cards[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT #1: 1\nINPUT #2: 2\nINPUT #3: 3\nINPUT #4: 4\nINPUT #5: 5\n")
    wild_card_handler(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 91
    assert len(MasterDeck.discard_pile) == 0
    assert len(P2.hand) == 1
    assert len(P2.play_cards) == 2
    assert len(P2.play_cards[0]) == 4
    assert len(P2.play_cards[1]) == 4
    assert len(P2.play_cards_wild_cards) == 0
    assert len(P2.melds) == 2
    assert len(P2.melds[0]) == 4
    assert len(P2.melds[1]) == 4
    assert P2.round_score == 320
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_5_wild_card_handler():
    print("\n# 49\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever the player has only melds/attempted
    melds with the maximum amount of wild cards in them that the wild cards are
    properly placed back into the player's hand and not errantly placed in those
    maxed out melds), and (#2 ensures expected lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['joker_none_1', 'joker_none_2', 'joker_none_3']:
        P2.play_cards_wild_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['four_diamond_1', 'four_diamond_2', 'four_heart_2', 'two_heart_1', 'two_heart_2', 'two_diamond_1']:
        P2.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['five_diamond_1', 'five_diamond_2', 'five_club_1', 'two_diamond_2', 'two_club_1', 'two_club_2']:
        P2.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.play_cards.append([])
    for card in ['jack_club_1', 'jack_club_2', 'jack_spade_1', 'two_spade_1', 'two_spade_2', 'joker_none_4']:
        P2.play_cards[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    wild_card_handler(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 87
    assert len(MasterDeck.discard_pile) == 0
    assert len(P2.hand) == 3
    assert len(P2.play_cards) == 1
    assert len(P2.play_cards[0]) == 6
    assert len(P2.play_cards_wild_cards) == 0
    assert len(P2.melds) == 2
    assert len(P2.melds[0]) == 6
    assert len(P2.melds[1]) == 6
    assert P2.round_score == 270
    assert (P2.has_canasta) == None
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_6_wild_card_handler():
    print("\n# 50\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever a player with no melds or a set of
    invalid attempted melds is trying to play some wild cards the wild cards do
    not get played but instead are properly replaced back into the player's hand)
    , and (#2 ensures expected lens of associated lists)."""
    # Arrange ---------------------------------
    for card in ['joker_none_1', 'joker_none_2', 'joker_none_3']:
        P2.play_cards_wild_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    wild_card_handler(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 105
    assert len(MasterDeck.discard_pile) == 0
    assert len(P2.hand) == 3
    assert len(P2.play_cards) == 0
    assert len(P2.play_cards_wild_cards) == 0
    assert len(P2.melds) == 0
    assert P2.round_score == 0
    assert (P2.has_canasta) == None
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_wild_card_meld_choice_prompt():
    print("\n# 51\n")
    # -------------------------------------
    """Tests to (#1 ensure that play_card attempted melds and melds are properly
    numbered in the function, so that player choice via input is accurately
    reflected in the returned value) and (#2 validates expected lens of
    associated lists."""
    # Arrange ---------------------------------
    P2.play_cards_wild_cards.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['joker_none_1'])))
    P2.melds.append([])
    for card in ['four_diamond_1', 'four_diamond_2', 'four_heart_2']:
        P2.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.play_cards.append([])
    for card in ['jack_club_1', 'jack_club_2', 'jack_spade_1']:
        P2.play_cards[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT: 2\n")
    meld_choice_index = wild_card_meld_choice_prompt(P2, P2.play_cards_wild_cards[0])
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 101
    assert len(MasterDeck.discard_pile) == 0
    assert len(P2.hand) == 0
    assert len(P2.play_cards) == 1
    assert len(P2.play_cards_wild_cards) == 1
    assert len(P2.melds) == 1
    assert P2.round_score == 45
    assert meld_choice_index == 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_1', autospec = True, return_value = None)
def test_discard(mock_play_1):
    print("\n# 52\n")
    # -------------------------------------
    """Tests to (#1 ensure a proper exchange between the player.hand and the
    MasterDeck.discard_pile), (#2 ensures that when player == P1, play_2(P2) is
    returned by the function), and (#3 validates expected lens of associated
    lists."""
    # Arrange ---------------------------------
    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_club_1'])))
    P1.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_club_2'])))
    # Act -------------------------------------
    print("\nINPUT: 1 or 2\n")
    discard(P1)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 106
    assert len(MasterDeck.discard_pile) == 1
    assert len(P1.hand) == 1
    mock_play_1.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.play_1', autospec = True, return_value = None)
def test_2_discard(mock_play_1):
    print("\n# 53\n")
    # -------------------------------------
    """Tests to (#1 ensure a proper exchange between the player.hand and the
    MasterDeck.discard_pile), (#2 ensures that when player == P2, play_2(P1) is
    returned by the function), and (#3 validates expected lens of associated
    lists."""
    # Arrange ---------------------------------
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_club_1'])))
    P2.hand.append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_club_2'])))
    # Act -------------------------------------
    print("\nINPUT: 1 or 2\n")
    discard(P2)
    # Assert ----------------------------------
    assert len(MasterDeck.deck) == 106
    assert len(MasterDeck.discard_pile) == 1
    assert len(P2.hand) == 1
    mock_play_1.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.round_reset', autospec = True, return_value = None)
@patch('Canasta_replica.Player.has_canasta', new_callable = PropertyMock, return_Value = True)
@patch('Canasta_replica.play_1', autospec = True, return_value = None)
def test_went_out_check(mock_play_1, mock_has_canasta, mock_round_reset):
    print("\n# 54\n")
    # -------------------------------------
    """Tests to (#1 ensure that when player.has_canasta == True, code block is
    thoroughly exectuted; therefore tests all levels of logic within that
    section), (#2 ensures that play_1(P2) is returned whenever player == P1 &
    player.has_canasta == True), and (#3 validates expected lens of associated
    lists)."""
    # Arrange ---------------------------------
    mock_has_canasta.return_value = True
    # Act -------------------------------------
    went_out_check(P1)
    # Assert ----------------------------------
    assert P1.going_out == True
    assert len(P1.initial_played_cards) == 0
    assert P1.went_out_concealed == True
    assert P2.going_out == False
    mock_has_canasta.assert_called()
    mock_round_reset.assert_called()
    mock_play_1.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.round_reset', autospec = True, return_value = None)
@patch('Canasta_replica.discard', autospec = True, return_value = None)
def test_2_went_out_check(mock_discard, mock_round_reset):
    print("\n# 55\n")
    # -------------------------------------
    """Tests to (#1 ensure that when player.has_canasta == False, code block is
    thoroughly exectuted; therefore tests all levels of logic within that
    section), and (#2 ensures that discard(P2) is returned whenever player == P2
    & player.round_score > player.meld_requirement), and (#3 validates expected
    lens of associated lists)."""
    # Arrange ---------------------------------
    P2.melds.append([])
    for card in ['ace_diamond_1', 'ace_diamond_2', 'ace_heart_2']:
        P2.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['jack_club_1', 'jack_club_2', 'two_spade_1']:
        P2.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.initial_played_cards = copy.deepcopy(P2.melds)
    P2.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_spade_2'])))
    P2.melds.append([])
    for card in ['king_club_1', 'king_club_2', 'king_spade_1']:
        P2.melds[2].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("INPUT #1: 2\nINPUT #2: Y\n")
    went_out_check(P2)
    # Assert ----------------------------------
    assert len(P2.hand) == 3
    assert len(P2.melds[0]) == 3
    assert len(P2.melds[1]) == 4
    assert len(P2.melds) == 2
    assert len(MasterDeck.deck) == 98
    assert P2.round_score == 110
    assert P2.has_canasta == None
    mock_discard.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.round_reset', autospec = True, return_value = None)
@patch('Canasta_replica.Player.meld_requirement', new_callable = PropertyMock, return_Value = True)
@patch('Canasta_replica.play_2', autospec = True, return_value = None)
def test_3_went_out_check(mock_play_2, mock_meld_requirement, mock_round_reset):
    print("\n# 56\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever player.has_canasta == False &
    player.round_score < player.meld_requirement, play_2(P2) is returned
    (whenever player == P2)), (#2 ensures that all cards from the attempted melds
    are properly replaced whenever player.round_score < player.meld_requirement),
    and (#3 validates expected lens for associated lists)."""
    # Arrange ---------------------------------
    mock_meld_requirement.return_value = 9999
    P2.melds.append([])
    for card in ['ace_diamond_1', 'ace_diamond_2', 'ace_heart_2']:
        P2.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.melds.append([])
    for card in ['jack_club_1', 'jack_club_2', 'two_spade_1']:
        P2.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P2.initial_played_cards = copy.deepcopy(P2.melds)
    P2.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['jack_spade_2'])))
    P2.melds.append([])
    for card in ['king_club_1', 'king_club_2', 'king_spade_1']:
        P2.melds[2].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    # Act -------------------------------------
    print("\nINPUT #1: 2\nINPUT #2: Y\n")
    went_out_check(P2)
    # Assert ----------------------------------
    mock_play_2.assert_called_with(P2)
    mock_meld_requirement.assert_called()
    print(P2.hand)
    assert len(P2.hand) == 10
    assert len(P2.melds) == 0
    assert len(MasterDeck.deck) == 98
    assert P2.round_score == 0
    assert P2.meld_requirement == 9999
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_went_out_check_replacement_card():
    print("\n# 57\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever there are both melds with 3 cards and
    melds with over 3 cards, and whenever a 3 len meld is chosen for card
    removal, and player opts to disband the meld, it properly disbands), and (#2
    verifies the expected lens of associated lists)."""
    # Arrange ---------------------------------
    P1.melds.append([])
    for card in ['ace_diamond_1', 'ace_diamond_2', 'ace_heart_2']:
        P1.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.melds.append([])
    for card in ['jack_club_1', 'jack_club_2', 'two_spade_1', 'jack_spade_2']:
        P1.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.melds.append([])
    for card in ['king_club_1', 'king_club_2', 'king_spade_1', 'king_diamond_2']:
        P1.melds[2].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.last_set_played_cards.append([P1.melds[0][0], P1.melds[0]])
    P1.last_set_played_cards.append([P1.melds[1][0], P1.melds[1]])
    P1.last_set_played_cards.append([P1.melds[2][0], P1.melds[2]])
    # Act -------------------------------------
    print("\nINPUT #1: 3\nINPUT #2: Y\n")
    went_out_check_replacement_card(P1)
    # Assert ----------------------------------
    assert len(P1.hand) == 3
    assert len(P1.melds) == 2
    assert len(P1.melds[0]) == 4
    assert len(P1.melds[1]) == 4
    assert len(MasterDeck.deck) == 97
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_2_went_out_check_replacement_card():
    print("\n# 58\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever there are both melds with 3 cards and
    melds with over 3 cards, and whenever a 3 len meld is chosen for card removal
    but player opts to instead choose a different card, the function properly
    restarts so that the player can make a different card choice), and (#2
    verifies the expected lens of associated lists)."""
    # Arrange ---------------------------------
    P1.melds.append([])
    for card in ['ace_diamond_1', 'ace_diamond_2', 'ace_heart_2']:
        P1.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.melds.append([])
    for card in ['jack_club_1', 'jack_club_2', 'two_spade_1', 'jack_spade_2']:
        P1.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.melds.append([])
    for card in ['king_club_1', 'king_club_2', 'king_spade_1', 'king_diamond_2']:
        P1.melds[2].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.last_set_played_cards.append([P1.melds[0][0], P1.melds[0]])
    P1.last_set_played_cards.append([P1.melds[1][0], P1.melds[1]])
    P1.last_set_played_cards.append([P1.melds[2][0], P1.melds[2]])
    # Act -------------------------------------
    print("INPUT #1: 3\nINPUT #2: N\nINPUT #3: 1\n")
    went_out_check_replacement_card(P1)
    # Assert ----------------------------------
    assert len(P1.hand) == 1
    assert len(P1.melds) == 3
    assert len(P1.melds[0]) == 3
    assert len(P1.melds[1]) == 3
    assert len(P1.melds[2]) == 4
    assert len(MasterDeck.deck) == 97
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_3_went_out_check_replacement_card():
    print("\n# 59\n")
    # -------------------------------------
    """Tests to (#1 ensure that whenever a player chooses to remove one card from
    two melds with a length greater than 3, each card is properly removed and the
    melds are preserved), and (#2 validates expected lens of associated lists)."""
    # Arrange ---------------------------------
    P1.melds.append([])
    for card in ['ace_diamond_1', 'ace_diamond_2', 'ace_heart_2']:
        P1.melds[0].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.melds.append([])
    for card in ['jack_club_1', 'jack_club_2', 'two_spade_1', 'jack_spade_2']:
        P1.melds[1].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.melds.append([])
    for card in ['king_club_1', 'king_club_2', 'king_spade_1', 'king_diamond_2']:
        P1.melds[2].append(MasterDeck.deck.pop(MasterDeck.deck.index(decktionary[card])))
    P1.last_set_played_cards.append([P1.melds[0][0], P1.melds[0]])
    P1.last_set_played_cards.append([P1.melds[1][0], P1.melds[1]])
    P1.last_set_played_cards.append([P1.melds[2][0], P1.melds[2]])
    # Act -------------------------------------
    print("\nINPUT #1: 1\nINPUT #2: 2\n")
    went_out_check_replacement_card(P1)
    went_out_check_replacement_card(P1)
    # Assert ----------------------------------
    assert len(P1.hand) == 2
    assert len(P1.melds) == 3
    assert len(P1.melds[0]) == 3
    assert len(P1.melds[1]) == 3
    assert len(P1.melds[2]) == 3
    assert len(MasterDeck.deck) == 97
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.Player.round_score', new_callable = PropertyMock, return_Value = 900)
@patch('Canasta_replica.win_check', autospec = True, return_value = None)
def test_round_reset(mock_win_check, mock_round_score):
    print("\n# 60\n")
    # -------------------------------------
    """Tests to (#1 ensure that all values are properly reset), and (#2 ensures
    that win_check() is called at the end of the function)."""
    # Arrange ---------------------------------
    mock_round_score.return_value = 900
    # Act -------------------------------------
    round_reset()
    # Assert ----------------------------------
    for player in (P1, P2): # ****
        assert player.finished_rounds_scores == [900] # ****
        assert player.round_score == 900
        assert player.the_draw == None # ****
        assert len(player.hand) == 0 # ****
        assert len(player.play_cards) == 0 # ****
        assert len(player.play_cards_wild_cards) == 0 # ****
        assert len(player.initial_played_cards) == 0 # ****
        assert len(player.last_set_played_cards) == 0 # ****
        assert len(player.red_3_meld) == 0 # ****
        assert len(player.black_3_meld) == 0 # ****
        assert len(player.melds) == 0 # ****
        assert len(player.len_2_temp_melds_list) == 0 # ****
        assert len(player.matched_card_list) == 0 # ****
        assert player.going_out == None # ****
        assert player.went_out_concealed == False # ****
        # --------------------------------------
    assert len(MasterDeck.discard_pile) == 0
    assert len(MasterDeck.deck) == 108
    assert MasterDeck.deck == MasterDeck.original_deck[:]
    mock_win_check.assert_called()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.check_total_score_winner', autospec = True, return_value = None)
@patch('Canasta_replica.the_draw_1', autospec = True, return_value = None)
def test_win_check(mock_the_draw_1, mock_check_total_score_winner):
    print("\n# 61\n")
    # -------------------------------------
    """Tests (#1 to ensure that whenever both players.total_score < 5000, the
    function properly bypasses everything and calls the_draw_1()."""
    # Arrange ---------------------------------
        # Nothing to arrange...both player's scores should be 0.
    # Act -------------------------------------
    win_check()
    # Assert ----------------------------------
    mock_the_draw_1.assert_called()
    mock_check_total_score_winner.assert_not_called()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.Player.total_score', new_callable = PropertyMock)
@patch('Canasta_replica.check_total_score_winner', autospec = True, return_value = None)
@patch('Canasta_replica.the_draw_1', autospec = True, return_value = None)
def test_2_win_check(mock_the_draw_1, mock_check_total_score_winner, mock_total_score):
    print("\n# 62\n")
    # -------------------------------------
    """Tests (#1 to ensure that whenever P2's players.total_score >= 5000 & >
    than P1.total_score, the function properly returns
    check_total_score_winner(P2, P1)."""
    # Arrange ---------------------------------
    mock_total_score.return_value = 5000
    P2.melds.append([MasterDeck.deck.pop(MasterDeck.deck.index(decktionary['ace_diamond_1']))])
    # Act -------------------------------------
    win_check()
    # Assert ----------------------------------
    mock_the_draw_1.assert_not_called()
    mock_check_total_score_winner.assert_called_with(P1, P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.winner_output', autospec = True, return_value = None)
def test_check_total_score_winner(mock_winner_output):
    print("\n# 63\n")
    # -------------------------------------
    """Tests (#1 to ensure that whenever P1.total_score > P2.total_score,
    winner_output(P1) is returned."""
    # Arrange ---------------------------------
    P1.finished_rounds_scores.append(5000)
    # Act -------------------------------------
    check_total_score_winner(P1, P2)
    # Assert ----------------------------------
    mock_winner_output.assert_called_with(P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.winner_output', autospec = True, return_value = None)
def test_2_check_total_score_winner(mock_winner_output):
    print("\n# 64\n")
    # -------------------------------------
    """Tests (#1 to ensure that whenever P2.total_score > P1.total_score,
    winner_output(P1) is returned."""
    # Arrange ---------------------------------
    P2.finished_rounds_scores.append(5000)
    # Act -------------------------------------
    check_total_score_winner(P1, P2)
    # Assert ----------------------------------
    mock_winner_output.assert_called_with(P2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.winner_output', autospec = True, return_value = None)
def test_3_check_total_score_winner(mock_winner_output):
    print("\n# 65\n")
    # -------------------------------------
    """Tests (#1 to ensure that whenever P2.total_score == P1.total_score,
    winner_output(P2, True) is returned."""
    # Arrange ---------------------------------
        # Nothing to arrange...both players' scores are 0, so the function should calculate their total_scores as == one another.
    # Act -------------------------------------
    check_total_score_winner(P2, P1)
    # Assert ----------------------------------
    mock_winner_output.assert_called_with(P2, True)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.the_draw_1', autospec = True, return_value = None)
def test_winner_output(mock_the_draw_1):
    print("\n# 66\n")
    # -------------------------------------
    """Tests (#1 to ensure the function runs cleanly when (P1, False) are passed
    to the function and the play_again_input == 'Y')"""
    # Arrange ---------------------------------
        # Nothing to arrange here.
    # Act -------------------------------------
    print("\nINPUT: Y\n")
    winner_output(P1)
    # Assert ----------------------------------
    mock_the_draw_1.assert_called()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.the_draw_1', autospec = True, return_value = None)
def test_2_winner_output(mock_the_draw_1):
    print("\n# 67\n")
    # -------------------------------------
    """Tests (#1 to ensure the function runs cleanly when (P2, True) are passed
    to the function and (#2 that the game closes when the play_again_input ==
    'N')."""
    # Arrange ---------------------------------
        # Nothing to arrange here.
    # Act -------------------------------------
    print("\nOUTPUT SHOULD REFLECT A TIE GAME\nINPUT: N\n")
    with pytest.raises(SystemExit):
        winner_output(P2, True)
    # Assert ----------------------------------
        # Nothing to assert here. Act is essentially Assert section.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@patch('Canasta_replica.the_draw_1', autospec = True, return_value = None)
def test_game_run(mock_the_draw_1):
    print("\n# 68\n")
    # -------------------------------------
    """Tests (#1 to ensure that the function calls the_draw_1() function)."""
    # Arrange ---------------------------------
        # Nothing to arrange here.
    # Act -------------------------------------
    game_run()
    # Assert ----------------------------------
    mock_the_draw_1.assert_called()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
