import pygame
import player
import deck
import locations
import card
import canasta_pygame
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Class - Customized list class which is used to call a particular function whenever the sub-classed list .append method is called, for the purpose of visually updating card locations by updating the card coordinate via the function call.
class CustomAppendList(list):
    def __init__(self, card_group_name):
        self.card_group_name = card_group_name
        self.list_location = [0, 0]
        super().__init__()
    # -------------------------------------
    # Below Section - ...
    @property
    def meld_num(self):
        list_index = player.Player.meld_group_dict[self.card_group_name].index(self)
        return list_index
    # -------------------------------------
    # Below Section - ...
    def append(self, item):
        super(CustomAppendList, self).append(item)
        locations.Locate.card_group_name_dict = {'deck': deck.MasterDeck.deck, 'discard_pile': deck.MasterDeck.discard_pile, 'P1.hand': player.P1.hand, 'P2.hand': player.P2.hand, 'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds, 'P1.red_3_meld': player.P1.red_3_meld, 'P2.red_3_meld': player.P2.red_3_meld}
        locations.Locate.card_group_loc_dict = {'P1.hand': locations.Locate.p1_hand_next_loc, 'P2.hand': locations.Locate.p2_hand_next_loc, 'P1.play_cards': locations.Locate.p1_play_cards_start_loc, 'P2.play_cards': locations.Locate.p2_play_cards_start_loc, 'P1.melds': locations.Locate.p1_melds_start_loc, 'P2.melds': locations.Locate.p2_melds_start_loc}
        player.Player.meld_group_dict = {'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds, 'P1.red_3_meld': player.P1.red_3_meld, 'P2.red_3_meld': player.P2.red_3_meld}
        if self.card_group_name in player.Player.meld_group_dict.keys():
            if type(item) == CustomAppendList:
                print("CustomAppendList")
                locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, len(self) - 1)
            elif type(item) == card.Card: # If it is a Card (For instances such as when a card is being added to a preexisting meld).
                # Below line - For when a meld is created for an intended location, but has not been placed there yet.
                if self in player.Player.meld_group_dict[self.card_group_name]:
                    print("card.Card")
                    locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, self.meld_num, len(self) - 1)
        elif 'hand' in self.card_group_name:
                print("hand")
                locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item)
        else:
            print("outer else - discard pile, deck")
            print(item, item.display_layer, '---')
            locations.Locate.func_dict[(self.card_group_name)](item)
        pygame.event.wait(2000)
