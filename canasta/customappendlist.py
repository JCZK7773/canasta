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
        if self in player.Player.meld_group_dict[self.card_group_name]:
            list_index = player.Player.meld_group_dict[self.card_group_name].index(self)
            return list_index
    # -------------------------------------
    # Below Function - Customized version of the built-in append method. Handles items differently based on certain qualifications, and also stores and passes certain required information about the self (list) to the various location movement functions for 'automation'.
    def append(self, item):
        # print("append")
        # Below Section - Appends the item to the self (list) and then updates the associated reference dictionaries for accurate comparisons. If these dicts are not updated, the locations are not properly calculated.
        super(CustomAppendList, self).append(item)
        locations.Locate.card_group_name_dict = {'deck': deck.MasterDeck.deck, 'discard_pile': deck.MasterDeck.discard_pile, 'P1.hand': player.P1.hand, 'P2.hand': player.P2.hand, 'P1.pre_sort_play_cards': player.P1.pre_sort_play_cards, 'P2.pre_sort_play_cards': player.P2.pre_sort_play_cards, 'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds, 'P1.red_3_meld': player.P1.red_3_meld, 'P2.red_3_meld': player.P2.red_3_meld}
        locations.Locate.card_group_loc_dict = {'deck': locations.Locate.deck_loc, 'discard_pile': locations.Locate.discard_pile_loc, 'P1.hand': locations.Locate.p1_hand_next_loc, 'P2.hand': locations.Locate.p2_hand_next_loc, 'P1.pre_sort_play_cards': locations.Locate.p1_pre_sort_play_cards_next_loc, 'P2.pre_sort_play_cards': locations.Locate.p2_pre_sort_play_cards_next_loc, 'P1.play_cards': locations.Locate.p1_play_cards_start_loc, 'P2.play_cards': locations.Locate.p2_play_cards_start_loc, 'P1.melds': locations.Locate.p1_melds_start_loc, 'P2.melds': locations.Locate.p2_melds_start_loc}
        player.Player.meld_group_dict = {'P1.play_cards': player.P1.play_cards, 'P2.play_cards': player.P2.play_cards, 'P1.melds': player.P1.melds, 'P2.melds': player.P2.melds}
        # -------------------------------------
        # Below Section - Assigns the item's card_group_name to the self's card_group_name so that they are properly updated as they are moved.
        if type(item) == CustomAppendList:
            item.card_group_name = self.card_group_name
            for current_card in item:
                item.card_group_name = self.card_group_name
        elif type(item) == card.Card:
            item.card_group_name = self.card_group_name
        # -------------------------------------
        # Below Section - Figures out which locations movement function needs to be called, and determines the correct parameters to be passed to the function for proper card movements.
        if self.card_group_name in player.Player.meld_group_dict.keys():
            if type(item) == CustomAppendList:
                # print("append > CustomAppendList")
                locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, len(self) - 1)
            elif type(item) == card.Card: # If it is a Card (For instances such as when a card is being added to a preexisting meld).
                # print("append > card.Card")
                # Below line - For when a meld is created for an intended location, but has not been placed there yet.
                if self in player.Player.meld_group_dict[self.card_group_name]:
                    # print('append > card.Card > self in player.Player.meld_group_dict[self.card_group_name]')
                    locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item, self.meld_num, len(self) - 1)
        # -------------------------------------
        # Below Section - Handles location movement function calls for the .deck, .discard_pile, .hand, and .pre_sort_play_cards.
        else:
            locations.Locate.func_dict[(self.card_group_name)](self.card_group_name, item)
        # -------------------------------------
        # Below Section - Resituate section. For whenever a card/meld is popped from another CustomAppendList list; calls the locations.Locate card group update function to visually 'resituate' the prior_card_group via the prior_card_group_name.
        if type(item) == CustomAppendList:
            # Below Line - Added specifically for the case whenever a temp_meld from valid_play_check_and_sort() is transferred from pre_sort_play_cards to play_cards. These are empty melds and we don't want the code to execute a resituation call because technically there is nothing to resituate as this append is not associated with a pop.
            if len(item) > 0:
                if item[0].prior_card_group_name != None:
                    ###### Below Line - May not need this line as all CustomAppendList instances should be melds in the meld_group_dict.
                    if item[0].prior_card_group_name in player.Player.meld_group_dict:
                        # Below Line - Added this if clause for the case in which a temp_meld is being appended into the play_cards card group, in which case there is no meld_num and no need to re-situate because in this case there are no melds.
                        if item[0].prior_meld_num != None:
                            meld_num = item.prior_meld_num
                            for meld in player.Player.meld_group_dict[item.prior_card_group_name][item.prior_meld_num:]:
                                locations.Locate.func_dict[(item.prior_card_group_name)](item.prior_card_group_name, meld, meld_num)
                                meld_num += 1
        elif type(item) == card.Card:
            if item.prior_card_group_name != None:
                # Below Section - For resituation. If the item is a Card and is in meld_group_dict; resituates the meld card by card for proper visual display.
                if item.prior_card_group_name in player.Player.meld_group_dict:
                    if item.prior_meld_num != None:
                        card_num = 0
                        for current_card in player.Player.meld_group_dict[item.prior_card_group_name][item.prior_meld_num]:
                            locations.Locate.func_dict[(item.prior_card_group_name)](item.prior_card_group_name, current_card, item.prior_meld_num, card_num)
                            card_num += 1
                # Below Section - Specifically for the cases in which the prior_group_name is 'hand'; whenever the player's hand is to be resituated, OR for the case in which the pre_sort_play_cards need to be resituated; the cards that have just been popped from pre_sort_play_cards are being appended to a temp_meld (play_cards).
                elif 'hand' in item.prior_card_group_name or 'pre_sort' in item.prior_card_group_name:
                    locations.Locate.func_dict[(item.prior_card_group_name)](item.prior_card_group_name)
    # -------------------------------------
    # Below Function - ...
    def pop(self, item):
        # print('pop')
        if type(self[item]) == card.Card:
            self[item].prior_card_group_name = self.card_group_name
            if self.card_group_name in player.Player.meld_group_dict:
                # Below Line - If the self(meld) is in the meld_group.
                if self in player.Player.meld_group_dict[self.card_group_name]:
                    self[item].prior_meld_num = self.meld_num
                # Below Line - If the card is coming from the self(meld_group) directly (not from within a meld in the meld_group) as in the case whenever a card is moved from the player.pre_sort_play_cards into the temp_meld before the temp_meld is reappended back into the play_cards group. If we did not have this else clause, whenever it would move the card it would errantly assign the index of the card in the card group as the meld_num, when it in fact did not come from a 'meld' in that sense.
                else:
                    self[item].prior_meld_num = None
        elif type(self[item]) == CustomAppendList:
            # Below Line - For the case in which an empty meld, such as a temp_meld in valid_play_check_and_sort() is being popped off after being emptied. It wouldn't have any cards inside of it therefore it would not be able to be assigned anything.
            if len(self[item]) > 0:
                self[item][0].prior_card_group_name = self.card_group_name
                if self.card_group_name in player.Player.meld_group_dict:
                    self[item][0].prior_meld_num = self.meld_num
        return super(CustomAppendList, self).pop(item)
