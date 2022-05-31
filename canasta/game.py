import time
import pygame
import sys
import math
import locations
import player
import deck
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Game():
    def __init__(self):
        # Below Line - The variable that is used to change the 'game_state', which determines which version of draw_window() will be called by card_movement() (via draw_window_main()()), so that the display properly reflects the content of the progression loops.
        self.game_state = None
    # -------------------------------------
    # Below Section - Color Section
    # -------------------------------------
        self.black_color = (0, 0, 0)
        self.grey_color = (79, 78, 74)
        self.light_blue_color = (36, 107, 240)
        self.dark_blue_color = (1, 16, 89)
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
        # Below Line - Type: dict. The dictionary that contains the (key) card distance from the click event collision point & associated card (value). Used to determine the card with the lowest distance from the collision point to pinpoint a clicked_card from a cluster of options.
        self.collided_cards_dict = {}
    # -------------------------------------
    # Below Section - Text Section
    # -------------------------------------
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        # -------------------------------------
        # Below Line - Type: dict. A dictionary of invalid keypresses (which cannot be displayed properly, but instead show as rectangular symbols). Key = description, Value = associated event_key.
        self.invalid_keypress_dict = {'numpad_enter': 1073741912, 'tab': 9, 'DEL': 127, 'ESC': 27}
        # -------------------------------------
        # Below Line - Type: bool. The active variable that changes whether or not text input is active or inactive (True or False).
        self.text_input_active = False
        # Below Line - Type: bool. The active error variable. Whenever an exception is raised, this is changed to True until the player reads the message and then hits 'Enter'.
        self.error_input_active = False
        # Below Line - Type: bool. The multiple choice active variable. This is altered in progression.py in various locations whenever a player is being prompted with a multiple choice question. When active (True), the game searches for the newly created text rects so that they will be rendered on the screen, and the rects are up for being clicked on and detected in the self.event_handler(). Once a choice is made, the choice is assigned to self.chosen.mc, and this bool is changed back to False via the event_handler().
        self.multiple_choice_active = False
        # Below Line - Type: bool. The internal use variable for the calculated property self.choose_multiple_cards; used when the player has to choose multiple cards instead of just one. Allows the player to keep adding cards to the self.clicked_card_list as long as it is active (True).
        self._choose_multiple_cards = False
        # -------------------------------------
        # Below Section - Type: str. The text associated with all of the different, unchanging player names and card groups.
        self.p1_hand_text = (f'{player.P1.name}\'s Hand')
        self.p2_hand_text = (f'{player.P2.name}\'s Hand')
        self.p1_play_cards_text = (f'{player.P1.name}\'s Play Cards')
        self.p2_play_cards_text = (f'{player.P2.name}\'s Play Cards')
        self.p1_melds_text = (f'{player.P1.name}\'s Melds')
        self.p2_melds_text = (f'{player.P2.name}\'s Melds')
        self.p1_red_3_meld_text = (f'{player.P1.name}\'s Red 3 Meld')
        self.p2_red_3_meld_text = (f'{player.P2.name}\'s Red 3 Meld')
        # -------------------------------------
        # Below Section - Placeholders to avoid error. Assigned through progression_text.
        # Below Line - Type: str. Internal value; external use value is self.progression text calculated property which assigns the self.progression_text_obj & self.progression_text_obj_rect automatically. The actual text the game outputs in the main loop, assigned through various locations in progression.py.
        self._progression_text = ('What is your name?!?')
        self.progression_text_obj = None
        self.progression_text_obj_rect = None
        # Below Line - Placeholder. Accessed and changed within the self.progression_text calculated property. The prior self.progression_text_obj_rect to be compared against the current rect.
        self.prior_progression_text_obj_rect = None
        # -------------------------------------
        # Below Section - Placeholders to avoid 'NoneType' error. Accessed through self.text_obj_dict & assigned through the self.input_text calculated property every time it is altered (except for .get_rect() as that does not need to be changed every time it is updated. If that is done, it messes up the text display by 'recreating' another rect centered at a different location centered on it's new dimensions).
        # Below Line - Type: str. Internal value; external use value is self.input_text as a calculated property which assigns the self.input_text_obj & self.input_text_obj_rect automatically. The actual text the user inputs via processed keypresses in the main loop.
        self._input_text = ''
        # Below Line - Type: rendered string. Placeholder to avoid error. Assigned through self.input_text calculated property.
        self.input_text_obj = None
        # Below Line - Type: rect. Placeholder: Assigned through calculated property self.input_text. This rect's .center is slightly offset from self.progression_text_obj_rect.center inside the self.input_text calculated property.
        self.input_text_obj_rect = None
        # Below Line - Placeholder: The background 'outline' text box for the input display.
        self.input_text_outline_rect = None
        # Below Line - Type: str. The finished input string which is the 'returned' input. After the user finishes input / hits enter/return, this string copies the input_text before the input_text is reset back to a blank string, input_text_reset.
        self.input_text_final = 'Return this input...'
        # Below Line - Type: str. Assigned inside of the self.input_text calcualted property.
        self.prior_input_text = None
        # -------------------------------------
        # Below Line - Type: str? or rect? The variable that is the player's selected choice from among the multiple choice options. Assigned in various places in progression.py
        self.selected_choice = None
        # -------------------------------------
        # Below Section - Placeholders to avoid error. Assigned through calculated property self.multiple_choice_text_1.
        # Below Line - Type: string. Internal value for the calculated property self.multiple_choice_text_1. The text for the first multiple choice option.
        self._multiple_choice_text_1 = 'MC Text 1'
        self.multiple_choice_text_1_obj = None
        self.multiple_choice_text_1_obj_rect = None
        # Below Line - Placeholder. Accessed inside of self.multiple_choice_text_1 calculated property; the previous self.multiple_choice_text_1_obj_rect to be compared against the new one to determine whether or not the screen needs to be cleared for proper visual display in the case that the new rect is smaller than the old one.
        self.prior_multiple_choice_text_1_obj_rect = None
        # -------------------------------------
        # Below Section - Placeholders to avoid error. Assigned through calculated property self.multiple_choice_text_2.
        # Below Line - Type: string. Placeholder for the calculated property self.multiple_choice_text_1. The text for the first multiple choice option.
        self._multiple_choice_text_2 = 'MC Text 2'
        self.multiple_choice_text_2_obj = None
        self.multiple_choice_text_2_obj_rect = None
        # Below Line - Placeholder. Accessed inside of self.multiple_choice_text_2 calculated property; the previous self.multiple_choice_text_2_obj_rect to be compared against the new one to determine whether or not the screen needs to be cleared for proper visual display in the case that the new rect is smaller than the old one.
        self.prior_multiple_choice_text_2_obj_rect = None
        # -------------------------------------
        self.deck_text_obj = self.font.render('Deck', True, (255, 255, 255), self.dark_blue_color)
        self.deck_text_obj_rect = self.deck_text_obj.get_rect()
        self.deck_text_obj_rect.center = locations.Locate.text_name_loc_dict['Deck']
        # -------------------------------------
        self.discard_pile_text_obj = self.font.render('Discard Pile', True, (255, 255, 255), self.dark_blue_color)
        self.discard_pile_text_obj_rect = self.discard_pile_text_obj.get_rect()
        self.discard_pile_text_obj_rect.center = locations.Locate.text_name_loc_dict['Discard Pile']
        # -------------------------------------
        self.p1_hand_text_obj = self.font.render(self.p1_hand_text, True, (255, 255, 255), self.dark_blue_color)
        self.p1_hand_text_obj_rect = self.p1_hand_text_obj.get_rect()
        self.p1_hand_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_hand_text_loc']
        # -------------------------------------
        self.p2_hand_text_obj = self.font.render(self.p2_hand_text, True, (255, 255, 255), self.dark_blue_color)
        self.p2_hand_text_obj_rect = self.p2_hand_text_obj.get_rect()
        self.p2_hand_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_hand_text_loc']
        # -------------------------------------
        self.p1_play_cards_text_obj = self.font.render(self.p1_play_cards_text, True, (255, 255, 255), self.dark_blue_color)
        self.p1_play_cards_text_obj_rect = self.p1_play_cards_text_obj.get_rect()
        self.p1_play_cards_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_play_cards_text_loc']
        # -------------------------------------
        self.p2_play_cards_text_obj = self.font.render(self.p2_play_cards_text, True, (255, 255, 255), self.dark_blue_color)
        self.p2_play_cards_text_obj_rect = self.p2_play_cards_text_obj.get_rect()
        self.p2_play_cards_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_play_cards_text_loc']
        # -------------------------------------
        self.p1_melds_text_obj = self.font.render(self.p1_melds_text, True, (255, 255, 255), self.dark_blue_color)
        self.p1_melds_text_obj_rect = self.p1_melds_text_obj.get_rect()
        self.p1_melds_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_melds_text_loc']
        # -------------------------------------
        self.p2_melds_text_obj = self.font.render(self.p2_melds_text, True, (255, 255, 255), self.dark_blue_color)
        self.p2_melds_text_obj_rect = self.p2_melds_text_obj.get_rect()
        self.p2_melds_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_melds_text_loc']
        # -------------------------------------
        self.p1_red_3_meld_text_obj = self.font.render(self.p1_red_3_meld_text, True, (255, 255, 255), self.dark_blue_color)
        self.p1_red_3_meld_text_obj_rect = self.p1_red_3_meld_text_obj.get_rect()
        self.p1_red_3_meld_text_obj_rect.center = locations.Locate.text_name_loc_dict['p1_red_3_meld_text_loc']
        # -------------------------------------
        self.p2_red_3_meld_text_obj = self.font.render(self.p2_red_3_meld_text, True, (255, 255, 255), self.dark_blue_color)
        self.p2_red_3_meld_text_obj_rect = self.p2_red_3_meld_text_obj.get_rect()
        self.p2_red_3_meld_text_obj_rect.center = locations.Locate.text_name_loc_dict['p2_red_3_meld_text_loc']
        # -------------------------------------
        self.p1_player_name_text_obj = self.font.render(player.P1.name, True, (255, 255, 255), self.dark_blue_color)
        self.p1_player_name_text_obj_rect = self.p1_player_name_text_obj.get_rect()
        self.p1_player_name_text_obj_rect.left = locations.Locate.text_name_loc_dict['p1_player_name_text_loc'][0]
        self.p1_player_name_text_obj_rect.top = locations.Locate.text_name_loc_dict['p1_player_name_text_loc'][1]
        # -------------------------------------
        # Below Section - Placeholder / initial settings for below values. Values are changed and assigned through player.P2.name calculated property.
        self.p2_player_name_text_obj = self.font.render(player.P2.name, True, (255, 255, 255), self.dark_blue_color)
        self.p2_player_name_text_obj_rect = self.p2_player_name_text_obj.get_rect()
        self.p2_player_name_text_obj_rect.right = locations.Locate.text_name_loc_dict['p2_player_name_text_loc'][0]
        self.p2_player_name_text_obj_rect.top = locations.Locate.text_name_loc_dict['p2_player_name_text_loc'][1]
        # -------------------------------------
        ###### Below Line - This is currently not being used.
        # self.top_center_title = [locations.Locate.visible_center[0] - (round(self.deck_text_obj_rect[2] / 2)), locations.Locate.visible_top + 20]
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
                              self.p1_player_name_text_obj: self.p1_player_name_text_obj_rect,
                              self.p2_player_name_text_obj: self.p2_player_name_text_obj_rect,
                              self.progression_text_obj: self.progression_text_obj_rect,
                              self.input_text_obj: self.input_text_obj_rect,
                              self.multiple_choice_text_1_obj: self.multiple_choice_text_1_obj_rect,
                              self.multiple_choice_text_2_obj: self.multiple_choice_text_2_obj_rect}
        # -------------------------------------
        self.object_card_group_dict = {self.deck_text_obj: deck.MasterDeck.deck,
                              self.discard_pile_text_obj: deck.MasterDeck.discard_pile,
                              self.p1_hand_text_obj: player.P1.hand,
                              self.p2_hand_text_obj: player.P2.hand,
                              self.p1_play_cards_text_obj: player.P1.play_cards,
                              self.p2_play_cards_text_obj: player.P2.play_cards,
                              self.p1_melds_text_obj: player.P1.melds,
                              self.p2_melds_text_obj: player.P2.melds,
                              self.p1_red_3_meld_text_obj: player.P1.red_3_meld,
                              self.p2_red_3_meld_text_obj: player.P2.red_3_meld}
        # -------------------------------------
    # Below Section - Calculated property; whenever a value is set for this, make it calculate and assign the rect and it's center based on the size of the rect so that it will always properly display on the screen.
    @property
    def progression_text(self):
        return self._progression_text

    @progression_text.setter
    def progression_text(self, val):
        # Below Section - The prior values of the progression_text, to be compared against the new self.progression_text values to determine if the screen needs to be redrawn to overwrite the previous (larger) rect for proper visual display.
        if self.progression_text_obj != None:
            self.prior_progression_text_obj_rect = self.progression_text_obj_rect
        # -------------------------------------
        self._progression_text = val
        self.progression_text_obj = self.font.render(val, True, (255, 255, 255), self.dark_blue_color)
        self.progression_text_obj_rect = self.progression_text_obj.get_rect()
        self.progression_text_obj_rect.center = locations.Locate.text_name_loc_dict['progression_text_loc']
        # -------------------------------------
        if self.progression_text_obj != None and self.prior_progression_text_obj_rect != None and self.progression_text_obj_rect[2] < self.prior_progression_text_obj_rect[2]:
            pygame.draw.rect(self.screen_surface, self.background_color, (self.prior_progression_text_obj_rect[0] - 6, self.prior_progression_text_obj_rect[1] - 5, self.prior_progression_text_obj_rect[2] + 11, self.prior_progression_text_obj_rect[3] + 10))
            for current_card in self.card_group:
                current_card.dirty = 1
    # -------------------------------------
    # Below Section - Calculated property; whenever a value is set for this, make it calculate and assign the self.input_text_obj and self.input_text_obj_rect.center() so that it will always properly display on the screen.
    @property
    def input_text(self):
        return self._input_text

    @input_text.setter
    def input_text(self, val):
        self._input_text = val
        self.prior_input_text = self._input_text
        self.input_text_obj = self.font.render(val, True, (255, 255, 255), self.dark_blue_color)
        self.input_text_obj_rect = self.input_text_obj.get_rect()
        # Below Line - Have to have this if clause during testing using test_run.test_run() because the script does not call progression_text_func() as does the actual progression.the_draw_1() call eventual does subsequent to calling this calculated property. Can remove this later once testing is verified as working 100%.
        if self.progression_text_obj_rect != None:
            self.input_text_obj_rect.center = [self.progression_text_obj_rect.center[0], self.progression_text_obj_rect.center[1] + 40]
    # -------------------------------------
    @property
    def multiple_choice_text_1(self):
        return self._multiple_choice_text_1

    @multiple_choice_text_1.setter
    def multiple_choice_text_1(self, val):
        self.prior_multiple_choice_text_1_obj_rect = self.multiple_choice_text_1_obj_rect
        # -------------------------------------
        self._multiple_choice_text_1 = val
        self.multiple_choice_text_1_obj = self.font.render(val, True, (255, 255, 255), self.dark_blue_color)
        self.multiple_choice_text_1_obj_rect = self.multiple_choice_text_1_obj.get_rect()
        if self.progression_text_obj_rect != None:
            self.multiple_choice_text_1_obj_rect.center = [self.progression_text_obj_rect.center[0], self.progression_text_obj_rect.center[1] + 40]
        if self.prior_multiple_choice_text_1_obj_rect != None:
            if self.multiple_choice_text_1_obj_rect[2] < self.prior_multiple_choice_text_1_obj_rect[2]:
                pygame.draw.rect(self.screen_surface, self.background_color, (self.prior_multiple_choice_text_1_obj_rect[0] - 6, self.prior_multiple_choice_text_1_obj_rect[1] - 5, self.prior_multiple_choice_text_1_obj_rect[2] + 11, self.prior_multiple_choice_text_1_obj_rect[3] + 10))
                for current_card in self.card_group:
                    current_card.dirty = 1
    # -------------------------------------
    @property
    def multiple_choice_text_2(self):
        return self._multiple_choice_text_2

    @multiple_choice_text_2.setter
    def multiple_choice_text_2(self, val):
        self.prior_multiple_choice_text_2_obj_rect = self.multiple_choice_text_2_obj_rect
        # -------------------------------------
        self._multiple_choice_text_2 = val
        self.multiple_choice_text_2_obj = self.font.render(val, True, (255, 255, 255), self.dark_blue_color)
        self.multiple_choice_text_2_obj_rect = self.multiple_choice_text_2_obj.get_rect()
        if self.multiple_choice_text_1_obj != None:
            self.multiple_choice_text_2_obj_rect.center = [self.multiple_choice_text_1_obj_rect.center[0], self.multiple_choice_text_1_obj_rect.center[1] + 40]
        if self.prior_multiple_choice_text_2_obj_rect != None:
            if self.multiple_choice_text_2_obj_rect[2] < self.prior_multiple_choice_text_2_obj_rect[2]:
                pygame.draw.rect(self.screen_surface, self.background_color, (self.prior_multiple_choice_text_2_obj_rect[0] - 6, self.prior_multiple_choice_text_2_obj_rect[1] - 5, self.prior_multiple_choice_text_2_obj_rect[2] + 11, self.prior_multiple_choice_text_2_obj_rect[3] + 10))
                for current_card in self.card_group:
                    current_card.dirty = 1
    # -------------------------------------
    # Below Section - Calculated property which assigns the value to the internal variable _choose_multiple_cards & clears the self.clicked_card_list so that it is cleared  when val == False for next time it is activated
    @property
    def choose_multiple_cards(self):
        return self._choose_multiple_cards

    @choose_multiple_cards.setter
    def choose_multiple_cards(self, val):
        self._choose_multiple_cards = val
        if val == False:
            self.clicked_card_list.clear()
            self.clickable_card_list.clear()
    # -------------------------------------
    # Below Function - Creates a border rect for better looking text display areas. Takes in a rect and creates the border from it's dimensions.
    def create_border_rect(self, rect):
        new_rect = pygame.Rect(rect[0] - 3, rect[1] - 3, rect[2] + 7, rect[3] + 7)
        pygame.draw.rect(self.screen_surface, self.dark_blue_color, new_rect)
        pygame.draw.rect(self.screen_surface, self.black_color, (rect[0] - 6, rect[1] - 5, rect[2] + 11, rect[3] + 10), 3)
    # -------------------------------------
    # Below Function - Handles all events for pygame. Called by the various draw_window() functions.
    def event_handler(self):
        # print("event_handler")
        # -------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Below Section - Quits the pygame window and terminates the entire program.
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.click_card_active == True:
                # Below Section - Whenever clicking a card; detects if the card was clicked, and appends it to clicked_card_list.
                self.clicked_card = None
                clicked_a_card = False
                for card in self.clickable_card_list:
                    if card.rect.collidepoint(event.pos):
                        clicked_a_card = True
                        card.pos_y_dist_to_card_top = event.pos[1] - card.rect.top
                        self.collided_cards_dict[card.pos_y_dist_to_card_top] = card
                if clicked_a_card == True:
                    if self.clicked_card == None:
                        self.clicked_card = self.collided_cards_dict[min(self.collided_cards_dict.keys())]
                        self.collided_cards_dict.clear()
                        self.clicked_card.highlighted = True
                        if self.choose_multiple_cards == True:
                            self.clicked_card_list.append(self.clicked_card)
                        else:
                            self.click_card_active = False
                            self.clickable_card_list.clear()
                            # Below Section - For the cases when a player has to choose from multiple card/meld options and the option to not use any card at all by clicking a multiple_choice_text rect. This will change the multiple_choice_text to False in the instance that they choose a card/meld instead, and visa versa in the other instance's code block.
                            if self.multiple_choice_active == True:
                                self.multiple_choice_active = False
                # -------------------------------------
            # Below Section - For clicking both of the multiple_choice_text rects (1 & 2) whenever the player is prompted with a multiple choice option.
            if event.type == pygame.MOUSEBUTTONDOWN and self.multiple_choice_active == True:
                for rect in [self.multiple_choice_text_1_obj_rect, self.multiple_choice_text_2_obj_rect]:
                    if rect.collidepoint(event.pos):
                        if rect == self.multiple_choice_text_1_obj_rect:
                            self.selected_choice = self.multiple_choice_text_1
                        else:
                            self.selected_choice = self.multiple_choice_text_2
                        ###### Below Line - Don't have this coded yet, but maybe want to make it so that the rect will become highlighted whenever a player clicks on it.
                        ###### self.selected_choice.highlighted = True
                        self.multiple_choice_active = False
                        # Below Section - For the case in which the player is choosing multiple cards and is finalizing their selections; changes self.click_card_active to False (as it remains active while self.multiple_choice_active == True).
                        if self.click_card_active == True:
                            self.click_card_active = False
            # -------------------------------------
            if event.type == pygame.KEYDOWN:
                if self.text_input_active == True:
                    # Below Section - Filters out keypresses from self.invalid_keypress_dict that do not have a proper visual display, but instead show as a 'rectangle' as the visual input value.
                    if event.key in self.invalid_keypress_dict.values():
                        pass
                    # -------------------------------------
                    elif event.key == pygame.K_RETURN:
                        self.text_input_active = False
                        self.input_text_final = self.input_text
                        self.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
                elif self.error_input_active == True:
                    if event.key == pygame.K_RETURN:
                        self.error_input_active = False
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Below Function - Called by progression.py in various locations. Used to display a progression_text output for 3 seconds so the player has time to read the message.
    def xs_display(self, num):
        # print('xs_display')
        prior_time = time.time()
        current_time = 0
        while (current_time - prior_time) < num:
            self.draw_window_main()
            current_time = time.time()
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Below Function - Called by locations.Locations.card_movement() via draw_window_main()(). Handles framerate, event handling, and updating display.
    def draw_window_main(self, reset = False):
        # print("draw_window_main")
        # -------------------------------------
        # Below Line - Calls the event handler which handles all events as if through a while loop.
        self.event_handler()
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
                              self.p1_player_name_text_obj: self.p1_player_name_text_obj_rect,
                              self.p2_player_name_text_obj: self.p2_player_name_text_obj_rect,
                              self.progression_text_obj: self.progression_text_obj_rect,
                              self.input_text_obj: self.input_text_obj_rect,
                              self.multiple_choice_text_1_obj: self.multiple_choice_text_1_obj_rect,
                              self.multiple_choice_text_2_obj: self.multiple_choice_text_2_obj_rect}
        # Below Line - A list of all of the text objects' keys; the surfaces (The values of the dict are the rects).
        text_obj_dict_keys_list = list(self.text_obj_dict.keys())
        # -------------------------------------
        if self.game_state == 'main':
            # Below Section - Handles the rendering of the card group info text and the associated surfaces.
            for obj in text_obj_dict_keys_list[0:10]:
                if obj != None:
                    if len(self.object_card_group_dict[obj]) != 0:
                        self.create_border_rect(self.text_obj_dict[obj])
                        self.screen_surface.blit(obj, self.text_obj_dict[obj])
            # Below Line - Draws the dividing line on the middle of the screen. Note: This has to go below self.card_group.update() & self.card_rects = self.card_group.draw(self.screen_surface) or it will not display on the screen surface.
            pygame.draw.line(self.screen_surface, self.black_color, [locations.Locate.visible_center[0] - 1, locations.Locate.visible_top], [locations.Locate.visible_center[0] - 1, locations.Locate.visible_bottom], 2)
        # -------------------------------------
        if self.game_state == 'the_draw_1':
            # Below Line - Blits (draws onto another surface) the background (Surface) to the background.rect (Rect).
            self.screen_surface.blit(self.background, self.background.get_rect())
        # -------------------------------------
        else:
            # Below Line - Updates the sprites rect locations for each frame. If this is not run, the cards simply teleport from the start location > the final location in card_movement() without any gradual movement.
            self.card_group.update()
            # Below Line - Calls the LayeredDirty draw() method which ensures the cards are updated; draws all sprites in the right order onto the passed surface.
            self.card_rects = self.card_group.draw(self.screen_surface)
        # -------------------------------------
        # Below Section - Handles the rendering of the player names.
        for obj in text_obj_dict_keys_list[10:12]:
            self.create_border_rect(self.text_obj_dict[obj])
            self.screen_surface.blit(obj, self.text_obj_dict[obj])
        # -------------------------------------
        # Below Section - Handles the rendering of the progression_text_obj/rect.
        if self.progression_text_obj != None:
            self.create_border_rect(self.progression_text_obj_rect)
            self.screen_surface.blit(self.progression_text_obj, self.progression_text_obj_rect)
        # -------------------------------------
        # Below Section - Handles the rendering of the input_text_obj and the input_text_surface.
        if self.input_text_obj != None and self.input_text != '':
            self.create_border_rect(self.input_text_obj_rect)
            self.screen_surface.blit(self.input_text_obj, self.input_text_obj_rect)
        # -------------------------------------
        # Below Section - Handles the rendering of the multiple_choice_text_1_obj and the associated surface.
        if self.multiple_choice_text_1_obj != None:
            self.create_border_rect(self.multiple_choice_text_1_obj_rect)
            self.screen_surface.blit(self.multiple_choice_text_1_obj, self.multiple_choice_text_1_obj_rect)
        # -------------------------------------
        # Below Section - Handles the rendering of the multiple_choice_text_2_obj and the associated surface.
        if self.multiple_choice_text_2_obj != None:
            self.create_border_rect(self.multiple_choice_text_2_obj_rect)
            self.screen_surface.blit(self.multiple_choice_text_2_obj, self.multiple_choice_text_2_obj_rect)
        # -------------------------------------
        # Below Line - Updates the display to reflect the new game information. This is required for the input text to properly display on the screen. If it is not called, input text only displays after it has been blitted over by a card or something.
        pygame.display.update()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
game = Game()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
