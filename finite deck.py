__author__ = 'miller'
__guy_who_looked_over_Jims_shoulder_and_also_wrote_some_cool_stuff__ = 'que'

#THIS MODULE BASICALLY DOES THE SAME STUFF AS infinte_deck.py BUT USES A FINITE NUMBER OF DECKS THAT GET RESHUFFLED
## ONCE A CERTAIN NUMBER OF CARDS HAVE BEEN DEALT

#COMBINES CONCEPTS FROM infinite_test_double_down.py and infinite_success_test.py

######## EVERY FUNCTION WILL BE PREFACED WITH A BASIC DESCRIPTION AS WELL AS THE ARGUMENTS AND THE RETURN VALUE ########

import random
import make_tables
import infinite_success_test as ist

################################ READ IN DATA TO MAKE APPROPRIATE TABLES TO DO MATH ON #################################
reg_table = make_tables.read_table_file('hit strategy.txt')
soft_table = make_tables.read_table_file('Soft Hit Strategy.txt')
split_table = make_tables.read_table_file('positive is split.txt')
double_table_soft = make_tables.read_table_file('soft double if greater than 0.txt')
double_table_reg = make_tables.read_table_file('double down if greater than 0.txt')

#################### DUMMY INSTANCES OF THE HIT AND SOFT HIT STRATEGIES, BECAUSE WE NEED MORE THAN ONE OF EACH #########
######### TYPING IN ALL CAPS MAKES ME FEEL LIKE I'M YELLING BUT I PROMISE I'M PRETTY LEVEL-HEADED AT THE MOMENT ########
hit_table_reg = reg_table
hit_table_soft = soft_table

#Creates a whole bunch of cards, depending on the number of decks we want to use
#ARGS: number of decks we want
#RETURN: a really long list of length (number_of_decks * 52)
def generate_decks(number_of_decks):
    numbers = ['ace',2,3,4,5,6,7,8,9,10,10,10,10]
    deck = 4*numbers
    total_deck = number_of_decks*deck
    return total_deck

########################################## INSPIRED BY INFINITE_DECK.PY ################################################

#Exactly identical to dealer_logic() in infinite_deck.py. Literally the exact same thing.
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

#Same as in infinite_deck.py, except uses a finite number of cards
#ARGS: total score as int
#RETURN: new total as int OR calls hit_soft_loop() again on new total
def hit_soft_loop(total):
    card_total = total
    randcard = random.choice(deck)
    deck.remove(randcard)
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

#Uses finite number of cards
#ARGS: total score as int
#RETURN: new total as int OR calls hit_loop() again on new total OR calls hit_soft_loop() on new total
def hit_loop(total):
    card_total = total
    randcard = random.choice(deck)
    deck.remove(randcard)
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

#Combines the three above functions to play a hand for the dealer
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

########################################################################################################################

################################################ PLAYER PLAYS HAND #####################################################

#Plays a normal hand for a player, no splitting, no doubling
#ARGS: player_score as int; dealer face-up card as int, boolean 'soft' defaults to False
#RETURN: player score as int OR recursively calls self
def play_a_hand_player(player_score,dealer_show_card_index,soft=False):
    player_current_score = player_score
    row_index = player_current_score - 4
    column_index = dealer_show_card_index

    if player_current_score >= 11:
        if soft == False:
            if reg_table[row_index][column_index] == False:
                return player_current_score
            else:
                new_card = random.choice(deck)
                deck.remove(new_card)
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
                new_card = random.choice(deck)
                deck.remove(new_card)
                if new_card == 'ace':
                    player_new_score = player_current_score + 1
                else:
                    player_new_score = player_current_score + new_card
                if player_new_score <= 21:
                    return play_a_hand_player(player_new_score,dealer_show_card_index,soft=True)
                else:
                    return play_a_hand_player(player_new_score-10,dealer_show_card_index,soft=False)

    else:
        new_card = random.choice(deck)
        deck.remove(new_card)
        if new_card == 'ace':
            player_new_score = player_current_score + 11
            return play_a_hand_player(player_new_score,dealer_show_card_index,soft=True)
        else:
            player_new_score = player_current_score + new_card
            return play_a_hand_player(player_new_score,dealer_show_card_index,soft=False)

#Turns a list [hand] into a tuple (score, soft, split)
#ARGS: hand as list
#RETURN: score, soft, and split as a tuple
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

#Checks hand for possibility of splitting
#ARGS: hand as list; dealer show card as int
#RETURN: split scores [score1,score2] as list OR calls play_a_hand_player()
def play_a_hand_player2(hand,dealer_show):
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
            return [play_a_hand_player(int(score),column_index,soft=True)]
        else:
            return [play_a_hand_player(int(score),column_index,soft=False)]
    else:
        split_card = score/2
        hand1 = [split_card,random.choice(deck)]
        deck.remove(hand1[1])
        hand2 = [split_card,random.choice(deck)]
        deck.remove(hand2[1])
        if ('ace' in hand1) and (10 in hand1):
            score1 = 22
        else:
            score1 = play_a_hand_player2(hand1,dealer_show)
        if ('ace' in hand2) and (10 in hand2):
            score2 = 22
        else:
            score2 = play_a_hand_player2(hand2,dealer_show)

        return [score1,score2]

#Checks hand for possibility of doubling
#ARGS: hand as list; dealer show card as int
#RETURN: two instances of player_score as list OR calls play_a_hand_player2()
def play_a_hand_player1(hand,dealer_show):
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
            hit_card = random.choice(deck)
            deck.remove(hit_card)
            if hit_card == 'ace':
                new_score = score + 1
            else:
                new_score = score + hit_card
            if new_score > 21:
                new_score = new_score - 10
            return [new_score,new_score]
        else:
            hit_card = random.choice(deck)
            deck.remove(hit_card)
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
        return play_a_hand_player2(hand,dealer_show)

no_decks = 6

deck = generate_decks(no_decks)


#initializes total money won as 0 and defines original deck length by calling generate_decks(no_decks)
#original_deck_length is reduced to min_deck_length, new deck is generated (reshuffled)
total_money = 0
original_deck_length = float(len(deck))
min_deck_length = (1/3)*original_deck_length


number_of_trials = 1000000

#play 1000000 hands, incorporating all funcitons defined in this module keeping a running total of money won and
## dividing by 1000000 to calculate expected return per hand

for i in range(number_of_trials):
    if len(deck) < min_deck_length:
        deck = generate_decks(no_decks)
    player_hand = [random.choice(deck)]
    deck.remove(player_hand[0])
    dealer_show = random.choice(deck)
    deck.remove(dealer_show)
    player_hand.append(random.choice(deck))
    deck.remove(player_hand[1])

    dealer_hand = [dealer_show,random.choice(deck)]
    deck.remove(dealer_hand[1])

    if ('ace' in player_hand) and (10 in player_hand):
        player_blackjack = True
    else:
        player_blackjack = False

    if ('ace' in dealer_hand) and (10 in dealer_hand):
        dealer_blackjack = True
    else:
        dealer_blackjack = False

    if (player_blackjack == True) and (dealer_blackjack == True):
        total_money += 0.0
    elif (player_blackjack == True) and (dealer_blackjack == False):
        total_money += 1.5
    elif (player_blackjack == False) and (dealer_blackjack == True):
        total_money += -1.0
    else:
        player_score = play_a_hand_player1(player_hand,dealer_show)

        dealer_score = play_a_hand_dealer(dealer_hand)
        if dealer_score == 'bust':
            dealer_score = 0
        format_score = ist.make_single_list(player_score)

        for score in format_score:
            if score == 0:
                total_money += -1.0
            elif score == 22:
                total_money += 1.5
            elif score > dealer_score:
                total_money += 1.0
            elif score == dealer_score:
                total_money += 0.0
            else:
                total_money += -1.0

print(total_money)
print(total_money/float(number_of_trials))
