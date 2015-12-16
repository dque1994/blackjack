__author__ = 'miller'
__guy_who_looked_over_Jims_shoulder_and_also_wrote_some_cool_stuff__ = 'que'

############## THIS MODULE CACLULATES THE TOTAL AND EXPECTED RETURNS WHEN PLAYING WITH AN INFINITE DECK ################

################################## CONSIDERS OPPORTUNITIES TO SPLIT AND DOUBLE DOWN ####################################

import infinte_deck as id
import random
import make_tables
import splitting

#read data in from .txt files, to be used as references for calculation
hit_table_reg = make_tables.read_table_file('hit strategy.txt')
hit_table_soft = make_tables.read_table_file('Soft Hit Strategy.txt')
split_table = make_tables.read_table_file('positive is split.txt')

soft_table = hit_table_soft
reg_table = hit_table_reg

#formats score, unpacking a nested list (e.g., the return value if a player doubles on a split hand
#ARGS: score as list within a list (listception?)
#RETURN: calls self until it finally returns a single list
def make_single_list(nested_list):
    final_list = []
    for element in nested_list:
        if isinstance(element,list):
            final_list+=element
        else:
            final_list.append(element)

    is_nested = False
    for element in final_list:
        if isinstance(element,list):
            is_nested = True
    if is_nested == True:
        return make_single_list(final_list)
    else:
        return final_list

#Turns a hand as list into a tuple of (score,soft,split)
#ARGS: hand as list
#RETURN: (score as int, soft as boolean, split as boolean) as tuple
def make_a_score(hand):
    [card1,card2] = hand
    if card1 == card2:
        split = True
    else:
        split = False
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

    return (score,soft,split)

#plays a hand for the player, considering doubling and splitting opportunities
#ARGS: hand as list, dealer show card as int
#RETURN: player score OR calls splitting.play_a_hand_player()
def play_a_hand_player(hand,dealer_show):
    if isinstance(hand,list):
        (score,soft,split) = make_a_score(hand)
        if 'ace' in hand:
            ace = True
        else:
            ace = False
    else:
        score = hand[0]
        soft = hand[1]
        split = False
        ace = False


    if dealer_show == 'ace':
        column_index = 0
    else:
        column_index = dealer_show - 1

    if split == True:
        if ace == False:
            row_index = int(int(score/2) - int(1))
        else:
            row_index = 9
        split_check = split_table[row_index][column_index]
    else:
        split_check = False

    row_index = score-4

    if split_check == False:
        if soft == True:
            return [splitting.play_a_hand_player(int(score),column_index,soft=True)]
        else:
            return [splitting.play_a_hand_player(int(score),column_index,soft=False)]

    else:
        split_card = score/2
        hand1 = [split_card,id.deck(random.randint(1,13))]
        hand2 = [split_card,id.deck(random.randint(1,13))]
        if ('ace' in hand1) and (10 in hand1):
            score1 = 22
        else:
            score1 = play_a_hand_player(hand1,dealer_show)
        if ('ace' in hand2) and (10 in hand2):
            score2 = 22
        else:
            score2 = play_a_hand_player(hand2,dealer_show)

        return [score1,score2]

#initialize total return as 0.0
total_return = 0.0

number_of_trials = 10000

if __name__ == "__main__":

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
            format_score = make_single_list(score)
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
