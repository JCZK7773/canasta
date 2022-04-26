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
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by locations.Locations.card_movement(). Handles framerate, event handling, and updating display.
def draw_window():
    # -------------------------------------
    # Below Section - Sets the max framerate for the game.
    clock = pygame.time.Clock()
    clock.tick(400)
    # -------------------------------------
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            # Below Section - Quits the pygame window and terminates the entire program.
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game.game.click_card_active == True:
            ###### Below Section - Needs to be finished. For whenever clicking a card, for detecting if the card was clicked, and saving it as a value to be accessed elsewhere for reference.
            for card in game.game.clickable_card_group:
                if card.collidepoint(event.pos):
                    game.game.clicked_card = card
                    game.game.clicked_card.highlighted = True
            ###### -------------------------------------
        elif event.type == pygame.KEYDOWN and game.game.text_input_active == True:
            if event.key == pygame.K_RETURN:
                game.game.text_input_active = False
                game.game.input_text_final = game.game.input_text
                game.game.input_text = game.game.input_text_reset
            elif event.key == pygame.K_BACKSPACE:
                game.game.input_text = game.game.input_text[:-1]
            else:
                game.game.input_text += event.unicode
    # -------------------------------------
    # text_obj_dict_keys_list = list(game.game.text_obj_dict.keys())
    # # -------------------------------------
    # for obj in text_obj_dict_keys_list[0:-1]:
    #     if obj != None:
    #         print(obj)
    #         game.game.screen_surface.blit(obj, game.game.text_obj_dict[obj])
    # # Below Section - Handles the rendering of the input text and the input text surface...
    # if text_obj_dict_keys_list[-1] != None:
    #     txt_surface = font.render(game.game.input_text, True, color)
    #     width = max(200, txt_surface.get_width() + 10)
    #     game.game.input_text_rect.w = width
    #     game.game.screen_surface.blit(txt_surface, (game.game.input_text_rect.x, game.game.input_text_rect.y))
    #     pygame.draw.rect(game.game.screen_surface, game.game.grey_color, game.game.input_text_rect, 2)
    # -------------------------------------
    game.game.card_group.update()
    game.game.card_rects = game.game.card_group.draw(game.game.screen_surface)
    # -------------------------------------
    # Below Line - Note: This has to go below game.game.card_group.update() & game.game.card_rects = game.game.card_group.draw(game.game.screen_surface) or it will not display on the screen surface.
    pygame.draw.line(game.game.screen_surface, game.game.black_color, [locations.Locate.visible_center[0] - 1, locations.Locate.visible_top], [locations.Locate.visible_center[0] - 1, locations.Locate.visible_bottom], 2)
    game.game.screen.update(game.game.card_rects)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by module when opened, if __name__ == "__main__". The main pygame loop. Handles FPS and calls draw_window() for screen updating.
def main():
    print("main")
    progression.logger.debug("main\n") # ****
    # -------------------------------------
    # Below Section - Sets up the run loop so that unless the player quits the game/exits the window, it continues to cycle through this progression loop.
    setup()
    test_run.test_run()
    # progression.the_draw_1()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
