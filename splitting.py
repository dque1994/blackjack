__author__ = 'miller'
__guy_who_looked_over_Jims_shoulder_and_also_wrote_some_cool_stuff__ = 'que'


############################# THIS MODULE CONSIDERS THE POSSIBILITY OF SPLITTING A HAND ################################

############################### PLAYS ON AN INFINITE DECK AND WRITES RESULTS TO .TXT FILE ##############################

import numpy as np
import infinte_deck as id
import random
import make_tables

#read in data from .txt files, to be used as reference in calculation
soft_table = make_tables.read_table_file('Soft Hit Strategy.txt')
reg_table = make_tables.read_table_file('hit strategy.txt')

#plays a hand for a player, considering opportunities to split
#ARGS: player_score as int; dealer show card as int, soft as boolean
#RETURN: player score as int OR calls self
def play_a_hand_player(player_score,dealer_show_card_index,soft=False):
    player_current_score = player_score
    row_index = player_current_score - 4
    column_index = dealer_show_card_index

    if player_current_score >= 11:
        if soft == False:
            if reg_table[row_index][column_index] == False:
                return player_current_score
            else:
                new_card = id.deck(random.randint(1,13))
                if new_card == 'ace':
                    player_new_score = player_current_score + 1
                else:
                    player_new_score = player_current_score + new_card
                if player_new_score > 21:
                    return 0
                else:
                    return play_a_hand_player(player_new_score,dealer_show_card_index,soft=False)

        else:
            if soft_table[row_index][column_index] == False:
                return player_current_score
            else:
                new_card = id.deck(random.randint(1,13))
                if new_card == 'ace':
                    player_new_score = player_current_score + 1
                else:
                    player_new_score = player_current_score + new_card
                if player_new_score <= 21:
                    return play_a_hand_player(player_new_score,dealer_show_card_index,soft=True)
                else:
                    return play_a_hand_player(player_new_score-10,dealer_show_card_index,soft=False)

    else:
        new_card = id.deck(random.randint(1,13))
        if new_card == 'ace':
            player_new_score = player_current_score + 11
            return play_a_hand_player(player_new_score,dealer_show_card_index,soft=True)
        else:
            player_new_score = player_current_score + new_card
            return play_a_hand_player(player_new_score,dealer_show_card_index,soft=False)

#takes two cards and calculates the score
#ARGS: card1, card2 as int OR str (if card == 'ace')
#RETURN: (score as int, soft as boolean) as tuple
def make_a_score(card1,card2):
    if (card1=='ace') and (card2=='ace'):
        score = 12
        soft = True
    elif (card1=='ace'):
        card1 = 11
        score = card1+card2
        soft = True
    elif (card2=='ace'):
        card2 = 11
        score = card1+card2
        soft = True
    else:
        score = card1+card2
        soft = False

    return (score,soft)

return_away_no_split = np.zeros((10,13))

l = 0
number_of_trials = 10000

#play number_of_trials hands ber [i][j] index and populate array
for card_total in (4,6,8,10,12,14,16,18,20,'ace'):
    for j in range(13):
        for x in range(number_of_trials):
            total_return = 0.0
            dealer_hand = [id.deck(j+1),id.deck(random.randint(1,13))]
            dealer_score = id.play_a_hand_dealer(dealer_hand)
            if dealer_score == 'bust':
                dealer_score = 0

            if card_total == 'ace':
                score = 12
                issoft = True

            else:
                score = card_total
                issoft = False

            if (10 in dealer_hand) and ('ace' in dealer_hand):
                dealer_blackjack = True
            else:
                dealer_blackjack = False

            player_score = play_a_hand_player(score,j,soft=issoft)

            if dealer_blackjack == True:
                money_return = -1.0
            else:
                if player_score == 0:
                    money_return = -1.0
                elif player_score > dealer_score:
                    money_return = 1.0
                elif player_score == dealer_score:
                    money_return = 0.0
                else:
                    money_return = -1.0

            total_return = money_return

            return_away_no_split[l][j] += total_return


    l += 1

#normalize array populate previously
return_no_split_norm = np.zeros((10,13))
r = 0
for row in return_away_no_split:
    c = 0
    for column in row:
        return_no_split_norm[r][c] = float(float(column)/float(number_of_trials))
        c += 1
    r += 1

#write result to .txt file
g2 = open('no_splitting_return4.txt','w')
g2.write("Expected return after not split (rows represent player's split card (2,3,4,...), columns represent card dealer shows (ace,2,...,king)"+'\n')
for line in return_no_split_norm:
    for element in line:
        string = str(element)+'\t'
        g2.write(string)
    g2.write('\n')
