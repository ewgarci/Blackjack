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

    def __eq__(self, other): 
       return self.__dict__ == other.__dict__

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
    def __init__(self, numberOfDecks = 8):
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

class Role(Enum):
    COMPUTER = 1,
    HUMAN = 2

class Table:
    def __init__(self, numberOfDecks = 8, roundsBeforeShuffling = 5):
        self.players = []
        self.activePlayers = []
        self.purse = 0
        self.hand = Hand()
        self.roundNumber = 1
        self.roundsBeforeShuffling = roundsBeforeShuffling
        self.deck = Deck(numberOfDecks)
        self.deck.shuffle()
        self.numberOfPlayers = 0
        self.pushes = 0
        self.losses = 0
        self.wins = 0

    def askNumberOfPlayers(self):
        while True:
            players = 0
            try:
               players  = int(raw_input("How many players? (1-6) "))
            except ValueError:
                print "Incorrect input"
                next
            if players > 6 or players < 1:
                print "Invalid number of players"
            else:
                self.numberOfPlayers = players
                return

    def askPlayersInfo(self):
        for i in range(self.numberOfPlayers):
            while True:
                name = raw_input("Player " + str(i+1) + 
                        ": What is your name? ").strip()
                if name == "":
                    print "Player " + str(i+1) + "Invalid Name"
                else:
                    newPlayer = Player(100, name, Role.HUMAN)
                    self.activePlayers.append(newPlayer)
                    self.players.append(newPlayer)
                    break

    def askPlayersBets(self):
        for player in self.activePlayers:
            while True:
                bet = player.askPlayerBet()
                valid = self.verifyBet(bet, player)
                if valid:
                    break

    def verifyBet(self, bet, player):
        if bet > player.purse:
            player.printStr("Insufficient funds")
            return False
        elif bet <= 0:
            player.printStr("Bet must be greater than 0")
            return False
        else:
            player.bet = bet
            player.printStr("Betting " + str(bet))
            return True

    def dealInitialHands(self):
        for _ in range(2):
            for player in self.activePlayers:
                player.hand.add(self.deck.getCard())
            self.hand.add(self.deck.getCard())
        self.printPlayersStates()
        self.printDealerConcealedState()

    def askPlayersActions(self):
        for player in self.activePlayers:
            while True:
                action = player.askPlayerAction(player)
                done = self.verifyAction(action, player)
                if done:
                    break

    def verifyAction(self, action, player):
        if action == 1:
            print "Standing"
            return True
        elif action == 2:
            player.hand.add(self.deck.getCard())
            player.printState()
            if player.hand.score == -1:
                player.printStr("Bust!!!")
                return True
            else:
                return False
        else:
            player.printStr("Incorrect Action")
            return False

    def playDealer(self):
        self.printDealerState()
        while self.hand.score < 17:
            self.hand.add(self.deck.getCard())
            self.printDealerState()
            if self.hand.score == -1:
                break

    def concludeRound(self):
        for i in xrange(len(self.activePlayers) - 1, -1, -1):
            player = self.activePlayers[i]
            self.evaluatePlayerBet(player)
            player.resetRound()
            self.removeLosingPlayer(player,i)
        self.resetRound()

    def evaluatePlayerBet(self, player):
        if player.hand.score == -1 or player.hand.score < self.hand.score:
            player.purse -= player.bet
            self.purse += player.bet
            player.printStr("Lost " + str(player.bet))
            player.losses += 1
            self.wins += 1
        elif player.hand.score == self.hand.score:
            player.printStr("Pushed")
            player.pushes += 1
            self.pushes += 1
        else: 
            player.printStr("Won " + str(player.bet))
            player.purse += player.bet
            self.purse -= player.bet
            player.wins += 1
            self.losses += 1

    def removeLosingPlayer(self, player, i):
        if player.purse == 0:
            player.printStr("No More Chips!")
            player.printStr("Removed from Game")
            del self.activePlayers[i]

    def resetRound(self):
        self.hand.empty()
        self.roundNumber += 1
        if self.roundNumber % self.roundsBeforeShuffling == 0:
            self.deck.shuffle()

    def checkGameEnd(self):
        return len(self.activePlayers) == 0

    def printStr(self, msg):
        print "Dealer: " + msg

    def printNewRound(self):
        print ""
        print "*************************************"
        print "*             Round  {0}              *".format(self.roundNumber)
        print "*************************************"
        print ""

    def printDealerState(self):
        self.printStr(str(self.hand) + " = " + str(self.hand.score))

    def printPlayersStates(self):
        for player in self.activePlayers:
            player.printState()

    def printEndingStats(self):
        for player in self.players:
            player.printStats()

    def printDealerConcealedState(self):
        self.printStr("[" + str(self.hand.cards[0]) + ", CONCEALED]")

class Player:
    def __init__(self, purse, name, role):
        self.purse = purse
        self.name = name
        self.role = role
        self.hand = Hand()
        self.bet = 0
        self.pushes = 0
        self.losses = 0
        self.wins = 0

    def resetRound(self):
        self.hand.empty()
        self.bet = 0

    def askPlayerBet(self):
        while True:
            bet = 0
            try:
                bet = int(raw_input(self.name + ": What is your bet amount? ("
                    + str(self.purse) + " chips available): "))
            except ValueError:
                self.printStr("Incorrect Input")
                next
            else:
                return bet

    def askPlayerAction(self, player):
        while True:
            action = 0
            try:
                self.printState()
                action = int(raw_input(self.name + ": What is your Action?" \
                       + " (Enter number)\n1.) Stand\n2.) Hit\n "))
            except ValueError:
                self.printStr("Incorrect input")
            else:
                return action

    def printStr(self, msg):
        print self.name + ": " + msg

    def printState(self):
        self.printStr(str(self.hand) + " = " + str(self.hand.score))

    def printStats(self):
        self.printStr("Wins = " + str(self.wins)   \
                + ", Losses = " + str(self.losses) \
                + ", Pushes = " + str(self.pushes))

    def printConcealedState(self):
        self.printStr("[" + str(self.hand.cards[0]) + ", CONCEALED]")


if __name__ == "__main__":
    table = Table()
    table.askNumberOfPlayers()
    table.askPlayersInfo()

    while True:
        table.printNewRound()
        table.askPlayersBets()
        table.dealInitialHands()
        table.askPlayersActions()
        table.playDealer()
        table.concludeRound()
        if table.checkGameEnd():
            print "The Casino took all your Money!"
            table.printEndingStats()
            exit(0)
