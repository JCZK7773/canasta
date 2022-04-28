import pygame
import sys
import locations
import player
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Game():
    def __init__(self):
        # Below Line - The variable that is used to change the 'game_state', which determines which version of draw_window() will be called by card_movement(), so that the display properly reflects the content of the progression loops.
        self.game_state = None
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
        # Below Line - This 'clears' the screen, retaining the LayeredDirty Sprites that are not being moved as still drawn on the screen, and then erasing the ones that need to be moved, and re-applies the background. If this is not run, the background does not display properly.
        self.card_group.clear(self.screen, self.background)
        # Below Line - Placeholder which = self.card_group.draw(self.screen_surface). Passed to screen.update() to draw the cards on the screen in the proper order.
        self.card_rects = None
    # -------------------------------------
    # Below Section - Card Clicking Section
    # -------------------------------------
        # Below Line - The 'active' variable for whether or not the event handler should process a clicked card.
        self.click_card_active = False
        # Below Line - The list group for cards that will be eligible for clicking in the event of choose_card_active being activated. Only these cards will be iterated through to check their positions against the click event position.
        self.clickable_card_list = []
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
        self.input_text_obj_rect = None
        # -------------------------------------
        self.deck_text_obj = self.font.render('Deck', True, (255, 255, 255), self.background_color)
        self.deck_text_obj_rect = self.deck_text_obj.get_rect()
        self.deck_text_obj_rect.center = locations.Locate.text_name_loc_dict['Deck']
        # -------------------------------------
        self.discard_pile_text_obj = self.font.render('Discard Pile', True, (255, 255, 255), self.background_color)
        self.discard_pile_text_obj_rect = self.discard_pile_text_obj.get_rect()
        self.discard_pile_text_obj_rect.center = locations.Locate.text_name_loc_dict['Discard Pile']
        # -------------------------------------
        self.p1_hand_text_obj = self.font.render(self.p1_hand_text, True, (255, 255, 255), self.background_color)
        self.p1_hand_text_obj_rect = self.p1_hand_text_obj.get_rect()
        self.p1_hand_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_hand_text_loc']
        # -------------------------------------
        self.p2_hand_text_obj = self.font.render(self.p2_hand_text, True, (255, 255, 255), self.background_color)
        self.p2_hand_text_obj_rect = self.p2_hand_text_obj.get_rect()
        self.p2_hand_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_hand_text_loc']
        # -------------------------------------
        self.p1_play_cards_text_obj = self.font.render(self.p1_play_cards_text, True, (255, 255, 255), self.background_color)
        self.p1_play_cards_text_obj_rect = self.p1_play_cards_text_obj.get_rect()
        self.p1_play_cards_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_play_cards_text_loc']
        # -------------------------------------
        self.p2_play_cards_text_obj = self.font.render(self.p2_play_cards_text, True, (255, 255, 255), self.background_color)
        self.p2_play_cards_text_obj_rect = self.p2_play_cards_text_obj.get_rect()
        self.p2_play_cards_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_play_cards_text_loc']
        # -------------------------------------
        self.p1_melds_text_obj = self.font.render(self.p1_melds_text, True, (255, 255, 255), self.background_color)
        self.p1_melds_text_obj_rect = self.p1_melds_text_obj.get_rect()
        self.p1_melds_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_melds_text_loc']
        # -------------------------------------
        self.p2_melds_text_obj = self.font.render(self.p2_melds_text, True, (255, 255, 255), self.background_color)
        self.p2_melds_text_obj_rect = self.p2_melds_text_obj.get_rect()
        self.p2_melds_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_melds_text_loc']
        # -------------------------------------
        self.p1_red_3_meld_text_obj = self.font.render(self.p1_red_3_meld_text, True, (255, 255, 255), self.background_color)
        self.p1_red_3_meld_text_obj_rect = self.p1_red_3_meld_text_obj.get_rect()
        self.p1_red_3_meld_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_red_3_meld_text_loc']
        # -------------------------------------
        self.p2_red_3_meld_text_obj = self.font.render(self.p2_red_3_meld_text, True, (255, 255, 255), self.background_color)
        self.p2_red_3_meld_text_obj_rect = self.p2_red_3_meld_text_obj.get_rect()
        self.p2_red_3_meld_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_red_3_meld_text_loc']
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
                              self.input_text_obj_rect: None}
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
    # -------------------------------------
    # Below Function - Called by various places in progression.py to update the self.progression_text and the associated rects and centers, as well as whether or not an input is being asked for from the user. If so, handles the assigning of the rect and center for the self.input_text and the activating of the text_input_active variable for the event handler to allow for processed input. If there is no input, ensures that input_text_obj_rect = None so that the renderer does not try to draw it on the screen.
    def progression_text_func(self, current_player, text, has_input = False, click_card_active = False):
        print("progression_text_func")
        self.progression_text = text
        # -------------------------------------
        if current_player.name == 'P1':
            self.progression_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_progression_text_loc']
        else:
            self.progression_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_progression_text_loc']
        # -------------------------------------
        # Below Section - Handles input. Assigns the input rect to coincide with the position of the progression_text
        if has_input == True:
            prog_txt_ctr = self.progression_text_obj_rect.center
            self.input_text_obj_rect = pygame.Rect(prog_txt_ctr[0], prog_txt_ctr[1] + 5, 70, 32)
            self.text_input_active = True
        else:
            self.input_text_obj_rect = None
        if click_card_active == True:
            self.click_card_active = True
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Below Function - Handles all events for pygame. Called by the various draw_window() functions.
    def event_handler(self):
        # print("event_handler")
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                # Below Section - Quits the pygame window and terminates the entire program.
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.click_card_active == True:
                print("event_handler > click_card_active == True")
                # Below Section - Whenever clicking a card; detects if the card was clicked, and appends it to clicked_card_list.
                for card in self.clickable_card_list:
                    if card.collidepoint(event.pos):
                        self.clicked_card = card
                        self.clicked_card_list.append(card)
                        self.clicked_card.highlighted = True
                # -------------------------------------
            elif event.type == pygame.KEYDOWN and self.text_input_active == True:
                print("event_handler > text_input_active == True")
                if event.key == pygame.K_RETURN:
                    self.input_text_final = self.input_text
                    self.input_text = self.input_text_reset
                    self.text_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
    # Below Function - Called by locations.Locations.card_movement(). Handles framerate, event handling, and updating display.
    def draw_window_main(self):
        # print("draw_window_main")
        # -------------------------------------
        # Below Section - Sets the max framerate for the game.
        clock = pygame.time.Clock()
        # clock.tick(500)
        # -------------------------------------
        self.event_handler()
        # -------------------------------------
        # Below Line - Updates the sprites rect locations for each frame. If this is not run, the cards simply teleport from the start location > the final location in card_movement() without any gradual movement.
        self.card_group.update()
        # Below Line - Calls the LayeredDirty draw() method which ensures the cards are updated; draws all sprites in the right order onto the passed surface.
        self.card_rects = self.card_group.draw(self.screen_surface)
        # -------------------------------------
        # Below Line - A list of all of the text objects' keys; the surfaces (The values are the rects).
        text_obj_dict_keys_list = list(self.text_obj_dict.keys())
        # -------------------------------------
        # Below Section - Handles the rendering of the card group info text and the associated surfaces.
        for obj in text_obj_dict_keys_list[0:-1]:
            if obj != None:
                self.screen_surface.blit(obj, self.text_obj_dict[obj])
        # -------------------------------------
        # Below Section - Handles the rendering of the input_text_obj and the input_text_surface.
        if self.input_text_obj_rect != None:
            txt_surface = font.render(self.input_text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            self.input_text_obj_rect.w = width
            self.screen_surface.blit(txt_surface, (self.input_text_obj_rect.x, self.input_text_obj_rect.y))
            # Below Line - The background text box for the input_text.
            pygame.draw.rect(self.screen_surface, self.grey_color, self.input_text_obj_rect, 2)
        # -------------------------------------
        # Below Line - Draws the dividing line on the middle of the screen. Note: This has to go below self.card_group.update() & self.card_rects = self.card_group.draw(self.screen_surface) or it will not display on the screen surface.
        pygame.draw.line(self.screen_surface, self.black_color, [locations.Locate.visible_center[0] - 1, locations.Locate.visible_top], [locations.Locate.visible_center[0] - 1, locations.Locate.visible_bottom], 2)
        # Below Line - The main .update() call which updates the new draw information for each frame.
        self.screen.update(self.card_rects)
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Below Function - Called by locations.Locations.card_movement(). Handles framerate, event handling, and updating display.
    def draw_window_the_draw(self):
        # print("draw_window_the_draw")
        # -------------------------------------
        # Below Section - Sets the max framerate for the game.
        clock = pygame.time.Clock()
        # clock.tick(500)
        # -------------------------------------
        self.event_handler()
        # -------------------------------------
        # Below Line - Updates the sprites rect locations for each frame. If this is not run, the cards simply teleport from the start location > the final location in card_movement() without any gradual movement.
        self.card_group.update()
        # Below Line - Calls the LayeredDirty draw() method which ensures the cards are updated; draws all sprites in the right order onto the passed surface.
        self.card_rects = self.card_group.draw(self.screen_surface)
        # -------------------------------------
        # Below Line - A list of all of the text objects' keys; the surfaces (The values are the rects).
        text_obj_dict_keys_list = list(self.text_obj_dict.keys())
        # -------------------------------------
        # Below Section - Handles the rendering of the progression_text_obj and the progression_text_obj_rect.
        if self.progression_text_obj != None:
            self.screen_surface.blit(self.progression_text_obj, self.progression_text_obj_rect)
        # -------------------------------------
        # Below Section - Handles the rendering of the input_text_obj and the input_text_surface.
        if self.input_text_obj_rect != None:
            print(f"self.input_text = {self.input_text}")
            txt_surface = self.font.render(self.input_text, True, self.grey_color)
            width = max(200, txt_surface.get_width() + 10)
            self.input_text_obj_rect.w = width
            self.screen_surface.blit(txt_surface, (self.input_text_obj_rect.x, self.input_text_obj_rect.y))
            # Below Line - The background text box for the input_text.
            pygame.draw.rect(self.screen_surface, self.grey_color, self.input_text_obj_rect, 2)
        # -------------------------------------
        # Below Line - Draws the dividing line on the middle of the screen. Note: This has to go below self.card_group.update() & self.card_rects = self.card_group.draw(self.screen_surface) or it will not display on the screen surface.
        pygame.draw.line(self.screen_surface, self.black_color, [locations.Locate.visible_center[0] - 1, locations.Locate.visible_top], [locations.Locate.visible_center[0] - 1, locations.Locate.visible_bottom], 2)
        # Below Line - The main .update() call which updates the new draw information for each frame.
        self.screen.update(self.card_rects)
        # print("draw_window_the_draw > finished")
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
game = Game()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
