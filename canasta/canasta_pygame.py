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
        # 04/05/22 - 04/07/22: Finished consolidating, improving readability, and reducing lines for visual_meld_group_update and stress tested the final form.
        # 04/08/22: Finished fixing all card group movement functions completely. Ran testing for the movement functions: Cards associated with a customappendlist meld, but that are not inside of the associated meld group, as intended, do not get rendered. Full melds appended to a customappendlist meld group are properly displayed. Red_3_melds are properly located as well..
        # 04/11/22: Finished adjusting all of the card group positions. Finished creating and adjusting the text labels for the various card groups.
        # 04/12/22 - 04/20/22: Began and finished implementing logic system for event handling of text output, user input, and card-clicking. Began and mostly finished reworking progression.py to be compatible with the modern 2D code base. Began work on determining how to change areas of code where numerical values were used to represent cards to the new system of card-clicking & processing.
        # 04/21/22: Spent entire 4 hr. session debugging and fixing up some bad code from the many changes I made from the last session. Worked out most of the bugs from that, such as some logic, improper indentations, improper module/class/instance references, etc.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# THINGS TO DO
    # Figure out current bug wherein the_draw_anim() is called before any pygame display appears. This probably has to do with the fact that the draw_window(), event handler, etc. are out of place. Probably need to fix that first.
    # Figure out a solution to problem of how to create a border/outline for the highlighted cards.
        # Test the below solution on new_features_test.py with a basic image and rect.
        # Following link is a possible solution for problem of how to create a border/outline for the highlighted cards by drawing a rect over the image.
            # https://stackoverflow.com/questions/46742393/how-to-draw-a-border-around-a-sprite-or-image-in-pygame
        # May have to use mask.outline() in conjunction with Rect() to get the desired result.
    # Have to rearrange the code at a high level so that event handling happens in one place and the code inside of draw_window() is directly inside of the main while loop.
    # Make all of the necessary changes to progression.py so that it will all operate smoothly. Take your time. Do it right.
        # Change the instances where numerical inputs are utilized, converting them to use card-clicks to determine the values instead.
        # Change progression.py so that all melds are instances of CustomAppendList & are assigned the proper card_group_names for proper visual placement.
    # Test & improve card movement system for smoothness / timing until satisfactory.
        # Implement delta timing frame system.
    # Go through all code to ensure that all for loops are being broken out of whenever a condition is met, instead of continuing the iteration as this slows the execution of the code.
    # Convert inputs to text rects on display.
    # Fix main game loop so that it will properly run through game progression loops while maintaining proper display outputs.
    # Move card creation, card ranks, card suits, and other attributes more properly associated with the Card class, into the Card class code base instead of being inside of the Deck class.
    # Change input system from keyboard-based to mouse-based.
    # Add in card sounds & background music.
    # Change length of import words/characters (and variable & function names) to a lesser amount by using import xxxxxx AS x to improve readability, etc.
    # Post on web so others can check for bugs as well.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Line - For the purpose of testing. Is used to store the cards passed through sorted_and_numbered_list_printer so that they can be tested to ensure they are in the proper ascending order according to card rank/suit combination value.
testing_register_list = []
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def setup():
    print("setup")
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
    player.P1.play_cards = customappendlist.CustomAppendList('P1.play_cards') # ****
    player.P2.play_cards = customappendlist.CustomAppendList('P2.play_cards') # ****
    player.P1.red_3_meld = customappendlist.CustomAppendList('P1.red_3_meld') # ****
    player.P2.red_3_meld = customappendlist.CustomAppendList('P2.red_3_meld') # ****
    player.P1.melds = customappendlist.CustomAppendList('P1.melds') # ***
    player.P2.melds = customappendlist.CustomAppendList('P2.melds') # ***
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_run():
    print("test_run 1")
    # Below Section - Test section to verify proper movement of card-screen locations.
    # -------------------------------------
    # Below Section - Player melds testing.
    meld_1 = customappendlist.CustomAppendList('P1.melds')
    for card in range(6):
        meld_1.append(deck.MasterDeck.deck.pop(-1))
    player.P1.melds.append(meld_1)
    # -------------------------------------
    print("test_run 2")
    meld_2 = customappendlist.CustomAppendList('P1.melds')
    for card in range(6):
        meld_2.append(deck.MasterDeck.deck.pop(-1))
    player.P1.melds.append(meld_2)
    # # -------------------------------------
    print("test_run 3")
    meld_3 = customappendlist.CustomAppendList('P2.melds')
    for card in range(6):
        meld_3.append(deck.MasterDeck.deck.pop(-1))
    player.P2.melds.append(meld_3)
    # -------------------------------------
    print("test_run 4")
    meld_4 = customappendlist.CustomAppendList('P2.melds')
    for card in range(6):
        meld_4.append(deck.MasterDeck.deck.pop(-1))
    player.P2.melds.append(meld_4)
    # # -------------------------------------
    # # -------------------------------------
    # # Below Section - Player play cards testing.
    print("test_run 5")
    meld_5 = customappendlist.CustomAppendList('P1.play_cards')
    for card in range(6):
        meld_5.append(deck.MasterDeck.deck.pop(-1))
    player.P1.play_cards.append(meld_5)
    # -------------------------------------
    print("test_run 6")
    new_meld = customappendlist.CustomAppendList('P2.play_cards')
    for card in range(6):
        new_meld.append(deck.MasterDeck.deck.pop(-1))
    player.P2.play_cards.append(new_meld)
    # -------------------------------------
    # print("test_run 7")
    # new_meld = customappendlist.CustomAppendList('P1.melds')
    # player.P1.melds.append(new_meld)
    # for card in player.P1.play_cards[0][:]:
    #     new_meld.append(player.P1.play_cards[0].pop(-1))
    # player.P1.play_cards.pop(0)
    # -------------------------------------
    # print("test_run 8")
    # new_meld = customappendlist.CustomAppendList('P2.play_cards')
    # player.P2.play_cards.append(new_meld)
    # for card in player.P2.melds[0][:]:
    #     player.P2.play_cards[1].append(player.P1.melds[0].pop(-1))
    # # # -------------------------------------
    # print("test_run 9")
    # for card in range(3):
    #     player.P2.play_cards[0].append(deck.MasterDeck.deck.pop(-1))
    # # # -------------------------------------
    # print("test_run 10")
    # for card in range(3):
    #     player.P2.melds[0].append(deck.MasterDeck.deck.pop(-1))
    # -------------------------------------
    # -------------------------------------
    # Below Section - Player hand testing.
    print("test_run 11")
    for card in range(4):
        player.P1.hand.append(deck.MasterDeck.deck.pop(-1))
    # # -------------------------------------
    print("test_run 12")
    for card in range(4):
        player.P2.hand.append(deck.MasterDeck.deck.pop(-1))
    # -------------------------------------
    # -------------------------------------
    # # Below Section - Deck & discard pile testing.
    print("test_run 13")
    for card in range(4):
        deck.MasterDeck.discard_pile.append(deck.MasterDeck.deck.pop(-1))
    # -------------------------------------
    # print("test_run 14")
    # for card in range(4):
    #     deck.MasterDeck.deck.append(deck.MasterDeck.discard_pile.pop(-1))
    # -------------------------------------
    # -------------------------------------
    # # Below Section - Player red 3 meld testing.
    print("test_run 15")
    for card in range(3):
        player.P1.red_3_meld.append(deck.MasterDeck.deck.pop(-1))
    # # -------------------------------------
    print("test_run 16")
    for card in range(3):
        player.P2.red_3_meld.append(deck.MasterDeck.deck.pop(-1))
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by module when opened, if __name__ == "__main__". The main pygame loop. Handles FPS, pygame.event handling, and calls draw_window() for screen updating.
def main():
    print("main")
    progression.logger.debug("main\n") # ****
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
