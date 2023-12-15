from dataclasses import dataclass

SYMBOLS = {"%", "=", "@", "+", "/", "&", "$", "#", "*", "-"}


@dataclass(frozen=True)
class SymbolLocation:
    x: int
    y: int


@dataclass(frozen=True)
class NumberLocation:
    value: int
    start_x: int
    end_x: int
    y: int

    def possible_symbol_locations(self) -> list[SymbolLocation]:
        locations = []
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.start_x - 1, self.end_x + 2):
                locations.append(SymbolLocation(x, y))
        return locations


def part_1() -> int:
    input = open("./input.txt", mode="r").read()
    lines = input.splitlines()
    symbol_location_to_symbol: dict[SymbolLocation, str] = {}
    number_locations: list[NumberLocation] = []
    grid = [list(line) for line in lines]
    for y, row in enumerate(grid):
        number = ""
        for x, char in enumerate(row):
            if char == ".":
                if number != "":
                    number_locations.append(
                        NumberLocation(
                            value=int(number), start_x=x - len(number), end_x=x - 1, y=y
                        )
                    )
                number = ""
                continue
            elif char in SYMBOLS:
                if number != "":
                    number_locations.append(
                        NumberLocation(
                            value=int(number), start_x=x - len(number), end_x=x - 1, y=y
                        )
                    )
                number = ""
                symbol_location_to_symbol[SymbolLocation(x, y)] = char
            else:
                number += char
                if x == len(row) - 1:
                    number_locations.append(
                        NumberLocation(
                            value=int(number), start_x=x - len(number) + 1, end_x=x, y=y
                        )
                    )

    total = 0
    for number_location in number_locations:
        for possible_symbol_location in number_location.possible_symbol_locations():
            if symbol_location_to_symbol.get(possible_symbol_location):
                total += number_location.value
                break
    return total


class GearLocation:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.adjacent_numbers: list[int] = []


def part_2() -> int:
    input = open("./input.txt", mode="r").read()
    lines = input.splitlines()
    gear_locations: list[GearLocation] = []
    number_locations: list[NumberLocation] = []
    grid = [list(line) for line in lines]

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "*":
                gear_locations.append(GearLocation(x, y))

    for y, row in enumerate(grid):
        number = ""
        for x, char in enumerate(row):
            if char == ".":
                if number != "":
                    number_locations.append(
                        NumberLocation(
                            value=int(number), start_x=x - len(number), end_x=x - 1, y=y
                        )
                    )
                number = ""
                continue
            elif char in SYMBOLS:
                if number != "":
                    number_locations.append(
                        NumberLocation(
                            value=int(number), start_x=x - len(number), end_x=x - 1, y=y
                        )
                    )
                number = ""
            else:
                number += char
                if x == len(row) - 1:
                    number_locations.append(
                        NumberLocation(
                            value=int(number), start_x=x - len(number) + 1, end_x=x, y=y
                        )
                    )

    for number_location in number_locations:
        possible_locations = number_location.possible_symbol_locations()
        for gear_location in gear_locations:
            for location in possible_locations:
                if location.x == gear_location.x and location.y == gear_location.y:
                    gear_location.adjacent_numbers.append(number_location.value)
                    break

    total = 0
    for gear_location in gear_locations:
        if len(gear_location.adjacent_numbers) == 2:
            total += (
                gear_location.adjacent_numbers[0] * gear_location.adjacent_numbers[1]
            )
    return total


if __name__ == "__main__":
    print(f"part 1 solution: {part_1()}")
    print(f"part 2 solution: {part_2()}")
