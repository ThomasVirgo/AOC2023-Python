from collections import defaultdict
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

CARD_RANKING_PART_2 = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
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

    def _hand_type(self, card_counts: dict[str, int]) -> HandType:
        del card_counts["J"]
        counts = [x for x in card_counts.values()]
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
        raise AssertionError(f"could not determine hand type for hand{self.hand}")

    def _hand_type_with_jokers(
        self, card_counts: dict[int, str], number_of_jokers: int
    ) -> HandType:
        if number_of_jokers == 5:
            return HandType.FIVE_OF_A_KIND

        highest_card_count_excluding_jokers = max(
            v for k, v in card_counts.items() if k != "J"
        )
        jokers_and_max_count: tuple[int, int] = (
            number_of_jokers,
            highest_card_count_excluding_jokers,
        )
        match jokers_and_max_count:
            case (1, 1):
                return HandType.ONE_PAIR
            case (1, 2):
                return HandType.THREE_OF_A_KIND
            case (1, 3):
                return HandType.FOUR_OF_A_KIND
            case (1, 4):
                return HandType.FIVE_OF_A_KIND
            case (2, 1):
                return HandType.THREE_OF_A_KIND
            case (2, 2):
                return HandType.FOUR_OF_A_KIND
            case (2, 3):
                return HandType.FIVE_OF_A_KIND
            case (3, 1):
                return HandType.FOUR_OF_A_KIND
            case (3, 2):
                return HandType.FIVE_OF_A_KIND
            case (4, 1):
                return HandType.FIVE_OF_A_KIND
            case _:
                raise AssertionError(
                    f"unexpected hand, {number_of_jokers} jokers and max card count {jokers_and_max_count[1]}"
                )

    def get_hand_type(self) -> HandType:
        card_counts = defaultdict(int)
        for card in self.hand:
            card_counts[card] += 1
        number_of_jokers = card_counts["J"]
        if number_of_jokers == 0:
            return self._hand_type(card_counts)
        else:
            return self._hand_type_with_jokers(card_counts, number_of_jokers)

    def __gt__(self, other: "CamelCards"):
        if self.hand_type.value > other.hand_type.value:
            return True
        elif self.hand_type.value < other.hand_type.value:
            return False
        else:
            for a, b in zip(self.hand, other.hand):
                if CARD_RANKING_PART_2[a] > CARD_RANKING_PART_2[b]:
                    return True
                elif CARD_RANKING_PART_2[a] < CARD_RANKING_PART_2[b]:
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
    # for cards in camel_cards:
    #     print(cards.hand_type, cards.hand)
    key_function = cmp_to_key(compare_cards)
    sorted_cards = sorted(camel_cards, key=key_function)
    total = 0
    for i, cards in enumerate(sorted_cards):
        total += (i + 1) * cards.bid
    return total


if __name__ == "__main__":
    print(part_1())
