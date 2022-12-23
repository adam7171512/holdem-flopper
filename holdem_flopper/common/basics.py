from typing import Union

ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
suits = ("c", "d", "h", "s")
cards = tuple(rank + suit for rank in ranks for suit in suits)
values = tuple(x for x in range(1, len(ranks) + 1))
ranks_values = {rank: value for rank, value in zip(ranks, values, strict=True)}
values_ranks = {value: rank for rank, value in zip(ranks, values, strict=True)}


class Flop:

    def __init__(self, flop: Union[tuple, str]):

        if isinstance(flop, str) and len(flop) == 6:
            self.flop = (flop[:2], flop[2:4], flop[4:])
        elif isinstance(flop, tuple) and len(flop) == 3:
            self.flop = flop
        else:
            raise ValueError("Unsupported flop type! ('2c','3d','4h') or '2c3d4h' formats only!")

        self.name = "".join(self.flop)
        self.ranks = tuple(x[0] for x in self.flop)
        self.suits = tuple(x[1] for x in self.flop)
        self.values = tuple(ranks_values[x] for x in self.ranks)
        self.values_sorted = tuple(sorted(self.values))
        self.max_value = max(self.values)
        self.min_value = min(self.values)
        self.high_rank = values_ranks[self.max_value]
        self.low_rank = values_ranks[self.min_value]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.flop

    def check_flop(self, fn, card=None):
        return fn(self, card)
