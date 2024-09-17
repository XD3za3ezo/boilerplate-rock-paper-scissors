# Define the ideal responses
ideal_response = {"P": "S", "R": "P", "S": "R"}

# Initialize global variables
my_moves = ["R"]
opponent_history = []
strategy = [0, 0, 0, 0]
opponent_guess = ["", "", "", ""]
strategy_guess = ["", "", "", "", ""]
opponent_play_order = {}
my_play_order = {}

def player(prev_play):
    # Update opponent's history and strategy counts
    if prev_play in ["R", "P", "S"]:
        opponent_history.append(prev_play)
        for i in range(4):
            if opponent_guess[i] == prev_play:
                strategy[i] += 1
    else:
        reset()
    
    # Determine the best move based on past moves
    my_last_ten = my_moves[-10:]
    if len(my_last_ten) > 0:
        my_most_frequent_move = max(set(my_last_ten), key=my_last_ten.count)
        opponent_guess[0] = ideal_response[my_most_frequent_move]
        strategy_guess[0] = ideal_response[opponent_guess[0]]
    
    if len(my_moves) > 0:
        my_last_play = my_moves[-1]
        opponent_guess[1] = ideal_response[my_last_play]
        strategy_guess[1] = ideal_response[opponent_guess[1]]
    
    if len(opponent_history) >= 3:
        opponent_guess[2] = predict_move(opponent_history, 3, opponent_play_order)
        strategy_guess[2] = ideal_response[opponent_guess[2]]
    
    if len(my_moves) >= 2:
        opponent_guess[3] = ideal_response[predict_move(my_moves, 2, my_play_order)]
        strategy_guess[3] = ideal_response[opponent_guess[3]]
    
    # Select the best strategy based on the counts
    best_strategy_index = strategy.index(max(strategy))
    guess = strategy_guess[best_strategy_index]
    
    if guess == "":
        guess = "S"
    
    my_moves.append(guess)
    return guess

def predict_move(history, n, play_order):
    # Update play order counts based on the last n moves
    if len(history) >= n:
        sequence = "".join(history[-n:])
        if sequence in play_order:
            play_order[sequence] += 1
        else:
            play_order[sequence] = 1
    
    # Create a list of possible future sequences
    possible = ["".join(history[-(n - 1):]) + k for k in ["R", "P", "S"]]
    
    for pm in possible:
        if pm not in play_order:
            play_order[pm] = 0
    
    # Predict the next move based on the most frequent sequence
    predict = max(possible, key=lambda key: play_order[key])
    return predict[-1]

def reset():
    global my_moves, opponent_history, strategy, opponent_guess, strategy_guess, opponent_play_order, my_play_order
    my_moves = ["R"]
    opponent_history.clear()
    strategy = [0, 0, 0, 0]
    opponent_guess = ["", "", "", ""]
    strategy_guess = ["", "", "", ""]
    opponent_play_order = {}
    my_play_order = {}
