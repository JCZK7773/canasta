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
    # Below Section - Color Section
    # -------------------------------------
        self.black_color = (0, 0, 0)
        self.grey_color = (79, 78, 74)
        self.background_color = (0,40,0)
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
        self._progression_text = ('What is your name?!?')
        # Below Section - Placeholder to avoid error. Assigned through progression_text.
        self.progression_text_obj = None
        self.progression_text_obj_rect = None
        # -------------------------------------
        # Below Line - Type: str. Internal value; external use value is self.input_text as a calculated property which assigns the self.input_text_obj & self.input_text_obj_rect automatically. The actual text the user inputs via processed keypresses in the main loop.
        self._input_text = 'input text'
        ###### Below Line - Do I actually need this? Can't I just run 'self.input_text = '''? Type: str. The blank string that the input_text will be reset to upon the user hitting enter/return, which causes input_text to be assigned to the finished input_text_final. This variable never changes.
        self.input_text_reset = ''
        # Below Line - Type: str. The finished input string which is the 'returned' input. After the user finishes input / hits enter/return, this string copies the input_text before the input_text is reset back to a blank string, input_text_reset.
        self.input_text_final = 'Return this input...'
        # Below Line -n The active variable that changes whether or not text input is active or inactive (True or False).
        self.text_input_active = False
        # -------------------------------------
        # Below Section - Placeholders to avoid 'NoneType' error. Accessed through self.text_obj_dict & assigned through the self.input_text calculated property every time it is altered (except for .get_rect() as that does not need to be changed every time it is updated. If that is done, it messes up the text display by 'recreating' another rect centered at a different location centered on it's new dimensions).
        self.input_text_obj = self.font.render(self._input_text, True, (255, 255, 255), self.grey_color)
        self.input_text_obj_rect = self.input_text_obj.get_rect()
        # Below Line - This changes to be slightly offset from self.progression_text_obj_rect.center inside the self.input_text calculated property.
        self.input_text_obj_rect.center = [400, 400]
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
                              self.input_text_obj: self.input_text_obj_rect}
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
    # Below Section - Calculated property; whenever a value is set for this, make it calculate and assign the self.input_text_obj and self.input_text_obj_rect.center() so that it will always properly display on the screen.
    @property
    def input_text(self):
        return self._input_text

    @input_text.setter
    def input_text(self, val):
        self._input_text = val
        self.input_text_obj = self.font.render(val, True, (255, 255, 255), self.grey_color)
        # Below Line - Have to have this during testing using test_run.test_run() because the script does not call progression_text_func() as does the actual progression.the_draw_1() call eventual does subsequent to calling this calculated property. Can remove this later once testing is verified as working 100%.
        if self.progression_text_obj_rect != None:
            self.input_text_obj_rect.center = [self.progression_text_obj_rect.center[0] - 100, self.progression_text_obj_rect.center[1] + 30]
    # -------------------------------------
    # Below Function - Called by various places in progression.py to update the self.progression_text and the associated rects and centers, as well as whether or not an input is being asked for from the user. If so, handles the assigning of the rect and center for the self.input_text and the activating of the text_input_active variable for the event handler to allow for processed input. If there is no input, ensures that input_text_obj = None so that the renderer does not try to draw it on the screen.
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
            self.text_input_active = True
        else:
            print("else")
            ###### Below Line - I need to make it so that whenever an input is completed, the input resets back to a blank value. I am not positive that this is the best way to reach that goal. It might be. Commenting out for further review.
            # self.input_text_obj = None
        if click_card_active == True:
            self.click_card_active = True
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Below Function - Handles all events for pygame. Called by the various draw_window() functions.
    def event_handler(self):
        # print("event_handler")
        # -------------------------------------
        # Below Line - Added merely for testing purposes.
        self.text_input_active = True
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
                    print("self.text_input_active = False")
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
        if self.input_text_obj != None:
            self.screen_surface.blit(self.input_text_obj, self.input_text_obj_rect)
            ###### Below Line - Disabled for now as not necessary for working input text. The background text box for the input_text.
            # pygame.draw.rect(self.screen_surface, self.grey_color, self.input_text_obj_rect, 2)
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
        if self.input_text_obj != None:
            self.screen_surface.blit(self.input_text_obj, self.input_text_obj_rect)
        # -------------------------------------
        # Below Line - Draws the dividing line on the middle of the screen. Note: This has to go below self.card_group.update() & self.card_rects = self.card_group.draw(self.screen_surface) or it will not display on the screen surface.
        pygame.draw.line(self.screen_surface, self.black_color, [locations.Locate.visible_center[0] - 1, locations.Locate.visible_top], [locations.Locate.visible_center[0] - 1, locations.Locate.visible_bottom], 2)
        ###### Below Line - *** Note: Is this a special method for LayeredDirty or something? Because this does not properly update the entire display as this alone does not cause the input text to be rendered on top of the screen, but only shows it if a card is blitted past it. ***  The main .update() call which updates the new draw information for each frame.
        self.screen.update(self.card_rects)
        # Below Line - Updates the display to reflect the new game information. This is required for the input text to properly display on the screen. If it is not called, input text only displays after it has been blitted over by a card or something.
        pygame.display.update()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
game = Game()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
