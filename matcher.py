import matching

# TODO: get data from airtable
#   TODO: marshal data to internal format
#   TODO: verify data integrity: 
#       - each user listed as another user"s preference must have its own lsit of preferences
#       - the correct number of preferences is given
#       - the number of rounds is defined 

### Dummy data
preferences = { "A" : ["Z", "B"], 
                "B" : ["Z", "A"], 
                "C" : ["A", "B"], 
                #"X" : ["A", "B"], 
                #"Y" : ["A", "B"], 
                "Z" : ["A", "B"]}

rounds = 2


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

pairings = gen_pairings(preferences, {})

print pairings

# Returns tuple of (number_of_matches (weight), pairings e.g. ("A", "B"))
def gen_pairings(preferences, match_history): # e.g. { "A" : {"B", "C"}}
    unmatched_users = preferences.keys()
    all_users = preferences.keys()

    # randomize unmatched_keys?

    pairings = [];
    num_matches = 0;

    # Find some actual pairings
    for user in all_users:
        for maybe_match in preferences[user]:
            if(user in preferences[maybe_match] and have_never_matched(user, maybe_match, match_history)):
                record_pairing(u1, u2, match_history)
                unmatched_users.remove(user, maybe_match)
                pairings.append((user, maybe_match))
                break;

    # Pair the unmatched users
    # TODO

    return (num_matches, pairings)

def have_never_matched(u1, u2, match_history):
    return (u2 not in match_history[u1]) and (u1 not in match_history[u2])
    # TODO

def record_pairing(u1, u2, match_history):
    match_history[u1].add(u2) # TODO: do I need to initialize the set? 
    match_history[u2].add(u1)
    # TODO


# Keep track of the solution list with the highest match weight (also keep track of the weight)

### Algo output
# Round 1        , Round ..., 
# e.g. [[("A","B"), ...], ...]

# TODO: Submit results back to airtable 