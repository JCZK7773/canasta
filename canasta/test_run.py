import customappendlist
import deck
import player
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_run():
    print("test_run 1")
    # Below Section - Test section to verify proper movement of card-screen locations.
    # -------------------------------------
    # Below Section - Player melds testing.
    meld_1 = customappendlist.CustomAppendList('P1.melds')
    for card in range(3):
        meld_1.append(deck.MasterDeck.deck.pop(-1))
    player.P1.melds.append(meld_1)
    # -------------------------------------
    print("test_run 2")
    meld_2 = customappendlist.CustomAppendList('P1.melds')
    for card in range(6):
        meld_2.append(deck.MasterDeck.deck.pop(-1))
    player.P1.melds.append(meld_2)
    # # -------------------------------------
    print("test_run 3")
    meld_3 = customappendlist.CustomAppendList('P2.melds')
    for card in range(6):
        meld_3.append(deck.MasterDeck.deck.pop(-1))
    player.P2.melds.append(meld_3)
    # -------------------------------------
    print("test_run 4")
    meld_4 = customappendlist.CustomAppendList('P2.melds')
    for card in range(6):
        meld_4.append(deck.MasterDeck.deck.pop(-1))
    player.P2.melds.append(meld_4)
    # # -------------------------------------
    # # -------------------------------------
    # # Below Section - Player play cards testing.
    print("test_run 5")
    meld_5 = customappendlist.CustomAppendList('P1.play_cards')
    for card in range(6):
        meld_5.append(deck.MasterDeck.deck.pop(-1))
    player.P1.play_cards.append(meld_5)
    # -------------------------------------
    print("test_run 6")
    new_meld = customappendlist.CustomAppendList('P2.play_cards')
    for card in range(6):
        new_meld.append(deck.MasterDeck.deck.pop(-1))
    player.P2.play_cards.append(new_meld)
    # -------------------------------------
    print("test_run 7")
    new_meld = customappendlist.CustomAppendList('P1.melds')
    player.P1.melds.append(new_meld)
    for card in player.P1.play_cards[0][:]:
        new_meld.append(player.P1.play_cards[0].pop(-1))
    player.P1.play_cards.pop(0)
    # -------------------------------------
    print("test_run 8")
    new_meld = customappendlist.CustomAppendList('P2.play_cards')
    player.P2.play_cards.append(new_meld)
    for card in player.P1.melds[0][:]:
        player.P2.play_cards[1].append(player.P1.melds[0].pop(-1))
    # # -------------------------------------
    print("test_run 9")
    for card in range(3):
        player.P2.play_cards[0].append(deck.MasterDeck.deck.pop(-1))
    # # -------------------------------------
    print("test_run 10")
    for card in range(3):
        player.P2.melds[0].append(deck.MasterDeck.deck.pop(-1))
    # -------------------------------------
    # -------------------------------------
    # Below Section - Player hand testing.
    print("test_run 11")
    for card in range(4):
        player.P1.hand.append(deck.MasterDeck.deck.pop(-1))
    # # -------------------------------------
    print("test_run 12")
    for card in range(4):
        player.P2.hand.append(deck.MasterDeck.deck.pop(-1))
    # -------------------------------------
    # -------------------------------------
    # # Below Section - Deck & discard pile testing.
    print("test_run 13")
    for card in range(4):
        deck.MasterDeck.discard_pile.append(deck.MasterDeck.deck.pop(-1))
    # -------------------------------------
    print("test_run 14")
    for card in range(4):
        deck.MasterDeck.deck.append(deck.MasterDeck.discard_pile.pop(-1))
    # -------------------------------------
    # -------------------------------------
    # Below Section - Player red 3 meld testing.
    print("test_run 15")
    for card in range(3):
        player.P1.red_3_meld.append(deck.MasterDeck.deck.pop(-1))
    # # -------------------------------------
    print("test_run 16")
    for card in range(3):
        player.P2.red_3_meld.append(deck.MasterDeck.deck.pop(-1))
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
