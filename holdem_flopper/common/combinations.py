from itertools import combinations
from .basics import cards
from .tools import ComboCounter

all_flop_combinations = combinations(cards, 3)
all_flop_comb_types = ComboCounter(all_flop_combinations).count_combos()
