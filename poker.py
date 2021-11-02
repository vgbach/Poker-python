import random
values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
suits = ['S','C','D','H']
real_values = {}
for i in range(len(values)):
    real_values[values[i]] = i+2
hand1 = ['4D','5D']
hand2 = []
table = ['6D','7D','8D','TD','7H']
combinations = {
    'high_card' : 0,
    'pair' : 1,
    'two_pairs':2,
    'set' : 3,
    'straight' : 4,
    'flush': 5,
    'full_house' : 6,
    'quad': 7,
    'straight_flush': 8,
    'royal_flush': 9}
'''This is a simple program that tries to figure out the distribution of probabilities behind
Poker's hand combinations'''
def deal(place,n):
    '''Parameters: 'place' to deal the card to, 'n'-times that the cards will be dealt to that
        place.
       It directly changes either of the two hands or the table.'''
    place.clear()
    while len(place) != n:
        new_card = random.choice(values)+random.choice(suits)
        if new_card not in hand1 and new_card not in hand2 and new_card not in table:
            place.append(new_card)
def check(hand):
    '''Find the best combinations of card for a hand'''
    total_hand = hand + table
    for i in range(1, len(total_hand)):
        #sort the cards for ease of checking using insert sort
        key = total_hand[i]
        j = i-1
        while j>=0 and real_values[key[0]] < real_values[total_hand[j][0]]:
            total_hand[j+1] = total_hand[j]
            j -= 1
        total_hand[j+1] = key
    #run through the list and store combinations
    best_hand = {}#overall best hands combinations
    same_values = {}
    best_sv_hand = []#the best hand when only same-valued cards are considered
    #the best hand if only cards with the same values are considered
    #adding cards with the same values to a dictionary
    for i in range(1,len(total_hand)):
        if real_values[total_hand[i][0]] == real_values[total_hand[i-1][0]]:
            if real_values[total_hand[i][0]] not in same_values:
                same_values[real_values[total_hand[i][0]]] = [i-1,i]
            else:
                same_values[real_values[total_hand[i][0]]].append(i)
                if len(same_values[real_values[total_hand[i][0]]]) == 4:
                    best_hand['quad'] = [real_values[total_hand[i][0]], max([real_values[total_hand[n][0]] for n in range(len(total_hand)) if (total_hand[n][0] != total_hand[i][0])])]
                    best_hand['pair'] = [real_values[total_hand[i][0]], 'lesser']#'lesser' indicates a combination that is not the best but still included for 'proper' statistics
                    best_hand['set'] = [real_values[total_hand[i][0]], 'lesser']
                    break
    #going throught the dictionary to find the best same-value combination
    temp_list = list(same_values.keys())
    if len(same_values) == 0:
        best_hand['high_card'] = [real_values[total_hand[i][0]] for i in range(len(total_hand)-5,len(total_hand))][::-1]
    elif len(same_values) == 1:
        card_group = next(iter(same_values))
        if len(same_values[card_group]) == 2:
            best_hand['pair'] = [card_group, [real_values[i[0]] for i in total_hand if real_values[i[0]]!=card_group][-3:][::-1]]
        else:
            best_hand['set'] = [card_group, [real_values[i[0]] for i in total_hand if real_values[i[0]]!=card_group][-2:][::-1]]
            best_hand['pair'] = [card_group, 'lesser']
    elif len(same_values) == 2:
        if len(same_values[temp_list[0]]) == len(same_values[temp_list[1]]):
            if len(same_values[temp_list[0]]) == 2:
                best_hand['two_pairs'] = [temp_list[::-1],max([real_values[i[0]] for i in total_hand if real_values[i[0]] not in temp_list])]
                best_hand['pair'] = [temp_list,'lesser']
            else:
                best_hand['full_house'] = temp_list[::-1]
        else:
            if len(same_values[temp_list[0]]) < len(same_values[temp_list[1]]):
                best_hand['full_house'] = temp_list[::-1]
                best_hand['pair'] = [temp_list[0],'lesser']
                best_hand['set'] = [temp_list[0],'lesser']
            else:
                best_hand['full_house'] = temp_list
                best_hand['pair'] = [temp_list[1],'lesser']
                best_hand['set'] = [temp_list[0],'lesser']
    else:
        if len(same_values[temp_list[0]]) == len(same_values[temp_list[1]]) == len(same_values[temp_list[2]]):
            best_hand['two_pairs'] = [temp_list[-2:][::-1],max([real_values[i[0]] for i in total_hand if real_values[i[0]] not in temp_list[-2:]])]
            best_hand['pair'] = [temp_list,'lesser']
        else:
            fh = [i for i in temp_list if len(same_values[i]) == 3] + [max([i for i in temp_list if len(same_values[i]) == 2 ])]
            best_hand['set'] = ['something','lesser']
            best_hand['pair'] = ['something','lesser']
            best_hand['full_house'] = fh
    #listing a series of ascending cards
    straight_cards = [0]
    straight_count = [1,0]
    if real_values[total_hand[len(total_hand)-1][0]] == 14 and total_hand[0][0]=='2':
        straight_count = [2,2]
        straight_cards = [(len(total_hand)-1), 0]
    for i in range(1, len(total_hand)):
        if real_values[total_hand[i][0]] == (real_values[total_hand[i-1][0]]+1):
            straight_count[0] += 1
            straight_count[1] = real_values[total_hand[i][0]]
            straight_cards.append(i)
        elif real_values[total_hand[i][0]] == real_values[total_hand[i-1][0]]:
            straight_cards.append(i)
        else:
            if straight_count[0] < 5:
                straight_count = [1,0]
                straight_cards = [i]
            else:
                break
    if straight_count[0] >= 5:
        best_hand['straight'] = straight_count[1]
    #Finding cards with the same suit
    for i in suits:
        suited_cards = [n for n in range(len(total_hand)) if total_hand[n][1] == i]
        if len(suited_cards) < 5:
            suited_cards.clear()
        else:
            break
    if suited_cards:
        best_hand['flush'] = [real_values[total_hand[n][0]] for n in suited_cards][::-1]
    #Checking for a straight flush and royal flush
    if 'straight' in best_hand and 'flush' in best_hand:
        common = [real_values[total_hand[i][0]] for i in suited_cards if i in straight_cards]
        if len(common) >= 5:
            nstraight_count = [1,0]
            nstraight_cards = [0]
            for i in range(1,len(common)):
                if common[i] == (common[i-1]+1):
                    nstraight_count[0]+=1
                    nstraight_count[1] = common[i]
                    nstraight_cards.append(common[i])
                else:
                    if nstraight_count[0] <5:
                        nstraight_count = [1,0]
                        nstraight_cards = [i]
                    else:
                        break
            if len(nstraight_cards) >= 5:
                if nstraight_count[1] == 14:
                    best_hand['royal_flush'] = []
                else:
                    best_hand['straight_flush'] = nstraight_count[1]  
    return best_hand
#Finding out the distribution of card combinations
counter = {}

#Comparing two poker hands and finding out the porbablity of winning for each hand
hand1_wins = 0
hand2_wins = 0
combination_storer = {}
def best(best_hand):
    #Finding out the best combination from a dictionary of hands
    best_combination = 'high_card'
    for i in best_hand:
        if combinations[i] > combinations[best_combination]:
            best_combination = i
    return best_combination 
def compare(hand1,hand2):
    global combination_storer
    global hand1_wins
    global hand2_wins
    temp_dict1 = check(hand1)
    temp_dict2 = check(hand2)
    #Storing the values of 'best-hand' (a dictionary containing all possible card combinations) into a new dictionary
    for i in temp_dict1:
        if i not in combination_storer:
            combination_storer[i] = 0
        else:
            combination_storer[i] += 1
    for i in temp_dict2:
        if i not in combination_storer:
            combination_storer[i] = 0
        else:
            combination_storer[i] += 1
    b1 = best(temp_dict1)
    b2 = best(temp_dict2)
    if combinations[b1] > combinations[b2]:
        hand1_wins += 1
    elif combinations[b1] < combinations[b2]:
        hand2_wins += 1
    else:
        if temp_dict1[b1]>temp_dict2[b2]:
            hand1_wins += 1
        elif temp_dict1[b1]<temp_dict2[b2]:
            hand2_wins += 1
        else:
            pass
    
for i in range(10000):
    deal(hand1,2)
    deal(hand2,2)
    deal(table,5)
    compare(hand1,hand2)
print(hand1_wins, hand2_wins)
print(combination_storer)
         
            
        
        
    
                
            
    

        
        
