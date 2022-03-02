# DEBUG
    # Error code goes here in this section; for debugging.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NOTES
    # - Devlog -
        # 02/01/22 - 02/07/22 : Completed implementation of the first pass of the card movement system by creating various methods, each associated with one of the various card lists, inside of the Locate instance which are to be called by CustomAppendList whenever they are appended to. Needs to be tested to work out bugs.
        # 02/08/22 : Began conversion of text-based inputs to be text display rects on the game screen. Continued working on ideas for card movements.
        # 02/09/22 - 02/17/22 : Put off converting text inputs after implementing the very first steps for the feature, and refocused on implementing card movements. Eventually implemented a successful card movement system, with some minor bugs in visual card overlap and game lag. Worked out all of the existing bugs from the card movement implementation and began working on reducing game lag via .convert() & using Dirty Sprites.
        # 02/18/22 : Tidied up some code, updated devlog, added in missing section commentary, and changed card movement values from 1 to 0.5 to (hopefully) help smooth the movements.
        # 02/19/22 - 02/27/22 : Divided up all of the code into various different files so that they are more easily organized and readable. Worked out bugs from that change. Fixed red 3 meld, mostly, which was broken.
        # 02/28/22: Fixed some card movement bugs including the issue with the red 3 meld, and almost fixed the issues of cards appearing in the top left corner of the screen. Spent a lot of time pinpointing the issue, which apparently lies in card.rect & card.rect.center initial assignments. Fixed the bug where the cards were staying rendered in the top left corner of the display.
        # 02/29/22: ...
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# THINGS TO DO
    # 1) Improve visual layout for play_cards.
    # 2) Test & improve card movement system for smoothness / timing until satisfactory.
    # 3) Convert inputs to text rects on display.
    # 4) Fix main game loop so that it will properly run through game progression loops while maintaining proper display outputs.
    # 5) Change input system from keyboard-based to mouse-based.
    # 6) Add in card sounds & background music.
    # 7) Move card creation, card ranks, card suits, and other attributes more properly associated with the Card class, into the Card class code base instead of being inside of the Deck class.
    # 8) Post on web so others can check for bugs as well.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import sys # ****
import logging # ****
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
# import progression - Have to change all of the references of players, decks, cards, etc to be accessed through their source location instead of directly since I divided up the files. Disabled for convenience until I am sure the rest of the file works properly.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Logger setup. # ****
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s" # ****
logging.basicConfig(filename = "J:\\Programming\\Projects\\Canasta\\canasta\\Canasta_log.log", level = logging.DEBUG, format = LOG_FORMAT, filemode = 'a') # ****
logger = logging.getLogger() # ****
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - For the purpose of testing. Is used to store the cards passed through sorted_and_numbered_list_printer so that they can be tested to ensure they are in the proper ascending order according to card rank/suit combination value.
testing_register_list = []
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def setup():
    logger.debug("setup\n") # ****
    # -------------------------------------
    # Below Section - Creates the actual decks via class method create_deck.
    deck.MasterDeck.create_deck() # ****
    deck.Deck2.create_deck() # ****
    # -------------------------------------
    # Below Section - Appends Deck2.deck to the MasterDeck.deck to create the required doubledeck.
    for card in deck.Deck2.deck: # ****
        deck.MasterDeck.deck.append(card) # ****
    # -------------------------------------
    # Below Section - Shuffles the MasterDeck & assigns MasterDeck.original_deck == the newly created doubledeck MasterDeck.deck.
    random.shuffle(deck.MasterDeck.deck) # ****
    deck.MasterDeck.original_deck = copy.copy(deck.MasterDeck.deck[:])
    # -------------------------------------
    # Below Section - Assigns each player's card groups that will be visually displayed on the pygame screen to be an instance of CustomAppendList, giving each a name associated with the card group name to be used for when cards are appended to these card groups. The dictionary func_dict has the names as the keys , and a function name which updates the card coordinates of the appended card group is the dict value, so that whenever a card is appended to one of these groups, through a modified append method, the function is called before the card is appended to the card group, for the purpose of automation and simplicity.
    player.P1.hand = deck.CustomAppendList('p1_hand') # ****
    player.P2.hand = deck.CustomAppendList('p2_hand') # ****
    player.P1.play_cards = deck.CustomAppendList('p1_play_cards') # ****
    player.P2.play_cards = deck.CustomAppendList('p2_play_cards') # ****
    player.P1.red_3_meld = deck.CustomAppendList('p1_red_3_meld') # ****
    player.P2.red_3_meld = deck.CustomAppendList('p2_red_3_meld') # ****
    player.P1.melds = deck.CustomAppendList('p1_melds') # ***
    player.P2.melds = deck.CustomAppendList('p2_melds') # ***
    # -------------------------------------
    # Below Section - Test section to verify proper movement of card-screen locations.
    # player.P2.melds.append(deck.MasterDeck.deck[0:7])
    player.P1.melds.append(deck.MasterDeck.deck[24:31])
    # player.P1.melds.append(deck.MasterDeck.deck[16:19])
    player.P2.melds.append(deck.MasterDeck.deck[16:23])
    # player.P2.melds.append(deck.MasterDeck.deck[24:29])
    # player.P2.melds.append(deck.MasterDeck.deck[30:36])
    # player.P2.melds.append(deck.MasterDeck.deck[36:41])
    # player.P2.melds.append(deck.MasterDeck.deck[42:48])
    # player.P1.red_3_meld.append(deck.MasterDeck.deck[49])
    # player.P1.red_3_meld.append(deck.MasterDeck.deck[50])
    # player.P2.red_3_meld.append(deck.MasterDeck.deck[51])
    # player.P2.red_3_meld.append(deck.MasterDeck.deck[52])
    player.P1.play_cards.append(deck.MasterDeck.deck[8:15])
    player.P2.play_cards.append(deck.MasterDeck.deck[0:7])

    player.P1.melds.append(player.P1.play_cards[0:7])
    player.P1.play_card.append(player.P1.melds[0:7])

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by module when opened, if __name__ == "__main__". The main pygame loop. Handles FPS, pygame.event handling, and calls draw_window() for screen updating.
def main():
    logger.debug("main\n") # ****
    # -------------------------------------
    # Below Section - Sets up the run loop so that unless the player quits the game/exits the window, it continues to cycle through this progression loop.
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    # -------------------------------------
        # Below Line - Handles creation, joining, and shuffling of the 2 initial decks into the finalized MasterDeck.deck, setting up of card lists to be associated with the different func_dict functions.
        setup()
        # progression.the_draw_1()
    # -------------------------------------
    # Below Section - Quits the pygame window and terminates the entire program.
    pygame.quit()
    sys.exit()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
