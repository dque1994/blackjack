__author__ = 'miller'

import random
import numpy as np

#print(random.randint(1,13))

#defines a variable card for a value of n between 1 and 13
#'ace' is a string; 2 through 10 are numeric
#if/elif/else structure checks 'if' condition first, then 'elif' conditions in order, then 'else' condition last
def deck(n):                                       
    if n not in range(14):                          #error checking for n not between 1 and 13
        print('number not in between 1 and 13')
    elif n == 1:                                    #defines card as 'ace' for n = 1
        card = 'ace'
    elif n <= 10:                                   #defines card as n for 2 <= n <= 10 
        card = n
    else:                                           #defines card as 10 for 11, 12, or 13 (J,Q,K)
        card = 10
    return card                                     #returns the value of 'card'

#deals a hand to the dealer and to the player
def deal():
    rand1 = random.randint(1,13)                    #random integer between 1 and 13, inclusive
    rand2 = random.randint(1,13)
    rand3 = random.randint(1,13)
    rand4 = random.randint(1,13)
    dealer = [deck(rand1),deck(rand2)]              #list of cards in dealer's hand
    player = [deck(rand3),deck(rand4)]              #list of cards in player's hand
    return [dealer,player]                          #returns list of dealer and player's hands

#logic function; takes dealer hand (list) as argument and checks if dealer has an ace; if dealer has an ace, his hand is soft
#and he would be required to hit if his intitial hand is 17. 'soft' is a Boolean variable (True or False). 'total' is a numerical
#value equal to the value of the dealer's hand. 'stay', 'hitsoft', and 'hit' are strings
def dealer_logic(hand):
    dealer_hand = hand
    if (dealer_hand[0] == 'ace') and (dealer_hand[1] == 'ace'):     #if both cards are aces, one must be worth 11 and the other must be worth 1
        soft = True
        dealer_hand[0] = 11
        dealer_hand[1] = 1

    if dealer_hand[0] == 'ace':             #if first card is an ace, set 'soft' equal to True and assign a value of 11 to the ace
        soft = True
        dealer_hand[0] = 11
    elif dealer_hand[1] == 'ace':           #if first card is not an ace but second card is, set 'soft' equal to True and assign a value of 11 to the ace
        soft = True
        dealer_hand[1] = 11
    else:                                   #if dealer doesn't have an ace, set 'soft' equal to False
        soft = False

    total = dealer_hand[0]+dealer_hand[1]   #sums the value of the two cards in the dealer's hand
    if total >= 17:                         #if 'total' is greater than or equal to 17, dealer must stay. return string 'stay' and numeric 'total'
        return ('stay',total)
    else:                                   #else ('total' is less than 17)
        if soft == True:                        #if 'soft' is True(i.e., dealer has an ace) return string 'hitsoft' and numeric 'total' 
            return ('hitsoft',total)
        else:                                   #else (dealer doesn't have an ace) return string 'hit' and numeric 'total'
            return ('hit',total)


def hit_soft_loop(total):
    card_total = total
    randcard = deck(random.randint(1,13))
    if randcard == 'ace':
        card_total += 1
    else:
        card_total += randcard
    if card_total > 21:
        return (card_total-10)
    elif card_total >= 17:
        return card_total
    else:
        return hit_soft_loop(card_total)

def hit_loop(total):
    card_total = total
    randcard = deck(random.randint(1,13))
    if randcard == 'ace':
        if card_total > 10:
            card_total += 1
            if 17 <= card_total <= 21:
                return card_total
            else:
                return hit_loop(card_total)
        else:
            card_total += 11
            if 17 <= card_total <= 21:
                return card_total
            else:
                new_total = hit_soft_loop(card_total)
                if 17 <= new_total <=21:
                    return new_total
                else:
                    return hit_loop(new_total)
    else:
        card_total += randcard
        if 17 <= card_total <= 21:
            return card_total
        elif card_total > 21:
            return 'bust'
        else:
            return hit_loop(card_total)

def play_a_hand_dealer(hand):
    logic = dealer_logic(hand)
    if logic[0] == 'stay':
        return logic[1]
    elif logic[0] == 'hitsoft':
        no_soft = hit_soft_loop(logic[1])
        if no_soft >= 17:
            return no_soft
        else:
            dealer = hit_loop(no_soft)
            return dealer

    else:
        dealer = hit_loop(logic[1])
        return dealer


#print(hit_loop(5))
#dealer = deal()[0]
#print(play_a_hand_dealer(dealer))

#for i in range(500):
#    dealer = deal()[0]
#    play_a_hand_dealer(dealer)

trans_array = np.zeros((18,3))
for i in range(18):
    for j in range(10000):
        player_score = i+4
        dealer_hand = deal()[0]
        dealer_score = play_a_hand_dealer(dealer_hand)
        if dealer_score == 'bust':
            dealer_score = 0
        if player_score > dealer_score:
            trans_array[i][0] += 1
        elif player_score == dealer_score:
            trans_array[i][1] += 1
        else:
            trans_array[i][2] += 1

normal_trans = np.zeros((18,3))
i = 0
for row in trans_array:
    row_sum = 0
    for elements in row:
        row_sum += elements
    j = 0
    for element in row:
        normal_trans[i][j] = element/row_sum
        j += 1
    i += 1

print(normal_trans)
