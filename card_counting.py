import random

# Defined constants
N_CARDS = 416
N_DECKS = N_CARDS / 52
N_BATCHES = 500

def count(card, r, counts):
    """Modify card count based on value of r.
    Update counts based on drawn card."""
    x, y, z = counts
    if r <= x:
        card = card - 1
        counts[0] = x - 1
    elif r <= x + y:
        card = card + 1
        counts[1] = y - 1
    # z condition doesn't change card count
    else:
        counts[2] = z - 1
    return card, counts

def count_208():
    """Perform card counting for 208 rounds,
    updating card counts based on random drawing."""
    # Initialize counts for each card value
    counts = [160, 160, 96]
    card = 0
    high = 0 
    low = 0
    for i in range(N_DECKS):
        remaining_cards = N_CARDS - i
        
        # Calculate 'xyz' which is the total remaining count
        xyz = sum(counts)
        r = random.randrange(1, xyz, 1)
        card, counts = count(card, r, counts)
        card_ = card / remaining_cards
        high = max(card_, high)
        low = min(card_, low)
    return low, high

# Running simulation for multiple batches
for j in range(20):
    lows, highs = [], []
    for _ in range(N_BATCHES):
        low, high = count_208()
        lows.append(low)
        highs.append(high)
    # Print minimum and maximum values
    print(min(lows))
    print(max(highs))
    print('---------')
