# -*- coding: utf-8 -*-
"""
Cribbage Utilities
Created on Sat Mar 20 07:35:09 2021

@author: wj
"""

import random
import pickle
import numpy as np
import os

cards = []
card_filenames = []


 # call with card_lookup, card_lookup_reverse = init_cards()

def init_cards():
    for s,name in enumerate(['SPADE','HEART','DIAMOND','CLUB']):
        for c in range (1,14):
            crd = (s+1) * 100 + c
            cards.append (crd)
            nm = name + '-' + str(c)
            if c == 11:
                nm += '-JACK'
            elif c == 12:
                nm += '-QUEEN'
            elif c == 13:
                nm += '-KING'
            nm += '.svg'
            card_filenames.append (nm)
    c_lookup = {c:n for c,n in zip(cards,card_filenames)}
    c_lookup_reverse = {n:c for c,n in zip(cards,card_filenames)}
    return c_lookup, c_lookup_reverse
"""
call with player_deals, player_card, computer_card = determine_dealer()
"""
def determine_dealer():
    player_wins = False
    drawing = True
    while drawing:
        sample = random.sample(cards,2)
        cv0 = sample[0]
        cv1 = sample[1]
        #print (cv0 % 100)
        #print (cv1 % 100)
        if cv0 % 100 == cv1 % 100:
            pass
        else:
            drawing = False
            if cv0%100 < cv1%100:
                player_wins = True
            return player_wins, cv0, cv1


class Hands:
    computer_hand = []
    player_hand = []
    starter = []

    def __init__(self):
        pass

    def deal_hands (self):
        hands = random.sample (cards,13)
        #print (hands)

        self.player_hand = hands[:6]
        self.computer_hand = hands[6:12]
        self.starter = hands[12]
    def get_player_hand (self):
        hand = np.array(self.player_hand)
        hand_n = (hand % 100)
        stacked = np.column_stack([hand, hand_n])
        sorted_hand = stacked[stacked[:, 1].argsort()]
        return (sorted_hand[:,0])

    def get_computer_hand (self):
        hand = np.array(self.computer_hand)
        hand_n = (hand % 100)
        stacked = np.column_stack([hand, hand_n])
        sorted_hand = stacked[stacked[:, 1].argsort()]
        return (sorted_hand[:,0])

    def get_starter_card (self):
        return [self.starter]

def init_score_lookup ():

    if os.path.isfile('OnlyOnVisualStudio.txt'):
        score_lookup_4 = pickle.load( open( "C:\\Users\\wj\\Documents\\cribbage\\static\\score_lookup_4.p", "rb" ))
        score_lookup_5 = pickle.load( open( "C:\\Users\\wj\\Documents\\cribbage\\static\\score_lookup_5.p", "rb" ))
    else:
        score_lookup_4 = pickle.load( open( "/home/cribbage152154/mysite/static/score_lookup_4.p", "rb" ))
        score_lookup_5 = pickle.load( open( "/home/cribbage152154/mysite/static/score_lookup_5.p", "rb" ))
    return score_lookup_4, score_lookup_5


def test_deal():
    h = Hands()
    random.seed(2)
    h.deal_hands()

    player_hand = h.get_player_hand()
    player_cardnames = [card_lookup[cn] for cn in player_hand]
    computer_hand = h.get_computer_hand()
    starter = h.get_starter_card()
    assert player_hand.all() == np.array([404,108,408,209,111,112]).all(), 'Invalid player hand'
    print (player_hand)
    print (player_cardnames)
    print (computer_hand)
    print (starter)

card_lookup, card_lookup_reverse = init_cards()
score_lookup_4, score_lookup_5 = init_score_lookup()
