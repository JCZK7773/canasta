import player
import deck
import locations
import card
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Class - Customized list class which is used to call a particular function whenever the sub-classed list .append method is called, for the purpose of visually updating card locations by updating the card coordinate via the function call.
class CustomAppendList(list):
    def __init__(self, card_group_name):
        self.card_group_name = card_group_name
        self.list_location = [0, 0]
        super().__init__()
    # -------------------------------------
    @property
    def meld_num(self):
        list_index = locations.Locate.card_group_name_dict[self.card_group_name].index(self)
        return list_index
    # -------------------------------------
    def append(self, item):
        super(CustomAppendList, self).append(item)
        if self.card_group_name in locations.Locate.meld_group_dict.keys():
            if type(item) == CustomAppendList:
                # Below Line - Do I even need this for any instance????? I think I used for testing purposes, but unsure if needed in actual game.
                # if item in item.meld_group_list[item.card_group]:
                locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, len(self) - 1)
            elif type(item) == card.Card: # If it is a Card (For instances such as when a card is being added to a preexisting meld).
                # Below line - For when a meld is created for an intended location, but has not been placed there yet.
                if self in locations.Locate.card_group_name_dict[self.card_group_name]:
                    print("card.Card *********")
                    locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, self.meld_num, len(self) - 1)
                else:
                    print("else")
            # Below Line - For the case where type(item) == list (A built-in, non-custom, standard list). Made this for testing purposes. Unsure if necessary for actual game. DO I NEED THIS? IF SO, NEED TO CHANGE LOCATIONS TO INCLUDE 'ELIF TYPE(ITEM) == LIST'.
            # elif type(item) == list:
            #     print("list")
            #     locations.Locate.func_dict[(self.card_group)](item)
        elif 'hand' in self.card_group_name:
                locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item)
        else:
            locations.Locate.func_dict[(self.card_group_name)](item)
