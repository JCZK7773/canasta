# D E B U G
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
        # 02/29/22 - 03/28/22: Made a lot of bug fixes, reworked all of the movement functions into a much smaller list of functions that take the specific lists as args, and did a lot of card movement testing. Card movement seems to be nearly at 100% success. Also, drastically reduced card movement times by fixing the game code, and rearranged some other code.
        # 03/29/22 - 04/04/22: Finished consolidating card movement functions into a smaller array of functions that take in the card group parameter instead. Finished and tested canasta sized melds to collapse visually within themselves for proper visual display, including rendering the proper face-up card dependent on whether or not the meld was natural or mixed. Finished and tested proper display_layer visual updates for canastas.
        # 04/05/22 - ...
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# THINGS TO DO
    # 1) Finish testing and modifying card movements and visual locations.
        # 1a) Change the visual_meld_group_update 'card' section to reflect the changes I made in the 'melds' section so that it also handles visual collapse for the melds that turn into canastas.
    # 2) Change progression.py so that all melds are instances of CustomAppendList & are assigned the proper card_group_names for proper visual placement.
    # 3) Improve visual layout for play_cards.
    # 4) Test & improve card movement system for smoothness / timing until satisfactory.
        # 4b) Implement delta timing frame system.
    # 5) Convert inputs to text rects on display.
    # 6) Fix main game loop so that it will properly run through game progression loops while maintaining proper display outputs.
    # 7) Change input system from keyboard-based to mouse-based.
    # 8) Add in card sounds & background music.
    # 9) Move card creation, card ranks, card suits, and other attributes more properly associated with the Card class, into the Card class code base instead of being inside of the Deck class.
    # 10) Post on web so others can check for bugs as well.
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
import customappendlist
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
    for card in deck.MasterDeck.deck:
        card.display_layer = display_layer + 1
        display_layer += 1
    # -------------------------------------
    # Below Section - Assigns each player's card groups that will be visually displayed on the pygame screen to be an instance of CustomAppendList, giving each a name associated with the card group name to be used for when cards are appended to these card groups. The dictionary func_dict has the names as the keys , and a function name which updates the card coordinates of the appended card group is the dict value, so that whenever a card is appended to one of these groups, through a modified append method, the function is called before the card is appended to the card group, for the purpose of automation and simplicity.
    player.P1.hand = customappendlist.CustomAppendList('P1.hand') # ****
    player.P2.hand = customappendlist.CustomAppendList('P2.hand') # ****
    player.P1.play_cards = customappendlist.CustomAppendList('P1.play_cards') # ****
    player.P2.play_cards = customappendlist.CustomAppendList('P2.play_cards') # ****
    player.P1.red_3_meld = customappendlist.CustomAppendList('P1.red_3_meld') # ****
    player.P2.red_3_meld = customappendlist.CustomAppendList('P2.red_3_meld') # ****
    player.P1.melds = customappendlist.CustomAppendList('P1.melds') # ***
    player.P2.melds = customappendlist.CustomAppendList('P2.melds') # ***
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_run():
    # Below Section - Test section to verify proper movement of card-screen locations.
    meld_1 = customappendlist.CustomAppendList('P1.melds')
    for card in range(10):
        meld_1.append(deck.MasterDeck.deck.pop(-1))
    player.P1.melds.append(meld_1)
    print("1")
    # # -------------------------------------
    # for card in meld_1[:]:
    #     deck.MasterDeck.deck.append(meld_1.pop(-1))
    # player.P1.melds.pop(0)
    # print("2")
    # # # -------------------------------------
    meld_2 = customappendlist.CustomAppendList('P1.melds')
    for card in range(7):
        meld_2.append(deck.MasterDeck.deck.pop(-1))
    player.P1.melds.append(meld_2)
    print("3")
    # # # -------------------------------------
    # meld_3 = customappendlist.CustomAppendList('P2.melds')
    # for card in range(10):
    #     meld_3.append(deck.MasterDeck.deck.pop(-1))
    # player.P2.melds.append(meld_3)
    # print("4")
    # -------------------------------------
    # meld_4 = customappendlist.CustomAppendList('P2.melds')
    # for card in range(7):
    #     meld_4.append(deck.MasterDeck.deck.pop(-1))
    # player.P2.melds.append(meld_4)
    # print("5")
    # # -------------------------------------
    # meld_5 = customappendlist.CustomAppendList('P1.play_cards')
    # for card in range(7):
    #     meld_5.append(deck.MasterDeck.deck.pop(-1))
    # player.P1.play_cards.append(meld_5)
    # print("6")
    # # -------------------------------------
    # new_meld = customappendlist.CustomAppendList('P2.play_cards')
    # for card in range(7):
    #     new_meld.append(deck.MasterDeck.deck.pop(-1))
    # player.P2.play_cards.append(new_meld)
    # print("7")
    # # -------------------------------------
    # new_meld = customappendlist.CustomAppendList('P1.melds')
    # player.P1.melds.append(new_meld)
    # for card in player.P1.play_cards[0][:]:
    #     new_meld.append(player.P1.play_cards[0].pop(-1))
    # player.P1.play_cards.pop(0)
    # print("8")
    # # -------------------------------------
    # new_meld = customappendlist.CustomAppendList('P2.play_cards')
    # player.P2.play_cards.append(new_meld)
    # for card in player.P2.melds[0][:]:
    #     player.P2.play_cards[1].append(player.P1.melds[0].pop(-1))
    # print("9")
    # # # # -------------------------------------
    # for card in range(3):
    #     player.P2.play_cards[0].append(deck.MasterDeck.deck.pop(-1))
    # print("10")
    # # # # -------------------------------------
    # for card in range(3):
    #     player.P2.melds[0].append(deck.MasterDeck.deck.pop(-1))
    # print("11")
    # # # -------------------------------------
    # for card in range(7):
    #     player.P1.hand.append(deck.MasterDeck.deck.pop(-1))
    # print("12")
    # # # -------------------------------------
    # for card in range(7):
    #     player.P2.hand.append(deck.MasterDeck.deck.pop(-1))
    # print("13")
    # -------------------------------------
    pygame.event.wait()
    pygame.quit()
    sys.exit()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by module when opened, if __name__ == "__main__". The main pygame loop. Handles FPS, pygame.event handling, and calls draw_window() for screen updating.
def main():
    logger.debug("main\n") # ****
    # -------------------------------------
    # Below Section - Sets up the run loop so that unless the player quits the game/exits the window, it continues to cycle through this progression loop.
    setup()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    # -------------------------------------
        test_run()
        # progression.the_draw_1()
    # -------------------------------------
    # Below Section - Quits the pygame window and terminates the entire program.
    pygame.quit()
    sys.exit()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
