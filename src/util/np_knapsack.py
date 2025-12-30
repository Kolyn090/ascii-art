from itertools import combinations_with_replacement

class Item:
    def __init__(self, stored, value: float = 0.0, size: int = 0):
        self.value = value
        self.size = size
        self.stored = stored

def np_knapsack(
    items_a: list[Item],
    items_b: list[Item],
    C: int,
    min_items: int = 1,
    max_items: int = 5,
    lambda_val: float = 0.5
) -> list[Item]:
    """
    Safe knapsack selection allowing duplicates from items_b.
    Returns the best subset according to capacity fill and value similarity.
    Always returns a subset if any item fits.
    """

    if not items_b or C <= 0:
        return []

    # Filter items that can fit in capacity
    fit_items = [item for item in items_b if item.size <= C]
    if not fit_items:
        return []  # nothing fits

    a_values = [a.value for a in items_a]
    best_subset: list[Item] = []
    best_score = -float('inf')

    ALPHA = lambda_val  # weight for capacity fill
    BETA = 1 - lambda_val   # weight for value similarity

    # Dynamically adjust min/max items so at least one combination can fit
    max_possible_items = min(max_items, C // min(item.size for item in fit_items))
    min_possible_items = max(min_items, 1)

    for k in range(min_possible_items, max_possible_items + 1):
        for combo in combinations_with_replacement(fit_items, k):
            total_size = sum(item.size for item in combo)
            if total_size > C:
                continue  # skip if over capacity

            fill_ratio = total_size / C

            if a_values:
                dist_sum = sum(min(abs(item.value - a) for a in a_values) for item in combo)
                avg_distance = dist_sum / k
                similarity_score = 1.0 / (1.0 + avg_distance)
            else:
                similarity_score = 0.0

            score = ALPHA * fill_ratio + BETA * similarity_score

            if score > best_score:
                best_score = score
                best_subset = list(combo)

    # If nothing selected (very small C), pick the single best-fit item
    if not best_subset:
        best_subset = [max(fit_items, key=lambda x: x.value / x.size)]

    return best_subset

def test():
    items_a: list[Item] = [
        Item('~', 17, 13),
        Item('&', 8, 15),
        Item('=', 7, 12),
        Item('^', 11, 11),
        Item('#', 15, 14),
        Item('*', 9, 9),
        Item('!', 8, 5),
        Item('M', 9, 18),
        Item('_', 9, 15),
        Item(';', 6, 5),
        Item('-', 7, 10),
        Item('$', 13, 13),
        Item('.', 3, 5),
        Item('+', 5, 12),
        Item(':', 4, 5),
        Item('i', 10, 5),
        Item('[', 13, 8),
        Item('%', 6, 19),
        Item('\'', 13, 5),
        Item('l', 11, 5),
        Item('B', 12, 14),
        Item(' ', -10000, 6),
        Item('@', 11, 23),
        Item('8', 10, 13),
        Item('W', 7, 23),
        Item(',', 5, 5),
        Item(']', 15, 8)
    ]

    items_b: list[Item] = [
        Item(' ', -10000, 6),
        Item('.', 3, 5),
        Item(':', 4, 5),
        Item('+', 5, 12),
    ]

    C = 4
    knapsack = np_knapsack(items_a, items_b, C)

    for item in knapsack:
        print(item.stored, item.value, item.size)

if __name__ == '__main__':
    test()
