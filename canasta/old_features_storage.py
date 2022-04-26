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
