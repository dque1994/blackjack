__author__ = 'miller'

import random
import numpy as np

#print(random.randint(1,13))

def deck(n):
    if n not in range(14):
        print('number not in between 1 and 13')
    elif n == 1:
        card = 'ace'
    elif n <= 10:
        card = n
    else:
        card = 10
    return card

def deal():
    rand1 = random.randint(1,13)
    rand2 = random.randint(1,13)
    rand3 = random.randint(1,13)
    rand4 = random.randint(1,13)
    dealer = [deck(rand1),deck(rand2)]
    player = [deck(rand3),deck(rand4)]
    return [dealer,player]

def dealer_logic(hand):
    dealer_hand = hand
    if (dealer_hand[0] == 'ace') and (dealer_hand[1] == 'ace'):
        soft = True
        dealer_hand[0] = 11
        dealer_hand[1] = 1

    if dealer_hand[0] == 'ace':
        soft = True
        dealer_hand[0] = 11
    elif dealer_hand[1] == 'ace':
        soft = True
        dealer_hand[1] = 11
    else:
        soft = False




    total = dealer_hand[0]+dealer_hand[1]
    if total >= 17:
        return ('stay',total)
    else:
        if soft == True:
            return ('hitsoft',total)
        else:
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
