import pygame
import sys
import locations
import player
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Game():
    def __init__(self):
    # -------------------------------------
    # Below Section - Pygame Display Setup Section
    # -------------------------------------
        # Below Line - Calls pygame.init (needed for other modules such as pygame.font)...
        pygame.init()
        # Below Section - Sets up the pygame window size and assigns a title caption for the game window.
        self.screen = pygame.display
        self.screen_surface = pygame.display.set_mode((1920, 1020))
        pygame.display.set_caption("Canasta")
        # -------------------------------------
        self.background = pygame.Surface([1920, 1020])
        self.background_color = (0,40,0)
        self.background.fill(self.background_color)
    # -------------------------------------
    # Below Section - Card Sprite Section
    # -------------------------------------
        # Below Line - Creates the card_group Sprite Group.
        self.card_group = pygame.sprite.LayeredDirty()
        self.card_group.clear(self.screen, self.background)
        self.card_rects = None
    # -------------------------------------
    # Below Section - Card Clicking Section
    # -------------------------------------
        # Below Line - The 'active' variable for whether or not the event handler should process a clicked card.
        self.click_card_active = False
        # Below Line - The list group for cards that will be eligible for clicking in the event of choose_card_active being activated. Only these cards will be iterated through to check their positions against the click event position.
        self.clickable_card_group = []
        # Below Line - Type: Card. The currently clicked card.
        self.clicked_card = None
        # Below Line - Type: list. The list that clicked_cards are added to so that they can be handled as a group instead of one by one.
        self.clicked_card_list = []
    # -------------------------------------
    # Below Section - Text Section
    # -------------------------------------
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        # -------------------------------------
        self.p1_hand_text = (f'{player.P1.name}\'s Hand')
        self.p2_hand_text = (f'{player.P2.name}\'s Hand')
        self.p1_play_cards_text = (f'{player.P1.name}\'s Play Cards')
        self.p2_play_cards_text = (f'{player.P2.name}\'s Play Cards')
        self.p1_melds_text = (f'{player.P1.name}\'s Melds')
        self.p2_melds_text = (f'{player.P2.name}\'s Melds')
        self.p1_red_3_meld_text = (f'{player.P1.name}\'s Red 3 Meld')
        self.p2_red_3_meld_text = (f'{player.P2.name}\'s Red 3 Meld')
        self._progression_text = (f'What is your name?')
        # Below Section - Placeholder to avoid error. Assigned through progression_text.
        self.progression_text_obj = None
        self.progression_text_obj_rect = None
        # -------------------------------------
        # Below Line - Type: str. The actual text the user inputs via processed keypresses in the main loop.
        self.input_text = 'While inputting...'
        # Below Line - Type: str. The blank string that the input_text will be reset to upon the user hitting enter/return, which causes input_text to be assigned to the finished input_text_final. This variable never changes.
        self.input_text_reset = ''
        # Below Line - Type: str. The finished input string which is the 'returned' input. After the user finishes input / hits enter/return, this string copies the input_text before the input_text is reset back to a blank string, input_text_reset.
        self.input_text_final = 'Return this input...'
        # Below Line -n The active variable that changes whether or not text input is active or inactive (True or False).
        self.text_input_active = False
        # Below Line - Placeholder. Type: pygame.Rect(top-left x, top-left y, width, height). Modified inside of progr_text() according to the current progression_text rect. The input rect object which is to be calculated based off of the current progression_text to create a text input window through which the player adds inputs in response to various questions throughout the game. Input must be filtered to process desired result.
        self.input_text_rect = None
        # -------------------------------------
        # Below Line - The number used in text_name_loc_dict to adjust how far above a card group the text display is situated.
        self.y_reduce_num = 93
        # -------------------------------------
        # Below Dictionary - Duplicated this in locations.Locations to be finally placed there. Holding here until I make sure that it works. It's commented out in locations.py
        self.text_name_loc_dict = {'Deck': [locations.Locate.deck_loc[0], locations.Locate.deck_loc[1] - self.y_reduce_num],
                              'Discard Pile': [locations.Locate.discard_pile_loc[0], locations.Locate.discard_pile_loc[1] - self.y_reduce_num],
                              'p1_hand_text_loc': [locations.Locate.p1_hand_start_loc[0] + 12, locations.Locate.p1_hand_start_loc[1] - self.y_reduce_num],
                              'p2_hand_text_loc': [locations.Locate.p2_hand_start_loc[0] + 12, locations.Locate.p2_hand_start_loc[1] - self.y_reduce_num],
                              'p1_play_cards_text_loc': [locations.Locate.p1_play_cards_start_loc[0] + 20, locations.Locate.p1_play_cards_start_loc[1] - self.y_reduce_num],
                              'p2_play_cards_text_loc': [locations.Locate.p2_play_cards_start_loc[0] + 20, locations.Locate.p2_play_cards_start_loc[1] - self.y_reduce_num],
                              'p1_melds_text_loc': [locations.Locate.p1_melds_start_loc[0], locations.Locate.p1_melds_start_loc[1] - self.y_reduce_num],
                              'p2_melds_text_loc': [locations.Locate.p2_melds_start_loc[0], locations.Locate.p2_melds_start_loc[1] - self.y_reduce_num],
                              'p1_red_3_meld_text_loc': [0, 0],
                              'p2_red_3_meld_text_loc': [0, 0],
                              # Below Section - Make it so that whenever a value is set for this (through progression.py) make it calculate and assign the rect and it's center based on the size of the rect so that it will always properly display on the screen.
                              'p1_progression_text_loc': [150, 30],
                              'p2_progression_text_loc': [1750, 30]}
        # -------------------------------------
        self.deck_text_obj = self.font.render('Deck', True, (255, 255, 255), self.background_color)
        self.deck_text_obj_rect = self.deck_text_obj.get_rect()
        self.deck_text_obj_rect.center = self.text_name_loc_dict['Deck']
        # -------------------------------------
        self.discard_pile_text_obj = self.font.render('Discard Pile', True, (255, 255, 255), self.background_color)
        self.discard_pile_text_obj_rect = self.discard_pile_text_obj.get_rect()
        self.discard_pile_text_obj_rect.center = self.text_name_loc_dict['Discard Pile']
        # -------------------------------------
        self.p1_hand_text_obj = self.font.render(self.p1_hand_text, True, (255, 255, 255), self.background_color)
        self.p1_hand_text_obj_rect = self.p1_hand_text_obj.get_rect()
        self.p1_hand_text_obj_rect.center = self.text_name_loc_dict['p1_hand_text_loc']
        # -------------------------------------
        self.p2_hand_text_obj = self.font.render(self.p2_hand_text, True, (255, 255, 255), self.background_color)
        self.p2_hand_text_obj_rect = self.p2_hand_text_obj.get_rect()
        self.p2_hand_text_obj_rect.center = self.text_name_loc_dict['p2_hand_text_loc']
        # -------------------------------------
        self.p1_play_cards_text_obj = self.font.render(self.p1_play_cards_text, True, (255, 255, 255), self.background_color)
        self.p1_play_cards_text_obj_rect = self.p1_play_cards_text_obj.get_rect()
        self.p1_play_cards_text_obj_rect.center = self.text_name_loc_dict['p1_play_cards_text_loc']
        # -------------------------------------
        self.p2_play_cards_text_obj = self.font.render(self.p2_play_cards_text, True, (255, 255, 255), self.background_color)
        self.p2_play_cards_text_obj_rect = self.p2_play_cards_text_obj.get_rect()
        self.p2_play_cards_text_obj_rect.center = self.text_name_loc_dict['p2_play_cards_text_loc']
        # -------------------------------------
        self.p1_melds_text_obj = self.font.render(self.p1_melds_text, True, (255, 255, 255), self.background_color)
        self.p1_melds_text_obj_rect = self.p1_melds_text_obj.get_rect()
        self.p1_melds_text_obj_rect.center = self.text_name_loc_dict['p1_melds_text_loc']
        # -------------------------------------
        self.p2_melds_text_obj = self.font.render(self.p2_melds_text, True, (255, 255, 255), self.background_color)
        self.p2_melds_text_obj_rect = self.p2_melds_text_obj.get_rect()
        self.p2_melds_text_obj_rect.center = self.text_name_loc_dict['p2_melds_text_loc']
        # -------------------------------------
        self.p1_red_3_meld_text_obj = self.font.render(self.p1_red_3_meld_text, True, (255, 255, 255), self.background_color)
        self.p1_red_3_meld_text_obj_rect = self.p1_red_3_meld_text_obj.get_rect()
        self.p1_red_3_meld_text_obj_rect.center = self.text_name_loc_dict['p1_red_3_meld_text_loc']
        # -------------------------------------
        self.p2_red_3_meld_text_obj = self.font.render(self.p2_red_3_meld_text, True, (255, 255, 255), self.background_color)
        self.p2_red_3_meld_text_obj_rect = self.p2_red_3_meld_text_obj.get_rect()
        self.p2_red_3_meld_text_obj_rect.center = self.text_name_loc_dict['p2_red_3_meld_text_loc']
        # -------------------------------------
        self.top_center_title = [locations.Locate.visible_center[0] - (round(self.deck_text_obj_rect[2] / 2)), locations.Locate.visible_top + 20]
        # -------------------------------------
        self.text_obj_dict = {self.deck_text_obj: self.deck_text_obj_rect,
                              self.discard_pile_text_obj: self.discard_pile_text_obj_rect,
                              self.p1_hand_text_obj: self.p1_hand_text_obj_rect,
                              self.p2_hand_text_obj: self.p2_hand_text_obj_rect,
                              self.p1_play_cards_text_obj: self.p1_play_cards_text_obj_rect,
                              self.p2_play_cards_text_obj: self.p2_play_cards_text_obj_rect,
                              self.p1_melds_text_obj: self.p1_melds_text_obj_rect,
                              self.p2_melds_text_obj: self.p2_melds_text_obj_rect,
                              self.p1_red_3_meld_text_obj: self.p1_red_3_meld_text_obj_rect,
                              self.p2_red_3_meld_text_obj: self.p2_red_3_meld_text_obj_rect,
                              self.progression_text_obj: self.progression_text_obj_rect,
                              self.input_text_rect: None}
    # -------------------------------------
    # Below Section - Color Section
    # -------------------------------------
        self.black_color = (0, 0, 0)
        self.grey_color = (79, 78, 74)
    # -------------------------------------
    # Below Section - Calculated property; whenever a value is set for this, make it calculate and assign the rect and it's center based on the size of the rect so that it will always properly display on the screen.
    @property
    def progression_text(self):
        return self._progression_text

    @progression_text.setter
    def progression_text(self, val):
        self._progression_text = val
        self.progression_text_obj = self.font.render(val, True, (255, 255, 255), self.background_color)
        self.progression_text_obj_rect = self.progression_text_obj.get_rect()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
game = Game()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by various places in progression.py to update the game.progression_text and the associated rects and centers, as well as whether or not an input is being asked for from the user. If so, handles the assigning of the rect and center for the game.input_text and the activating of the text_input_active variable for the event handler to allow for processed input. If there is no input, ensures that input_text_rect = None so that the renderer does not try to draw it on the screen.
def progr_text(current_player, text, has_input = False, click_card_active = False):
    print("progr_text")
    game.progression_text = text
    # -------------------------------------
    if current_player.name == 'P1':
        game.progression_text_obj_rect.center = game.text_name_loc_dict['p1_progression_text_loc']
    else:
        game.progression_text_obj_rect.center = game.text_name_loc_dict['p2_progression_text_loc']
    # -------------------------------------
    # Below Section - Handles input. Assigns the input rect to coincide with the position of the progression_text
    if has_input == True:
        prog_txt_ctr = game.progression_text_obj_rect.center
        game.input_text_obj_rect = pygame.Rect(prog_txt_ctr[0], prog_txt_ctr[1] + 5, 70, 32)
        game.text_input_active = True
    else:
        game.input_text_rect = None
    if click_card_active == True:
        game.click_card_active = True
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by main(). Handles screen background assignment, card_group draw updating, and the pygame.display updates.
def draw_window():
    print("draw_window")
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game.click_card_active == True:
            ###### Below Section - Needs to be finished. For whenever clicking a card, for detecting if the card was clicked, and saving it as a value to be accessed elsewhere for reference.
            for card in game.clickable_card_group:
                if card.collidepoint(event.pos):
                    game.clicked_card = card
                    game.clicked_card.highlighted = True
        elif event.type == pygame.KEYDOWN and game.text_input_active == True:
            if event.key == pygame.K_RETURN:
                game.text_input_active = False
                game.input_text_final = game.input_text
                game.input_text = game.input_text_reset
            elif event.key == pygame.K_BACKSPACE:
                game.input_text = game.input_text[:-1]
            else:
                game.input_text += event.unicode
    # -------------------------------------
    # text_obj_dict_keys_list = list(game.text_obj_dict.keys())
    # # -------------------------------------
    # for obj in text_obj_dict_keys_list[0:-1]:
    #     if obj != None:
    #         print(obj)
    #         game.screen_surface.blit(obj, game.text_obj_dict[obj])
    # # Below Section - Handles the rendering of the input text and the input text surface...
    # if text_obj_dict_keys_list[-1] != None:
    #     txt_surface = font.render(game.input_text, True, color)
    #     width = max(200, txt_surface.get_width() + 10)
    #     game.input_text_rect.w = width
    #     game.screen_surface.blit(txt_surface, (game.input_text_rect.x, game.input_text_rect.y))
    #     pygame.draw.rect(game.screen_surface, game.grey_color, game.input_text_rect, 2)
    # -------------------------------------
    game.card_group.update()
    print(f"type(game.screen_surface) = {type(game.screen_surface)}")
    print(game.card_rects)
    game.card_rects = game.card_group.draw(game.screen_surface)
    game.screen_surface.blit(game.text, game.textRect.center)
    game.screen.update(game.card_rects)
    # -------------------------------------
    # Below Line - Note: This has to go below game.card_group.update() & game.card_rects = game.card_group.draw(game.screen_surface) or it will not display on the screen surface.
    # pygame.draw.line(game.screen_surface, game.black_color, [locations.Locate.visible_center[0] - 1, locations.Locate.visible_top], [locations.Locate.visible_center[0] - 1, locations.Locate.visible_bottom], 2)


    ###### Below Section - This is how the code for draw_window looked before I made some of these big changes to game.py. For reference when debugging.
    # # Below Function - Called by main(). Handles screen background assignment, card_group draw updating, and the pygame.display updates.
    # def draw_window():
    #     # print("draw_window")
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #     # -------------------------------------
    #     game.card_group.update()
    #     game.card_rects = game.card_group.draw(game.screen_surface)
    #     game.screen_surface.blit(game.text, game.textRect.center)
    #     game.screen.update(game.card_rects)
    ###### -------------------------------------
