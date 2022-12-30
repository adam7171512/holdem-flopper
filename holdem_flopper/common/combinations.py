from itertools import combinations
from holdem_flopper.common.basics import cards
from holdem_flopper.common.tools import ComboCounter

all_flop_combinations = combinations(cards, 3)
all_flop_comb_types = ComboCounter(all_flop_combinations).count_combos()
