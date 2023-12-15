class Card:
    def __init__(
        self, id: int, winning_numbers: list[int], elfs_numbers: list[int]
    ) -> None:
        self.id = id
        self.winning_numbers = winning_numbers
        self.elfs_numbers = elfs_numbers
        self.creates_cards = self.cards_won()

    @classmethod
    def from_str(cls, card_str: str) -> "Card":
        """
        'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'
        -->
        Card(id=1, winning_numbers=[41,48,83,86,17], elfs_numbers=[83,86,6,31,17,9,48,53])
        """
        card_id_str, numbers_str = card_str.split(":")
        _, card_id = card_id_str.split()
        card_id = int(card_id)
        winning_numbers_str, elfs_numbers_str = numbers_str.split("|")
        winning_numbers_str_list = winning_numbers_str.split()
        elfs_numbers_str_list = elfs_numbers_str.split()
        return cls(
            id=card_id,
            winning_numbers=[int(x) for x in winning_numbers_str_list],
            elfs_numbers=[int(x) for x in elfs_numbers_str_list],
        )

    @property
    def matches(self) -> int:
        total = 0
        for number in self.elfs_numbers:
            if number in self.winning_numbers:
                total += 1
        return total

    def cards_won(self) -> list[int]:
        return list(range(self.id + 1, self.id + self.matches + 1))

    def calculate_score(self) -> int:
        total = 0.5
        for number in self.elfs_numbers:
            if number in self.winning_numbers:
                total *= 2
        if total == 0.5:
            return 0
        return int(total)


def part_1() -> int:
    input = open("./input.txt", mode="r").read()
    lines = input.splitlines()
    cards = [Card.from_str(line) for line in lines]
    total = 0
    for card in cards:
        total += card.calculate_score()
    return total


def part_2() -> int:
    input = open("./input.txt", mode="r").read()
    lines = input.splitlines()
    cards = [Card.from_str(line) for line in lines]
    card_id_to_cards_won: dict[int, list[int]] = {
        card.id: card.cards_won() for card in cards
    }

    def add_cards(ids: list[int], total_cards: int):
        for id in ids:
            cards_won = card_id_to_cards_won[id]
            total_cards += len(cards_won)
            total_cards = add_cards(cards_won, total_cards)
        return total_cards

    total_cards = 0
    for card in cards:
        total_cards += 1
        total_cards = add_cards([card.id], total_cards)

    return total_cards


if __name__ == "__main__":
    print(f"part 1 solution: {part_1()}")
    print(f"part 2 solution: {part_2()}")
