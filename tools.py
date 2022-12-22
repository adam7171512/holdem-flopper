from collections import namedtuple
from typing import Iterable
import conditions
from canonical import get_canonical_flops
from fractions import Fraction
from basics import Flop

canonical_flops = tuple(get_canonical_flops(get_list=True))
flop_types = ("all", "mono", "tripsed", "paired", "rainbow_unpaired", "two_tone_unpaired")
FlopTypesCombs = namedtuple("FlopCombos", flop_types)
CombTypeFractions = namedtuple("CombTypeFractions", flop_types[1:])
all_flop_comb_types = FlopTypesCombs(all=22100,
                                     mono=1144,
                                     tripsed=52,
                                     paired=3744,
                                     rainbow_unpaired=6864,
                                     two_tone_unpaired=10296)  # sourced from combinations module
all_flop_comb_fractions = CombTypeFractions(
    *(Fraction(numerator=x, denominator=all_flop_comb_types.all)
      for x in all_flop_comb_types[1:]))


class FlopFilter:

    def __init__(self, flops: tuple = canonical_flops):
        self.starting_flops = {Flop(x) for x in flops}
        self.filtered_flops = self.starting_flops

    def add_filter(self, fn: callable, card: str = None, negate: bool = False, operator: str = "and") -> None:
        if operator == "and":
            self.filtered_flops = self._filter_flops(fn, card, negate)
        elif operator == "or":
            self.filtered_flops = self.filtered_flops.union(
                self._filter_flops(fn, card, negate, flops=self.starting_flops))
        else:
            raise ValueError("Wrong logical operator! Only 'and' and 'or' accepted!")

    def get_flops(self):
        return sorted([x.name for x in self.filtered_flops])

    def __call__(self):
        return self.get_flops()

    def __str__(self):
        return str(self.get_flops())

    def _filter_flops(self, fn: callable, card: str = None, negate=False, flops=None) -> set:
        # "flops" parameter used if we're adding an "or" filter, because then
        # we have to iterate the original flop set

        if not flops:
            flops = self.filtered_flops

        temp_flops = set()
        for flop in flops:
            if flop.check_flop(fn, card):
                temp_flops.add(flop)
        if negate:
            return flops.difference(temp_flops)
        else:
            return temp_flops


class ComboCounter:

    def __init__(self, flops: Iterable):

        self.flops = flops
        self.monotone = 0
        self.tripsed = 0
        self.paired = 0
        self.rainbow_unpaired = 0
        self.two_tone_unpaired = 0

    @property
    def all(self):
        return self.monotone + self.tripsed + self.paired + self.rainbow_unpaired + self.two_tone_unpaired

    def count_combos(self):

        for flop in self.flops:
            if not isinstance(flop, Flop):
                flop = Flop(flop)
            if conditions.is_mono(flop):
                self.monotone += 1
            elif conditions.is_tripsed(flop):
                self.tripsed += 1
            elif conditions.is_paired(flop):
                self.paired += 1
            elif conditions.is_rainbow(flop) and not conditions.is_paired(flop):
                self.rainbow_unpaired += 1
            elif conditions.is_two_tone(flop) and not conditions.is_paired(flop):
                self.two_tone_unpaired += 1
            else:
                raise ValueError("Something went wrong, can't assign a type to the flop")

        flop_type_combs = FlopTypesCombs(self.all, self.monotone, self.tripsed,
                                         self.paired, self.rainbow_unpaired, self.two_tone_unpaired)
        return flop_type_combs

    def __str__(self):
        text = f'Total number of flops: {self.all}\n' \
               f'Number of monotone flops: {self.monotone}\n' \
               f'Number of tripsed flops: {self.tripsed}\n' \
               f'Number of paired flops: {self.paired}\n' \
               f'Number of rainbow_unpaired flops: {self.rainbow_unpaired}\n' \
               f'Number of two tone_unpaired flops: {self.two_tone_unpaired}\n'
        return text


class WeightAdder:

    def __init__(self, flops):
        self.flops = flops

    def get_weights(self):

        current_flop_combos = ComboCounter(self.flops).count_combos()

        mono_w = current_flop_combos.mono and all_flop_comb_fractions.mono \
            * (current_flop_combos.all / current_flop_combos.mono)
        tripsed_w = current_flop_combos.tripsed and all_flop_comb_fractions.tripsed \
            * (current_flop_combos.all / current_flop_combos.tripsed)
        paired_w = current_flop_combos.paired and all_flop_comb_fractions.paired \
            * (current_flop_combos.all / current_flop_combos.paired)
        rainbow_unpaired_w = current_flop_combos.rainbow_unpaired and all_flop_comb_fractions.rainbow_unpaired \
            * (current_flop_combos.all / current_flop_combos.rainbow_unpaired)
        two_tone_unpaired_w = current_flop_combos.two_tone_unpaired and all_flop_comb_fractions.two_tone_unpaired \
            * (current_flop_combos.all / current_flop_combos.two_tone_unpaired)
        weights = [mono_w, tripsed_w, paired_w, rainbow_unpaired_w, two_tone_unpaired_w]

        if any(weights):
            min_weight = min(x for x in weights if x > 0)
            weights = [round((x / min_weight), 4) if x > 0 else None for x in weights]
        else:
            weights = [None for _ in weights]

        FlopWeights = namedtuple("FlopWeights", "mono tripsed paired rainbow_unpaired two_tone_unpaired")
        flop_weights = FlopWeights(*weights)
        return flop_weights

    def get_flops_with_weights(self):
        weights = self.get_weights()
        flops_with_weights = []
        for flop in self.flops:
            flop = Flop(flop)
            if conditions.is_mono(flop):
                flops_with_weights.append(flop.name + f':{weights.mono}')
            elif conditions.is_tripsed(flop):
                flops_with_weights.append(flop.name + f':{weights.tripsed}')
            elif conditions.is_paired(flop):
                flops_with_weights.append(flop.name + f':{weights.paired}')
            elif conditions.is_rainbow(flop) and not conditions.is_paired(flop):
                flops_with_weights.append(flop.name + f':{weights.rainbow_unpaired}')
            elif conditions.is_two_tone and not conditions.is_paired(flop):
                flops_with_weights.append(flop.name + f':{weights.two_tone_unpaired}')
            else:
                raise ValueError("Something went wrong! Cant assign a type to the flop!")
        return flops_with_weights

    def __str__(self):
        return str(self.get_weights())
