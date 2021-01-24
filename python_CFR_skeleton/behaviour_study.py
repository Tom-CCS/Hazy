ALL_IN_RATIO = 0.5
def is_all_in(large_raise_count, round_count):
    """
    Determines if the opponent is an all-in bot.
    Input: 
        large_raise_count: int
            the number of raises over LARGE_RAISE_THRESHOLD the opponent made.
            LARGE_RAISE_THRESHOLD is defined in player.py
        round_count: int
            the number of rounds played.
    Output:
        true if the enemy is all-in bot, false otherwise.
    """
    return large_raise_count > ALL_IN_RATIO * round_count

