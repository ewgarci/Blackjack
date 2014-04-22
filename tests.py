#!flask/bin/python
# -*- coding: utf-8 -*-
import unittest, copy
from blackjack import Player, Table, Role, Deck, Hand, Suits, CardValues, suitDict, cardValues, Card
from coverage import coverage
from collections import Counter

cov = coverage(branch = True, omit = ['flask/*', 'tests.py'])
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
            a1.append(card.value + card.suit)
        deck.shuffle()

        for card in deck._Deck__deck:
            a2.append(card.value + card.suit)

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
            a1.append(card.value + card.suit)

        for card in deck2._Deck__deck:
            a2.append(card.value + card.suit)

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
            assert(a[i].value + a[i].suit == deck._Deck__deck[i].value + deck._Deck__deck[i].suit)


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
