from typing import List

cards = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
ranks = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
cards_and_ranks = {cards[i]: ranks[i] for i in range(len(cards))}
inv_cards_and_ranks = {v: k for k, v in cards_and_ranks.items()}
# flop naming convention in canonical flop list -> "3c8dAh"


def get_ranks(flop: str) -> List[int]:
    flop_cards = [flop[0], flop[2], flop[4]]
    values = [cards_and_ranks[x] for x in flop_cards]
    return values


def get_ranks_sorted(flop: str) -> List[int]:
    return sorted(get_ranks(flop))


def high_card(flop: str) -> str:
    max_rank = max(get_ranks(flop))
    return inv_cards_and_ranks[max_rank]


def max_bound_card(flop: str, card: str) -> bool:
    if max(get_ranks(flop)) <= cards_and_ranks[card]:
        return True
    else:
        return False


def min_bound_card(flop: str, card: str) -> bool:
    if min(get_ranks(flop)) >= cards_and_ranks[card]:
        return True
    else:
        return False


def straight_possible(flop: str) -> bool:
    sorted_ranks = get_ranks_sorted(flop)
    if len(sorted_ranks) == len(set(sorted_ranks)):
        if sorted_ranks[2] - sorted_ranks[0] <= 4:
            return True
        else:
            return False
    else:
        return False


def has_card(flop: str, card: str) -> bool:
    if cards_and_ranks[card] in get_ranks(flop):
        return True
    else:
        return False


"""
As we use "clubs, diamond, hearts" convention
of canonical flop list, defining
simple (omitting suits of specific ranks)
flush structure can be simplified:
"""


def is_mono(flop: str) -> bool:
    if 'd' not in flop:
        return True
    else:
        return False


def is_two_tone(flop: str) -> bool:
    if ('d' in flop) and ('h' not in flop):
        return True
    else:
        return False


def is_rainbow(flop: str) -> bool:
    if 'h' in flop:
        return True
    else:
        return False


def is_paired(flop: str) -> bool:
    if len(set(get_ranks(flop))) == 2:
        return True
    else:
        return False


def is_tripsed(flop: str) -> bool:
    if len(set(get_ranks(flop))) == 1:
        return True
    else:
        return False


class Flopper:

    def __init__(self, input_file_path: str =
                 "canonical_flops.txt"
                 ):
        self.input_file_path = input_file_path

    def save_flops(self, cond_check: callable, output_file_path: str) -> None:
        all_flops = open(self.input_file_path, "r")
        with open(output_file_path, 'w') as new_flops:
            for line in all_flops:
                if cond_check(line):
                    new_flops.write(line)
            new_flops.close()
        all_flops.close()

    def get_flops(self, cond_check: callable) -> List[str]:
        new_flops = []
        all_flops = open(self.input_file_path, "r")
        for line in all_flops:
            if cond_check(line):
                new_flops.append(line[:-1])
        all_flops.close()
        return new_flops


"""
example use case -> prints list of rainbow
(every card has different suit) flops along with their weights
that can be used later on for statistical analysis:

a = Flopper()
print(a.get_flops(is_rainbow))

only methods returning boolean values can be passed to Flopper class instance.
for other methods or combinations of them, define another method combining them
that returns bool value. Example: 

def conditions(flop: str) -> bool:
    if straight_possible(flop) and has_card(flop, "K"):
        return True
    else:
        return False
        
a = Flopper()
print(a.get_flops(conditions)
"""
