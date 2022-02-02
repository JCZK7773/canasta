# J2, which cards would you like to play? (Use the ordered number of the card(s) as listed below. (i.e. - '1,3,4,8')
#
# iterated_and_numbered_list_printer
#
# 1) ('3', 'S')
# 2) ('3', 'C')
# 3) ('4', 'H')
# 4) ('7', 'H')
# 5) ('8', 'D')
# 6) ('Ja', 'C')
# 7) ('Q', 'D')
# 8) ('Q', 'H')
# 9) ('K', 'S')
# 10) ('A', 'H')
# 11) ('10', 'S')
# 12) ('6', 'D')
#
# > 1,2,3,4,5,6,7,8,9,10,11,12
#
# valid_play_check_and_sort
#
# player.round_score < meld
#
# Sorry, but you cannot play Black 3(s) in this way. Black 3s can only be used to freeze the discard pile. The Black 3(s) that are being removed from your attempted play cards back into your hand are as follows:
#
# iterated_and_numbered_list_printer
#
# 1) ('3', 'C')
# 2) ('3', 'S')
#
# Sorry, but you have some play cards that do not pass the rule requirements. You cannot create a new meld without at least 2 natural cards of the same rank, or without a wild card to add to it to reach the 3 card minimum meld requirement. The attempted meld(s) will be removed and placed back in your hand:
#
# iterated_and_numbered_list_printer
#
# 1) []
#
# 2) []
#
# 3) []
#
# 4) []
#
# 5) [('Q', 'D')]
# 6) []
#
# 7) []
#
# 8) []
#
# 9) []
#
# Traceback (most recent call last):
#   File "Canasta_Main_Improving_and_Testing.py", line 816, in <module>
#     game_run()
#   File "Canasta_Main_Improving_and_Testing.py", line 812, in game_run
#     the_draw_1()
#   File "Canasta_Main_Improving_and_Testing.py", line 182, in the_draw_1
#     the_draw_3(player)
#   File "Canasta_Main_Improving_and_Testing.py", line 221, in the_draw_3
#     the_deal(P2,P1)
#   File "Canasta_Main_Improving_and_Testing.py", line 252, in the_deal
#     play_1(player1) # ***
#   File "Canasta_Main_Improving_and_Testing.py", line 329, in play_1
#     play_2(player)
#   File "Canasta_Main_Improving_and_Testing.py", line 486, in play_2
#     if valid_play_check_and_sort(player) == True: # ***
#   File "Canasta_Main_Improving_and_Testing.py", line 645, in valid_play_check_and_sort
#     if len(play_cards_wild_cards) > 0:
# NameError: name 'play_cards_wild_cards' is not defined
# PS J:\Programming\Projects\Canasta>
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


J1, which cards would you like to play? (Use the ordered number of the card(s) as listed below. (i.e. - '1,3,4,8')

iterated_and_numbered_list_printer

1) 2♣
2) 4♥
3) 4♦
4) 7♦
5) 8♦
6) 9♠
7) 10♥
8) 10♦
9) Q♦
10) K♣
11) A♣
12) 8♠

> 1,2,3,4,5,6,7,8,9,10,11,12

valid_play_check_and_sort

player.round_score < meld

The below meld(s) from your attempted play cards have only 2 cards in them. Since 3 cards are required for a valid meld, you must add a wild card to them for them to remain in play. It looks as if you have 1 wild card(s) in your set of play cards to use for this. Choose a meld from the list below that you would like to add a wild card to.

iterated_and_numbered_list_printer

1) [8♠, 8♦]
2) [10♦, 10♥]
3) [4♦, 4♥]

4) I would rather use the wild card(s) elsewhere, and let the meld(s) be placed back into my hand.

> 2

Which wild card would you like to add to the following meld? - [10♦, 10♥] - Choose from the below choices.

iterated_and_numbered_list_printer

1) 2♣

> 1

You successfully added the 2♣ to your meld.

You have some attemped melds that do not pass the rule requirements. You cannot create a new meld without at least 2 natural cards of the same rank, or without a wild card to add to it to reach the 3 card minimum meld requirement. The attempted meld(s) will be removed and placed back in your hand:

iterated_and_numbered_list_printer

1) [A♣]
2) [K♣]
3) [Q♦]
4) [9♠]
5) [7♦]
6) [8♠, 8♦]
7) [4♦, 4♥]

final play 2 player.melds print

You successfully melded the cards below!

iterated_and_numbered_list_printer

1) [10♦, 10♥, 2♣]

True - initial_played_card_count != final_played_card_count

discard

Which card would you like to discard? Your available cards in hand are:

iterated_and_numbered_list_printer

1) A♣
2) K♣
3) Q♦
4) 9♠
5) 7♦
6) 8♠
7) 8♦
8) 4♦
9) 4♥


> 5

You discarded the 7♦.

went out check

play_1

J2, which method would you like to use to draw?

1) Draw from Stack
2) Draw from Discard Pile

> 2
draw_discard_pile_attempt

draw_discard_pile_attempt_check_hand_match

draw_1 part 2

draw 3

return_draw_card

the deal

J1 is dealt 11 cards. Your hand consists of:

sort_player_cards

iterated_and_numbered_list_printer

1) 2♥
2) 2♦
3) 3♣
4) 3♦
5) 4♦
6) 4♥
7) 4♣
8) 5♦
9) 5♥
10) 6♦
11) 6♥
12) 8♠
13) 8♦
14) 9♠
15) J♣
16) Q♦
17) K♣
18) A♠
