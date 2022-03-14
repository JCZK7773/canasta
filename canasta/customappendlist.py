import player
import deck
import locations
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Class - Customized list class which is used to call a particular function whenever the sub-classed list .append method is called, for the purpose of visually updating card locations by updating the card coordinate via the function call.
class CustomAppendList(list):
    def __init__(self, card_group_name):
        self.card_group_name = card_group_name
        self.meld_group_name_dict = {'p1_play_cards': player.P1.play_cards, 'p2_play_cards': player.P2.play_cards, 'p1_melds': player.P1.melds, 'p2_melds': player.P2.melds, 'p1_red_3_meld': player.P1.red_3_meld, 'p2_red_3_meld': player.P2.red_3_meld}
        self.list_location = [0, 0]
        super().__init__()
    # -------------------------------------
    @property
    def meld_num(self):
        list_index = self.meld_group_name_dict[self.card_group_name].index(self)
        return list_index

    def append(self, item):
        super(CustomAppendList, self).append(item)
        if self.card_group_name in self.meld_group_name_dict:
            if item in self.meld_group_name_dict[self.card_group_name]:
                print("in meld_group_name_dict")
                locations.Locate.func_dict[(self.card_group_name)](item, len(self), self.meld_num)
            else:
                print(item)
                print(self.meld_group_name_dict[self.card_group_name])
                print("else")
        else:
            print("elseelse")
            locations.Locate.func_dict[(self.card_group_name)](item)
