import random
from collections import defaultdict

def player(prev_play, opponent_history=[],
           my_history=[], pattern_length=5,
           pattern_db=defaultdict(lambda: defaultdict(int))):
    
    if not prev_play:
        # Reset for new game
        opponent_history.clear()
        my_history.clear()
        pattern_db.clear()
    else:
        opponent_history.append(prev_play)
    
    # Counter moves
    counter = {'P': 'S', 'R': 'P', 'S': 'R'}
    
    # Default move if no history
    if not opponent_history:
        my_history.append('R')
        return 'R'
    
    # Detect opponent type based on patterns
    if len(opponent_history) > 20:
        # Check for Quincy (fixed pattern)
        quincy_pattern = ['R', 'R', 'P', 'P', 'S']
        is_quincy = all(opponent_history[i] == quincy_pattern[i % 5] 
                       for i in range(-15, -1))
        
        # Check for Kris (always counters our last move)
        is_kris = all(counter.get(my_history[i-1], '') == opponent_history[i]
                     for i in range(-15, -1))
        
        if is_quincy:
            # Predict Quincy's next move
            next_quincy = quincy_pattern[len(opponent_history) % 5]
            my_history.append(counter[next_quincy])
            return counter[next_quincy]
        
        if is_kris:
            # Anti-Kris strategy: play what would counter their counter
            last_move = my_history[-1] if my_history else 'R'
            move = counter[counter[last_move]]
            my_history.append(move)
            return move
    
    # Abbey-style pattern recognition
    if len(opponent_history) >= pattern_length:
        # Look for patterns of length pattern_length-1
        last_pattern = ''.join(opponent_history[-(pattern_length-1):])
        
        # Update pattern database
        if len(opponent_history) >= pattern_length:
            prev_pattern = ''.join(opponent_history[-pattern_length:-1])
            pattern_db[prev_pattern][opponent_history[-1]] += 1
        
        # Predict next move based on patterns
        if last_pattern in pattern_db:
            predicted = max(pattern_db[last_pattern].items(), key=lambda x: x[1])[0]
            move = counter[predicted]
            my_history.append(move)
            return move
    
    # Mrugesh counter (most frequent move)
    if len(opponent_history) >= 10:
        freq = {'R': 0, 'P': 0, 'S': 0}
        for m in opponent_history[-10:]:
            freq[m] += 1
        most_freq = max(freq, key=freq.get)
        move = counter[most_freq]
        my_history.append(move)
        return move
    
    # Fallback strategy
    move = counter[random.choice(opponent_history)]
    my_history.append(move)
    return move
