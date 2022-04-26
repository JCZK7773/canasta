import card
import game
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Deck(): # ****
    def __init__(self): # ****
        self.deck = [] # ****
        self.original_deck = [] # ****
        self.draw_ranks = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}
        self.draw_suit_ranks = {'Joker': 0, 'Club': 1, 'Diamond': 2, 'Heart': 3, 'Spade': 4} # ****
        self.ranks = {'Joker':50, '2':20, '3':100, '4':5, '5':5, '6':5, '7':5, '8':10, '9':10, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':20}
        self.suits = ['Club', 'Diamond', 'Heart', 'Spade'] # ****
        self.suits_symbols = {'Heart': '♥', 'Diamond': '♦', 'Spade': '♠', 'Club': '♣', 'Joker': '🃟'} # ****
        self.discard_pile = []
        self.red_3s = [('3', 'Diamond'), ('3', 'Heart')] # ****
        self.black_3s = [('3', 'Club'), ('3', 'Spade')] # ****
        self.wild_cards = [('2', 'Diamond'), ('2', 'Heart'), ('2', 'Spade'), ('2', 'Club'), ('Joker', 'Joker')] # ****
    # -------------------------------------
    @property # ****
    def face_up_discard(self): # ****
        return self.discard_pile[-1] # ****
    # -------------------------------------
    @property # ****
    def discard_pile_is_frozen(self): # ****
        discard_pile_is_frozen = False
        for card in MasterDeck.discard_pile: # ****
            if (card.rank, card.suit) in MasterDeck.wild_cards or (card.rank, card.suit) in MasterDeck.black_3s : # ****
                discard_pile_is_frozen = True # ****
        return discard_pile_is_frozen # ****
    # -------------------------------------
    def create_double_deck(self): # ****
    # -------------------------------------
        for x in range(2):
            for rank in self.ranks: # ****
                if rank != 'Joker': # ****
                    for suit in self.suits: # ****
                        current_card = card.Card(rank, suit) # ****
                        # Below Line - This function has to be ran here because this is after it's creation and before it's first attempted rendering. The cards cannot be rendered unless they have both a rect and an image, which this function assigns to them.
                        card.Card.assign_card_images_and_rects(current_card)
                        # Below Line - Appends card into the canasta_pygame.card_group (Sprite Group) so that the entire group location can be updated with only one line instead of coding movement updates of each card inidividually.
                        game.game.card_group.add(current_card)
                        self.deck.append(current_card) # ****
                else: # ****
                    for Joker in range(2): # ****
                        current_card = card.Card(rank, 'Joker') # ****
                        # Below Line - This function has to be ran here because this is after it's creation and before it's first attempted rendering. The cards cannot be rendered unless they have both a rect and an image, which this function assigns to them.
                        card.Card.assign_card_images_and_rects(current_card)
                        # Below Line - Appends card into the canasta_pygame.card_group (Sprite Group) so that the entire group location can be updated with only one line instead of coding movement updates of each card inidividually.
                        game.game.card_group.add(current_card)
                        self.deck.append(current_card) # ****
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Section - Creates the MasterDeck & Deck2 instances so that the can later be combined into the one MasterDeck. # ****
MasterDeck = Deck() # ****
