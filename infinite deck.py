__author__ = 'miller'

import random
import numpy as np

#print(random.randint(1,13))

#returns a variable 'card' for a value of n between 1 and 13
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

#loop that simulates hitting on a soft hand; this function is called later in the hit_loop() and play_a_hand_dealer() functions;
#first checks value of the next card drawn, then checks the total value of the player's hand
def hit_soft_loop(total):
    card_total = total                          #'card_total' is a placeholder variable that takes the intial value of 'total'; it's the player's score
    randcard = deck(random.randint(1,13))       #'randcard' is a random value, either 'ace' or an integer from 2-10, resulting from calling deck()
    if randcard == 'ace':                       #if 'randcard' is an ace, increment 'card_total' by 1
        card_total += 1                     
    else:                                       #else increment 'card_total' by the value of 'randcard'
        card_total += randcard
    if card_total > 21:                         #if 'card_total' is greater than 21, the ace already in the hand takes a value of 1,
        return (card_total-10)                  #so return 10 less than 'card_total'
    elif card_total >= 17:                      #elif 'card_total' is >= 17 (and <= 21) return the straight up value of 'card_total'
        return card_total       
    else:                                       #else, iterate through the loop again
        return hit_soft_loop(card_total)

#loop that simulates a hit; this function is called later in the play_a_hand_dealer() function
#continues to hit until the hand is between 17 and 21 inclusive, or a bust
def hit_loop(total):
    card_total = total                          #'card_total' is a placeholder variable that takes the initial value of 'total'; it's the player's score
    randcard = deck(random.randint(1,13))       #'randcard' is a random value, either 'ace' or an integer from 2-10, resulting from calling deck() 
    if randcard == 'ace':                       #check if 'randcard' is an ace. if so:
        if card_total > 10:                         #if 'card_total' is greater than 10, increment by 1
            card_total += 1         
            if 17 <= card_total <= 21:                  #if 'card_total' is between 17 and 21, inclusive, return 'card_total'
                return card_total
            else:                                       #else iterate through hit_loop() again
                return hit_loop(card_total)
        else:                                       #else increment 'card_total' by 11
            card_total += 11
            if 17 <= card_total <= 21:                  #if 'card_total' is between 17 and 21, inclusive, return 'card_total'
                return card_total
            else:                                   #else (if card_total < 17) create a new variable 'new_total' and set it equal to the value returned by hit_soft_loop() with argument 'card_total' (hit on a soft hand)
                new_total = hit_soft_loop(card_total)
                if 17 <= new_total <=21:                #if 'new_total' is between 17 and 21 inclusive, return 'new_total'
                    return new_total
                else:                                   #else iterate through hit_loop() again, this time with argument 'new_total'
                    return hit_loop(new_total)
    else:                                       #else increment 'card_total' by the value of 'randcard'
        card_total += randcard
        if 17 <= card_total <= 21:                  #if 'card_total' is between 17 and 21 inclusive, return 'card_total'
            return card_total
        elif card_total > 21:                       #elif 'card_total' is greater than 21, bust
            return 'bust'
        else:                                       #else iterate through hit_loop again, this time with 'card_total' as the argument
            return hit_loop(card_total)

#simulates a hand for the dealer; dealer must hit on 16 and below, as well as on soft 17 (ace and a 6)
#takes as an argument a 2-element list comprised of the dealer's 2 cards
def play_a_hand_dealer(hand):                   #'hand' is the dealer's hand
    logic = dealer_logic(hand)                  #calls dealer_logic() on 'hand' and sets it equal to a variable 'logic'
    if logic[0] == 'stay':                      #if dealer has to stay, return logic[1], which is the value of the hand
        return logic[1]
    elif logic[0] == 'hitsoft':                 #elif dealer has a soft hand and is required to hit, begin that process
        no_soft = hit_soft_loop(logic[1])           #call hit_soft_loop() on the current value of the hand and set it equal to new variable 'no_soft'
        if no_soft >= 17:                           #if 'no_soft' is greater than or equal to 17, return 'no_soft' 
            return no_soft
        else:                                       #else call hit_loop() on 'no_soft' and set it equal to new variable 'dealer'
            dealer = hit_loop(no_soft)              
            return dealer                               #return 'dealer'

    else:                                       #else call hit_loop() on logic[1], which is the value of the hand
        dealer = hit_loop(logic[1])             #set it equal to new variable 'dealer'
        return dealer                           #return 'dealer'


#print(hit_loop(5))
#dealer = deal()[0]
#print(play_a_hand_dealer(dealer))

#for i in range(500):
#    dealer = deal()[0]
#    play_a_hand_dealer(dealer)

trans_array = np.zeros((18,3))          #creates an 18 x 3 array of zeroes

#monte carlo simulation, runs 10000 trials for every score from 4 to 21 and populates 'trans_array' instances of winning, pushing, and losing (from the player's perspective)
#column 0 = player win, column 1 = push, column 2 = player loss
for i in range(18):                                         #for every i from 0 to 17 inclusive:
    for j in range(10000):                                      #for every j from 0 to 9999 inclusive
        player_score = i+4                                          #set 'player_hand' equal to i+4
        dealer_hand = deal()[0]                                     #call deal() and set 'dealer_hand' equal to the 'dealer' value returned by 'deal'
        dealer_score = play_a_hand_dealer(dealer_hand)              #call play_a_hand_dealer() on 'dealer_hand', set it equal to 'dealer_score'
        if dealer_score == 'bust':                                  #if 'dealer_score' is a bust, reset 'dealer_score' to 0
            dealer_score = 0
        if player_score > dealer_score:                             #if player_score is greater than dealer_score, increment the 'i'th row of column 0 by 1
            trans_array[i][0] += 1
        elif player_score == dealer_score:                          #elif 'player_score' is equal to 'dealer_score', increment the 'i'th row of column 1 by 1
            trans_array[i][1] += 1
        else:                                                       #else, increment the 'i'th row of column 2 by 1
            trans_array[i][2] += 1

normal_trans = np.zeros((18,3))         #creates an 18 x 3 array of zeroes

#normalize 'trans_array'
i = 0                                   #initialize i as 0
for row in trans_array:                 #iterates over each row in 'trans_array'
    row_sum = 0                             #set 'row_sum' = 0 at the beginning of each iteration
    for elements in row:                    #calculate the sum of the row elements (wins, pushes, and losses)
        row_sum += elements
    j = 0                               #initialize j as 0
    for element in row:                 #divide each element in each row by the row sum to normalize the array
        normal_trans[i][j] = element/row_sum
        j += 1                          #increment j by 1
    i += 1                          #increment i by 1

print(normal_trans)                 #print the normalized array


#The following produces tables that show the calculated probabilities of a player winning, pushing, and losing against the dealer.
#Losing in this case means either a bust, or finishing with a score lower than the dealer.
#The first table shows the probabilities of winning, pushing, and losing when a player doesn't hit after the initial deal; the
#second table shows the same probabilites if a player hits once on their initial hand

#create three 18x13 arrays; one each to contain the probabilities of winning, pushing, and losing. Each array has 18 rows to account 
#for the 18 different possible scores, and 13 columns to account for the 13 possible cards to receive on a hit
win_array = np.zeros((18,13))       
push_array = np.zeros((18,13))
lose_array = np.zeros((18,13))

#Populate the win, push, and lose arrays with the number of instances of each occurence for every combination of player and
#dealer hands
for i in range(18):             #controls the player scores
    for j in range(13):             #controls the dealer scores
        for k in range(10000):          #runs 10000 trials for each combination of player and dealer hands
            player_score = i+4              #i runs from 0 to 17, so player score will run from 4 to 21
            dealer_score = play_a_hand_dealer([deck(j+1),deck(random.randint(1,13))])   #calls play_a_hand_dealer() on the 2-element list comprised of calling deck() on j+1 and calling deck on a random integer from 1 to 13, and assigns it to new variable 'dealer_score'
            if dealer_score == 'bust':      
                dealer_score = 0
            if (10 in dealer_hand) and ('ace' in dealer_hand):  #checks if dealer has blackjack; if so, 
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

# print(win_array)
# print(push_array)
# print(lose_array)

win_norm = np.zeros((18,13))
push_norm = np.zeros((18,13))
lose_norm = np.zeros((18,13))

for l in range(18):
    for m in range(13):
        total = win_array[l][m]+lose_array[l][m]+push_array[l][m]
        win_norm[l][m] = win_array[l][m]/total
        push_norm[l][m] = push_array[l][m]/total
        lose_norm[l][m] = lose_array[l][m]/total

print(win_norm)
print(push_norm)
print(lose_norm)


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
    
cards_under = [1,2,3,4,5,6,7,8,9,10,10,10,10] #cards under 11
cards_over = [11,2,3,4,5,6,7,8,9,10,10,10,10] #cards over 11


win_hit_array = np.zeros((18,13))
push_hit_array = np.zeros((18,13))
lose_hit_array = np.zeros((18,13))

for i in (4,5,6,7,8,9,10):
    for card in cards_over:
        new_total = i+card
        win_hit_array[i-4] += (1/13)*win_norm[new_total-4]
        push_hit_array[i-4] += (1/13)*push_norm[new_total-4]
        lose_hit_array[i-4] += (1/13)*lose_norm[new_total-4]

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

# print(win_hit_array)
# print(push_hit_array)
# print(lose_hit_array)

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
