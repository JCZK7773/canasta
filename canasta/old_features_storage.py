# Below Function - Called by main(). Handles screen background assignment, card_group draw updating, and the pygame.display updates.
# def draw_window():
#     # print("draw_window")
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN and game.game.click_card_active == True:
#             ###### Below Section - Needs to be finished. For whenever clicking a card, for detecting if the card was clicked, and saving it as a value to be accessed elsewhere for reference.
#             for card in game.game.clickable_card_group:
#                 if card.collidepoint(event.pos):
#                     game.game.clicked_card = card
#                     game.game.clicked_card.highlighted = True
#             ###### -------------------------------------
#         elif event.type == pygame.KEYDOWN and game.game.text_input_active == True:
#             if event.key == pygame.K_RETURN:
#                 game.game.text_input_active = False
#                 game.game.input_text_final = game.game.input_text
#                 game.game.input_text = game.game.input_text_reset
#             elif event.key == pygame.K_BACKSPACE:
#                 game.game.input_text = game.game.input_text[:-1]
#             else:
#                 game.game.input_text += event.unicode
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
    # game.game.card_group.update()
    # game.game.card_rects = game.game.card_group.draw(game.game.screen_surface)
    # game.game.screen.update(game.game.card_rects)
    # -------------------------------------
    # Below Line - Note: This has to go below game.game.card_group.update() & game.game.card_rects = game.game.card_group.draw(game.game.screen_surface) or it will not display on the screen surface.
    # pygame.draw.line(game.game.screen_surface, game.game.black_color, [locations.Locate.visible_center[0] - 1, locations.Locate.visible_top], [locations.Locate.visible_center[0] - 1, locations.Locate.visible_bottom], 2)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# def card_movement(self, loc, current_card):
#     print("card_movement")
#     # Below Section - For testing. Trying to find the cause of inconsistent card movement times.
#     prior_time = time.time()
#     # -------------------------------------
#     current_card.display_layer = 9999
#     # -------------------------------------
#     x_difference = 0
#     y_difference = 0
#     # -------------------------------------
#     y_lesser = None
#     x_lesser = None
#     # -------------------------------------
#     if current_card.x < loc[0]:
#         x_difference = loc[0] - current_card.x
#         x_lesser = True
#     elif current_card.x > loc[0]:
#         x_difference = current_card.x - loc[0]
#         x_lesser = False
#     if current_card.y < loc[1]:
#         y_difference = loc[1] - current_card.y
#         y_lesser = True
#     elif current_card.y > loc[1]:
#         y_difference = current_card.y - loc[1]
#         y_lesser = False
#     # -------------------------------------
#     outer_break = False
#     if x_difference > y_difference:
#         greater_difference = x_difference
#         lesser_difference = y_difference
#         one_coord = current_card.x
#         one_lesser = x_lesser
#         one_loc = loc[0]
#         ratio_coord = current_card.y
#         ratio_lesser = y_lesser
#         ratio_loc = loc[1]
#     elif y_difference > x_difference:
#         greater_difference = y_difference
#         lesser_difference = x_difference
#         one_coord = current_card.y
#         one_lesser = y_lesser
#         one_loc = loc[1]
#         ratio_coord = current_card.x
#         ratio_lesser = x_lesser
#         ratio_loc = loc[0]
#     # Below Section - For the rare instance when both the current x & y coordinates are the same distance from the final location's x & y coordinates.
#     elif int(y_difference) == int(x_difference):
#         outer_break = True
#         while [int(current_card.x), int(current_card.y)] != loc:
#             if x_lesser == True:
#                 current_card.x += 1
#             else:
#                 current_card.x -= 1
#             if y_lesser == True:
#                 current_card.y += 1
#             else:
#                 current_card.y -= 1
#             game.draw_window()
#     # -------------------------------------
#     if outer_break == True:
#         return None
#     else:
#         ratio = round((lesser_difference / greater_difference), 2)
#         # -------------------------------------
#         while [int(current_card.x), int(current_card.y)] != loc:
#             print("while")
#             if one_lesser == True and int(one_coord) != int(one_loc):
#                 one_coord += 1
#             elif one_lesser == False and int(one_coord) != int(one_loc):
#                 one_coord -= 1
#             if ratio_lesser == True and int(ratio_lesser) != int(ratio_loc):
#                 prior_ratio_coord = ratio_coord
#                 ratio_coord += ratio
#                 current_ratio_coord = ratio_coord
#                 if int(prior_ratio_coord) < int(current_ratio_coord):
#                     print(one_coord, ratio_coord)
#                     print(current_card.x, current_card.y)
#                     print("draw 1")
#                     game.draw_window()
#             elif ratio_lesser == False and int(ratio_coord) != int(ratio_loc):
#                 prior_ratio_coord = ratio_coord
#                 ratio_coord -= ratio
#                 current_ratio_coord = ratio_coord
#                 if int(prior_ratio_coord) > int(current_ratio_coord):
#                     print("draw 2")
#                     game.draw_window()
#             if ratio_lesser == None:
#                 # Below Line -  Added for the instance in which the y-coordinate is == final y-coordinate, but x-coordinate still needs to be changed.
#                 print("draw 3")
#                 game.draw_window()
#         # -------------------------------------
#         # Below Section - For testing. Trying to figure out the cause of inconsistent times for card movements.
#         current_time = time.time()
#         print(round(current_time - prior_time, 2))
# # -------------------------------------




###### Below Section - I THINK I CAN REMOVE THIS AS I HAVE MOVED THIS CODE BLOCK TO BE RUN EVERY TIME progression_text IS UPDATED IF THE VAL IS SMALLER THAN PREVIOUS VAL. Trying to make it so that the progression_text & rect are 'erased' from the screen so that it doesn't leave behind changed pixels after the fact.
# Below Secion - Fixes issue by redrawing the background and all of the cards. I believe there is a more proper way to do this, though.
# for card in game.game.card_group:
#     card.dirty = 1
# -------------------------------------
# Below Section - Does not fix the issue. For reference so I don't try this stuff again.
# game.game.screen_surface.blit(game.game.background, game.game.background.get_rect())
# game.game.card_rects = game.game.card_group.draw(game.game.screen_surface)
# pygame.display.update()
###### -------------------------------------




# Below Function - NO LONGER NEEDED IN 2D VERSION. Called by sorted_and_numbered_list_printer(). To be used as a sorter key function which orders the cards in ascending order based on card rank. # ****
# def sorter_key_function(item): # ****
#     # Below - If item is a Card (not a list or tuple). # ****
#     if type(item) != list: # ****
#         int_suit = MasterDeck.draw_suit_ranks.get(item.suit)
#         if item.rank != 'Joker': # ****
#             int_rank = MasterDeck.draw_ranks.get(item.rank) # ****
#             final_value = int(str(int_rank) + str(int_suit)) # ****
#             return final_value # ****
#         else: # ****
#             final_value = int(str(1) + str(int_suit)) # ****
#             return final_value # ****
#     # Below - If item is a meld (list). # ****
#     else: # ****
#         if item[0].rank != 'Joker': # ****
#             int_rank = MasterDeck.draw_ranks.get(item[0].rank) # ****
#             return int_rank # ****
#         else: # ****
#             return int(1) # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




###### Below Function - NO LONGER NEEDED IN 2D VERSION. Not sure I will continue to use this in the 2D version of the game. Called by play_1(), draw_discard_pile_attempt_temp_meld_wild_card_addition(), play_2(), valid_play_check_and_sort(), wild_card_meld_choice_prompt(), discard(), went_out_check() functions. Miscellaneous function for handling printed lists that I want to be sorted and then numbered; for the purpose of input choice selection via the preceding num. # ****
# def sorted_and_numbered_list_printer(passed_list_1, passed_list_2 = None): # ****
#     logger.debug("sorted_and_numbered_list_printer\n") # ****
#     # -------------------------------------
#     passed_list_1.sort(key=sorter_key_function) # ****
#     # -------------------------------------
#     num = 1 # ****
#     for item in passed_list_1: # ****
#         # -------------------------------------
#         # Below Line - Strictly for the purpose of testing.
#         testing_register_list.append(item)
#         # -------------------------------------
#         if item != passed_list_1[-1]: # ****
#             print(f"{num}) {item}") # ****
#         else: # ****
#             print(f"{num}) {item}\n") # ****
#         num += 1 # ****
#         # -------------------------------------
#     if passed_list_2 != None: # ****
#         passed_list_2.sort(key=sorter_key_function) # ****
#         for item in passed_list_2: # ****
#             if item != passed_list_2[-1]: # ****
#                 print(f"{num}) {item}") # ****
#             else: # ****
#                 print(f"{num}) {item}\n") # ****
#             num += 1 # ****
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
