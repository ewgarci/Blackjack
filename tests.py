#!flask/bin/python
# -*- coding: utf-8 -*-
import unittest
from blackjack import Player, Table, Role, States, Deck, Hand, Suits, CardValues, suitDict, cardValues  
from coverage import coverage

cov = coverage(branch = True, omit = ['flask/*', 'tests.py'])
cov.start()

class TestDeck(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_createSingleDeck(self):
        """A single deck should have 52 cards and all should be unique """

    def test_createMultipleDeck(self):
        """A deck made of 5 decks should have 5 of each card """

    def test_createDeckShuffled(self):
        """Cards in a shuffled deck should be in a different order than it was previously """

    def test_compareShuffledDecks(self):
        """The same Deck shuffled at different times should have different ordering  """

    def test_getCard(self):
        """Getting the next card should produces cards in sequencial index order""" 
    
    def test_getCardEnd(self):
        """Getting the next card should return None if no more cards are left""" 

class TestHand(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):
        """A hand should calculate the score correctly with every card added"""

    def test_addAce(self):
        """A hand should the highest score when an ace is added"""
    
    def test_addAce2(self):
        """A hand should the highest score when 2 aces are added"""
    
    def test_addAce2_1(self):
        """A hand should the highest score when 2 aces are added"""
    
    def test_addAce2_2(self):
        """A hand should the highest score when 2 aces are added"""

    def test_addAce4(self):
        """A hand should the highest score when 4 aces are added"""
    
    def test_addAce11(self):
        """A hand should the highest score when 11 aces are added"""
    
    def test_addAce12(self):
        """A hand should bust when 12 aces are added"""

    def test_empty(self):
        """A hand should reset after using the empty command"""

if __name__ == '__main__':
    unittest.main()
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
    cov.html_report(directory = 'tmp/coverage')
    cov.erase()
