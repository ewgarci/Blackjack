#!flask/bin/python
# -*- coding: utf-8 -*-
import code
from enum import Enum
from random import shuffle

class CardValues(Enum):
    ACE = 'A'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'

class Suits(Enum):
    CLUBS = 'C'
    DIAMONDS = 'D'
    HEARTS = 'H'
    SPADES = 'S'

cardValues = {
    CardValues.ACE:1,
    CardValues.TWO:2,
    CardValues.THREE:3,
    CardValues.FOUR:4,
    CardValues.FIVE:5,
    CardValues.SIX:6,
    CardValues.SEVEN:7,
    CardValues.EIGHT:8,
    CardValues.NINE:9,
    CardValues.TEN:10,
    CardValues.JACK:10,
    CardValues.QUEEN:10,
    CardValues.KING:10
}

suitDict = { 
    Suits.CLUBS: '♣', 
    Suits.HEARTS: '♥',
    Suits.DIAMONDS: '♦', 
    Suits.SPADES: '♠'
}

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return self.value + suitDict[self.suit]

class Hand:
    def __init__(self):
        self.cards = []
        self.containsAce = False
        self.score = 0

    def add(self, card):
        self.cards.append(card)
        if card.value == CardValues.ACE:
            self.containsAce = True
        self.score = self.__evaluate()

    def __evaluate(self):
        if len(self.cards) == 0:
            return 0

        total = 0

        for card in self.cards:
            total += cardValues[card.value]

        if self.containsAce and (total + 10) <= 21:
            return total + 10
        elif total <= 21:
            return total
        else:
            return -1

    def empty(self):
        del self.cards[:]
        self.containsAce = False
        self.score = 0

    def __str__(self):
        return '[%s]' % ', '.join(map(str, self.cards)) 

class Deck:
    def __init__(self, numberOfDecks = 1):
        self.numberOfDecks = numberOfDecks
        self.__deck = []
        self.__deckIndex = 0

        for _ in range(numberOfDecks):
            for cardVal in cardValues:
                for suit in suitDict:
                    self.__deck.append(Card(cardVal, suit))

    def shuffle(self):
        shuffle(self.__deck)
        self.__deckIndex = 0

    def getCardIndex(self):
        return self.__deckIndex

    def getTotalCards(self):
        return len(self.__deck)

    def getCard(self):
        if self.__deckIndex == len(self.__deck):
            return None
        else:
           card = self.__deck[self.__deckIndex]
           self.__deckIndex += 1
           return card

    def __str__(self):
        return '[%s]' % ', '.join(map(str, self.__deck)) 

class States(Enum):
    BETTING = 1,
    DEALING = 2,
    PLAYER_TURN = 3,
    DEALER_TURN = 4,
    ROUND_END = 5

class Role(Enum):
    COMPUTER = 1,
    HUMAN = 2

class Table:
    def __init__(self):
        self.players = []
        self.activePlayers = []
        self.purse = 0
        self.state = States.BETTING
        self.hand = Hand()
        self.roundNumber = 0

    def resetRound(self):
        del table.activePlayers[:]
        self.hand.empty()

    def getHighestHand(self):
        highestHand = self.hand.score
        for player in self.activePlayers:
            handScore = player.hand.score
            if player.hand.score > highestHand:
                highestHand = player.hand.score
        return highestHand

class Player:
    def __init__(self, purse, name, role):
        self.purse = purse
        self.name = name
        self.role = role
        self.hand = Hand()
        self.bet = 0

    def resetRound(self):
        self.hand.empty()
        self.bet = 0

if __name__ == "__main__":
    table = Table()
    deck = Deck(6)
    while True:
        name = raw_input("What is your name? ").strip()
        if name == "":
            print "Invalid Name"
        else:
            break
    mainPlayer = Player(100, name, Role.HUMAN)
    table.players.append(mainPlayer)

    while True:
        table.roundNumber += 1
        deck.shuffle()
        if table.state == States.BETTING:
            for player in table.players:
                while True:
                    if player.purse == 0:
                        print player.name + ": No More Chips!"
                        print player.name + ": You Lose!"
                        exit()

                    bet = 0
                    try:
                        bet = int(raw_input(player.name + ": What is your bet amount? (" + str(player.purse) + " chips available) "))
                    except ValueError:
                        print "incorrect input"
                        next

                    if bet > player.purse:
                        print "insufficient funds"
                        next
                    elif bet == 0:
                        print "sitting out"
                        player.bet = bet
                        break
                    elif bet > 0:
                        player.bet = bet
                        print "betting " + str(bet)
                        table.activePlayers.append(player)
                        break
                    else:
                        print "incorrect input"
                        next
            if len(table.activePlayers) != 0:
                table.state = States.DEALING

        if table.state == States.DEALING:
            for player in table.activePlayers:
                player.hand.add(deck.getCard())
            table.hand.add(deck.getCard())

            for player in table.activePlayers:
                player.hand.add(deck.getCard())
            table.hand.add(deck.getCard())

            for player in table.activePlayers:
                print player.name + ": " + str(player.hand) + " = " + str(player.hand.score)

            print "dealer: [" + str(table.hand.cards[0]) + ", CONCEALED]"
            table.state = States.PLAYER_TURN

        if table.state == States.PLAYER_TURN:
            for player in table.activePlayers:
                while True:
                    action = 0
                    try:
                        action = int(raw_input(player.name + ": What is your Action? (Enter number)\n1.) Stand\n2.) Deal\n "))
                    except ValueError:
                        print "incorrect input"
                        next

                    if action == 1:
                        print "Standing"
                        break
                    elif action == 2:
                        player.hand.add(deck.getCard())
                        print player.name + ": " + str(player.hand) + " = " + str(player.hand.score)
                        if player.hand.score == -1:
                            break
                    else:
                        print "incorrect input"
                        next
            table.state = States.DEALER_TURN

        if table.state == States.DEALER_TURN:
            print "Dealer: " + str(table.hand) + " = " + str(table.hand.score)
            while table.hand.score < 17:
                table.hand.add(deck.getCard())
                print "Dealer: " + str(table.hand) + " = " + str(table.hand.score)
                if table.hand.score == -1:
                    break
            table.state = States.ROUND_END

        if table.state == States.ROUND_END:
            for player in table.activePlayers:
                if player.hand.score == -1 or player.hand.score < table.hand.score:
                    player.purse -= player.bet
                    table.purse += player.bet
                elif player.hand.score == table.hand.score:
                    pass
                else: 
                    player.purse += player.bet
                    table.purse -= player.bet
                player.resetRound()
            table.resetRound()
            table.state = States.BETTING

