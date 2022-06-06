import itertools
import random
from lib.card import Card


class Set:
    def __init__(self):
        # Generate all possible combinations of numbers, symbols, color and fills
        self.deck = Card.new_deck()
        self.table = []

        # Shuffle the deck of Set cards
        random.shuffle(self.deck)
        self.fill_table()

    def fill_table(self):
        # Fill the table so that there are 12 cards (if possible)
        cards_missing = 12 - len(self.table)

        self.table += self.deck[:cards_missing]
        del self.deck[:cards_missing]

    def remove_from_table(self, cards):
        # Remove the given cards from the table
        for c in cards:
            del self.table[self.table.index(c)]

    @staticmethod
    def is_set(*cards):
        # Check if the given cards form a Set
        assert len(cards) == 3
        numbers = [c.number for c in cards]
        symbols = [c.symbol for c in cards]
        colors = [c.color for c in cards]
        fills = [c.fill for c in cards]

        for values in [numbers, symbols, colors, fills]:
            if len(set(values)) == 2:
                return False

        return True

    def set_generator(self):
        # Iterate over all possible combinations of cards on the table and check for Sets
        for pot_set in itertools.combinations(self.table, 3):
            if Set.is_set(*pot_set):
                yield pot_set
