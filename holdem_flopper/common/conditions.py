from basics import Flop, ranks_values


def is_paired(flop: Flop, rank: str = None) -> bool:
    return len(set(flop.values)) == 2


def is_tripsed(flop: Flop, rank: str = None) -> bool:
    return len(set(flop.values)) == 1


def is_mono(flop: Flop, rank: str = None) -> bool:
    return len(set(flop.suits)) == 1


def is_two_tone(flop: Flop, rank: str = None) -> bool:
    return len(set(flop.suits)) == 2


def is_rainbow(flop: Flop, rank: str = None) -> bool:
    return len(set(flop.suits)) == 3


def has_rank(flop: Flop, rank: str) -> bool:
    return rank in flop.ranks


def is_not_higher_than(flop: Flop, rank: str) -> bool:
    return max(flop.values) <= ranks_values[rank]


def is_not_lower_than(flop: Flop, rank: str) -> bool:
    return min(flop.values) >= ranks_values[rank]


def has_paired_rank(flop: Flop, rank: str) -> bool:
    return len(set(flop.values)) == 2 and flop.ranks.count(rank) == 2


def is_straight_possible(flop: Flop, rank: str = None) -> bool:
    if len(flop.values) == len(set(flop.values)):
        if max(flop.values) < 13:
            return max(flop.values) - min(flop.values) <= 4
        else:
            return max(flop.values) - min(flop.values) <= 4 or max(flop.values_sorted[:2]) < 5  # wheel
    else:
        return False


def is_straight_draw_possible(flop: Flop, rank: str = None) -> bool:
    values = flop.values_sorted
    min_dif = max(values)

    if len(set(values)) == 1:
        return False

    for i in range(len(values) - 1):
        if 0 < values[i + 1] - values[i] < min_dif:
            min_dif = values[i + 1] - values[i]

    if max(values) < 13:
        return 0 < min_dif < 5
    else:
        # wheel
        return 0 < min_dif < 5 or min(values) < 5
