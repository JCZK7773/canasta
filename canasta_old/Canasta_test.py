players = [P1,P2]

def the_draw_2(player):
    player.name = input("\nWhat is your name? \n\n")
    player.the_draw = int(input("\n{p_name}, Select your card from the stack to determine which player will have the first play. (Pick a card, represented as a number from 1-108) \n".format(p_name = player.name)))
    player.draw_card = MasterDeck.deck[player.the_draw - 1]
    print("\nYou drew a {p_draw_card}".format(p_draw_card = player.draw_card))
    draw_joker_check(player)
    MasterDeck.deck.pop(player.the_draw - 1)

def the_draw_3(player):
    if P1.draw_card == P2.draw_card:
        print("You have the same exact card! You both must pick another card!\n")
        return the_draw()
    elif P1.draw_card_val > P2.draw_card_val:
        the_deal(P1,P2)
    elif P2.draw_card_val > P1.draw_card_val:
        the_deal(P2,P1)
    elif P1.draw_card_val == P2.draw_card_val:
        if Deck.draw_suite_ranks.get(P1.draw_card[0]) > Deck.draw_suite_ranks.get(P2.draw_card[0]):
            the_deal(P1,P2)
        else:
            the_deal(P2,P1)

def the_draw_1(player):
    if player == P1:
        for player in players:
            the_draw_2(player)
        the_draw_3(player)
    else:
        the_draw_2(player)
        the_draw_3(player)

            if player == P2:
                if P1.draw_card == P2.draw_card:
                    print("You have the same exact card! You both must pick another card!\n")
                    return the_draw()
                elif P1.draw_card_val > P2.draw_card_val:
                    the_deal(P1,P2)
                elif P2.draw_card_val > P1.draw_card_val:
                    the_deal(P2,P1)
                elif P1.draw_card_val == P2.draw_card_val:
                    if Deck.draw_suite_ranks.get(P1.draw_card[0]) > Deck.draw_suite_ranks.get(P2.draw_card[0]):
                        the_deal(P1,P2)
                    else:
                        the_deal(P2,P1)
    else:
        player.the_draw = int(input("\n{p_name}, Select your card from the stack to determine which player will have the first play. (Pick a card, represented as a number from 1-108)\n".format(p_name = player.name)))
        player.draw_card = MasterDeck.deck[player.the_draw - 1]
        MasterDeck.deck.pop(player.the_draw - 1)
        draw_joker_check(player)

        if player == P2:
            if P1.draw_card == P2.draw_card:
                print("You have the same exact card! You both must pick another card!\n")
                return the_draw()
            elif P1.draw_card_val > P2.draw_card_val:
                the_deal(P1,P2)
            elif P2.draw_card_val > P1.draw_card_val:
                the_deal(P2,P1)
            elif P1.draw_card_val == P2.draw_card_val:
                if Deck.draw_suite_ranks.get(P1.draw_card[0]) > Deck.draw_suite_ranks.get(P2.draw_card[0]):
                    the_deal(P1,P2)
                else:
                    the_deal(P2,P1)
            MasterDeck.deck.append(P1.draw_card, P2.draw_card)
##################################################################################################
def draw_joker_check(player):
    if player.draw_card == "Joker":
        print("Sorry, you picked a Joker, which is not available for use during The Draw! You must choose another card!\n")
        return the_draw_2(player)
##################################################################################################
for player in players:
    the_draw_1()
# -------------------------------------------------------------------------------------------------
def the_draw_3(player):
    if P1.draw_card == P2.draw_card:
        print("\nYou have the same exact card! You both must pick another card!\n")
        for player in players:
            MasterDeck.deck.append(player.hand.pop(0))
        return the_draw_1()
    elif P1.draw_card_val > P2.draw_card_val:
        for player in players:
            MasterDeck.deck.append(player.hand.pop(0))
        the_deal(P1,P2)
    elif P2.draw_card_val > P1.draw_card_val:
        for player in players:
            MasterDeck.deck.append(player.hand.pop(0))
        the_deal(P2,P1)
    elif P1.draw_card_val == P2.draw_card_val:
        if Deck().draw_suite_ranks.get(P1.draw_card[0]) > Deck.draw_suite_ranks.get(P2.draw_card[0]):
            for player in players:
                MasterDeck.deck.append(player.hand.pop(0))
            the_deal(P1,P2)
        else:
            for player in players:
                MasterDeck.deck.append(player.hand.pop(0))
            the_deal(P2,P1)
