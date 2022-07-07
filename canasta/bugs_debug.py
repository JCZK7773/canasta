# D E B U G
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Current bugs.
    # Current Bug - Bug Number = None - When I played 2x 2-card attempted melds and 2x wild cards along with them, after I was given the choice to place them in the len 2 melds, which I did, making the 2x melds consist of 3 cards each, but it errantly output the message - 'You have attempted to create meld(s) with less than 3 cards' - and then errantly output the message - 'Sorry, but the value of your play cards (0)...'. :|
    # Current Bug - Bug Number = None - The play_cards are not being resituated after cards are popped from them, as is done for all of the other card groups.
    # Current Bug - Bug Number = None - The card group name display boxes should only display whenever there are cards in the card group associated with each text box.
    # Current Bug - Bug Number = None - In the case that both players have the same draw card, the player names stay what the players gave them previously, but the game prompts the players to give them new names. It should just keep those names, I believe.
    # Current Bug - Bug Number = None - Whenever I played a 2 card meld with 2 Joker wild cards, after I chose 'Yes' to using a wild card to make it a 3 card meld, the output displayed 'Okay, you will use the Joker', and THEN asked me to choose which of the 2 Jokers I would like to use. It shouldn't have said the first input because it shouldn't determine which wild card I am going to use.
    # Current Bug - Bug Number = None - Whenever a Red 3 is played as the first 'meld' in a player's meld, since it is offset on the y-plane, it makes the player meld text box overlap the top of the card. I need to make the text box calculated off of the location of the first meld in the meld group or remove the offset for the red 3 meld to fix this.
    # Current Bug - Bug Number = None - After players have been named, the various card group text info boxes say 'Player 1' or 'Player 2' instead of the actual player's current name.
    # Current Bug - Bug Number = None - The 'Type error: cannot pickle 'pygame.Surface' object' traceback seems to happen whenever I make 2 consecutive play attempts (one turn for P1 (play some cards), one turn for P2, another turn for P1 (attempt to play some cards)).
    # Current Bug - Bug Number = None - Whenever prompted with the output: 'j, which meld from your play cards or your melds would you like to add the Joker to? Click any meld to choose it.', it does not allow me to choose a wild card.
    # ATTEMPTED BUT CAN'T SEE ERRORS IN CODE - Current Bug - Bug Number = None - When picking up the discard pile successfully via using 2 cards from the player's hand to create a meld (having already had a meld and met the meld requirement on a previous turn), it looks as if the cards from the discard pile were appended to the player's hand but it doesn't look like they were popped from the discard pile. The discard pile should be empty at this point but it definitely is not.
    # SHOULD BE SOLVED - Current Bug - Bug Number = None - Whenever there are preexisting Red 3's visually displayed in a player's meld group before the player has melded any cards, whenever he does meld cards subsequently the first meld is visually placed in the same location as the Red 3 meld. I have to make it so that the Red 3 meld is visually located based on an updated list of the current melds (if that is the root cause).
    # SHOULD BE SOLVED - Current Bug - Bug Number = None - Not Finished: game.progression_text_obj section; need to make it so that both of the text objs get blitted and that in the case that obj_2 was previously blitted that the 'erase' section is run in that instance as well as all of the others. Also need to finish loigc concerning whether or not when in this case 'obj' should be changed to none, then create 'obj_1' & 'obj_2', having the blit section chcek whether or not 'obj_1' & 'obj_2' are none, just as it # checks for all of the other renders...
    # SHOULD BE SOLVED - Current Bug - Bug Number = None - Whenever attempting to add wild_cards to temp_melds during valid_play_check_and_sort(), whenever it asks the player to choose a meld to add the wild card to, the game does not recognize any card clicks and never does anything or progresses any further. No crash, just no click recognition.
    # SOLVED????? Current Bug - Bug Number = None - When playing a set of cards, it properly situated them, and the value was over 50 points, but instead game output said that I had (0) points from the play cards and denied the play.
    # SOLVED - Current Bug - Bug Number = None - NOTE: Not a bug! It's just that the cards move so fast it seems they move all at once. Perhaps adding in framerate control via delta time will solve this issue. Whenever cards are transferred from the hand to pre_sort_play_cards, instead of moving card for card they are moved one time as an entire unit.
    # SOLVED - Current Bug - Bug Number = None - Whenever there are so many play_cards attempted melds that they visually take up all of the available visual meld slots, the remaining wild cards in the list of play cards visually overlay the meld groups. I need to code in a limit for valid x-coordinates for the play_cards melds and make the cards in pre_sort_play_cards have their visual locations calculated based on the visual locations of the melds in play_cards so that they never visually overlap. Might hvae to make it so the limit-exceeding cards get displayed on the next row (below or above).
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Error traceback code goes here in this section; for debugging.
# -------------------------------------
    #     Traceback (most recent call last):
    #   File ".\main.py", line 65, in <module>
    #     main()
    #   File ".\main.py", line 62, in main
    #     progression.the_draw_1()
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 48, in the_draw_1
    #     return the_draw_2()
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 86, in the_draw_2
    #     the_draw_3()
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 120, in the_draw_3
    #     return the_deal(player.P2, player.P1) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 168, in the_deal
    #     return play_1(player1) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 216, in play_1
    #     stock_draw(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 230, in stock_draw
    #     play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 693, in valid_play_check_and_sort
    #     discard(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 825, in discard
    #     play_1(player.P1) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 216, in play_1
    #     stock_draw(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 230, in stock_draw
    #     play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 693, in valid_play_check_and_sort
    #     discard(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 823, in discard
    #     play_1(player.P2) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 216, in play_1
    #     stock_draw(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 230, in stock_draw
    #     play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 489, in valid_play_check_and_sort
    #     current_player.initial_played_cards = copy.deepcopy(current_player.melds) # ****
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 287, in _reconstruct
    #     item = deepcopy(item, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 287, in _reconstruct
    #     item = deepcopy(item, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 270, in _reconstruct
    #     state = deepcopy(state, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 270, in _reconstruct
    #     state = deepcopy(state, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 270, in _reconstruct
    #     state = deepcopy(state, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 161, in deepcopy
    #     rv = reductor(4)
    # TypeError: cannot pickle 'pygame.Surface' object
# -------------------------------------
    # Traceback (most recent call last):
    #   File ".\main.py", line 65, in <module>
    #     main()
    #   File ".\main.py", line 62, in main
    #     progression.the_draw_1()
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 48, in the_draw_1
    #     return the_draw_2()
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 86, in the_draw_2
    #     the_draw_3()
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 111, in the_draw_3
    #     return the_deal(player.P1, player.P2) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 168, in the_deal
    #     return play_1(player1) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 216, in play_1
    #     stock_draw(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 230, in stock_draw
    #     play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 661, in valid_play_check_and_sort
    #     return play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 661, in valid_play_check_and_sort
    #     return play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 476, in play_2
    #     discard(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 823, in discard
    #     play_1(player.P2) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 216, in play_1
    #     stock_draw(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 230, in stock_draw
    #     play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 693, in valid_play_check_and_sort
    #     discard(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 825, in discard
    #     play_1(player.P1) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 218, in play_1
    #     draw_discard_pile_attempt(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 261, in draw_discard_pile_attempt
    #     return stock_draw(current_player)
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 230, in stock_draw
    #     play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 661, in valid_play_check_and_sort
    #     return play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 476, in play_2
    #     discard(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 823, in discard
    #     play_1(player.P2) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 218, in play_1
    #     draw_discard_pile_attempt(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 288, in draw_discard_pile_attempt
    #     stock_draw(current_player)
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 230, in stock_draw
    #     play_2(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 474, in play_2
    #     valid_play_check_and_sort(current_player) # ****
    #   File "J:\Programming\Projects\Canasta\canasta\progression.py", line 489, in valid_play_check_and_sort
    #     current_player.initial_played_cards = copy.deepcopy(current_player.melds) # ****
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 287, in _reconstruct
    #     item = deepcopy(item, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 287, in _reconstruct
    #     item = deepcopy(item, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 270, in _reconstruct
    #     state = deepcopy(state, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 270, in _reconstruct
    #     state = deepcopy(state, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 172, in deepcopy
    #     y = _reconstruct(x, memo, *rv)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 270, in _reconstruct
    #     state = deepcopy(state, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 146, in deepcopy
    #     y = copier(x, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 230, in _deepcopy_dict
    #     y[deepcopy(key, memo)] = deepcopy(value, memo)
    #   File "C:\Users\JMT3E\anaconda3\lib\copy.py", line 161, in deepcopy
    #     rv = reductor(4)
    # TypeError: cannot pickle 'pygame.Surface' object
