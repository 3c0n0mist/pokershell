import enum

import minsk.utils as utils


@enum.unique
class Street(enum.IntEnum):
    PRE_FLOP = 2
    FLOP = 5
    TURN = 6
    RIVER = 7


class GameState(utils.CommonEqualityMixin):
    def __init__(self, cards, player_num, pot):
        super().__init__()
        self._cards = cards
        self._player_num = player_num
        self._pot = pot

    def is_successor(self, other):
        if self == other:
            return False
        my_cards = ''.join(map(repr, self._cards))
        other_cards = ''.join(map(repr, other._cards))
        return all((my_cards.startswith(other_cards),
                    self._pot >= other._pot,
                    self._player_num <= other._player_num,))

    @property
    def cards(self):
        return self._cards

    @property
    def player_num(self):
        return self._player_num

    @property
    def pot(self):
        return self._pot

    @property
    def street(self):
        return Street(len(self._cards))


class GameStack:
    def __init__(self):
        super().__init__()
        self._stack = []

    def add_state(self, state):
        if state.player_num and state.pot:
            if self._stack and not state.is_successor(self._stack[-1]):
                self._stack = []
            self._stack.append(state)

    @property
    def stack(self):
        return self._stack
