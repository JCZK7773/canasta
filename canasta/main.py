import sys #
import random # ****
import copy
import pygame
import os
import time
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import game
import card
import locations
import deck
import player
import customappendlist
import progression
import test_run
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - For the purpose of testing. Is used to store the cards passed through sorted_and_numbered_list_printer so that they can be tested to ensure they are in the proper ascending order according to card rank/suit combination value.
testing_register_list = []
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def setup():
    # print("setup")
    progression.logger.debug("setup\n") # ****
    # Below Line - Loads the Card class's self.face_down_image (one time, instead of many, as they all use this same image), which must be called here because it requires pygame.display to be initiated.
    card.Card.assign_face_down_image()
    # Below Section - Assigns the MasterDeck.deck & .discard_pile to both be instances of CustomAppendList so that they will handle card location updates whenever cards are appended to the lists.
    deck.MasterDeck.deck = customappendlist.CustomAppendList('deck')
    deck.MasterDeck.discard_pile = customappendlist.CustomAppendList('discard_pile')
    # -------------------------------------
    # Below Section - Creates the actual decks via class method create_deck.
    deck.MasterDeck.create_double_deck() # ****
    # -------------------------------------
    # Below Section - Shuffles the MasterDeck & assigns MasterDeck.original_deck == the newly created doubledeck MasterDeck.deck.
    random.shuffle(deck.MasterDeck.deck) # ****
    deck.MasterDeck.original_deck = copy.copy(deck.MasterDeck.deck[:])
    # -------------------------------------
    # Below Section - Sets up the display_layer for all of the cards in the deck, ordering them least to greatest, for proper visuals.
    display_layer = 0
    for current_card in deck.MasterDeck.deck:
        current_card.display_layer = display_layer + 1
        display_layer += 1
    # -------------------------------------
    # Below Section - Assigns each player's card groups that will be visually displayed on the pygame screen to be an instance of CustomAppendList, giving each a name associated with the card group name to be used for when cards are appended to these card groups. The dictionary func_dict has the names as the keys , and a function name which updates the card coordinates of the appended card group is the dict value, so that whenever a card is appended to one of these groups, through a modified append method, the function is called before the card is appended to the card group, for the purpose of automation and simplicity.
    player.P1.hand = customappendlist.CustomAppendList('P1.hand') # ****
    player.P2.hand = customappendlist.CustomAppendList('P2.hand') # ****
    player.P1.pre_sort_play_cards = customappendlist.CustomAppendList('P1.pre_sort_play_cards')
    player.P2.pre_sort_play_cards = customappendlist.CustomAppendList('P2.pre_sort_play_cards')
    player.P1.play_cards = customappendlist.CustomAppendList('P1.play_cards') # ****
    player.P2.play_cards = customappendlist.CustomAppendList('P2.play_cards') # ****
    player.P1.red_3_meld = customappendlist.CustomAppendList('P1.red_3_meld') # ****
    player.P2.red_3_meld = customappendlist.CustomAppendList('P2.red_3_meld') # ****
    player.P1.melds = customappendlist.CustomAppendList('P1.melds') # ***
    player.P2.melds = customappendlist.CustomAppendList('P2.melds') # ***
    player.P1.matched_card_list = customappendlist.CustomAppendList('P1.melds')
    player.P2.matched_card_list = customappendlist.CustomAppendList('P2.melds')
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by module when opened, if __name__ == "__main__". The main pygame loop. Handles FPS and calls draw_window() for screen updating.
def main():
    # print("main")
    progression.logger.debug("main\n") # ****
    # -------------------------------------
    # Below Section - Sets up the run loop so that unless the player quits the game/exits the window, it continues to cycle through this progression loop.
    setup()
    # test_run.test_run()
    progression.the_draw_1()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
