# class Locations():
#     def __init__(self):
#         pass
#
#     def funct_1(self):
#         print("1")
#
#
# Locate = Locations()
#
#
# func_dict = {'MasterDeck': Locate.funct_1}
#
#
# class OverrideAppendList(list):
#     def __init__(self, name):
#         self.name = name
#
#     def append(self, item):
#         if self.name in func_dict:
#             func_dict[self.name]()
#             func_dict[self.name]()
#         super().append(item)
#
#
# class Deck():
#     def __init__(self):
#         self.MasterDeck = OverrideAppendList('MasterDeck')
#
#
# Deck_1 = Deck()
#
#
# Deck_1.MasterDeck.append(4)
# Deck_1.MasterDeck.pop(-1)
# Deck_1.MasterDeck.append(4)

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
