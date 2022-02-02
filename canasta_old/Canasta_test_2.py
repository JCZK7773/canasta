# input = input("Select some numbers")
# for char in input:
#     print(char)
#     if type(char) == int:
#         print(char)
#     else:
#         pass
# ---------------------------------------------------
# wild_cards_loc = ['card1', 'card2', 'card3', 'card4']
#
# s = ("Which wild card would you like to use? You have these wild cards: " + ', '.join(['%s']*len(wild_cards_loc)) + "") % tuple(wild_cards_loc)
# g = input(s)

# wild_card = input("Which wild card would you like to use? You have these wild cards: "+', '.join(['%s']*len(wild_cards_loc))+"") % tuple(wild_cards_loc)

# wild_card_str = ("Which wild card would you like to use? You have these wild cards:")
#
# ', '.join('%'*len(wild_cards_loc))
# ---------------------------------------------------
# print s % tuple(x)

# Following this resource page, if the length of x is varying, we can use:
#
# ', '.join(['%.2f']*len(x))
# to create a place holder for each element from the list x. Here is the example:
#
# x = [1/3.0, 1/6.0, 0.678]
# s = ("elements in the list are ["+', '.join(['%.2f']*len(x))+"]") % tuple(x)
# print s
# >>> elements in the list are [0.33, 0.17, 0.68]
#
# >>> s = '{0} BLAH BLAH {1} BLAH {2} BLAH BLIH BLEH'
# >>> x = ['1', '2', '3']
# >>> print s.format(*x)
# '1 BLAH BLAH 2 BLAH 3 BLAH BLIH BLEH'
#
# @kotchwane : the * function is a special python keyword that transform an argument that is a list into a list of arguements :). In our case, *x will pass to the format method the 3 members of x. – Cédric Julien Nov 16
#
# sample_list = ['cat', 'dog', 'bunny', 'pig']
# print("Your list of animals are: {}, {}, {} and {}".format(*sample_list))
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ LINK TO ABOVE
# https://stackoverflow.com/questions/7568627/using-python-string-formatting-with-lists
