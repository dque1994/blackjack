__author__ = 'miller'
__guy_who_looked_over_Jims_shoulder_and_also_wrote_some_cool_stuff__ = 'que'

########## THIS MODULE TESTS THE TOTAL RETURN EXPECTED FROM AN INFINITE DECK WHEN CONSIDERING DOUBLING DOWN ############

import infinite_success_test as ist
import infinte_deck as id
import random
import make_tables

#Read data from .txt files to be used in calculations
hit_table_reg = make_tables.read_table_file('hit strategy.txt')
hit_table_soft = make_tables.read_table_file('Soft Hit Strategy.txt')
split_table = make_tables.read_table_file('positive is split.txt')
double_table_soft = make_tables.read_table_file('soft double if greater than 0.txt')
double_table_reg = make_tables.read_table_file('double down if greater than 0.txt')

soft_table = hit_table_soft
reg_table = hit_table_reg

#Plays a hand for the player, considering opportunities to double
#ARGS: hand as list; dealer show card as int
#RETURN: two copies of player score as list OR calls ist.play_a_hand_player()
def play_a_hand_player(hand,dealer_show):
    [card1,card2] = hand
    if (card1 == 'ace') and (card2 == 'ace'):
        score = 12
        soft = True
    elif card1 == 'ace':
        score = card2 + 11
        soft = True
    elif card2 == 'ace':
        score = card1 + 11
        soft = True
    else:
        score = card1+card2
        soft = False
    row_index = score - 4
    if dealer_show == 'ace':
        column_index = 0
    else:
        column_index = dealer_show - 1
    if soft == True:
        double_down_check = double_table_soft[row_index][column_index]
        double_check = hit_table_soft[row_index][column_index]
        if double_check == False:
            double_down_check = False
    else:
        double_down_check = double_table_reg[row_index][column_index]
        double_check = hit_table_reg[row_index][column_index]
        if double_check == False:
            double_down_check = False
    if double_down_check == True:
        if soft == True:
            hit_card = id.deck(random.randint(1,13))
            if hit_card == 'ace':
                new_score = score + 1
            else:
                new_score = score + hit_card
            if new_score > 21:
                new_score = new_score - 10
            return [new_score,new_score]
        else:
            hit_card = id.deck(random.randint(1,13))
            if score < 11:
                if hit_card == 'ace':
                    new_score = score + 11
                else:
                    new_score = score + hit_card
            else:
                if hit_card == 'ace':
                    new_score = score + 1
                else:
                    new_score = score + hit_card
            if new_score > 21:
                new_score = 0
            return [new_score,new_score]
    else:
        return ist.play_a_hand_player(hand,dealer_show)

#initialize total return as 0.0
total_return = 0.0

number_of_trials = 10000

#Play number_of_trials trials (that many hands) and print expected return
for i in range(number_of_trials):
    dealer_show_card = id.deck(random.randint(1,13))
    dealer_hand = [dealer_show_card,id.deck(random.randint(1,13))]
    player_hand = [id.deck(random.randint(1,13)),id.deck(random.randint(1,13))]
    if ('ace' in dealer_hand) and (10 in dealer_hand):
        dealer_blackjack = True
    else:
        dealer_blackjack = False
    if ('ace' in player_hand) and (10 in player_hand):
        player_blackjack = True
    else:
        player_blackjack = False

    if (dealer_blackjack == True) and (player_blackjack == True):
        total_return += 0.0
    elif (dealer_blackjack == True) and (player_blackjack == False):
        total_return += -1.0
    elif (dealer_blackjack == False) and (player_blackjack == True):
        total_return += 1.5
    else:

        score = play_a_hand_player(player_hand,dealer_show_card)
        dealer_score = id.play_a_hand_dealer([dealer_show_card,id.deck(random.randint(1,13))])
        if dealer_score == 'bust':
            dealer_score = 0
        format_score = ist.make_single_list(score)
        for element in format_score:
            if element == 22:
                total_return += 1.5
            elif element == 0:
                total_return += -1.0
            elif element > dealer_score:
                total_return += 1.0
            elif element == dealer_score:
                total_return += 0.0
            else:
                total_return += -1.0

print(total_return)
print(total_return/float(number_of_trials))
