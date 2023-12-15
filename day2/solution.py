from dataclasses import dataclass


class Cubes:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def power(self) -> int:
        return self.red * self.green * self.blue

    def __str__(self) -> str:
        return f"red={self.red} green={self.green} blue={self.blue}"


MAX_CUBES = Cubes(red=12, green=13, blue=14)


@dataclass(frozen=True)
class Game:
    id: int
    cubes_shown: list[Cubes]

    @classmethod
    def from_str(cls, input_str: str) -> "Game":
        cubes_list = []
        game_str, cube_str = input_str.split(":")
        _, game_id = game_str.strip().split(" ")
        game_id = int(game_id)
        cube_str = cube_str.strip()
        cube_strs = cube_str.split(";")
        cube_lists = [x.split(",") for x in cube_strs]
        for cube_list in cube_lists:
            cubes = Cubes()
            for cubes_string in cube_list:
                cubes_string = cubes_string.strip()
                number, colour = cubes_string.split(" ")
                setattr(cubes, colour, int(number))
            cubes_list.append(cubes)
        return cls(id=game_id, cubes_shown=cubes_list)

    def is_possible(self, max_cubes: Cubes = MAX_CUBES) -> bool:
        for cubes in self.cubes_shown:
            if (
                cubes.red > max_cubes.red
                or cubes.green > max_cubes.green
                or cubes.blue > max_cubes.blue
            ):
                return False
        return True

    def fewest_cubes(self) -> Cubes:
        max_red = 0
        max_green = 0
        max_blue = 0
        for cubes in self.cubes_shown:
            if cubes.red > max_red:
                max_red = cubes.red
            if cubes.green > max_green:
                max_green = cubes.green
            if cubes.blue > max_blue:
                max_blue = cubes.blue
        return Cubes(red=max_red, green=max_green, blue=max_blue)

    def __repr__(self) -> str:
        rtn = f"Game {self.id}: \n"
        for cubes in self.cubes_shown:
            rtn += f"   {str(cubes)}\n"
        return rtn


def part_1() -> int:
    input = open("./input.txt", mode="r").read()
    lines = input.splitlines()
    games: list[Game] = [Game.from_str(x) for x in lines]
    total = 0
    for game in games:
        if game.is_possible():
            total += game.id
    return total


def part_2() -> int:
    input = open("./input.txt", mode="r").read()
    lines = input.splitlines()
    games: list[Game] = [Game.from_str(x) for x in lines]
    total = 0
    for game in games:
        cubes = game.fewest_cubes()
        total += cubes.power()
    return total


if __name__ == "__main__":
    print(f"part 1 solution: {part_1()}")
    print(f"part 2 solution: {part_2()}")
