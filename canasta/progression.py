import sys # ****
import random # ****
import copy
import os
import time
import logging # ****
import pygame
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import player
import deck
import locations
import card
import customappendlist
import game
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Logger setup. # ****
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s" # ****
logging.basicConfig(filename = "J:\\Programming\\Projects\\Canasta\\canasta\\Canasta_log.log", level = logging.DEBUG, format = LOG_FORMAT, filemode = 'a') # ****
logger = logging.getLogger() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by main.main(). Handles name creation. # ****
def the_draw_1(testing = False): # ****
    # print('the_draw_1')
    logger.debug("the_draw_1") # ****
    # -------------------------------------
    game.game.game_state = 'the_draw_1'
    # -------------------------------------
    for current_player in [player.P1, player.P2]:
        if current_player.name == 'Player 1' or 'Player 2':
            while True: # ****
                try: # ****
                    game.game.progression_text = (f"{current_player.name}, what is your name?")
                    game.game.text_input_active = True
                    while game.game.text_input_active == True:
                        game.game.draw_window_main()
                    if len(game.game.input_text_final) < 1: # ****
                        raise ValueError # ****
                    else:
                        current_player.name = game.game.input_text_final
                    break # ****
                except ValueError: # ****
                    game.game.progression_text = ("Sorry, but your name must be at least one character long. It looks as if your input was blank. Hit Enter to try again.")
                    game.game.error_input_active = True
                    while game.game.error_input_active == True:
                        game.game.draw_window_main()
    # -------------------------------------
    game.game.progression_text = ''
    return the_draw_2()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_1() function. Handles draw card choice to determine first player and checks the player's draw card to ensure it is not a Joker; if it is, player chooses another card.
def the_draw_2(testing = False):
    # print('the_draw_2')
    logger.debug('the_draw_2') # ****
    # -------------------------------------
    game.game.game_state = 'the_draw_2'
    # -------------------------------------
    locations.Locate.the_draw_anim()
    # -------------------------------------
    for current_player in [player.P1, player.P2]:
        game.game.progression_text = (f"{current_player.name}, pick your card from the stack to determine which player will have the first play. Click a card to choose.")
        game.game.click_card_active = True
        # Below Line - Called the_draw_anim() function to visually lay our the cards in the 2 decks so the player can click the card they want to choose.
        while True: # ****
            for current_card in deck.MasterDeck.deck:
                game.game.clickable_card_list.append(current_card)
            while game.game.clicked_card == None:
                game.game.draw_window_main()
            current_player.draw_card = game.game.clicked_card
            current_player.hand.append(deck.MasterDeck.deck.pop(deck.MasterDeck.deck.index(current_player.draw_card)))
            # -------------------------------------
            game.game.clicked_card = None
            game.game.clicked_card_list.clear()
            # -------------------------------------
            # Below Section - Checks to see if the current_player's draw_card is a Joker; if so, places the card back into the deck.MasterDeck from the current_player.hand, and assigns the .draw_card to None. It will then make the current_player choose another card. If not, calls the_draw_3().
            if current_player.draw_card.rank == 'Joker': # ****
                game.game.progression_text = (f"Sorry, {current_player.name}, you picked a Joker, which is not available for use during The Draw! Choose another card!") # ****
                game.game.xs_display(2)
                game.game.click_card_active = True
                deck.MasterDeck.deck.append(current_player.hand.pop(0)) # ****
                current_player.draw_card = None
            else:
                game.game.progression_text = (f"{current_player.name}, you picked a {current_player.draw_card}!") # ****
                game.game.xs_display(2)
                break # ****
            # -------------------------------------
    the_draw_3()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_2() function. Checks whether or not the players have the same draw card. If they do, redirects the process back to the_draw_1() and places players' cards back into the MasterDeck.deck. If not, checks to see who wins the draw and returns the_deal() after determination. # ****
def the_draw_3(testing = False): # ****
    # print('the_draw_3')
    logger.debug("the_draw_3\n") # ****
    # ------------------------------------- # ****
    if (player.P1.draw_card.rank, player.P1.draw_card.suit) == (player.P2.draw_card.rank, player.P2.draw_card.suit): # ****
        # -------------------------------------
        if testing == True:
            return "You have the same exact card! You both must pick another card!" # ****
        # -------------------------------------
        game.game.progression_text = ("You have the same exact card! You both must pick another card!") # ****
        game.game.xs_display(2)
        # -------------------------------------
        return_draw_card() # ****
        return the_draw_1() # ****
    elif player.P1.draw_card_val > player.P2.draw_card_val: # ****
        # -------------------------------------
        if testing == True:
            return "the_deal(P1,P2)"
        # -------------------------------------
        game.game.progression_text = f'{player.P1.name}\'s {player.P1.draw_card.rank} trumps {player.P2.name}\'s {player.P2.draw_card.rank}, so {player.P1.name} gets first play!'
        game.game.xs_display(3)
        return_draw_card() # ****
        return the_deal(player.P1, player.P2) # ****
    elif player.P2.draw_card_val > player.P1.draw_card_val: # ****
        # -------------------------------------
        if testing == True:
            return "the_deal(P2,P1)"
        # -------------------------------------
        game.game.progression_text = f'{player.P2.name}\'s {player.P2.draw_card.rank} trumps {player.P1.name}\'s {player.P1.draw_card.rank}, so {player.P2.name} gets first play!'
        game.game.xs_display(3)
        return_draw_card() # ****
        return the_deal(player.P2, player.P1) # ****
    elif player.P1.draw_card_val == player.P2.draw_card_val: # ****
        if deck.MasterDeck.draw_suit_ranks.get(player.P1.draw_card.suit) > deck.MasterDeck.draw_suit_ranks.get(player.P2.draw_card.suit): # ****
            # -------------------------------------
            if testing == True:
                return "the_deal(P1,P2)"
            # -------------------------------------
            return_draw_card() # ****
            game.game.progression_text = f'{player.P1.name}\'s draw card trumps {player.P2.name}\'s because {player.P1.draw_card.suit} trumps {player.P2.draw_card.suit}! {player.P1.name} will have first play!'
            game.game.xs_display(3)
            return the_deal(player.P1, player.P2) # ****
        else: # ****
            # -------------------------------------
            if testing == True:
                return "the_deal(P2,P1)"
            # -------------------------------------
            game.game.progression_text = f'{player.P2.name}\'s draw card trumps {player.P1.name}\'s because {player.P2.draw_card.suit} trumps {player.P1.draw_card.suit}! {player.P2.name} will have first play!'
            game.game.xs_display(3)
            return_draw_card() # ****
            return the_deal(player.P2, player.P1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_3() function. Changes all of the cards in the deck.MasterDeck.deck to be located at the locations.Locate.deck_loc and returns the player.draw_card from player.hand back into deck.MasterDeck.deck. # ***
def return_draw_card(): # ****
    # print('return_draw_card')
    logger.debug("return_draw_card\n") # ****
    # Below Section - Moves each card from the deck into the proper deck location (from the draw_anim) locations.
    for current_card in deck.MasterDeck.deck:
        [current_card.x, current_card.y] = locations.Locate.deck_loc
    # -------------------------------------
    for current_player in [player.P1, player.P2]: # ****
        deck.MasterDeck.deck.append(current_player.hand.pop(0)) # ****
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_draw_3() function. Handles dealing, sorting, printing; red 3 checks each player's cards, creates a discard pile from deck.MasterDeck, and directs to play_1(). # ****
def the_deal(player1, player2): # ****
    # print('the_deal()')
    logger.debug("the_deal\n") # ****
    # -------------------------------------
    game.game.game_state = 'main'
    # Below - Deals each player their 11 cards, sorts them, prints them, and checks for Red 3s. # ****
    for current_player in (player1, player2): # ****
        game.game.progression_text = (f"{current_player.name} is dealt 11 cards.") # ****
        for card in range(11): # ****
            current_player.hand.append(deck.MasterDeck.deck.pop(0)) # ****
        red_3_check(current_player) # ****
    # -------------------------------------
    # Below - Creates the discard pile from the deck.MasterDeck # ****
    deck.MasterDeck.discard_pile.append(deck.MasterDeck.deck.pop(0)) # ****
    # -------------------------------------
    return play_1(player1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by the_deal() & . Handles initially dealt and drawn Red 3s. Removes them from player.hand, replaces it with a newly drawn card from the deck, and prints associated output. # ****
def red_3_check(current_player, drawn = False): # ****
    print('red_3_check')
    logger.debug("red_3_check\n") # ****
    # -------------------------------------
    current_player.prior_red_3_meld_len = len(current_player.red_3_meld)
    # -------------------------------------
    # Below Section - Checks the entire current_player.hand for Red 3's. If found, checks to see if it was drawn. If so, displays informative message. Then places it in current_player.red_3_meld. *** Remember that this is ran whenever the player picks up a discard pile, which means that the entire hand needs to be checked, not just .hand[-1]. This is why it is coded the way it is. Do not change it.
    for current_card in current_player.hand[:]: # ****
        if (current_card.rank, current_card.suit) in deck.Deck().red_3s: # ****
            if drawn == True: # ****
                game.game.progression_text = (f"{current_player.name}, you drew a Red 3! The {current_card} will be placed in your Red 3 meld, and you will automatically draw another card to replace it.") # ****
                game.game.xs_display(3)
            current_player.red_3_meld.append(current_player.hand.pop(current_player.hand.index(current_card))) # ****
    # -------------------------------------
    # Below Line - If the player has gained a Red 3.
    if current_player.prior_red_3_meld_len != len(current_player.red_3_meld):
        # Below Section - If drawn == False; gives an informative message to the player showing how many Red 3s they have received from the_deal() as well as the rules concerning how they are handled.
        if drawn == False: # ****
            if len(current_player.red_3_meld) == 4: # ****
                game.game.progression_text = (f"Congratulations, {current_player.name}! You have 4 Red 3s, so you get a 400 point bonus when the round ends if you have at least 1 Canasta, or a deduction of 400 points if you have no Canastas! All Red 3s must be played down and you will withdraw replacements from the stock for each one!") # ****
                game.game.xs_display(4)
            elif len(current_player.red_3_meld) > 0: # ****
                game.game.progression_text = f"{current_player.name}, you have {len(current_player.red_3_meld)} Red 3(s) in your hand! All Red 3s must be played, and you will draw a new card from the stock for each one!"
                game.game.xs_display(4)
        # -------------------------------------
        # Below Section - Replaces the Red 3s that were moved to current_player.red_3_meld with an equal amount of cards from the deck.MasterDeck.deck. Compares the current len against the prior len to determine how many cards to replace, so that it doesn't replace an errant amount whenever the player already had some Red 3s whenever this function was called.
        for red_3 in range(len(current_player.red_3_meld) - current_player.prior_red_3_meld_len):
            game.game.xs_display(1)
            current_player.hand.append(deck.MasterDeck.deck.pop(0)) # ****
            game.game.progression_text = f'{current_player.name}, in place of your Red 3, you drew a {current_player.hand[-1]}' # ****
            red_3_check(current_player, True)
            game.game.xs_display(2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by went_out_check(), the_deal() functions. Gives the player the option to either draw from the deck or to attempt a draw from the discard pile. Also prints out all preexisting melds for reference as it is important for choosing between the draw options. # ****
def play_1(current_player): # ****
    print('play_1')
    logger.debug("play_1\n") # ****
    # -------------------------------------
    game.game.progression_text = (f"{current_player.name}, which method would you like to use to draw? Click on your preferred option.")
    game.game.multiple_choice_text_1 = ('Draw from Stack')
    game.game.multiple_choice_text_2 = ('Draw from Discard Pile')
    game.game.multiple_choice_active = True
    while game.game.multiple_choice_active == True:
        game.game.draw_window_main()
    if game.game.selected_choice == 'Draw from Stack': # ****
        stock_draw(current_player) # ****
    else: # ****
        draw_discard_pile_attempt(current_player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_1(), draw_discard_pile_attempt_check_meld_match(), draw_discard_pile_attempt_check_hand_match(), replace_discard_pile_temp_meld() functions. For drawing a card from the stock & giving associated output. If stock is empty, redirects to draw_discard_pile_attempt(). # ****
def stock_draw(current_player, from_draw_discard_pile_attempt_no_canasta_fail = False): # ****
    print('stock_draw')
    logger.debug("stock_draw\n") # ****
    # -------------------------------------
    if len(deck.MasterDeck.deck) > 0: # ****
        current_player.hand.append(deck.MasterDeck.deck.pop(0)) # ****
        game.game.progression_text = (f"{current_player.name} drew a {current_player.hand[-1]} from the stack.")
        game.game.xs_display(2)
        red_3_check(current_player) # ****
        play_2(current_player) # ****
    else: # ****
        if from_draw_discard_pile_attempt_no_canasta_fail == False:
            game.game.progression_text = ("There are no cards left in the stock pile. If you have a meld that matches the rank of the face up discard, you are required to draw the discard pile's face up discard (or the entire discard pile), per the rules. This rule will continue until no player has a matching meld for the face up discard; at that point the round will end.") # ****
            game.game.xs_display(3)
            draw_discard_pile_attempt(current_player, True) # ****
        else:
            game.game.progression_text = ("It looks as if there are no cards in the stock pile for you to draw from, and since you cannot draw from the discard pile, your turn is forfeited and the opposing player will be allowed a chance at playing.")
            game.game.xs_display(3)
            if current_player == player.P1:
                return play_1(player.P2)
            else:
                return play_1(player.P1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_1(), stock_draw() functions. For attempting to draw the discard pile. If the stock_depleted parameter is true, checks to see if the discard pile is depleted; if not, checks for a matching meld for the face up discard, but if so, ends the round per the rules. # ****
def draw_discard_pile_attempt(current_player, stock_depleted = False): # ****
    print('draw_discard_pile_attempt')
    logger.debug("\ndraw_discard_pile_attempt\n") # ****
    # -------------------------------------
    # Below Section - Checks to see if the player can draw the discard pile in the case that the stock_depleted parameter is True. If so, attempts to draw the discard pile. If there is a matching meld, successfully draws the discard pile. If not, the round ends, per the rules. # ****
    if stock_depleted == True: # ****
        if len(deck.MasterDeck.discard_pile) == 0: # ****
            game.game.progression_text = ("It looks as if the discard pile is depleted as well. Per the rules, this means the round is ended since there is no means by which you can draw another card.") # ****
            game.game.xs_display(3)
            return round_reset() # ****
    # -------------------------------------
    # Below Section - In the case that a player attempts to draw the discard pile whenever the face up discard is a Wild Card or a Black 3. Outputs an informative prompt and returns stock_draw(), unless the stock_depleted == True, in which case round_reset() is called because there is no means by which anybody can draw a card.
    if (deck.MasterDeck.face_up_discard.rank, deck.MasterDeck.face_up_discard.suit) in deck.MasterDeck.wild_cards or (deck.MasterDeck.face_up_discard.rank, deck.MasterDeck.face_up_discard.suit) in deck.MasterDeck.black_3s:
        if stock_depleted == False:
            game.game.progression_text = ("Sorry, but you cannot draw the discard pile whenever the face up discard is a Wild Card or a Black 3. You will instead have to draw from the Stock.")
            game.game.xs_display(3)
            return stock_draw(current_player)
        else:
            game.game.progression_text = ("It looks as if the stock is depleted and the discard pile is topically frozen, which means nobody has a means by which to draw a card. Therefore the round is over!")
            game.game.xs_display(3)
            return round_reset()
    # -------------------------------------
    # Below Section - For discard pile draw attempt when it is not internally or topically frozen. Redirects to eligibility determinations based on player's initial meld status, and finalizes determination by either allowing drawing of the discard pile, or denial and subsequent redirection back to play_1. # ****
    if deck.MasterDeck.discard_pile_is_frozen == False: # ****
        logger.debug("discard_pile_is_frozen == False\n") # ****
        if stock_depleted == True:
            draw_discard_pile_attempt_check_meld_match(current_player, True) # ****
        else:
            # Below Line - Checks the player's existing melds to see if they have a match for the top discard to be used as a means to withdraw the discard pile. If so, draws the discard pile and creates a meld from the face up discard, and returns True. If not, continues to check the hand for an alternate route to draw the discard pile. # ****
            draw_discard_pile_attempt_check_meld_match(current_player) # ****
    elif deck.MasterDeck.discard_pile_is_frozen == True: # ****
        logger.debug("discard_pile_is_frozen == True\n") # ****
        game.game.progression_text = ("It looks as if the discard pile is frozen, which means that you cannot pick up the pile using a preexisting meld. You instead have to have matches to the face up discard in your hand, or one match and a Wild Card (in certain circumstances).")
        game.game.xs_display(3)
    # -------------------------------------
    # Below Line - For when the discard_pile_is_frozen is either True or False, and if draw_discard_pile_attempt_check_meld_match did not succeed. Checks the player's hand to see if they have matching cards in their hand (for when they have no melds that match the top discard) as an alternative means to pick up the discard pile. If so, draws the discard pile and creates a meld from the face up discard, and returns True, If not... # ****
    draw_discard_pile_attempt_check_hand_match(current_player) # ****
    # Below Section - Since the player was unable to draw the discard pile after attempting all of the possible methods, they must instead draw from the stock; calls stock_draw(current_player), unless the stock is depleted, in which case the player is given the opportunity to make a play via play_2(). In the latter case, player.special_case_cant_draw is changed to = True. If both players have went through this process, meaning both players' .special_case_cant_draw == True, then round_reset() is called as the round is functionally over since nobody can draw a card and both players have had the opportunity to make a final play.
    game.game.progression_text = ("It looks as if you were unable to draw the discard pile after attempting all of the possible methods.")
    game.game.xs_display(1)
    if stock_depleted == False:
        game.game.progression_text = ("You will draw from the stock instead.")
        game.game.xs_display(1)
        stock_draw(current_player)
    else:
        current_player.special_case_cant_draw = True
        if player.P1.special_case_cant_draw == True and player.P2.special_case_cant_draw == True:
            game.game.progression_text = ("Since both players have had a final opportunity to draw a card and both have been unsuccessful, and since both players have had a final opportunity to play their remaining plays, and since the round is functionally gridlocked, the round is over!")
            game.game.xs_display(3)
            round_reset()
        else:
            game.game.progression_text = ("Since the stock is depleted and you were unable to draw from the discard pile, you will not draw any card, and will instead move to your play, if you have one planned.")
            game.game.xs_display(2)
            play_2(current_player)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt(). Checks player's existing melds to see if they have a meld match for the face up discard, for the purpose of drawing the discard pile. # ****
def draw_discard_pile_attempt_check_meld_match(current_player, stock_depleted = False): # ****
    print('draw_discard_pile_attempt_check_meld_match')
    logger.debug("draw_discard_pile_attempt_check_meld_match")
    for meld in current_player.melds: # ****
        if deck.MasterDeck.face_up_discard.rank == meld[0].rank: # ****
            meld.append(deck.MasterDeck.discard_pile.pop(-1)) # ****
            # Below - In the case that the player is trying to draw from the discard pile because the stock is depleted. Per the rules, in this instance, only the face up discard is withdrawn, unless the player chooses otherwise. # ****
            if stock_depleted == True: # ****
                game.game.progression_text = (f"{current_player.name}, you successfully withdrew the face up discard from the discard pile, as you had a matching meld! Per the rules, you have the choice to either pick up the entire discard pile, or to take just the face up discard. Would you like to take the rest of the pile as well?")
                multiple_choice_text_1 = ('Yes')
                multiple_choice_text_2 = ('No')
                game.game.multiple_choice_active = True
                while game.game.selected_choice == None:
                    game.game.draw_window_main()
                if game.game.selected_choice == 'No': # ****
                    return play_2(current_player) # ****
            # If draw_rest_of_discard_pile_input was 'Yes'. Or if stock_depleted was not True and a face_up_discard match was found. # ****
            return draw_discard_pile(current_player) # ****
            # -------------------------------------
    # Below - When stock_depleted == True and the player cannot draw the pile because of the above section not detecting a match for the face up discard. # ****
    if stock_depleted == True: # ****
        game.game.progression_text = (f"{current_player.name}, unfortunately, you were unable to draw the discard pile because you did not have a matching meld. Therefore, since you have no means to draw a card, the round is over, per the rules.") # ****
        game.game.xs_display(3)
        round_reset() # ****
        # -------------------------------------
    if len(current_player.melds) > 0:
        game.game.progression_text = (f"You were unable to draw the discard pile using a matching meld.") # ****
        game.game.xs_display(1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt(). Checks the player's hand to see if they have a qualifying set of matching cards for the purpose of drawing the discard pile. # ****
def draw_discard_pile_attempt_check_hand_match(current_player): # ****
    print('draw_discard_pile_attempt_check_hand_match')
    logger.debug("draw_discard_pile_attempt_check_hand_match\n") # ****
    # -------------------------------------
    # Below Line - Clears player.matched_card_list so that whenever it has been previously appended to or modified, it is reset back to an empty list upon the start of this function so as to not mix up cards from previous play attempts.
    current_player.matched_card_list.clear()
    # Below Section - Checks each card in current_player.hand[:] to see if there is a match to the face_up_discard. If so, appends that card to current_player.matched_card_list and pops it from current_player.hand.
    for card in current_player.hand[:]: # ****
        if card.rank == deck.MasterDeck.face_up_discard.rank: # ****
            current_player.matched_card_list.append(current_player.hand.pop(current_player.hand.index(card))) # ****
    # -------------------------------------
    if len(current_player.matched_card_list) == 0: # ****
        game.game.progression_text = ("Sorry, but you did not have any matches to the face up discard.")
        game.game.xs_display(1)
        return None
    # -------------------------------------
    # Below Section - Copies the current_player.matched_card_list so as to create a fixed, static rank value, as the variable player_matched_card_list_copy. Next the player_matched_card_list_copy is appended to current_player.melds, and finally appends the face_up_discard to that meld, popping the cards from their original locations. Also gives an informative prompt and returns None so as not to continue on errantly to remainder of function code. # ****
    else:
        player_matched_card_list_copy = copy.copy(current_player.matched_card_list)
        current_player.melds.append(player_matched_card_list_copy) # ****
        current_player.melds[-1].append(deck.MasterDeck.discard_pile.pop(-1)) # ****
        # Below Section - If the player has 2 natural matches for the face up discard, (plus the face_up_discard in current_player.melds[-1]). Checks that the player has met meld requirement. If so, draws discard pile successfully. If not, attempts to use additional wild cards within the hand to reach the meld requirement via draw_discard_pile_wild_card_prompt. # ****
        if len(current_player.melds[-1]) >= 3: # ****
            if current_player.round_score >= current_player.meld_requirement: # ****
                if len(current_player.hand) < 1:
                    if current_player.has_canasta == True:
                        went_out_check(current_player, going_out_from_discard_draw = True)
                    else:
                        game.game.progression_text = ("It looks as if you are attempting to go out, but do not have a Canasta, which is against the rules. This means the drawing of the discard pile attempt must be cancelled. All of the cards that would have been used in the meld, along with the face up discard, will be replaced to their proper locations. You will instead have to draw from the stock.")
                        game.game.xs_display(3)
                        replace_discard_pile_temp_meld(current_player)
                game.game.progression_text = ("You successfully created a valid meld from the face up discard and met the meld requirements!\n")
                game.game.xs_display(3)
                return draw_discard_pile(current_player) # ****
            else: # ****
                draw_discard_pile_wild_card_prompt(current_player) # ****
        # -------------------------------------
        # Below Section - If the meld consists of only 1 natural card from the hand and the face up discard; if the discard_pile_is_frozen == True, reroutes the player to replace_discard_pile_temp_meld (which redirects to stock_draw()). If discard_pile_is_frozen == False, checks to see if the player has any wild cards to help them reach the meld length requirement. If so, attempts this via draw_discard_pile_wild_card_prompt(). Otherwise, redirects to replace_discard_pile_temp_meld(). # ****
        elif len(current_player.melds[-1]) == 2: # ****
            if deck.MasterDeck.discard_pile_is_frozen == True: # ****
                game.game.progression_text = (f"Sorry, {current_player.name}, but you don't have 2 natural cards of the face up discard's rank in your hand, which is required to pick up the discard pile when it is frozen, which it currently is. Therefore you will have to withdraw from the stock pile.") # ****
                game.game.xs_display(3)
                replace_discard_pile_temp_meld(current_player)
            elif deck.MasterDeck.discard_pile_is_frozen == False: # ****
                if len(current_player.hand_wild_cards_reference_list) > 0: # ****
                    draw_discard_pile_wild_card_prompt(current_player) # ****
                else: # ****
                    game.game.progression_text = ("Sorry, but you only had 1 natural card to match the face up discard's rank, with no wild cards to use to help reach the 3 card minimum for a valid meld. Therefore your meld and the face up discard will be placed back into the hand and discard pile respectively and you will instead have to draw from the stock.") # ****
                    game.game.xs_display(4)
                    replace_discard_pile_temp_meld(current_player)
        # -------------------------------------
        # Below Section - If the player did not have any matching cards to the face up discard in their hand; redirects player to stock_draw. # ****
        else: # ****
            game.game.progression_text = ("You did not have enough matches to the face up discard in your hand to draw the discard pile using cards in your hand.") # ****
            game.game.xs_display(2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_wild_card_prompt(), draw_discard_pile_attempt_check_meld_match(), draw_discard_pile_attempt_check_hand_match() functions. Pops and appends each card from the discard pile to the player's hand. # ****
def draw_discard_pile(current_player): # ****
    print('draw_discard_pile')
    logger.debug("draw_discard_pile\n") # ****
    # -------------------------------------
    game.game.progression_text = (f"{current_player.name}, you successfully drew the discard pile!") # ****
    for card in deck.MasterDeck.discard_pile[:]: # ****
        current_player.hand.append(deck.MasterDeck.discard_pile.pop(-1)) # ****
    red_3_check(current_player) # ****
    play_2(current_player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_wild_card_prompt() function. Prompts the player to choose which wild card they would like to use to add to their temp_meld for use in attempting to draw the discard pile. # ****
def draw_discard_pile_attempt_temp_meld_wild_card_addition(current_player): # ****
    print('draw_discard_pile_attempt_temp_meld_wild_card_addition')
    logger.debug("draw_discard_pile_attempt_temp_meld_wild_card_addition")
    game.game.progression_text = (f"{current_player.name}, please choose a wild card.") # ****
    game.game.click_card_active = True
    while game.game.clicked_card == None: # ****
        game.game.draw_window_main()
    current_player.melds[-1].append(current_player.hand.pop(current_player.hand.index(game.game.clicked_card))) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt_check_meld_match(), draw_discard_pile_attempt_check_hand_match() functions. Prompts the player to choose which wild card they would like to use to help them in withdrawing the discard pile. # ****
def draw_discard_pile_wild_card_prompt(current_player):
    print('draw_discard_pile_wild_card_prompt')
    logger.debug("draw_discard_pile_wild_card_prompt")
    game.game.multiple_choice_text_1 = 'Yes'
    game.game.multiple_choice_text_2 = 'No'
    game.game.multiple_choice_active = True
    while len(current_player.hand_wild_cards_reference_list) > 0: # ****
        game.game.progression_text = (f"Your attempted meld using the face up discard did not meet the meld requirement, therefore you would have to add a/some wild card(s) to the meld to help you reach the score requirement. It looks as if you have {len(current_player.hand_wild_cards_reference_list)} wild card(s) to use for this. Would you like to do this?")
        while game.game.multiple_choice_active == True: # ****
            game.game.draw_window_main()
        if game.game.selected_choice == 'Yes': # ****
            draw_discard_pile_attempt_temp_meld_wild_card_addition(current_player) # ****
            if current_player.round_score >= current_player.meld_requirement: # ****
                game.game.progression_text = ("You successfully created a valid meld from the face up discard and met the meld requirements!") # ****
                game.game.xs_display(2)
                return draw_discard_pile(current_player) # ****
        else: # ****
            game.game.progression_text = ("Okay, the attempted meld will be placed back into your hand, and the face up discard will be placed back on top of the discard pile. You will also draw from the stock pile instead.") # ****
            game.game.xs_display(4)
            return replace_discard_pile_temp_meld(current_player) # ****
            # -------------------------------------
    game.game.progression_text = ("Unfortunately your attempted meld using the face up discard did not meet the meld requirement, and you do not have any wild cards to add to it to help reach the required score. Your attempted meld will be placed back in your hand, and the face up discard will be placed back into the discard pile. You will instead draw from the stock pile.") # ****
    game.game.xs_display(4)
    return replace_discard_pile_temp_meld(current_player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_wild_card_prompt() function. Replaces the face up discard back into the discard pile and replaces the matched cards from the current_player.meld back into the current_player.hand. # ****
def replace_discard_pile_temp_meld(current_player): # ****
    print('replace_discard_pile_temp_meld')
    logger.debug("replace_discard_pile_temp_meld")
    deck.MasterDeck.discard_pile.append(current_player.melds[-1].pop(-1)) # ****
    for matched_card in current_player.matched_card_list[:]: # ****
        current_player.hand.append(current_player.melds[-1].pop(-1)) # ****
    current_player.melds.pop(-1) # ****
    current_player.matched_card_list.clear()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt_check_meld_match(), stock_draw(), draw_discard_pile(), and valid_play_check_and_sort() functions. Prompts the player to choose between either playing a set of cards or discarding instead. If player chooses to play cards, then the player is prompted to choose a set of cards to play and is then  # ****
def play_2(current_player, rerouted = False): # ****
    print('play_2')
    logger.debug("play_2\n") # ****
    # -------------------------------------
    # Below Line - For when valid_play_check_and_sort(), etc. functions do not successfully lead to a valid complete play and reroute back here mid-play. Instead of doing this each time an attempt is unsuccessful & redirects back here, it is done here once, for all instances. # ****
    current_player.play_cards.clear() # ****
    # -------------------------------------
    if rerouted == False:
        game.game.progression_text = (f"{current_player.name}, it is your turn to play!") # ****
        game.game.xs_display(2)
    game.game.progression_text = (f"{current_player.name}, what would you like to do with your turn?")
    game.game.multiple_choice_text_1 = 'Play Cards'
    game.game.multiple_choice_text_2 = 'Discard'
    game.game.multiple_choice_active = True
    while game.game.multiple_choice_active == True: # ****
        game.game.draw_window_main()
    if game.game.selected_choice == 'Play Cards': # ****
        game.game.progression_text = (f"{current_player.name}, which cards would you like to play?") # ****
        game.game.clickable_card_list = current_player.hand[:]
        game.game.click_card_active = True
        game.game.choose_multiple_cards = True
        game.game.multiple_choice_active = True
        game.game.multiple_choice_text_1 = 'Play Selected Cards'
        while game.game.multiple_choice_active == True:
            game.game.draw_window_main()
        for current_card in game.game.clicked_card_list:
            # print(f'current_card {current_card}')
            current_player.play_cards.append(current_card)
        game.game.choose_multiple_cards = False
        valid_play_check_and_sort(current_player) # ****
    else: # ****
        discard(current_player) # ****
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_2() function. For ensuring that a set of attempted play cards are valid according to game rules. # ****
def valid_play_check_and_sort(current_player): # ****
    print('valid_play_check_and_sort')
    logger.debug("\nvalid_play_check_and_sort\n") # ****
    # -------------------------------------
    play_cards_new_ranks = [] # ****
    bad_len_temp_melds_list_print = [] # ****
    play_cards_removed_black_3s = [] # ****
    # -------------------------------------
    # Below Section - Clears current_player.initial_played_cards and iterates through current_player.melds, appending each existing meld to initial_played_cards so that initial_played_cards == current_player.melds at this point in time. For the purpose of comparing current_player.initial_played_cards against current_player.melds later on to see if any cards/melds were successfully added to current_player.melds throughout the play after sorting and validation. # ****
    current_player.initial_played_cards.clear()
    current_player.initial_played_cards = copy.deepcopy(current_player.melds) # ****
    # -------------------------------------
    # Below Section - Checks to see if the player has NOT met the initial meld requirements. If so, valid plays are different than if they had met the requirement, thus puts different restrictions on what a valid play is. # ****
    if current_player.round_score < current_player.meld_requirement: # ****
        logger.debug("current_player.round_score < current_player.meld_requirement\n") # ****
        # -------------------------------------
        if len(current_player.play_cards) < 3: # ****
            game.game.progression_text = (f"Sorry, {current_player.name}, but you must play at least 3 cards for a new meld. Please select a new set of cards to play, or you can choose to discard if you like.") # ****
            game.game.xs_display(3)
            for current_card in current_player.play_cards[:]: # ****
                current_player.hand.append(current_card) # ****
            current_player.play_cards.clear() # ****
            return play_2(current_player, True) # ****
    # -------------------------------------
    # Below Extended Section - Sorts all of the individual play cards, putting them either in matching melds, or creating temp_melds and putting those back into play_cards to be further sorted. Also places all played wild cards into play_cards_wild_cards and removes any played Black 3s unless special requirements are met. # ****
    for current_card in current_player.play_cards[:]: # ****
        # Below Section - Checks to see if the player already has existing melds. If so, checks to see if card rank is already in a preexisting meld. If so, pops the card from current_player.play_cards and appends it to the meld. # ****
        card_found_in_meld = False # ****
        if len(current_player.melds) > 0: # ****
            for meld in current_player.melds: # ****
                if current_card.rank == meld[0].rank: # ****
                    meld.append(current_player.play_cards.pop(current_player.play_cards.index(current_card))) # ****
                    # Below Line - Changes the variable card_found_in_meld to True in the case that it is matched and subsequently popped from the list, so that if it also meets another parameter later on in the loop, it will not be recognized again and attempted to be handled again, which caused errors wherein it was trying to place the card in two different locations in the past. # ****
                    card_found_in_meld = True # ****
        # -------------------------------------
        # Below Extended Section - Handles all cards that were not found in a preexisting meld. Handles black_3s, wild cards, new melds, and cards that match the rank of new melds so that they can all be properly sorted and later validated. # ****
        if card_found_in_meld == False: # ****
            # Below Section - Checks if card is a Black 3 and whether the player meets the card count requirements to be able to play a Black 3 meld. If not, appends it to play_cards_removed_black_3s, which is used to print out all of these instances later on to inform the player, and removes it from current_player.play_cards, placing it back into current_player.hand. If so, appends the Black 3s into current_player.black_3_meld. # ****
            if (current_card.rank, current_card.suit) in deck.Deck().black_3s: # ****
                if len(current_player.hand) <= 1: # ****
                    current_player.black_3_meld.append(current_player.play_cards.pop(current_player.play_cards.index(current_card))) # ****
                else: # ****
                    play_cards_removed_black_3s.append(current_player.play_cards.pop(current_player.play_cards.index(current_card))) # ****
            # -------------------------------------
            # Below Section - If card is a Wild Card; appends it to play_cards_wild_cards, popping it from current_player.play_cards, for the purpose of segregation so that later on when meld lengths are determined, they are not convoluted by having individual wild cards mixed in. # ****
            elif (current_card.rank, current_card.suit) in deck.Deck().wild_cards: # ****
                current_player.play_cards_wild_cards.append(current_player.play_cards.pop(current_player.play_cards.index(current_card))) # ****
            # -------------------------------------
            # Below Section - If card is a valid, non-wild card that is the first of it's rank iterated through in the group of play cards. Creates a new temp_meld for it to be placed into, and the temp_meld is then placed back into current_player.play_cards, which is where other cards of the same rank will be placed. # ****
            elif current_card.rank not in play_cards_new_ranks: # ****
                play_cards_new_ranks.append(current_card.rank) # ****
                temp_meld = [] # ****
                temp_meld.append(current_player.play_cards.pop(current_player.play_cards.index(current_card))) # ****
                current_player.play_cards.append(temp_meld) # ****
            # -------------------------------------
            # Below Section - If card's rank exists in play_cards_new_ranks. Sorts the card into the temp_meld that matches the card's rank. For grouping cards of the same rank together. # ****
            elif current_card.rank in play_cards_new_ranks: # ****
                for item in current_player.play_cards: # ****
                    if type(item) == list: # ****
                        if current_card.rank == item[0].rank: # ****
                            item.append(current_player.play_cards.pop(current_player.play_cards.index(current_card))) # ****
        # -------------------------------------
    # -------------------------------------
    # Below Section - Handles temp_melds that are too small or that require a wild card to be able to meet the 3 card minimum requirement. If the melds consist of only 1 card, they are appended to bad_len_temp_melds_list_print for later output and removal from current_player.play_cards back into current_player.hand, and the melds that require a wild card (consisting of 2 cards) are put in len_2_temp_melds_list, given that there is at least one card in play_cards_wild_cards so that the player can later choose which meld he would like to add the wild card(s) to. If there is nothing in play_cards_wild_cards, those melds are also added to bad_len_temp_melds_list_print for later removal back into the current_player.hand. # ****
    for temp_meld in current_player.play_cards[:]: # ****
        if type(temp_meld) != card.Card:
            if len(temp_meld) < 2: # ****
                bad_len_temp_melds_list_print.append(current_player.play_cards.pop(current_player.play_cards.index(temp_meld))) # ****
            elif len(temp_meld) == 2: # ****
                if len(current_player.play_cards_wild_cards) < 1: # ****
                    bad_len_temp_melds_list_print.append(current_player.play_cards.pop(current_player.play_cards.index(temp_meld))) # ****
                else: # ****
                    current_player.len_2_temp_melds_list.append(current_player.play_cards.pop(current_player.play_cards.index(temp_meld))) # ****
        else:
            # Below Line - Quite sure I added this for debugging purposes only.
            logger.debug(f"{temp_meld} is in the list of play_cards after all sorting, which means somewhere the code is wrong. Only melds should be here, no single cards: melds of one card should exist, but not single cards outside of a meld. If this is showing, a Card type is the object being handled.")
    # -------------------------------------
    # Below Section - For adding available played wild cards to melds consisting of 2 cards (len_2_temp_melds_list) so that they will meet the 3 card minimum requirement. # ****
    while len(current_player.len_2_temp_melds_list) > 0: # ****
        if len(current_player.play_cards_wild_cards) > 0: # ****
            game.game.progression_text = (f"{current_player.name}, at least one of your attempted play card melds have only 2 cards in them. 3 cards are required for a valid meld, so you must add a wild card to them for them to remain in play. It looks as if you have {len(current_player.play_cards_wild_cards)} wild card(s) in your set of play cards to use for this. Would you like to do this?") # ****
            game.game.multiple_choice_text_1 = 'Yes'
            game.game.multiple_choice_text_2 = 'No'
            game.game.multiple_choice_active = True
            while game.game.multiple_choice_active == True:
                game.game.draw_window_main()
            if game.game.selected_choice == 'Yes':
                if len(current_player.len_2_temp_melds_list) > 1:
                    clicked_len_2_meld = False
                    while clicked_len_2_meld == False:
                        game.game.progression_text = 'Click the meld that you would like to add the wild card to.'
                        game.game.click_card_active = True
                        while game.game.click_card_active == True:
                            game.game.draw_window_main()
                        for meld in current_player.len_2_temp_melds_list:
                            if game.game.clicked_card in meld:
                                clicked_len_2_meld = True
                                len_2_temp_meld_choice = meld
                            else:
                                game.game.progression_text = 'You clicked a meld with more than 2 cards. You must choose one of the melds with only 2 cards.'
                                game.game.xs_display(1)
                else:
                    len_2_temp_meld_choice = current_player.len_2_temp_melds_list[0]
                if len(current_player.play_cards_wild_cards) > 1:
                    clicked_wild_card = False
                    while clicked_wild_card == False:
                        game.game.progression_text = 'Click the wild card that you would like to use.'
                        game.game.click_card_active = True
                        while game.game.click_card_active == True:
                            game.game.draw_window_main()
                        if (game.game.clicked_card.rank, game.game.clicked_card.suit) in deck.MasterDeck.wild_cards:
                            clicked_wild_card = True
                            wild_card_choice = game.game.clicked_card
                else:
                    wild_card_choice = current_player.play_cards_wild_cards[0]
                game.game.progression_text = (f"You successfully added the {wild_card_choice} to your meld.") # ****
                current_player.len_2_temp_melds_list[len_2_temp_meld_choice].append(current_player.play_cards_wild_cards.pop(wild_card_choice)) # ****
                current_player.play_cards.append(current_player.len_2_temp_melds_list.pop(len_2_temp_meld_choice)) # ****
        # -------------------------------------
            # Below Section - If the player chooses not to use the available wild card(s); places the len_2_temp_melds_list melds into bad_len_temp_melds_list_print, leaving the wild cards in play cards to be handled by wild_card_handler(). # ****
            else: # ****
                game.game.progression_text = ("Okay, the meld(s) will be put back into your hand.") # ****
                game.game.xs_display(1)
                for temp_meld in current_player.len_2_temp_melds_list[:]: # ****
                    bad_len_temp_melds_list_print.append(current_player.len_2_temp_melds_list.pop(current_player.len_2_temp_melds_list.index(temp_meld))) # ****
            # -------------------------------------
        # Below Section - If player does not have any wild cards left to use for appending to the short melds. Appends the melds to bad_len_temp_melds_list_print for placement back into the current_player.hand # ****
        elif len(current_player.play_cards_wild_cards) == 0: # ****
            for temp_meld in current_player.len_2_temp_melds_list[:]: # ****
                bad_len_temp_melds_list_print.append(current_player.len_2_temp_melds_list.pop(current_player.len_2_temp_melds_list.index(temp_meld))) # ****
        # -------------------------------------
    # Below  Section - Handles the informative output for melds of bad length & removal of said melds back into the current_player.hand. # ****
    if len(bad_len_temp_melds_list_print) > 0: # ****
        game.game.progression_text = (f"{current_player.name}, you have some attemped melds that do not pass the rule requirements. You cannot create a new meld without at least 2 natural cards of the same rank, or without a wild card to add to it to reach the 3 card minimum meld requirement. The attempted meld(s) will be removed and placed back in your hand.") # ****
        game.game.xs_display(3)
        for bad_len_meld in bad_len_temp_melds_list_print[:]: # ****
            for current_card in bad_len_meld[:]: # ****
                current_player.hand.append(bad_len_meld.pop(bad_len_meld.index(current_card))) # ****
    # -------------------------------------
    # Below Section - Checks to see if current_player.play_cards_wild_cards is populated, and if so, calls wild_card_handler to distribute them. # ****
    if len(current_player.play_cards_wild_cards) > 0: # ****
        wild_card_handler(current_player) # ****
    # -------------------------------------
    # Below Section - If the player had 1 or 0 cards left in his hand for this play, then Black 3s were segregated into current_player.black_3_meld until their played cards were sorted and validated (this point). If they have a Canasta at this point, then the black_3_meld will be appended to their list of play cards, and current_player.black_3_meld will be .clear()ed. If not, the cards in the black_3_meld will be placed back into their hand. # ****
    if len(current_player.black_3_meld) >= 3:
        if current_player.has_canasta == True:
            current_player.play_cards.append(current_player.black_3_meld[:]) # ****
            current_player.black_3_meld.clear() # ****
    elif len(current_player.black_3_meld) > 0:
        game.game.progression_text = (f"Sorry, {current_player.name}, but your attempted Black 3 meld (made possible because you played them with 1 or 0 cards left in your hand) did not succeed because you must have at least 1 Canasta to be eligible for this play. Therefore, your Black 3(s) will be placed back into your hand.")
        game.game.xs_display(3)
        for current_card in current_player.black_3_meld[:]:
            current_player.hand.append(current_player.black_3_meld.pop(-1))
    # -------------------------------------
    # Below Section - Checks to see if there are any Black 3s that were removed from the play cards, and if so, informs the player of their removal. # ****
    if len(play_cards_removed_black_3s) > 0:  # ****
        game.game.progression_text = (f"Sorry, {current_player.name}, but you cannot play Black 3s unless you are going out during this play and have a preexisiting Canasta. The Black 3s will be placed back into your hand.") # ****
        game.game.xs_display(2)
        for current_card in play_cards_removed_black_3s[:]: # ****
            current_player.hand.append(play_cards_removed_black_3s.pop(play_cards_removed_black_3s.index(current_card))) # ****
    # -------------------------------------
    # Below Section - Checks to ensure that after all the sorting and validation the player's melds meet their minimum meld requirement score, in the case that they have no established melds/have not already met the meld requirement. If, so, cards are kept in current_player.play_cards, but if not, they are transferred back into current_player.hand. # ****
    if len(current_player.melds) == 0:
        if current_player.round_score < current_player.meld_requirement: # ****
            if len(current_player.play_cards) > 0:
                game.game.progression_text = (f"Sorry, {current_player.name}, but the value of your play cards: ({current_player.round_score}) - after filtering and sorting your attempted melds is not enough to meet the minimum meld requirement of {current_player.meld_requirement}. Your play cards will be placed back into your hand and you will be redirected to make another play attempt.") # ****
                game.game.xs_display(3)
            else:
                game.game.progression_text = (f"Sorry, {current_player.name}, none of your attempted melds were valid after filtering and sorting them. Your play cards will be placed back into your hand and you will be redirected to discard or make another play attempt.") # ****
                game.game.xs_display(3)
            # -------------------------------------
            for meld in current_player.play_cards[:]: # ****
                for current_card in meld[:]: # ****
                    current_player.hand.append(meld.pop(-1)) # ****
            current_player.play_cards.clear() # ****
            # -------------------------------------
            return play_2(current_player) # ****
            # -------------------------------------
        else:
            game.game.progression_text = (f"You succeeded in meeting your minimum meld score requirement of {current_player.meld_requirement}!")
            game.game.xs_display(2)
    # -------------------------------------
    # Below Section - Transfers the played cards to current_player.melds (granted there were successfully played cards), and directs the player to either went_out_check() or discard() depending on the amount of cards in the player's hand. If no cards were played, prints an informative message, and reroutes the player to make a new play attempt via play_2(). # ****
    if len(current_player.play_cards) > 0: # ****
        game.game.progression_text = (f"{current_player.name}, you successfully created the meld(s) below!") # ****
        game.game.xs_display(1)
        # -------------------------------------
    for temp_meld in current_player.play_cards[:]: # ****
        current_player.melds.append(current_player.play_cards.pop(current_player.play_cards.index(temp_meld))) # ****
        # -------------------------------------
    # Below Section - Creates 2 variables, total_melds_len & total_initial_played_cards_len, with values of 0, then gets the sum of all meld lens in current_player.melds & current_player.initial_played_cards, then compares them to one another to determine if any cards were successfully played during the current play.
    total_melds_len = 0
    total_initial_played_cards_len = 0
    for meld in current_player.melds:
        total_melds_len += len(meld)
    for meld in current_player.initial_played_cards:
        total_initial_played_cards_len += len(meld)
    if total_initial_played_cards_len == total_melds_len: # ****
        game.game.progression_text = ("It looks as if you were unable to succeed in playing any of your attempted play cards. Therefore you will have to choose another set of play cards, or opt to discard instead if you have no valid plays to make.") # ****
        game.game.xs_display(2)
        play_2(current_player) # ****
    else: # ****
        logger.debug("total_initial_played_cards_len != total_melds_len\n") # ****
        current_player.final_played_cards = 1
    # -------------------------------------
        if len(current_player.hand) <= 1: # ****
            went_out_check(current_player) # ****
        else: # ****
            discard(current_player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below - Called by valid_play_check_and_sort() function. Handles all played wild cards (after len_2_temp_melds_list sorting and placement of played wild cards), prompting the player to determine their placement. Also determines whether or not a Wild Card Canasta is being played. Any unplayed wild cards are placed back into the player's hand. # ****
def wild_card_handler(current_player): # ****
    print('wild_card_handler')
    logger.debug("wild_card_handler") # ****
    # Below Section - In the case that player plays 7 or more wild cards, checks via prompt to see if player is trying to play a Wild Card Canasta. # ****
    if len(current_player.play_cards_wild_cards) >= 7: # ****
        game.game.multiple_choice_text_1 = 'Yes'
        game.game.multiple_choice_text_1 = 'No'
        game.game.multiple_choice_active = True
        while game.game.multiple_choice_active == True: # ****
            game.game.progression_text = (f"{current_player.name}, are you trying to play a Wild Card Canasta?") # ****
        if game.game.selected_choice == 'Yes': # ****
    # ------------------------------------- ****
            # Below Section - Checks if the amount of wild cards in current_player.play_cards_wild_cards is exactly 7 cards, in which case the entire list will be appended to current_player.play_cards, then current_player.play_cards_wild_cards will be cleared. Finally, returns None. # ****
            if len(current_player.play_cards_wild_cards) == 7: # ****
                game.game.progression_text = (f"{current_player.name}, you successfully played a Wild Card Canasta! Congratulations!") # ****
                current_player.play_cards.append(current_player.play_cards_wild_cards[:]) # ****
                current_player.play_cards_wild_cards.clear() # ****
                return None
            # ------------------------------------- ****
            # Below Section - If the amount of wild cards being played is greater than 7; player is prompted to choose which wild cards they want to use in the canasta. The non-chosen wild cards will remain in play to be distributed later in the function, unless this is the player's first meld. In this case, appends left over wild cards back into current_player.hand, and returns None. # ****
            else: # ****
                game.game.progression_text = (f"{current_player.name}, choose 7 wild cards that you want to use for your Wild Card Canasta.") # ****
                game.game.click_card_active = True
                game.game.choose_multiple_cards = True
                game.game.multiple_choice_text_1 = 'Done Selecting'
                game.game.multiple_choice_active = True
                clicked_7_cards = False
                while clicked_7_cards == False:
                    while game.game.multiple_choice_active == True:
                        game.game.draw_window_main()
                    if len(game.game.clicked_card_list) == 7:
                        clicked_7_cards = True
                    else:
                        game.game.progression_text = (f"Sorry, but you chose less than 7 wild cards. You must play an entire 7 card Canasta when playing a Wild Card Canasta.") # ****
                        game.game.xs_display(2)
                for current_card in game.game.clicked_card_list[:]:
                    current_player.play_cards.append(current_card)
                if current_player.round_score < current_player.meld_requirement: # ****
                    game.game.progression_text = (f"{current_player.name}, since you only have the Wild Card Canasta in your available melds and extra wild cards left over, they will be placed back into your hand as there is currently no other place to put them.") # ****
                    game.game.xs_display(1)
                    for wild_card in current_player.play_cards_wild_cards[:]: # ****
                        current_player.hand.append(current_player.play_cards_wild_cards.pop(-1)) # ****
                    return None # ****
            # ------------------------------------- ****
    # Below Section - Runs if the player has less than 7 wild cards in current_player.play_cards_wild_cards OR if they have/had 7 or more wild cards but chose not to create a wild card canasta/had leftover wild cards after creating a wild card canasta with them, and if the player has at least 1 meld in current_player.play_cards or current_player.melds that does not contain the max amount of wild cards; iterates through each wild card in current_player.play_cards_wild_cards and prompts the player to choose a destination for each card. # ****
    if len(current_player.play_cards) > 0 or len(current_player.melds) > 0: # ****
        for wild_card in current_player.play_cards_wild_cards[:]: # ****
            if len(current_player.non_maxed_out_melds) > 0: # ****
                meld_choice_index = wild_card_meld_choice_prompt(current_player, wild_card) # ****
    # -------------------------------------
                # Below Section - If player chooses not to use the wild card, it is popped from play_cards_wild_cards and appended back into the player's hand. # ****
                if meld_choice_index == game.game.multiple_choice_text_1: # ****
                    game.game.progression_text = ("Okay, the wild card will be placed back into your hand.") # ****
                    game.game.xs_display(1)
                    current_player.hand.append(current_player.play_cards_wild_cards.pop(current_player.play_cards_wild_cards.index(wild_card))) # ****
                # -------------------------------------
                # Below Section - If player chooses to place the wild card into a meld; determines which meld group (current_player.play_cards or current_player.melds) they chose, and appends the wild card to that meld, popping it from play_cards_wild_cards. # ****
                elif current_player.non_maxed_out_melds[meld_choice_index] in current_player.play_cards: # ****
                    game.game.progression_text = (f"{current_player.name}, you successfully added the {current_player.play_cards_wild_cards[current_player.play_cards_wild_cards.index(wild_card)]} to your meld.") # ****
                    current_player.play_cards[current_player.play_cards.index(current_player.non_maxed_out_melds[meld_choice_index])].append(current_player.play_cards_wild_cards.pop(current_player.play_cards_wild_cards.index(wild_card))) # ****
                    game.game.xs_display(1)
                elif current_player.non_maxed_out_melds[meld_choice_index] in current_player.melds: # ****
                    game.game.progression_text = (f"{current_player.name}, you successfully added the {current_player.play_cards_wild_cards[current_player.play_cards_wild_cards.index(wild_card)]} to your meld.") # ****
                    current_player.melds[current_player.melds.index(current_player.non_maxed_out_melds[meld_choice_index])].append(current_player.play_cards_wild_cards.pop(current_player.play_cards_wild_cards.index(wild_card))) # ****
                    game.game.xs_display(1)
                # -------------------------------------
            # Below Section - For the case whenever the player has nowhere to place the wild card. Places all of the remaining wild cards back into the player's hand after an informative message. # ****
            else: # ****
                game.game.progression_text = (f"{current_player.name}, it looks as if every meld in your play cards and/or in your melds have the maximum amount of wild cards possible. Therefore the remaining wild cards in play will be placed back into your hand.") # ****
                game.game.xs_display(1)
                for wild_card in current_player.play_cards_wild_cards[:]: # ****
                    current_player.hand.append(current_player.play_cards_wild_cards.pop(-1)) # ****
                return None # ****
            # ------------------------------------- # ****
    # Below Section - If a player who has no melds in play_card melds or current_player.meld tried to play some wild cards. Since there is nowhere to put them, places the cards back into the player's hand. # ****
    else: # ****
        game.game.progression_text = (f"It looks as if you have some wild cards leftover in your group of play cards, {current_player.name}, but there is nowhere to place them, since you have no existing melds. The cards will be placed back into your hand.") # ****
        game.game.xs_display(3)
        for wild_card in current_player.play_cards_wild_cards[:]: # ****
            current_player.hand.append(current_player.play_cards_wild_cards.pop(-1)) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by wild_card_handler() function. Prompts the player to choose a meld to add the wild_card to, or to opt to not use the wild card at all in this manner. Returns the choice. # ****
def wild_card_meld_choice_prompt(current_player, wild_card): # ****
    print('wild_card_meld_choice_prompt')
    logger.debug("wild_card_meld_choice_prompt")
    game.game.progression_text = (f"{current_player.name}, which meld from your play cards or your melds would you like to add the {current_player.play_cards_wild_cards[current_player.play_cards_wild_cards.index(wild_card)]} to? Click any meld to choose it.") # ****
    game.game.multiple_choice_text_1 = 'I would not like to use this wild card, and would rather have it be replaced back into my hand.'
    game.game.click_card_active = True
    game.game.multiple_choice_active = True
    while game.game.click_card_active == True:
        game.game.draw_window_main()
    if game.game.clicked_card == None:
        print('wild_card_meld_choice_prompt - game.game.clicked_card == None')
        meld_choice_index = game.game.multiple_choice_text_1
    else:
        if len(current_player.play_cards) > 0:
            for meld in current_player.play_cards:
                if game.game.clicked_card in meld:
                    print('wild_card_meld_choice_prompt - game.game.clicked_card in play_cards')
                    meld_choice_index = game.game.clicked_card
        if len(current_player.melds) > 0:
            for meld in current_player.melds:
                if game.game.clicked_card in meld:
                    print('wild_card_meld_choice_prompt - game.game.clicked_card in melds')
                    meld_choice_index = game.game.clicked_card
    return meld_choice_index # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by play_2(), valid_play_check_and_sort(), went_out_check() functions. For discarding; prompts the player to choose a card from their hand to be placed into the discard pile. # ****
def discard(current_player): # ****
    print('discard')
    logger.debug("discard\n") # ****
    # -------------------------------------
    game.game.clickable_card_list = current_player.hand[:]
    game.game.progression_text = f'{current_player.name}, which card would you like to discard? Click the card of your choice.' # ****
    game.game.click_card_active = True
    while game.game.click_card_active == True:
        game.game.draw_window_main()
    game.game.progression_text = f'{current_player.name}, you discarded the {game.game.clicked_card}!'
    deck.MasterDeck.discard_pile.append(current_player.hand.pop(current_player.hand.index(game.game.clicked_card))) # ****
    # -------------------------------------
    if len(current_player.hand) == 0: # ****
        went_out_check(current_player) # ****
    else:
        if current_player == player.P1: # ****
            play_1(player.P2) # ****
        else: # ****
            play_1(player.P1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by valid_play_check_and_sort(), discard() functions. Checks to see if player is eligible to go out, and whether or not they went out during their last turn. If they are not trying to go out, redirects to beginning of the player turn loop via play_1() function. If so, ends round via round_reset(). # ****
def went_out_check(current_player, going_out_from_discard_draw = False): # ****
    print('went_out_check')
    logger.debug("went out check\n") # ****
    # -------------------------------------
    if current_player.has_canasta == True: # ****
        current_player.going_out = True # ****
        if going_out_from_discard_draw == False:
            if len(current_player.initial_played_cards) == 0: # ****
                current_player.went_out_concealed = True # ****
                # -------------------------------------
        else:
            if len(current_player.final_played_cards) == 0:
                current_player.went_out_concealed = True # ****
                # -------------------------------------
        if current_player == player.P1: # ****
            P2.going_out = False # ****
            game.game.progression_text = f'{player.P1.name}, you successfully went out!'
            game.game.xs_display(2)
            game.game.progression_text = f'Round Score: {player.P1.name}: {player.P1.round_score} {player.P2.name}: {player.P2.round_score}' # ****
            game.game.xs_display(3)
        else: # ****
            player.P1.going_out = False # ****
            game.game.progression_text = f'{player.P2.name}, you successfully went out!'
            game.game.xs_display(2)
            game.game.progression_text = f'Round Score: {player.P2.name}: {player.P2.round_score} {player.P1.name}: {player.P1.round_score}' # ****
            game.game.xs_display(3)
            # -------------------------------------
        round_reset() # ****
        # -------------------------------------
    # Below Extended Section - In the case that a player is attempting to go out (has 0 cards in their hand) but does not have the required canasta to do so. Gives the player an informative message and prompts them to choose 2 cards to take back into their hand from the available melds to use as a discard and a required card to be kept in their hand. # ****
    else: # ****
        # Below Section - Checks current_player.melds against current_player.initial_played_cards to create a list of each card that was just played and its associated meld. # ****
        for meld_index in range(len(current_player.melds)): # ****
            # Below Line - Checks for melds that were preexisting before current play. # ****
            if (meld_index + 1) <= len(current_player.initial_played_cards):
                if len(current_player.melds[meld_index]) > len(current_player.initial_played_cards[meld_index]): # ****
                    meld_len_difference = len(current_player.melds[meld_index]) - len(current_player.initial_played_cards[meld_index]) # ****
                    for current_card in current_player.melds[meld_index][-meld_len_difference:]: # ****
                        current_player.last_set_played_cards.append([current_card, current_player.melds[meld_index]]) # ****
            # Below Line - For melds that were created during current play. # ****
            else: # ****
                for current_card in current_player.melds[meld_index]: # ****
                    current_player.last_set_played_cards.append([current_card, current_player.melds[meld_index]]) # ****
        # -------------------------------------
        ###### Below Section - DO I HAVE TO USE COPY HERE? WOULD IT NOT JUST REFERENCE THE CURRENT VALUE AND NOT BE AFFECTED BY LATER CHANGES TO WHERE IT IS COPIED FROM??? Creates a variable prior_hand_len to reference the len(current_player.hand) before running went_out_check_replacement_card() so that it can be determined whether or not the function needs to be run twice instead of once for the instance in which only one card was removed from a meld, as opposed to multiple cards being removed from a meld due to entire meld disbandment, resulting in the 2 card replacement requirement having already been met with a single function call. Finally, clears current_player.last_set_played_cards so that the next time this is called it does not have the previous set of played cards included. # ****
        prior_hand_len = copy.copy(len(current_player.hand))
        went_out_check_replacement_card(current_player) # ****
        if len(current_player.hand) < 2:
            went_out_check_replacement_card(current_player, True) # ****
        current_player.last_set_played_cards.clear()
        # -------------------------------------
        # Below Section - Checks to ensure that after alteration of existing melds the player still reaches their meld requirement. If not, gives the player an informative message, replaces all of the cards in their melds back into their hand, and reroutes them back to a new play attempt. If so, directs the player to discard. # ****
        if current_player.round_score < current_player.meld_requirement: # ****
            game.game.progression_text = ("It looks as if you no longer reach the meld reqiurement after making the replacements. Therefore all cards have been placed back into your hand from your melds and you will be redirected to make another play attempt.") # ****
            game.game.xs_display(3)
            for meld in current_player.melds[:]: # ****
                for current_card in meld[:]: # ****
                    current_player.hand.append(meld.pop(-1)) # ****
            current_player.melds.clear() # ****
            return play_2(current_player) # ****
        else: # ****
            return discard(current_player) # ****
    # -------------------------------------
    if current_player == player.P1: # ****
        return play_1(player.P2) # ****
    else: # ****
        return play_1(player.P1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by went_out_check() function. Prompts the player to choose which card they would like to place back into their hand from the available melds. Determines whether or not the card's removal would require the associated meld to be disbanded. If not, places all of their melds back into their hand and redirects them back to make another play attempt. If so, redirects the player to the discard() function. # ****
def went_out_check_replacement_card(current_player, second_run = False): # ****
    print('went_out_check_replacement_card')
    logger.debug("went_out_check_replacement_card")
    if second_run == False:
        game.game.progression_text = f'{current_player.name}, it looks as if you are trying to go out without having a Canasta, which is required. Because of this you cannot go out and will have to draw back 2 of your play cards (required: 1 card in the hand, 1 for a discard). Please choose the first card you wish to take back into your hand from the highlighted cards. NOTE: In the case that a card is taken from a meld with only 3 cards, the entire meld will be disbanded and all of the meld will be replaced back into your hand. Also, if after replacing the 2 cards back into your hand you no longer meet the meld requirement, the play will be invalid and you will have to try again.'
        game.game.xs_display(3)
    else:
        game.game.progression_text = f'{current_player.name}, choose the 2nd card to be placed back in your hand (to be used either as a discard or to be kept in the hand) from among the highlighted cards.'
        game.game.xs_display(2)
    for current_card in current_player.last_set_played_cards:
        current_card.highlighted = True
    game.game.click_card_active = True
    clicked_highlighted_card = False
    while clicked_highlighted_card == False:
        while game.game.click_card_active == True:
            game.game.draw_window_main()
        if game.game.clicked_card in current_player.last_set_played_cards:
            clicked_highlighted_card = True
            for meld in current_player.melds:
                if game.game.clicked_card in meld:
                    clicked_card_meld_index = meld.meld_num
                    clicked_card_index = meld.index(game.game.clicked_card)
                    if len(meld) > 3:
                        # Below Line - Appends the chosen card to the current_player.hand, popping from current_player.meld. # ****
                        current_player.hand.append(current_player.melds[clicked_card_meld_index].pop(clicked_card_index)) # ****
                        game.game.progression_text = (f"You removed the {game.game.clicked_card} from it's meld back into your hand.") # ****
                        game.game.xs_display(1)
                    else: # ****
                        # Below Section - Checks to see if the player has any melds with more than 3 cards in them, since they chose to disband a meld of 3 or less cards. If they do have one of these melds, presents the player with an informative message and asks for verification of their choice. # ****
                        melds_len_over_3 = False # ****
                        for card_and_meld in current_player.last_set_played_cards: # ****
                            if len(card_and_meld[1]) > 3: # ****
                                melds_len_over_3 = True # ****
                        if melds_len_over_3 == True: # ****
                            game.game.progression_text = ("This meld has 3 cards, which means the entire meld would have to be disbanded if you were to remove this card. It looks like you have a meld in your list of choices that has more than 3 cards, which means it would not have to be completely disbanded. Are you sure that you want to disband this meld instead?") # ****
                            game.game.multiple_choice_text_1 = 'Yes'
                            game.game.multiple_choice_text_1 = 'No'
                            game.game.multiple_choice_active = True
                            while game.game.multiple_choice_active == True:
                                game.game.draw_window_main()
                            if game.game.selected_choice == 'Yes': # ****
                                game.game.progression_text = ("Okay, the meld will be disbanded and placed back into your hand.") # ****
                                game.game.xs_display(1)
                                for current_card in current_player.melds[clicked_card_meld_index][:]: # ****
                                    current_player.hand.append(current_player.melds[clicked_card_meld_index].pop(-1)) # ****
                                # Below Line - Pops the emptied meld from current_player.melds.
                                current_player.melds.pop(current_player.melds.index(clicked_card_meld_index))
                        else:
                            game.game.progression_text = 'Since this meld consists of 3 cards, the entire meld will be disbanded.'
                            game.game.xs_display(1)
                            for current_card in current_player.melds[clicked_card_meld_index][:]: # ****
                                current_player.hand.append(current_player.melds[clicked_card_meld_index].pop(-1)) # ****
                                # Below Line - Pops the emptied meld from current_player.melds.
                                current_player.melds.pop(current_player.melds.index(clicked_card_meld_index))
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by draw_discard_pile_attempt(), draw_discard_pile_attempt_check_meld_match(), went_out_check() functions. Resets all settable attributes and values back to default/starting conditions to start a new round. Also displays an informative output showing the players' scores, and who won the round. # ****
def round_reset(): # ****
    print('round_reset')
    logger.debug("round_reset")
    for current_player in (player.P1, player.P2): # ****
        current_player.finished_rounds_scores.append(current_player.round_score) # ****
        current_player.draw_card = None # ****
        current_player.hand.clear() # ****
        current_player.play_cards.clear() # ****
        current_player.play_cards_wild_cards.clear() # ****
        current_player.initial_played_cards.clear() # ****
        current_player.final_played_cards = 0
        current_player.last_set_played_cards.clear() # ****
        current_player.red_3_meld.clear() # ****
        current_player.black_3_meld.clear() # ****
        current_player.melds.clear() # ****
        current_player.len_2_temp_melds_list.clear() # ****
        current_player.matched_card_list.clear() # ****
        current_player.going_out = None # ****
        current_player.went_out_concealed = False # ****
        current_player.total_score_over_5000 = False
        current_player.special_case_cant_draw = False
    # --------------------------------------
    game.game.progression_text = (f"The round is over! {player.P1.name}'s final round score was {player.P1.finished_rounds_scores[-1]}, and {player.P2.name}'s final round score was {player.P2.finished_rounds_scores[-1]}.")
    game.game.xs_display(3)
    if player.P1.finished_rounds_scores[-1] > player.P2.finished_rounds_scores[-1]:
        game.game.progression_text = (f"{player.P1.name} was the winner of the round!")
        game.game.xs_display(1)
    elif player.P1.finished_rounds_scores[-1] == player.P2.finished_rounds_scores[-1]:
        game.game.progression_text = (f"Both players had the same score! The round was a tie!")
        game.game.xs_display(1)
    elif player.P2.finished_rounds_scores[-1] > player.P1.finished_rounds_scores[-1]:
        game.game.progression_text = (f"{player.P2.name} was the winner of the round!")
        game.game.xs_display(1)
    # --------------------------------------
    deck.MasterDeck.discard_pile.clear()
    deck.MasterDeck.deck.clear()
    deck.MasterDeck.deck = deck.MasterDeck.original_deck[:]
    # --------------------------------------
    win_check() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by round_reset() function. Checks a winning value (5000) against each player's score to determine whether or not someone has won. If so, calls check_total_score_winner() function to determine the winner. If not, begins a new round via the_draw_1() function. # ****
def win_check(): # ****
    print('win_check')
    logger.debug("win_check") # ****
    for current_player in (player.P1, player.P2): # ****
        other_player = None
        if current_player == player.P1:
            other_player = player.P2
        else:
            other_player = player.P1
        if current_player.total_score >= 5000: # ****
            return check_total_score_winner(current_player, other_player)
     # -------------------------------------
    # Below Line - In the case that nobody has won yet, restarts a new round. # ****
    the_draw_1() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by win_check() function. In the case that one player has reached 5000 points, checks player & other_player's player.total_score to determine the input for the winner_output() function. If the players have an equal score, (current_player, True) is passed into winner_output() function so that the tie game output is processed. Otherwise, the winning player is passed in; either player or other_player.
def check_total_score_winner(current_player, other_player):
    print('check_total_score_winner')
    if current_player.total_score > other_player.total_score: # ****
        return winner_output(current_player) # ****
    elif current_player.total_score == other_player.total_score: # ****
        winner_output(current_player, True) # ****
    elif current_player.total_score < other_player.total_score: # ****
        return winner_output(other_player) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by win_check() function. Prints outputs for the winner (unless it was a draw) and a game summary including all of the players' round scores. Also prompts the user on whether or not they would like to play again. # ****
def winner_output(current_player, tie_game = False): # ****
    print('winner_output')
    logger.debug("winner_output") # ****
    if tie_game == False: # ****
        game.game.progression_text = (f"Congratulations, {current_player.name}, you are the winner! You are the champion, my friend!!") # ****
        game.game.xs_display(3)
    else: # ****
        game.game.progression_text = ("You both had the same score over 5,000 which means it is a tie game!") # ****
        game.game.xs_display(3)
    # -------------------------------------
    ###### Below Section - Have to figure out how to fix this so that it displays the text on multiple lines without using \n, as that does not work in the 2D output version.
    p1_game_summary_string = (f"{player.P1.name}'s Game Summary:\n\nRound Scores:\n\n" + '\n'.join(['%s']*len(current_player.finished_rounds_scores)) % tuple(current_player.finished_rounds_scores) + "\n") # ****
    p2_game_summary_string = (f"{player.P2.name}'s Game Summary:\n\nRound Scores:\n\n" + '\n'.join(['%s']*len(current_player.finished_rounds_scores)) % tuple(current_player.finished_rounds_scores) + "\n") # ****
    ###### -------------------------------------
    game.game.progression_text = ("Would you like to play again?") # ****
    game.game.multiple_choice_text_1 = 'Yes'
    game.game.multiple_choice_text_1 = 'No'
    game.game.multiple_choice_active = True
    while game.game.multiple_choice_active == True:
        game.game.draw_window_main()
    if game.game.selected_choice == 'Yes': # ****
        for current_player in (player.P1, player.P2):
            current_player.finished_rounds_scores.clear()
            if current_player == player.P1:
                current_player.name = 'Player 1'
            else:
                current_player.name = 'Player 2'
        return the_draw_1() # ****
    else: # ****
        sys.exit() # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
