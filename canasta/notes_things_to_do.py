# THINGS TO DO
    # Worked on this a bit. Will continue later when more sure about solution. Make it so that whenever visually displayed card groups are popped from (technically done at the end of the append()) the card group is visually reorganized. Already started this process by creating custom .pop() function, etc...
    # Make all of the necessary changes to progression.py so that it will all operate smoothly. Take your time. Do it right.
        # Change progression.py so that all melds are instances of CustomAppendList & are assigned the proper card_group_names for proper visual placement.
        # Go through all code to ensure that all for loops are being broken out of whenever a condition is met, instead of continuing the iteration as this slows the execution of the code.
    # Pretty sure that I am loading the images each time I reassign the image. I think it would increase performance to load the image once and then just assign a variable to the image??
    # Implement delta timing frame system.
    # I think I tried this but it did not work. Change event_handler() so that the 'for event in pygame.event.get()' is instead 'for event in pygame.event.wait()'?? Or something along those lines. Supposedly this will reduce CPU usage. Perhaps I can call pygame.event.wait() in the progression loops ONLY whenever I am expecting user input. See NOTES for a paste of supposedly improved code snippet.
    # Move card creation, card ranks, card suits, and other attributes more properly associated with the Card class, into the Card class code base instead of being inside of the Deck class.
    # Change length of import words/characters (and variable & function names) to a lesser amount by using import xxxxxx AS x to improve readability, etc.
    # Add in card sounds & background music.
    # Post on web so others can check for bugs as well.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DEVLOG
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
    # 04/22/22 - 05/04/22: Finished and polished the progression text and input text sections in game.py and the associated logic. Completely debugged the system, and cleaned up and changed things around in the code for draw_window_the_draw(). Input happens in real time, backspace works, and display is reset each time a value is processed. Continued to debug logic in progression.py.
    # 05/05/22 - 05/09/22: Started, finished, debugged, and tested the card movement speed issue, card click event handling, input (backspacking, clearing the rects after input, etc.), reworked much of the logic in progression.py, and continued to clean up comments and outdated code as I go along.
    # 05/10/22 - ...
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NOTES
    #     pygame.Rect
    # pygame object for storing rectangular coordinates
    # Rect(left, top, width, height) -> Rect

    #     pygame.draw.rect()
    # draw a rectangle
    # rect(surface, color, rect) -> Rect
    # rect(surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1) -> Rect
    # Draws a rectangle on the given surface.
    #
    # Parameters
    # surface (Surface) -- surface to draw on
    #
    # color (Color or int or tuple(int, int, int, [int])) -- color to draw with, the alpha value is optional if using a tuple (RGB[A])
    #
    # rect (Rect) -- rectangle to draw, position and dimensions
    #
    # width (int) --
    #
    # (optional) used for line thickness or to indicate that the rectangle is to be filled (not to be confused with the width value of the rect parameter)

    #     render()¶
    # draw text on a new Surface
    # render(text, antialias, color, background=None) -> Surface
    # This creates a new Surface with the specified text rendered on it. pygame provides no way to directly draw text on an existing Surface: instead you must use Font.render() to create an image (Surface) of the text, then blit this image onto another Surface.

    # If you reassign self.image.get_rect() then you have to reassign .center() as well. You do not need to reassign .get_rect() every time you edit the object!!!!!

    # Using this suggested line: for event in [pygame.event.wait()]+pygame.event.get(): greatly reduces CPU usage in games where the CPU runs full-bore when there are no events (compared to for event in pygame.event.get():). Nice. –

    # Debugging Info for Card Movement Speed Testing
        # First Half of List Iteration
            # Highest Performance Card Info
                # Lowest Time = 0.01
                # Iter_num = 1,000
                # Ratio = .001
                # Iter_num/Final_time = 100,000
            # Lowest Performance Card Info
                # Highest Time = 1.1
                # Iter_num = 288
                # Ratio = .976
                # Iter_num/Final_time = 261
        # Second Half of List Iteration
            # Highest Performance Card Info
                # Lowest Time = 0.01
                # Iter_num = 501
                # Ratio = .002
                # Iter_num/Final_time = 50,100
            # Lowest Performance Card Info
                # Highest Time = 1.71
                # Iter_num = 712
                # Ratio = .608
                # Iter_num/Final_time = 424
        # Conclusions
            # Higher the Ratio = Higher the Total Time
            # Higher the draw_window_calls_num = Higher the Total Time. More calls; more time.
            # Actual problem was in game.py. Was updating every single card again after only updating them via LayeredDirty .update() method.

    # The best alternative is DeviantArt, which is free. Other great sites and apps similar to OpenGameArt.org are Freesound (Free, Open Source), Poly Haven (Free), SkinBase (Free) and RateMyDrawings (Free).
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
