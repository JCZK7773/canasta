# D E B U G
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Current bugs.
    # Current Bug - Bug Number = None - I am quite sure that visual placement for play_cards during valid_play_check_and_sort() are not proper. It looks like the meld nums, card nums, etc. are not properly calculated whenever pre-sorted visual arrangements are made.
    # Current Bug - Bug Number = None - Whenever attempting to add wild_cards to temp_melds during valid_play_check_and_sort(), whenever it asks the player to choose a meld to add the wild card to, the game does not recognize any card clicks and never does anything or progresses any further. No crash, just no click recognition.
    # Current Bug - Bug Number = None - Not Finished: game.progression_text_obj section; need to make it so that both of the text objs get blitted and that in the case that obj_2 was previously blitted that the 'erase' section is run in that instance as well as all of the others. Also need to finish loigc concerning whether or not when in this case 'obj' should be changed to none, then create 'obj_1' & 'obj_2', having the blit section chcek whether or not 'obj_1' & 'obj_2' are none, just as it # checks for all of the other renders...
    # Current Bug - Bug Number = None - When playing a set of cards, it properly situated them, and the value was over 50 points, but instead game output said that I had (0) points from the play cards and denied the play.
    # Current Bug - Bug Number = None - Whenever there are so many play_cards attempted melds that they visually take up all of the available visual meld slots, the remaining wild cards in the list of play cards visually overlay the meld groups. I need to code in a limit for valid x-coordinates for the play_cards melds and make the cards in pre_sort_play_cards have their visual locations calculated based on the visual locations of the melds in play_cards so that they never visually overlap. Might hvae to make it so the limit-exceeding cards get displayed on the next row (below or above).
    # Current Bug - Bug Number = None - Whenever there are preexisting Red 3's visually displayed in a player's meld group before the player has melded any cards, whenever he does meld cards subsequently the first meld is visually placed in the same location as the Red 3 meld. I have to make it so that the Red 3 meld is visually located based on an updated list of the current melds (if that is the root cause).
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Error traceback code goes here in this section; for debugging.

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
