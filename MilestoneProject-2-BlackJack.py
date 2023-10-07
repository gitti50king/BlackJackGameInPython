import random

# Declaration
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
            'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        return self.deck.pop()

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_cards(self, card):
        #card passed in form Deck.deal()
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_aces(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

def show_some(player, dealer):

    # dealer one card hidden and second card display
    print(f"\n Dealer's hand: ")
    print("first card hidden!")
    print(dealer.cards[1])

    # display both player's cards
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)
    
    # print("\n Player's hand: ", *dealer.cards, sep = '\n')

def show_all(player, dealer):

    #all dealer cards display
    print("\n Dealer's hand: ")
    for card in dealer.cards:
        print(card)
    print(f"value Dealer's hand is: {dealer.value}")

    #all player cards display
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)
    print(f"value Players's hand is: {player.value}")

class Chips:
    
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Please provide an integer.")
        else:
            if chips.bet > chips.total:
                print(f"You do not have enough chips, you have {chips.total} chips.")
            else:
                break

def hit(deck, hand):

    hand.add_cards(deck.deal())
    hand.adjust_for_aces()

def  hit_or_stand(deck, hand):
    global playing

    while True:
        
        x = input('Would you like to hit or stand? Enter h or s: ')

        if x[0].lower() == 'h':

            hit(deck, hand)

        elif x[0].lower() == 's':

            print('Player stands, Dealer is playing.')
            playing = False
        
        else:
            print('Please enter h and s only.')
            continue
        
        break

def player_busts(player, dealer, chips):
    print('BUST PLAYER')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('Player wins')
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print('Dealer busted! Player wins')
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print('DEALER WINS')
    chips.lose_bet()

def push(player_hand, dealer_hand):
    print("Dealer and Player Tie! PUSH")

####################################################################
################### GAME LOGIC ######################################

while True:
    #deck
    deck = Deck()
    deck.shuffle()

    # player hand cards
    player_hand = Hand()
    player_hand.add_cards(deck.deal())
    player_hand.add_cards(deck.deal())

    # dealer hand cards
    dealer_hand = Hand()
    dealer_hand.add_cards(deck.deal())
    dealer_hand.add_cards(deck.deal())

    # setting player's chips
    player_chips = Chips()

    #prompt player for their bet
    take_bet(player_chips)

    # show cards but keep them hidden
    show_some(player_hand, dealer_hand)

    while playing:

        # prompt player for hit or stand
        hit_or_stand(deck, player_hand)  # if stand then playing = false and loop breaks

        # show player cards while dealers cards kept hidden
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

            break

        if player_hand.value <= 21:

            while dealer_hand.value < player_hand.value:
                hit(deck, dealer_hand)

            #show all cards
            show_all(player_hand, dealer_hand)

            # Run different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)
            
        # Inform player of the total chips
    print("\n Player's total chips are at {}".format(player_chips.total))

    # Ask to play again
    new_game = input("do you want to play again? y/n: ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing")
        break