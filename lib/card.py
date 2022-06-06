from enum import Enum
import itertools


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class Symbol(Enum):
    DIAMOND = 'diamond'
    OVAL = 'oval'
    SQUIGGLE = 'squiggle'


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    PURPLE = 'purple'


class Fill(Enum):
    EMPTY = 'empty'
    FILLED = 'filled'
    SHADED = 'shaded'


class Card:
    def __init__(self, number, symbol, color, fill):
        self.number = number
        self.symbol = symbol
        self.color = color
        self.fill = fill

    def __str__(self):
        return self.color.value \
               + self.symbol.value \
               + self.fill.value \
               + str(self.number.value)

    def __repr__(self):
        return str(self)

    @staticmethod
    def new_deck():
        return [Card(n, s, c, f) for n, s, c, f in itertools.product(Number, Symbol, Color, Fill)]
