from typing import Union

canon_suits = ("c", "d", "h", "s")
canon_ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')


def get_canonical_flops(suits: tuple = canon_suits, ranks: tuple = canon_ranks,
                        rev_suits: bool = False, rev_figures: bool = False, get_list=False) -> Union[set, list]:
    """
    Returns a complete set of strategically meaningful poker flops (tuples).
    By default, flops are generated from lowest to highest card and suits appear in alphabetical order ("c", "d", "h").

    :param suits: tuple of 3 suits chosen for canonical flop representation
    :param ranks: tuple of cards that can form poker flop (usually 13 elements, 9 in 6+ holdem)
    :param rev_suits: If set to True, then card suit order will be reversed ("s", "h", "d")
     for canonical representation instead of ("c", "d", "h")
    :param rev_figures: If set to True, then flop figure order will be reversed (from high to low card)
    :param get_list: If true, returns an ordered list instead of a set.
    :return: A complete set of tuples of canonical poker flops (or an ordered list when get_list is set to True).
    """

    if rev_suits:
        suits = tuple(reversed(suits))
    if rev_figures:
        ranks = tuple(reversed(ranks))

    canonical_flops = set()

    # generating rainbow flops (3 different suits present on the flop)
    # figures don't have to be distinct
    for i in range(len(ranks)):
        for j in range(i, len(ranks)):
            for k in range(j, len(ranks)):
                flop = (ranks[i] + suits[0],
                        ranks[j] + suits[1],
                        ranks[k] + suits[2])
                canonical_flops.add(flop)

    # generating monotone flops (cards of only 1 suit present on the flop)
    # figures have to be distinct
    for i in range(len(ranks) - 2):
        for j in range(i + 1, len(ranks) - 1):
            for k in range(j + 1, len(ranks)):
                flop = (ranks[i] + suits[0],
                        ranks[j] + suits[0],
                        ranks[k] + suits[0])
                canonical_flops.add(flop)

    # generating two-tone boards (cards of 2 different suits present on flop):

    # two-tone flops that have pair,  forming pattern suit0, suit1, suit0 (2c 2d 8c)
    # or suit0, suit0, suit1 (2c 8c 8d)
    for i in range(len(ranks) - 1):
        for j in range(i + 1, len(ranks)):
            flop1 = (ranks[i] + suits[0],
                     ranks[i] + suits[1],
                     ranks[j] + suits[0])
            flop2 = (ranks[i] + suits[0],
                     ranks[j] + suits[0],
                     ranks[j] + suits[1])
            canonical_flops.add(flop1)
            canonical_flops.add(flop2)
    i, j, k = 0, 0, 0

    # two-tone flops that don't have pair, forming pattern suit0, suit0, suit1 (2c3c8d)
    # or suit0, suit1, suit1 (2c 3d 8d) or suit0, suit1, suit0 (2c 3d 8c)
    for i in range(len(ranks) - 2):
        for j in range(i + 1, len(ranks) - 1):
            for k in range(j + 1, len(ranks)):
                flop1 = (ranks[i] + suits[0],
                         ranks[j] + suits[0],
                         ranks[k] + suits[1])
                flop2 = (ranks[i] + suits[0],
                         ranks[j] + suits[1],
                         ranks[k] + suits[1])
                flop3 = (ranks[i] + suits[0],
                         ranks[j] + suits[1],
                         ranks[k] + suits[0])
                canonical_flops.add(flop1)
                canonical_flops.add(flop2)
                canonical_flops.add(flop3)

    if not get_list:
        return canonical_flops
    else:
        def _sortkey(x):
            return (ranks.index(x[0][0]), ranks.index(x[1][0]), ranks.index(x[2][0]),
                    suits.index(x[0][1]), suits.index(x[1][1]), suits.index(x[2][1]))

        canonical_flops_list = sorted(canonical_flops, key=_sortkey)
        return canonical_flops_list

