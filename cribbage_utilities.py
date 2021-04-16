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
from itertools import combinations 
import pandas as pd

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
        if os.path.isfile('wjh_on_visual_studio.txt'):
            score_lookup_4 = pickle.load( open( "C:\\Users\\wj\\Documents\\cribbage\\static\\score_lookup_4.p", "rb" ))
            score_lookup_5 = pickle.load( open( "C:\\Users\\wj\\Documents\\cribbage\\static\\score_lookup_5.p", "rb" ))
        else:
            score_lookup_4 = pickle.load( open( "C:\\Users\\Walt\\OneDrive\\Documents\\Programming\\Python\\Cribbage\\static\\score_lookup_4.p", "rb" ))
            score_lookup_5 = pickle.load( open( "C:\\Users\\Walt\\OneDrive\\Documents\\Programming\\Python\\Cribbage\\static\\score_lookup_5.p", "rb" ))    
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

def sum_combinations (comb):
    lsum = 0
    for c in comb:
        if np.sum(c) == 15:
            lsum += 2 
    return lsum

def score_15 (hand):
    hand = np.array(hand)
    #print ('in score 15, hand is ' + str(hand))
    #new_hand = np.array(hand)
    # discard the suit
    new_hand = hand % 100
    # convert JQK to 10
    new_hand[new_hand > 10] = 10
    sum_15 = 0
    for i in range(2,6):
        comb = combinations(new_hand,i)
        sum_15 += sum_combinations (comb)
    return sum_15                    

def is_run (arr):
    is_run = True
    prior = arr[0]
    for a in arr[1:]:
        consecutive = (prior + 1) == a
        is_run = is_run and consecutive
        #print (is_run)
        prior = a.copy()
    return is_run
#a = np.array ([4,5,6,7])
#print (is_run(a))

def score_run (hand):
    new_hand = hand % 100
    sortedn = np.sort(new_hand)
    sum_comb = 0
    if (len(sortedn) == 5) and is_run(sortedn):
        return 5
    for c in combinations(sortedn,4):
        if is_run(c):
            sum_comb += 4
    if sum_comb == 0: # there are no 4 way combinations
        for c in combinations(sortedn,3):
            if is_run(c):
                sum_comb += 3
    return sum_comb  

def score_pairs (hand):
    new_hand = hand % 100
    sum_pairs = 0
    for c in combinations(new_hand,2):
        if c[0] == c[1]:        
            sum_pairs += 2
    return sum_pairs    

def score_flush (hand):
    suits = hand // 100
    #print (suits)
    if len(hand) == 5:
        result = len(set(suits)) == 1  
        if result:
            return 5
    result = len(set(suits[:4])) == 1  
    if result:
        return 4
    else:
        return 0

def score_nobs (hand):
    if len(hand) < 5:
        return 0
    starter = hand[4]
    if starter % 100 == 11:
        return 0 #heels    
    # starter card is last in list
    starter_suit = hand[4] // 100
    #print (starter_suit)

    jacks = []
    for c in hand:
        if c % 100 == 11:
            jacks.append(c)
    #print (jacks)
    if len(jacks) == 0:
        return 0
    else:    
        suits = np.array(jacks) // 100
        is_nobs = False
        for s in suits:
            is_nobs = is_nobs or (s == starter_suit)
        return int(is_nobs)
#hnd = [103,204,311,411,410]        
#print (score_nobs (hnd))       

def score_all (hand):
    total = 0
    s15 = score_15(hand)
    runs = score_run(hand)
    pairs = score_pairs(hand)
    flush = score_flush(hand)
    nobs = score_nobs(hand)
    total = s15 + runs + pairs + flush + nobs
    return s15, runs, pairs, flush, nobs, total

def score_all_numeric (hand):
    total = 0
    s15 = score_15(hand)
    runs = score_run(hand)
    pairs = score_pairs(hand)
    total = s15 + runs + pairs
    return s15, runs, pairs, total

def create_deck ():
    deck = []
    for s in range (1,5):
        for n in range (1,14):
            deck.append (s*100 + n)
    deck_set = set(deck)
    return deck, deck_set
deck, deck_set = create_deck()

def score_mean (tmp_hand, full_hand):
    all_scores = []
    #print ('for tmp hand ' + str(tmp_hand))
    remaining = deck_set.difference(set(full_hand))     
    for c in remaining:
        #tmp = tmp_hand.copy()
        tmp = np.append(tmp_hand, c)
        (s15, runs, pairs, flush, nobs, total) = score_all (tmp)
        #print (total)
        all_scores.append (total)

#    print ('mean score is ' + str(np.mean(all_scores)))
    return np.mean(all_scores) 
        

def score_crib (tmp_hand,full_hand,use_full_hand):
    all_scores = []

    if use_full_hand:
        remaining = deck_set.difference(set(full_hand))
    else:
        remaining = deck_set.difference(set(tmp_hand))    
    for c in combinations(remaining,2):

        tmp = np.append(tmp_hand,c)
        (s15, runs, pairs, flush, nobs, total) = score_all (tmp)       
        all_scores.append (total)
        #print (total)    
    return np.mean(all_scores), all_scores

#make a list from key

def key_to_list (key):
    length = round((len(str(key)) + 0.001)/2)
    #print (length)
    lst = []
    rem = key
    for i in reversed (range(length)):
        digit = rem // 100**i
        rem = key % (100**i)
        lst.append (digit)
    return np.array(lst)

# make a key from a list

def list_to_key (lst):
    k = 0
    for i, l in enumerate(reversed(lst)):

        k += l * (100**i)
    return k    
# call like this: k = list_to_key (sorted([13,12,2,3,4]))       

card_lookup, card_lookup_reverse = init_cards()
score_lookup_4, score_lookup_5 = init_score_lookup()

'''
There are 2 cards passed to the crib, plus the potential starter, plus the remaining cards in the deck after the 6 card hand.

'''
def evaluate_crib_w_starter (cards, starter, remaining):
    i = 0
    l_remaining = remaining.difference ([starter])
    #    print (l_remaining)
    score_list = []
    for c in combinations(l_remaining,2):
        hand = []
        #print (c)
        hand = list(cards) + [starter] + list(c)
        #print (hand)
        hand = np.array(hand) % 100
        #print (hand)
        
        score = score_lookup_5[list_to_key(sorted(hand))] + score_flush(hand) + score_nobs(hand)

        score_list.append(score)
        i += 1
    
    return (np.mean(score_list))   
"""
This function differs in that the starter is not passed. Instead 3 random cards
added to the crib from the remaining cards. This is not quite as accurate, but
should suffice, given that 46-C-3 hands are evaluated.
"""
def evaluate_crib_wo_starter (cards, remaining):

    #    print (l_remaining)
    #print ('crib cards are ' + str(cards))
    score_list = []
    for c in combinations(remaining,3):
        hand = []
        #print (c)
        hand = list(cards) + list(c)
        #print (hand)
        hand = (np.array(hand) % 100)
        #print (hand)
        
        score = score_lookup_5[list_to_key(sorted(hand))] + score_flush(hand) + score_nobs(hand)

        score_list.append(score)
    #print (len(score_list))
    
    return (np.mean(score_list))   

if False: # this is test code only
    hnd = [101,203,204,205,307,308]
    hd = [101,203,204,205]
    remaining = deck_set.difference(hnd)
    crib = set(hnd).difference(set(hd))  
    for i in range(15):
        for s in remaining:
    
            evaluate_crib_w_starter (crib,s,remaining)

    print (evaluate_crib_wo_starter(crib,remaining))

def evaluate_hand (hand, ):
    remaining = deck_set.difference (set(hand))
    results = []
    for c in combinations(hand,4):
        crib = set(hand).difference (c)
        score_list = []
        for r in remaining:
            hnd = []
            hnd = list(c) + [r]
            hnd = np.array(hnd) % 100
            sorted_hnd = sorted(hnd)
            #print (sorted_hnd)
            score = score_lookup_5[list_to_key(sorted_hnd)] + score_flush(hnd) + score_nobs(hnd)
            score_list.append (score)
        #print ('hand:' + str(hnd))        
        hand_score = np.mean (score_list)

        #print ('crib:'+str(crib))
        crib_score = evaluate_crib_wo_starter(crib,remaining) 
        lcrib = list(crib)

        #print (crib_score)
        results.append ([list(c), list(crib), hand_score, crib_score, hand_score+crib_score, hand_score-crib_score])
    results = pd.DataFrame(results)
    results.columns = ['Hand','Crib','Hand Score','Crib Score','Dealer','Opponent']
    return results


computer_hand = [401,201,305,208,313,213]


def pick_best_hand (hand, player_crib):
    computer_crib = not player_crib
    evaluation = evaluate_hand(hand)
    if computer_crib:
        print ('computer crib')
        crib_owner = 'C'
        #print ('computer hand/crib cards are ')
        best = evaluation.sort_values('Dealer',ascending=False).head(5)
        #print (best)
        hnd = best['Hand']

        crb = best['Crib']
        cr = [c for c in crb]
        
    else:
        crib_owner = 'P'
        #print ('player hand/crib cards are ')
        best = evaluation.sort_values('Opponent',ascending=False).head(5)
        #print (best)
    hnd = best['Hand']
    crb = best['Crib']
    cr = [c for c in crb]
    #print (hnd)
    hd = [h for h in hnd]
    #print (hd[0])
    cr[0]
    return hd[0], cr[0]
computer_hand = ([104,105,206,307,205,308])
computer_hand = [401,201,305,208,313,213]
#print (pick_best_hand(computer_hand,player_crib=True))