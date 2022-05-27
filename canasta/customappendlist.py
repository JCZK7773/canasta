import pygame
import player
import deck
import locations
import card
import game
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Class - Customized list class which is used to call a particular function whenever the sub-classed list .append method is called, for the purpose of visually updating card locations by updating the card coordinate via the function call.
class CustomAppendList(list):
    def __init__(self, card_group_name):
        self.card_group_name = card_group_name
        super().__init__()
    # -------------------------------------
    # Below Section - Calculates the meld_num dynamically.
    @property
    def meld_num(self):
        list_index = player.Player.meld_group_dict[self.card_group_name].index(self)
        return list_index
    # -------------------------------------
    # Below Function - Customized version of the built-in append method. Handles items differently based on certain qualifications, and also stores and passes certain required information about the self (list) to the various location movement functions for 'automation'.
    def append(self, item):
        # print("append")
        # Below Section - Appends the item to the self (list) and then updates the associated reference dictionaries for accurate comparisons. If these dicts are not updated, the locations are not properly calculated.
        super(CustomAppendList, self).append(item)
        locations.Locate.card_group_name_dict = {'deck': deck.MasterDeck.deck, 'discard_pile': deck.MasterDeck.discard_pile, 'P1.hand': player.P1.hand, 'P2.hand': player.P2.hand, 'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds, 'P1.red_3_meld': player.P1.red_3_meld, 'P2.red_3_meld': player.P2.red_3_meld}
        locations.Locate.card_group_loc_dict = {'deck': locations.Locate.deck_loc, 'discard_pile': locations.Locate.discard_pile_loc, 'P1.hand': locations.Locate.p1_hand_next_loc, 'P2.hand': locations.Locate.p2_hand_next_loc, 'P1.play_cards': locations.Locate.p1_play_cards_start_loc, 'P2.play_cards': locations.Locate.p2_play_cards_start_loc, 'P1.melds': locations.Locate.p1_melds_start_loc, 'P2.melds': locations.Locate.p2_melds_start_loc}
        player.Player.meld_group_dict = {'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds}
        # -------------------------------------
        # Below Section - Figures out which locations movement function needs to be called, and determines the correct parameters to be passed to the function for proper card movements.
        if self.card_group_name in player.Player.meld_group_dict.keys():
            if type(item) == CustomAppendList:
                # print("CustomAppendList")
                locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, len(self) - 1)
            elif type(item) == card.Card: # If it is a Card (For instances such as when a card is being added to a preexisting meld).
                # print("card.Card")
                # Below line - For when a meld is created for an intended location, but has not been placed there yet.
                if self in player.Player.meld_group_dict[self.card_group_name]:
                    locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, self.meld_num, len(self) - 1)
        # -------------------------------------
        # Below Section - Handles location movement function calls for the .deck, .discard_pile, and .hand.
        else:
            print(f'append {item}')
            locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item)
        # -------------------------------------
        # Below Section - For whenever a card/meld is popped from another CustomAppendList list; calls the locations.Locate card group update function to visually 'resituate' the prior_card_group via the prior_card_group_name.
        if type(item) == CustomAppendList:
            if item[0].prior_card_group_name != None:
                ###### Below Line - May not need this line as all CustomAppendList instances should be melds in the meld_group_dict.
                if item[0].prior_card_group_name in player.Player.meld_group_dict:
                    meld_num = item.prior_meld_num
                    for meld in player.Player.meld_group_dict[item.prior_card_group_name][item.prior_meld_num:]:
                        locations.Locate.func_dict[(item.prior_card_group_name)](item.prior_card_group_name, meld, meld_num)
                        meld_num += 1
        else:
            if item.prior_card_group_name != None:
                # Below Section - If the item is a Card and is in meld_group_dict; resituates the meld card by card for proper visual display.
                if item.prior_card_group_name in player.Player.meld_group_dict:
                    card_num = 0
                    for current_card in player.Player.meld_group_dict[item.prior_card_group_name][item.prior_meld_num]:
                        locations.Locate.func_dict[(item.prior_card_group_name)](item.prior_card_group_name, current_card, item.prior_meld_num, card_num)
                        card_num += 1
    # -------------------------------------
    # Below Function - ...
    def pop(self, item):
        # print('pop')
        if type(item) == card.Card:
            item.prior_card_group_name = self.card_group_name
            if self.card_group_name in player.Player.meld_group_dict:
                item.prior_meld_num = self.meld_num
        elif type(item) == CustomAppendList:
            item[0].prior_card_group_name = self.card_group_name
            if self.card_group_name in player.Player.meld_group_dict:
                item[0].prior_meld_num = self.meld_num
        super(CustomAppendList, self).pop(item)
