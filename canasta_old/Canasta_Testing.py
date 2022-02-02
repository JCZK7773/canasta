# string = "1"
# string_list = list(string)
#
# for item in string_list:
#     item = int(item)
#     print(type(item))
#     if type(item) == int:
#         print("int type")
#     else:
#         print("else")

# list_num = [0, 1]
#
# print(list_num[-1])
# print(list_num[-2])

# melds = [("ONE", "BLUE"), ("TWO", "GREEN"), ("THREE", "RED")]
#
# for item in melds:
#     if "ONE" in item:
#         print("in")
#     else:
#         print("out")

# list = [11,12,13,14,15]
#
# for num in range(len(list)):
#     print(num)

#
# discard_preparing = ("Which card would you like to discard? Your available cards in hand are: " + ', '.join(['%s']*len(list)) + "") % tuple(list)
# print(discard_preparing)
# for item in discard_preparing.split():
#     if "%" in item:
#         print("%")
#     else:
#         print("no")

# discard_preparing = ("Which card would you like to discard? Your available cards in hand are: " + ', '.join(['%s']*len(list)) + "")
# COULD I JUST MAKE IT SO THAT THERE IS A DOUBLE ITERATION THAT GRABS EACH NUM AS "NUM)" (i.e. "1) ", "2) )" FOR LEN OF (LIST OF "%s"), WHILE ALSO GRABBING EACH "%s" AND JOINING IT TO THE STRING. EXAMPLE CODE BELOW.
# FOR LEN(LIST)

# list = []
#
# for item in list:
#     for items in item:
#         if items:
#             print("Iteration")
#         else:
#             print("Else")
#
# print(list)


# # ------------------------------------------
# def discard(player):
#     # Stems (#2) from Play_2. For discarding.
#     # discard_d = ("Which card would you like to discard? Your available cards in hand are: " + ', '.join(['%s']*len(player.hand)) + "")
#     print("discard")
#     print("Which card would you like to discard? Your available cards in hand are: ")
#     discard_prep = ("" + ', '.join(['%s']*len(player.hand)) + "")
#     discard_prep = discard_prep.split()
#     num = 0
#     for word in discard_prep:
#         num += 1
#         discard_prep[discard_prep.index(word)] = "{num}) %s".format(num = str(num))
#     discard_prep = (" ".join(discard_prep) + "\n\n")
#     discard_input = int(input(discard_prep % tuple(player.hand))) - 1
#     print("You discarded the {discard}.".format(discard = player.hand[discard_input]))
#     MasterDeck.discard_pile.append(player.hand.pop(discard_input))
# # ------------------------------------------


# # # ------------------------------------------
# def discard(player):
#     # Stems (#2) from Play_2. For discarding.
#     print("discard")
#     discard_prep = ("Which card would you like to discard? Your available cards in hand are: " + ', '.join(['%s']*len(player.hand)) + "")
#     discard_prep = discard_prep.split()
#     num = 0
#     for word in discard_prep:
#         if "%" in word:
#             num += 1
#             discard_prep[discard_prep.index(word)] = "{num}) %s".format(num = str(num))
#     discard_prep = (" ".join(discard_prep) + "\n\n")
#     discard_input = int(input(discard_prep % tuple(player.hand))) - 1
#     print("You discarded the {discard}.".format(discard = player.hand[discard_input]))
#     MasterDeck.discard_pile.append(player.hand.pop(discard_input))
# # # ------------------------------------------


# # # # ------------------------------------------
# items = [0,1,2,3,4,5,6,7,7,8,10]
# list_of_lists = []
# def create_lists():
#     list = []
#     list.append(items[0])
#     list_of_lists.append(list)
# create_lists()
# create_lists()
# print(list_of_lists)
# if items[0] in lists in list_of_lists:
#     print("in")
# # # # ------------------------------------------

# # # # ------------------------------------------
# items = [0,1,2,3,4,5,6,7,7,8,10]
# object_list = [0,1,2,3,4]
# for object in object_list:
#     items.remove(object)
# print(items)
# # # # ------------------------------------------


# # # # # ------------------------------------------
#   File "Canasta.py", line 434, in valid_play_check_and_sort
#     temp_melds_removed_black_3s_str = ("Sorry, but you cannot play Black 3(s) in this way. Black 3s can only be used to freeze the discard pile. The Black 3(s) that are being removed from your attempted play cards back into your hand are as follows:") + ', '.join('%s') * len(temp_melds_removed_black_3s) % tuple(temp_melds_removed_black_3s)
# ValueError: unsupported format character ',' (0x2c) at index 1
# # # # # ------------------------------------------


# # # # # # ------------------------------------------
# wild_card_num = 1
# for wild_card in player.play_cards_wild_cards:
#     if wild_card == player.play_cards_wild_cards[-1]:
#         print("{wild_card_num}) {wild_card}\n".format(wild_card_num = wild_card_num, wild_card = wild_card))
#     else:
#         print("{wild_card_num}) {wild_card}".format(wild_card_num = wild_card_num, wild_card = wild_card))
#     wild_card_num += 1
#
# list = ['two','cheese','dog','blank','know']
#
# def iterated_list_string_num_counter(passed_list):
#     num = 1
#     for item in passed_list:
#         if item == passed_list[-1]:
#             print("{num}) {item}\n".format(num = num, item = item))
#         else:
#             print("{num}) {item}".format(num = num, item = item))
#         num += 1
#
# iterated_list_string_num_counter(list)
# # # # # # ------------------------------------------


# # # # # # # ------------------------------------------
# a_list = [0,1,2,3,4,5]
#
# new_list = []
#
# for item in a_list[:]:
#     new_list.append(a_list.pop(a_list.index(item)))
# print(new_list)
# # # # # # # ------------------------------------------


# # # # # # # ------------------------------------------
# card_rank_num_range = range(2,11)
# for num in card_rank_num_range:
#     print(str(num))
# # # # # # # # ------------------------------------------


# # # # # # # # # ------------------------------------------
# a_list = ['0','1','2','3','4','5']
# for item in enumerate(a_list):
#     index = item[0]
#     content = item[1]
#     print(index, content)
# # # # # # # # # ------------------------------------------

# # # # # # # # # ------------------------------------------
# class Card():
#     def __init__(self, rank, suit):
#         self.rank = rank
#         self.suit = suit
# # # # # # # # # ------------------------------------------


# # # # # # # # # ------------------------------------------
# def func():
#     cheese = int(input("\n")) - 1
#     print(cheese)
#     return cheese
#
# def bigger_func():
#     result = func()
#     if result == 1:
#         print("1")
#     else:
#         print("not 1")
#
# bigger_func()
# # # # # # # # # ------------------------------------------


# # # # # # # # # ------------------------------------------
# list = []
# for item in list:
#     print("here")
# print('ran')
# # # # # # # # # ------------------------------------------


# # # # # # # # # # ------------------------------------------
# for item in range(10):
#     print(item)
# # # # # # # # # # ------------------------------------------


# # # # # # # # # # ------------------------------------------
# list = ["a","b","c","d","e","f","g"]
# for item in range(len(list)):
#     print(item)
# # # # # # # # # # ------------------------------------------


# # # # # # # # # # ------------------------------------------
# list_1 = [0,1,2,3,4,5,6,7,8,9,10]
# for item in list_1[:]:
#     print(list_1.pop(0))
#     print(list_1)
# # # # # # # # # # ------------------------------------------


# # # # # # # # # # # ------------------------------------------
# diction = {'a':1, 'b':2, 'c':3, 'd':4}
# print(diction['a'])
# # # # # # # # # # # ------------------------------------------


# # # # # # # # # # # ------------------------------------------
# input = input("> ")
# print(type(input))
# for char in input:
#     print(char)
# if char == '1':
#     print("True")
# # # # # # # # # # # ------------------------------------------


# # # # # # # # # # # ------------------------------------------
# list_1 = [0,1,2,3,4,5,6]
# print(list_1[7])

# input_1 = int(input("> "))
# print(input_1)
# # # # # # # # # # # ------------------------------------------


# # # # # # # # # # # ------------------------------------------
# for x in range(2):
#     print(x)
# # # # # # # # # # # ------------------------------------------


# # # # # # # # # # # ------------------------------------------
# melds_1 = [0,1,2]
# melds_2 = [3,4,5]
# for meld_group in [melds_1, melds_2]: # ****
#     for item in meld_group:
#         print(item)


# # # # # # # # # # # # ------------------------------------------
# class aClass():
#     def __init__(self):
#         None
#
#     def __str__(self):
#         return ("__str__")
#
#     def __repr__(self):
#         return 1 < 0
#
# aClass_1 = aClass()
#
# print(aClass_1)
#
# print(repr(aClass_1 ))
# # # # # # # # # # # ------------------------------------------


# # # # # # # # # # # ------------------------------------------
# list_1 = ['0','1','2','3','4','5']
# for item in list_1[:]:
#     list_1.pop(item)
# print(list_1)
# # # # # # # # # # # ------------------------------------------


# # # # # # # # # # # ------------------------------------------
# def func():
#     while True:
#         print("a")
#         return
# func()
# # # # # # # # # # # ------------------------------------------
