from dataclasses import dataclass


@dataclass
class Seeds:
    values: list[int]

    @classmethod
    def from_str(cls, string: str) -> "Seeds":
        """
        seeds: 79 14 55 13 --> Seeds(values=[79,14,55,13])
        """
        _, seeds = string.split(":")
        seeds = seeds.split()
        values = [int(x) for x in seeds]
        return cls(values)

    def get_all_seed_values(self) -> list[tuple[int, int]]:
        seed_ranges = []
        groups = []
        for i in range(0, len(self.values), 2):
            groups.append(self.values[i : i + 2])


@dataclass
class Range:
    destination_start: int
    source_start: int
    length: int

    def is_in_source_range(self, source: int) -> bool:
        if self.source_start <= source <= self.source_start + self.length:
            return True
        else:
            return False

    def get_destination(self, source: int) -> int:
        """
        3  4  5  6
        28 29 30 21
        """
        diff_from_start = source - self.source_start
        return self.destination_start + diff_from_start


@dataclass
class Map:
    ranges: list[Range]

    @classmethod
    def from_str(cls, string: str) -> "Map":
        lines = string.splitlines()
        lines.pop(0)  # remove description
        ranges = []
        for line in lines:
            values = line.split()
            values = [int(x) for x in values]
            ranges.append(Range(*values))
        return cls(ranges)

    def get_destination(self, source: int) -> int:
        for r in self.ranges:
            if r.is_in_source_range(source):
                return r.get_destination(source)
        # if can't find it in a map, source maps to itself
        return source


def part_1() -> int:
    input = open("./input.txt", mode="r").read()
    blocks = input.split("\n\n")
    seeds = Seeds.from_str(blocks.pop(0))
    maps = [Map.from_str(block) for block in blocks]
    destinations = []
    for seed in seeds.values:
        output = seed
        for map in maps:
            output = map.get_destination(output)
        destinations.append(output)
    return min(destinations)


def part_2() -> int:
    """
    seeds: 79 14 55 13

    maps:
    50 98 2  ----  98-99 -> 50-51
    52 50 48 ---- 50-97 -> 52-99

    (14,79) and (13,55)
    (14,49) (52, 81)  (13,49) (52,57)
    """
    input = open("./input.txt", mode="r").read()
    blocks = input.split("\n\n")
    seeds = Seeds.from_str(blocks.pop(0))
    maps = [Map.from_str(block) for block in blocks]
    destinations = []
    seed_range = seeds.get_all_seed_values()[0]
    for seed in range(seed_range[0], seed_range[1]):
        count += 1
        output = seed
        for map in maps:
            output = map.get_destination(output)
        destinations.append(output)
    return min(destinations)


if __name__ == "__main__":
    print(f"part 1 solution: {part_1()}")
    print(f"part 2 solution: {part_2()}")
