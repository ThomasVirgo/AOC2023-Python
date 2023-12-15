import math


def number_of_possible_wins(T: int, R: int) -> int:
    """
    T = total race time
    R = distance record
    t_b = time holding button
    t_m = time moving

    then we can write:
    T = t_b + t_m
    distance = speed * time
    speed = time holding button = t_b
    distance = t_b * t_m

    so will match the record when following is satisfied:
    t_b(T-t_b) = R
    -t_b^2 + Tt_b - R = 0
    """
    a = -1
    b = T
    c = -R

    solution_1 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    solution_2 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    lower, higher = sorted([solution_1, solution_2])

    dps = str(solution_1)[::-1].find(".")
    if dps <= 1:
        return int(higher) - int(lower) - 1

    lower_bound = math.floor(lower)
    higher_bound = math.floor(higher)

    return higher_bound - lower_bound


def part_1() -> int:
    input = open("./input.txt", "r").read()
    times, distances = input.splitlines()
    _, times = times.split(":")
    _, distances = distances.split(":")
    times = [int(x) for x in times.split()]
    distances = [int(x) for x in distances.split()]
    total = 1
    for time, distance in zip(times, distances):
        wins = number_of_possible_wins(time, distance)
        total *= wins
    return total


def part_2() -> int:
    input = open("./input.txt", "r").read()
    times, distances = input.splitlines()
    _, times = times.split(":")
    _, distances = distances.split(":")
    total_time = int(times.replace(" ", ""))
    total_distance = int(distances.replace(" ", ""))
    print(total_time, total_distance)
    return number_of_possible_wins(total_time, total_distance)


if __name__ == "__main__":
    print(f"part 1 solution: {part_1()}")
    print(f"part 2 solution: {part_2()}")
