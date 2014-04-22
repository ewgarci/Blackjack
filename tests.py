#!flask/bin/python
# -*- coding: utf-8 -*-
import unittest, copy
from blackjack import Player, Table, Role, Deck, Hand, Suits, CardValues, suitDict, cardValues, Card
from coverage import coverage
from collections import Counter

cov = coverage(branch = True, omit = ['venv/*', 'tests.py'])
cov.start()

class TestDeck(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_createSingleDeck(self):
        """A single deck should have 52 cards and all should be unique """
        a = [] 
        deck = Deck(1)
        for card in deck._Deck__deck:
            a.append(card.value + card.suit)

        counts = Counter(a).values()
        assert(len(a) == 52)
        for c in counts:
            assert(c == 1)

    def test_createMultipleDeck(self):
        """A deck made of 5 decks should have 5 of each card """
        a = [] 
        deck = Deck(5)
        for card in deck._Deck__deck:
            a.append(card.value + card.suit)

        counts = Counter(a).values()
        assert(len(a) == (52*5))
        for c in counts:
            assert(c == 5)

    def test_createDeckShuffled(self):
        """Cards in a shuffled deck should be in a different order than it was previously """
        a1 = [] 
        a2 = []
        deck = Deck(5)
        for card in deck._Deck__deck:
            a1.append(card)
        deck.shuffle()

        for card in deck._Deck__deck:
            a2.append(card)

        different = False
        for i in range(len(a1)):
            if a1[i] != a2[i]:
                different = True

        assert(different == True)


    def test_compareShuffledDecks(self):
        """The same Deck shuffled at different times should have different ordering  """
        a1 = [] 
        a2 = []
        deck = Deck(5)
        deck2 = copy.deepcopy(deck)

        deck.shuffle()
        deck2.shuffle()

        for card in deck._Deck__deck:
            a1.append(card)

        for card in deck2._Deck__deck:
            a2.append(card)

        different = False
        for i in range(len(a1)):
            if a1[i] != a2[i]:
                different = True


    def test_getCard(self):
        """Getting the next card should produces cards in sequencial index order""" 
        deck = Deck(5)

        deck.shuffle()
        a = []

        for i in range(len(deck._Deck__deck)):
            card = deck.getCard()
            a.append(card)

        for i in range(len(deck._Deck__deck)):
            assert(a[i] == deck._Deck__deck[i])


    def test_getCardEnd(self):
        """Getting the next card should return None if no more cards are left""" 
        deck =  Deck(3)
        a = []

        for i in range(len(deck._Deck__deck)):
            card = deck.getCard()
            a.append(card)

        last_card = deck.getCard()
        last_card2 = deck.getCard()
        last_card3 = deck.getCard()
        last_card4 = deck.getCard()

        assert(last_card is None and last_card2 is None and 
                last_card3 is None and last_card4 is None)
        assert(deck.getCardIndex() == len(deck._Deck__deck))
        assert(deck.getCardIndex() == deck.getTotalCards())
    
    def test_add(self):
        """A hand should calculate the score correctly with every card added"""
        h = Hand()
        h.add(Card(CardValues.JACK, Suits.CLUBS))
        assert(h.score == 10)
        h.add(Card(CardValues.THREE, Suits.DIAMONDS))
        assert(h.score == 13)
        h.add(Card(CardValues.TWO, Suits.SPADES))
        assert(h.score == 15)
        h.add(Card(CardValues.SIX, Suits.HEARTS))
        assert(h.score == 21)
        h.add(Card(CardValues.SEVEN, Suits.HEARTS))
        assert(h.score == -1)


    def test_addAce(self):
        """A hand should the highest score when an ace is added"""
        h = Hand()
        h.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        assert(h.score == 10)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 21)
    
    def test_addAce2(self):
        """A hand should pick the highest score when 2 aces are added unless bust"""
        h = Hand()
        h.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        assert(h.score == 10)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 21)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 12)
    
    def test_addAce2_1(self):
        """A hand should the highest score when 2 aces are added"""
        h = Hand()
        h.add(Card(CardValues.TWO, Suits.DIAMONDS))
        assert(h.score == 2)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 13)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 14)
    
    def test_addAce2_2(self):
        """A hand should the highest score when 2 aces are added"""
        h = Hand()
        h.add(Card(CardValues.TWO, Suits.DIAMONDS))
        assert(h.score == 2)
        h.add(Card(CardValues.NINE, Suits.SPADES))
        assert(h.score == 11)
        h.add(Card(CardValues.EIGHT, Suits.HEARTS))
        assert(h.score == 19)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 20)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 21)

    def test_addAce4(self):
        """A hand should the highest score when 4 aces are added"""
        h = Hand()
        h.add(Card(CardValues.NINE, Suits.SPADES))
        assert(h.score == 9)
        h.add(Card(CardValues.EIGHT, Suits.HEARTS))
        assert(h.score == 17)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 18)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 19)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 20)
        h.add(Card(CardValues.ACE, Suits.HEARTS))
        assert(h.score == 21)
    
    def test_addAce11(self):
        """A hand should the highest score when 11 aces are added"""
        h = Hand()
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 11)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 12)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 13)
        h.add(Card(CardValues.ACE, Suits.HEARTS))
        assert(h.score == 14)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 15)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 16)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 17)
        h.add(Card(CardValues.ACE, Suits.HEARTS))
        assert(h.score == 18)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 19)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 20)
        h.add(Card(CardValues.ACE, Suits.HEARTS))
        assert(h.score == 21)
    
    def test_addAce22(self):
        """A hand should bust when 22 aces are added"""
        h = Hand()
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 11)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 12)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 13)
        h.add(Card(CardValues.ACE, Suits.HEARTS))
        assert(h.score == 14)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 15)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 16)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 17)
        h.add(Card(CardValues.ACE, Suits.HEARTS))
        assert(h.score == 18)
        h.add(Card(CardValues.ACE, Suits.CLUBS))
        assert(h.score == 19)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 20)
        h.add(Card(CardValues.ACE, Suits.HEARTS))
        assert(h.score == 21)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 12)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 13)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 14)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 15)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 16)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 17)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 18)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 19)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 20)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == 21)
        h.add(Card(CardValues.ACE, Suits.DIAMONDS))
        assert(h.score == -1)

    def test_empty(self):
        """A hand should reset after using the empty command"""
        h = Hand()
        h.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        assert(h.score == 10)
        h.add(Card(CardValues.ACE, Suits.SPADES))
        assert(h.score == 21)
        h.empty()
        assert(h.score == 0)
        assert(len(h.cards) == 0)
        assert(h.containsAce == False)

    def test_dealInitialHands(self):
        """Each player should recive an card from the first to dealer in the initial deal
            This process should happend twice """

        table = Table()
        newPlayer = Player(0, '1', Role.HUMAN)
        table.activePlayers.append(newPlayer)
        newPlayer = Player(20, '2', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)
        newPlayer = Player(40, '3', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)

        table.dealInitialHands()

        for player in table.activePlayers:
            assert(len(player.hand.cards) == 2)

        for i in range(len(table.activePlayers)):
            assert(table.activePlayers[i].hand.cards[0] == table.deck._Deck__deck[i])
            assert(table.activePlayers[i].hand.cards[1] == table.deck._Deck__deck[i + 4])

        assert(table.hand.cards[0] == table.deck._Deck__deck[3])
        assert(table.hand.cards[1] == table.deck._Deck__deck[7])
    
    def test_playDealer(self):
        """the dealer should draw cards until his hand is 17 or greater"""
        table = Table()
        newPlayer = Player(0, '1', Role.HUMAN)
        newPlayer.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        newPlayer.hand.add(Card(CardValues.FOUR, Suits.DIAMONDS))
        table.activePlayers.append(newPlayer)

        table.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        table.hand.add(Card(CardValues.SIX, Suits.DIAMONDS))

        table.deck._Deck__deck[0] = Card(CardValues.ACE, Suits.DIAMONDS)

        table.playDealer()
        assert(len(table.hand.cards) == 3)
        assert(table.hand.score == 17)

    def test_playDealer_2(self):
        """the dealer should draw cards until his hand is 17 or greater"""
        table = Table()
        newPlayer = Player(0, '1', Role.HUMAN)
        newPlayer.hand.add(Card(CardValues.FOUR, Suits.DIAMONDS))
        newPlayer.hand.add(Card(CardValues.TWO, Suits.DIAMONDS))
        table.activePlayers.append(newPlayer)

        table.hand.add(Card(CardValues.ACE, Suits.DIAMONDS))
        table.hand.add(Card(CardValues.SIX, Suits.DIAMONDS))

        table.deck._Deck__deck[0] = Card(CardValues.TWO, Suits.DIAMONDS)

        table.playDealer()
        assert(len(table.hand.cards) == 2)
        assert(table.hand.score == 17)

    def test_playDealer_3(self):
        """the dealer should draw cards until his hand is 17 or greater"""
        table = Table()
        newPlayer = Player(0, '1', Role.HUMAN)
        newPlayer.hand.add(Card(CardValues.TEN, Suits.DIAMONDS))
        newPlayer.hand.add(Card(CardValues.EIGHT, Suits.DIAMONDS))
        table.activePlayers.append(newPlayer)

        table.hand.add(Card(CardValues.TEN, Suits.DIAMONDS))
        table.hand.add(Card(CardValues.EIGHT, Suits.DIAMONDS))

        table.deck._Deck__deck[0] = Card(CardValues.TWO, Suits.DIAMONDS)

        table.playDealer()
        assert(len(table.hand.cards) == 2)
        assert(table.hand.score == 18)

    def test_concludeRound(self):
        """at the end of the round  all players should be deleted properly and reset"""
        table = Table()
        newPlayer = Player(0, '1', Role.HUMAN)
        table.activePlayers.append(newPlayer)
        newPlayer = Player(20, '2', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)
        newPlayer = Player(40, '3', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)

        for player in table.activePlayers:
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        
        newPlayer = Player(40, '4', Role.HUMAN)
        newPlayer.bet = 20
        newPlayer.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        newPlayer.hand.add(Card(CardValues.ACE, Suits.DIAMONDS))
        table.activePlayers.append(newPlayer)

        table.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        table.hand.add(Card(CardValues.KING, Suits.DIAMONDS))

        table.concludeRound()
        assert(len(table.activePlayers) == 2)
        assert (table.activePlayers[0].name == '3')
        assert (table.activePlayers[1].name == '4')
        assert (len(table.activePlayers[0].hand.cards) == 0)
        assert (table.activePlayers[0].purse == 20)
        assert (table.activePlayers[1].purse == 60)
        assert (len(table.activePlayers[1].hand.cards) == 0)

    def test_concludeRoundPush(self):
        """at the end of the round  all players should be deleted properly and reset"""
        table = Table()
        newPlayer = Player(20, '1', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)

        for player in table.activePlayers:
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))

        table.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        table.hand.add(Card(CardValues.KING, Suits.DIAMONDS))

        table.concludeRound()
        assert(len(table.activePlayers) == 1)
        assert (table.activePlayers[0].name == '1')
        assert (len(table.activePlayers[0].hand.cards) == 0)
        assert (table.activePlayers[0].purse == 20)

    def test_checkGameEnd(self):
        """game should end when there are no active players at table"""
        table = Table()
        newPlayer = Player(20, '1', Role.HUMAN)
        table.players.append(newPlayer)

        assert(table.checkGameEnd() == True)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    cov.erase()
    def test_concludeRound(self):
        """at the end of the round  all players should be deleted properly and reset"""
        table = Table()
        newPlayer = Player(0, '1', Role.HUMAN)
        table.activePlayers.append(newPlayer)
        newPlayer = Player(20, '2', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)
        newPlayer = Player(40, '3', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)

        for player in table.activePlayers:
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        
        newPlayer = Player(40, '4', Role.HUMAN)
        newPlayer.bet = 20
        newPlayer.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        newPlayer.hand.add(Card(CardValues.ACE, Suits.DIAMONDS))
        table.activePlayers.append(newPlayer)

        table.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        table.hand.add(Card(CardValues.KING, Suits.DIAMONDS))

        table.concludeRound()
        assert(len(table.activePlayers) == 2)
        assert (table.activePlayers[0].name == '3')
        assert (table.activePlayers[1].name == '4')
        assert (len(table.activePlayers[0].hand.cards) == 0)
        assert (table.activePlayers[0].purse == 20)
        assert (table.activePlayers[1].purse == 60)
        assert (len(table.activePlayers[1].hand.cards) == 0)

    def test_concludeRoundPush(self):
        """at the end of the round  all players should be deleted properly and reset"""
        table = Table()
        newPlayer = Player(20, '1', Role.HUMAN)
        newPlayer.bet = 20
        table.activePlayers.append(newPlayer)

        for player in table.activePlayers:
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
            player.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))

        table.hand.add(Card(CardValues.QUEEN, Suits.DIAMONDS))
        table.hand.add(Card(CardValues.KING, Suits.DIAMONDS))

        table.concludeRound()
        assert(len(table.activePlayers) == 1)
        assert (table.activePlayers[0].name == '1')
        assert (len(table.activePlayers[0].hand.cards) == 0)
        assert (table.activePlayers[0].purse == 20)

    def test_checkGameEnd(self):
        """game should end when there are no active players at table"""
        table = Table()
        newPlayer = Player(20, '1', Role.HUMAN)
        table.players.append(newPlayer)

        assert(table.checkGameEnd() == True)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    cov.erase()
