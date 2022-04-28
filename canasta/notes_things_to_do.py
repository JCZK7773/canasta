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

# FOR REFERENCE
    #     pygame.Rect
    # pygame object for storing rectangular coordinates
    # Rect(left, top, width, height) -> Rect

    #     pygame.draw.rect()
    # draw a rectangle
    # rect(surface, color, rect) -> Rect

    #     Using this suggested line: for event in [pygame.event.wait()]+pygame.event.get(): greatly reduces CPU usage in games where the CPU runs full-bore when there are no events (compared to for event in pygame.event.get():). Nice. –
    # Moondoggy
    #  Nov 25, 2021 at 15:24
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# THINGS TO DO
    # Model the input_text_obj_rect after the same manner in which all of the other text objects are rendered and assigned rects (through .get_rect())
    # Change event_handler() so that the 'for event in pygame.event.get()' is instead 'for event in pygame.event.wait()'?? Or something along those lines. Supposedly this will reduce CPU usage. Perhaps I can call pygame.event.wait() in the progression loops ONLY whenever I am expecting user input. See NOTES for a paste of supposedly improved code snippet.
    # FINISHED BUT NOT 100% SATISFIED - CHANGE LATER?
        # Figure out a solution to problem of how to create a border/outline for the highlighted cards.
            # Test the below solution on new_features_test.py with a basic image and rect.
            # Following link is a possible solution for problem of how to create a border/outline for the highlighted cards by drawing a rect over the image.
                # https://stackoverflow.com/questions/46742393/how-to-draw-a-border-around-a-sprite-or-image-in-pygame
        # May have to use mask.outline() in conjunction with Rect() to get the desired result.
    # Make all of the necessary changes to progression.py so that it will all operate smoothly. Take your time. Do it right.
        # Change the instances where numerical inputs are utilized, converting them to use card-clicks to determine the values instead.
        # Change progression.py so that all melds are instances of CustomAppendList & are assigned the proper card_group_names for proper visual placement.
    # Test & improve card movement system for smoothness / timing until satisfactory.
        # Implement delta timing frame system.
    # Go through all code to ensure that all for loops are being broken out of whenever a condition is met, instead of continuing the iteration as this slows the execution of the code.
    # Convert inputs to text rects on display.
    # Move card creation, card ranks, card suits, and other attributes more properly associated with the Card class, into the Card class code base instead of being inside of the Deck class.
    # Change input system from keyboard-based to mouse-based.
    # Add in card sounds & background music.
    # Change length of import words/characters (and variable & function names) to a lesser amount by using import xxxxxx AS x to improve readability, etc.
    # Post on web so others can check for bugs as well.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
