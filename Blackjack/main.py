import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return f"{self.rank['RANK']} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [] # populate later
        suits = ['❤️', '🔷', '♣️', '♠️']
        ranks = [
            {"RANK": '2', "VALUE": '2'},
            {"RANK": '3', "VALUE": '3'},
            {"RANK": '4', "VALUE": '4'},
            {"RANK": '5', "VALUE": '5'},
            {"RANK": '6', "VALUE": '6'},
            {"RANK": '7', "VALUE": '7'},
            {"RANK": '8', "VALUE": '8'},
            {"RANK": '9', "VALUE": '9'},
            {"RANK": '10', "VALUE": '10'},
            {"RANK": 'J', "VALUE": '10'},
            {"RANK": 'Q', "VALUE": '10'},
            {"RANK": 'K', "VALUE": '10'},
            {"RANK": 'A', "VALUE": '11'}
            ]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle_deck(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)   

    def deal_card(self, num_cards=1):
        cards_dealt = []
        if num_cards > len(self.cards):
            num_cards = len(self.cards)
        for x in range(num_cards):
            card = self.cards.pop()
            cards_dealt.append(card)
        return cards_dealt

class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_cards(self, new_cards): 
        self.cards.extend(new_cards)

    def calculate_value(self):
        self.value = 0
        for card in self.cards:
            self.value += int(card.rank['VALUE'])
        for card in self.cards:
            if card.rank['RANK'] == 'A' and self.value > 21:
                self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value
    
    def is_blackjack(self):
        return self.get_value() == 21 and len(self.cards) == 2
    
    def display(self, show_all=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if self.dealer and index == 0 \
                    and not show_all and not self.is_blackjack():
                print("***hidden***")
            else:
                print(card)
            
        if not self.dealer:
            print(f"Value: {self.get_value()}")

class Game:
    def play(self):
        gamenumber = 0
        games_to_play = 0
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games would you like to play? "))
            except ValueError:
                print("Invalid input. Please enter a number.")

        while gamenumber < games_to_play:       
            gamenumber += 1
            
            deck = Deck()
            deck.shuffle_deck()
            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for _ in range(2):
                player_hand.add_cards(deck.deal_card(1))
                dealer_hand.add_cards(deck.deal_card(1))

            print()
            print("*" * 20)
            print(f"--- Game {gamenumber} of {games_to_play} ---")
            print("*" * 20)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue
            
            choice = ""
            
            while player_hand.get_value() and choice != 's':
                choice = input("Would you like to (H)it or (S)tand? ").lower()
                if choice == 'h':
                    player_hand.add_cards(deck.deal_card(1))
                    player_hand.display()
                elif choice == 's':
                    print("You chose to stand.")
                else:
                    print("Invalid input. Please enter H or S.")

            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_cards(deck.deal_card(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all=True)  
            self.check_winner(player_hand, dealer_hand)

            print("Final Hands:")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, game_over=True)
            print("\nThank you for playing!")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:            
            if player_hand.get_value() > 21:
                print("Dealer wins! You busted.")
                return True
            elif dealer_hand.get_value() > 21:
                print("You win! Dealer busted.")
                return True
            elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
                print("It's a tie!")
                return True
            elif player_hand.is_blackjack():
                print("You win with a Blackjack!")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer wins with a Blackjack!")
                return True            
        else:
            if player_hand.get_value() > 21:
                print("Dealer wins! You busted.")
            elif dealer_hand.get_value() > 21:
                print("You win! Dealer busted.")
            elif player_hand.get_value() > dealer_hand.get_value():
                print("You win!")
            elif dealer_hand.get_value() > player_hand.get_value():
                print("Dealer wins!")
            else:
                print("It's a tie!")
            return True
        return False

g = Game()
g.play()        
