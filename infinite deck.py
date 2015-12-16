__author__ = 'miller'
__guy_who_looked_over_Jims_shoulder_and_also_wrote_some_cool_stuff__ = 'que'

#Not entirely sure about common commenting ettiquette

############## THIS MODULE CALCULATES THE BASIC PROBABILITIES FOR THE MODEL - STAYING AND HITTING ######################
###################### #ALSO CONTAINS DEALER A.I. AND NECESSARY FUNCTIONS FOR DEALING CARDS ############################

######## EVERY FUNCTION WILL BE PREFACED WITH A BASIC DESCRIPTION AS WELL AS THE ARGUMENTS AND THE RETURN VALUE ########

import random
import numpy as np

#Selects a card, converting int 1 to ace as str and ints 11-13 to int 10
#ARGS: n (n must be an int between 0 and 13 inclusive)
#RETURN: value of card as int or str
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

#Deals a hand to a player and dealer. Each hand contains two cards
#ARGS: none
#RETURN: list containing lists of dealer hand, player hand
def deal():
    rand1 = random.randint(1,13)
    rand2 = random.randint(1,13)
    rand3 = random.randint(1,13)
    rand4 = random.randint(1,13)
    dealer = [deck(rand1),deck(rand2)]
    player = [deck(rand3),deck(rand4)]
    return [dealer,player]

#Determines what course of action the dealer must take
#ARGS: hand as list of length 2
#RETURN: command as str ('hit', 'hitsoft', or 'stay') and total score as int
def dealer_logic(hand):
    dealer_hand = hand
    if (dealer_hand[0] == 'ace') and (dealer_hand[1] == 'ace'):
        soft = True
        dealer_hand[0] = 11
        dealer_hand[1] = 1

    elif dealer_hand[0] == 'ace':
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

#Called in hit situation if hand contains an ace
#ARGS: total score as int
#RETURN: new total as int OR calls hit_soft_loop() again on new total
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

#Called in hit situation, hand doesn't contain ace
#ARGS: total score as int
#RETURN: new total as int OR calls hit_loop() again on new total OR calls hit_soft_loop() on new total
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

#Plays a hand as the dealer. Must stay at or above 17, hit below 17
#ARGS: hand as list
#RETURN dealer score as int (score) OR dealer score as str ('bust')

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


####################################### CALCULATION OF STAY/HIT PROBABILITIES ##########################################

############################################## STAY PROBABILITIES ######################################################

#Calculate the probabilities of winning, pushing, and losing assuming the player constantly stays. Dealer, of course, is
##required to follow standard dealer protocol

#Create three 18x13 arrays of zeroes- one each for winning, pushing, losing
win_array = np.zeros((18,13))
push_array = np.zeros((18,13))
lose_array = np.zeros((18,13))

#row i represents a player's total score without regard for the cards that comprise the score
#column j represents the dealer's face-up card
#counter k controls the number of trials. k trials run for each [i][j] entry
#This for-loop populates the three arrays with the number of instances of each occurrence at each combination of player
##score and dealer face-up card
for i in range(18):
    for j in range(13):
        for k in range(10000):
            player_score = i+4
            dealer_hand = [deck(j+1),deck(random.randint(1,13))]
            dealer_score = play_a_hand_dealer(dealer_hand)

            if dealer_score == 'bust':
                dealer_score = 0

            if (10 in dealer_hand) and ('ace' in dealer_hand):
                dealer_blackjack = True
            else:
                dealer_blackjack = False

            if player_score == 21:
                player_blackjack = True
            else:
                player_blackjack = False

            if (dealer_blackjack == False) and (player_blackjack == False):

                if player_score > dealer_score:
                    win_array[i][j] += 1
                elif player_score == dealer_score:
                    push_array[i][j] += 1
                else:
                    lose_array[i][j] += 1

            elif (dealer_blackjack == False) and (player_blackjack == True):

                win_array[i][j] += 1

            elif (dealer_blackjack == True) and (player_blackjack == False):

                lose_array[i][j] += 1

            else:

                push_array[i][j] += 1

#Create three more 18x13 arrays of zeroes
win_norm = np.zeros((18,13))
push_norm = np.zeros((18,13))
lose_norm = np.zeros((18,13))

#This for-loop iterates through each array (win,push,lose) and normalizes them by dividing entry [i][j] of a given array
##by the total of the entries at [i][j] for each array
for l in range(18):
    for m in range(13):
        total = win_array[l][m]+lose_array[l][m]+push_array[l][m]
        win_norm[l][m] = win_array[l][m]/total
        push_norm[l][m] = push_array[l][m]/total
        lose_norm[l][m] = lose_array[l][m]/total

#Write the results to separate .txt files
f = open('win_probs_no_hit.txt','w')
f.write("Probabilities of Winning (rows represent total of player's cards (4-21), columns represent card dealer shows (ace,2,...,king)"+'\n')
for line in win_norm:
    for element in line:
        string = str(element)+'\t'
        f.write(string)
    f.write('\n')

g = open('push_probs_no_hit.txt','w')
g.write("Probabilities of Pushing (rows represent total of player's cards (4-21), columns represent card dealer shows (ace,2,...,king)"+'\n')
for line in push_norm:
    for element in line:
        string = str(element)+'\t'
        g.write(string)
    g.write('\n')

h = open('lose_probs_no_hit.txt','w')
h.write("Probabilities of Losing (rows represent total of player's cards (4-21), columns represent card dealer shows (ace,2,...,king)"+'\n')
for line in lose_norm:
    for element in line:
        string = str(element)+'\t'
        h.write(string)
    h.write('\n')

############################################### HIT PROBABILITIES ######################################################

#Need to separately consider hands with aces and hands sans aces

#The list cards_under treats aces as having value 1, meaning that the player's score is 11 or greater
cards_under = [1,2,3,4,5,6,7,8,9,10,10,10,10]
#The list cards_over treats aces as having value 11, meaning that the player's score is 10 or less
cards_over = [11,2,3,4,5,6,7,8,9,10,10,10,10]

#You know the drill by now
win_hit_array = np.zeros((18,13))
push_hit_array = np.zeros((18,13))
lose_hit_array = np.zeros((18,13))

#This for-loop iterates through possible scores from 4-10 inclusive. A new card is added to the player's score. Since it
## is imppossible to uust here, the appropriate row index [new_total - 4] (-4 to line up properly with the array index)
## is multiplied by (1/13) and added to the row index [i - 4], with the gentle reminder that i is the original score
for i in (4,5,6,7,8,9,10):
    for card in cards_over:
        new_total = i+card
        win_hit_array[i-4] += (1/13)*win_norm[new_total-4]
        push_hit_array[i-4] += (1/13)*push_norm[new_total-4]
        lose_hit_array[i-4] += (1/13)*lose_norm[new_total-4]

#Same story for possible score from 11-21 inclusive. If new_total > 21, the player busts and only lose_hit_array is incremented
for i in (11,12,13,14,15,16,17,18,19,20,21):
    for card in cards_under:
        new_total = i+card
        if new_total <= 21:
            win_hit_array[i-4] += (1/13)*win_norm[new_total-4]
            push_hit_array[i-4] += (1/13)*push_norm[new_total-4]
            lose_hit_array[i-4] += (1/13)*lose_norm[new_total-4]
        else:
            win_hit_array[i-4] += 0
            push_hit_array[i-4] += 0
            lose_hit_array[i-4] += (1/13)

######################################## Write results to separate .txt files ##########################################
f2 = open('win_probs_hit.txt','w')
f2.write("Probabilities of Winning After Hit (rows represent total of player's cards (4-21), columns represent card dealer shows (ace,2,...,king)"+'\n')
for line in win_hit_array:
    for element in line:
        string = str(element)+'\t'
        f2.write(string)
    f2.write('\n')

g2 = open('push_probs_hit.txt','w')
g2.write("Probabilities of Pushing After Hit (rows represent total of player's cards (4-21), columns represent card dealer shows (ace,2,...,king)"+'\n')
for line in push_hit_array:
    for element in line:
        string = str(element)+'\t'
        g2.write(string)
    g2.write('\n')

h2 = open('lose_probs_hit.txt','w')
h2.write("Probabilities of Losing After Hit (rows represent total of player's cards (4-21), columns represent card dealer shows (ace,2,...,king)"+'\n')
for line in lose_hit_array:
    for element in line:
        string = str(element)+'\t'
        h2.write(string)
    h2.write('\n')
