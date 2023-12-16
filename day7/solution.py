from enum import Enum
from functools import cmp_to_key


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


CARD_RANKING = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class CamelCards:
    def __init__(self, hand: list[str], bid: int) -> None:
        self.hand = hand
        self.bid = bid
        self.hand_type = self.get_hand_type()

    @classmethod
    def from_str(cls, string: str) -> "CamelCards":
        """
        "32T3K 765" --> CamelCards(hand=[3,2,T,3,K], bid=765)
        """
        hand, bid = string.split(" ")
        return cls(hand=list(hand), bid=int(bid))

    def get_hand_type(self) -> HandType:
        card_counts = {k: 0 for k in CARD_RANKING.keys()}
        for card in self.hand:
            card_counts[card] += 1
        counts = [x for x in card_counts.values() if x != 0]
        if counts.count(2) == 2:
            return HandType.TWO_PAIR
        counts = set(counts)
        if len(counts) == 1:
            if 1 in counts:
                return HandType.HIGH_CARD
            else:
                return HandType.FIVE_OF_A_KIND
        else:
            if 4 in counts:
                return HandType.FOUR_OF_A_KIND
            if 3 in counts and 2 in counts:
                return HandType.FULL_HOUSE
            if 3 in counts:
                return HandType.THREE_OF_A_KIND
            if 2 in counts:
                return HandType.ONE_PAIR

    def __gt__(self, other: "CamelCards"):
        if self.hand_type.value > other.hand_type.value:
            return True
        elif self.hand_type.value < other.hand_type.value:
            return False
        else:
            for a, b in zip(self.hand, other.hand):
                if CARD_RANKING[a] > CARD_RANKING[b]:
                    return True
                elif CARD_RANKING[a] < CARD_RANKING[b]:
                    return False

        raise AssertionError(f"unable to compare cards {self.hand} and {other.hand}")


def compare_cards(a: CamelCards, b: CamelCards):
    if a > b:
        return 1
    else:
        return -1


def part_1():
    input = open("./input.txt", "r").read()
    lines = input.splitlines()
    camel_cards = [CamelCards.from_str(line) for line in lines]
    key_function = cmp_to_key(compare_cards)
    sorted_cards = sorted(camel_cards, key=key_function)
    total = 0
    for i, cards in enumerate(sorted_cards):
        total += (i + 1) * cards.bid
    return total


if __name__ == "__main__":
    print(part_1())
