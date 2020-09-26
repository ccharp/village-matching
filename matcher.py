import copy
import random
import json

import api


# TODO: get data from airtable
#   TODO: marshal data to internal format
#   TODO: verify data integrity: 
#       - each user listed as another user"s preference must have its own lsit of preferences
#       - the correct number of preferences is given
#       - the number of rounds is defined 


# TODO: Actually do the match-making
### Generate the matches while keeping track of the parings used in each round  

# k is the number of allowable preferencs. k is constant. 
# n is the number of users 

### Brute force:
# Complexity: n^k
# let k = 5, n = 30
# time: 30^5 = 24,300,000 operations
# space: time * num_rounds * n * k = 24300000 * 2 * 30 * 5a = 7,230,000,000 Bytes = 7GB

# ------
# Start with
#for p in pref_list:

#ll_ Returns tuple of (number_of_matches (weight), pairings e.g. ("A", "B"))
def gen_round_pairings(users, preferences, match_history): # e.g. { "A" : {"B", "C"}}
    unmatched_users = set(preferences.keys())

    pairings = [];
    num_matches = 0;

    # Find some actual pairings
    for user in preferences.keys():
        if user not in unmatched_users:
            continue

        for maybe_match in preferences[user]:
            if maybe_match not in unmatched_users:
                continue
            if(user in preferences[maybe_match] and have_never_matched(user, maybe_match, match_history)):
                unmatched_users.remove(user)

                # TODO: Account here for person that preferred themself
                unmatched_users.remove(maybe_match)
                record_pairing(user, maybe_match, match_history)
                pairings.append((user, maybe_match))
                num_matches += 1
                break;

    # TODO look for half matches
    unmatched_for_iterating = copy.deepcopy(unmatched_users)
    for user1 in unmatched_for_iterating:
        if user1 not in unmatched_users:
            continue;
        
        for user2 in unmatched_users:
            if user2 in preferences[user1] and have_never_matched(user1, user2, match_history):
                unmatched_users.remove(user1)
                unmatched_users.remove(user2)
                record_pairing(user1, user2, match_history)
                pairings.append((user1, user2))
                num_matches += 0.5
                break;

    # Pair the unmatched users
    # !!! We assume that we'll have a low enough round:user ratio that this is possible
    unmatched_for_iterating = copy.deepcopy(unmatched_users)
    for user1 in unmatched_for_iterating:
        if user1 not in unmatched_users:
            continue;
        
        unmatched_users.remove(user1)
        for user2 in unmatched_users:
            if have_never_matched(user1, user2, match_history):
                unmatched_users.remove(user2)
                record_pairing(user1, user2, match_history)
                pairings.append((user1, user2))
                break;
                
    return (num_matches, pairings)

def have_never_matched(u1, u2, match_history):
    if u1 not in match_history or u2 not in match_history:
        return True 
    return (u2 not in match_history[u1]) and (u1 not in match_history[u2])

def record_pairing(u1, u2, match_history):
    try:
        match_history[u1].add(u2) # TODO: do I need to initialize the set? 
    except KeyError:
        match_history[u1] = {u2}

    try:
        match_history[u2].add(u1) # TODO: do I need to initialize the set? 
    except KeyError:
        match_history[u2] = {u1}


# Keep track of the solution list with the highest match weight (also keep track of the weight)

### Algo output
# Round 1        , Round ..., 
# e.g. [[("A","B"), ...], ...]

# TODO: Submit results back to airtable 

def generate_matches(random_attempts, game_rounds, preferences):
    max_weight = 0
    max_pairings_set = []

    for _ in range(random_attempts):
        curr_pairings_set = []
        curr_weight = 0
        match_history = {}

        should_skip = True

        for _ in range(game_rounds):
            all_users = random.sample(preferences.keys(), len(preferences))
            round_pairings = gen_round_pairings(all_users, preferences, match_history) 
            curr_weight += round_pairings[0]
            curr_pairings_set.append(round_pairings[1])
            print(json.dumps(round_pairings, indent=2))
            # print(json.dumps(match_history, indent=2))
            #print("END ROUND")
            if len(round_pairings) < (len(preferences)//2 * game_rounds):
                should_skip = True
                #break 

        if should_skip:
            print('would have skipped')
            #continue
           
        if curr_weight > max_weight:
            max_weight = curr_weight
            max_pairings_set = curr_pairings_set
        #print("END ATTEMPT\n")

    return max_pairings_set

def add_game_data(matches):
    output = [] 
    round_number = 1
    for round in matches:
        room_number = 1
        for (u1, u2) in round:
            match_details = {
                'Person 1': [u1],
                'Person 2': [u2],
                'Session': str(round_number),
                'Room Assignment': 'Room ' + str(room_number)
            }
            room_number += 1
            output.append(match_details)
        round_number += 1
    return output

### Dummy data
preferences_dummy = { "A" : ["Z", "B"], 
                "B" : ["Z", "C"], 
                "C" : ["Y", "B"], 
                "X" : ["A", "B"], 
                "Y" : ["A", "C"], 
                "Z" : ["A", "B"]}

#### MAIN STUFF
preferences = api.get_user_preferences()
matches = generate_matches(random_attempts=200, game_rounds=3, preferences=preferences)
complete_output = add_game_data(matches)

# json stuff for easy pretty printing
#print(json.dumps(complete_output, indent=2))

api.upload_matches(complete_output)

