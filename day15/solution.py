def hash(char: str, start_val: int) -> int:
    ascii_num = ord(char)
    output = start_val + ascii_num
    output = output * 17
    return output % 256


def hash_label(label: str) -> int:
    val = 0
    for char in label:
        val = hash(char, val)
    return val


def part1():
    input = open("./input.txt", "r").read()
    commands = input.split(",")
    total = 0
    for command in commands:
        val = 0
        for char in command:
            val = hash(char, val)
        total += val
    print(total)


class Lens:
    def __init__(self, label: str, focal_length: int) -> None:
        self.label = label
        self.focal_length = focal_length


class Box:
    def __init__(self, number: int) -> None:
        self.number = number
        self.lenses: list[Lens] = []

    def remove_lens(self, label: str) -> None:
        self.lenses = [l for l in self.lenses if l.label != label]

    def add_lens(self, label: str, focal_length: int) -> None:
        lens_index = -1
        for i, lens in enumerate(self.lenses):
            if lens.label == label:
                lens_index = i
                break
        if lens_index >= 0:
            self.lenses[lens_index] = Lens(label, focal_length)
        else:
            self.lenses.append(Lens(label, focal_length))

    @property
    def focusing_power(self):
        power = 0
        for i, lens in enumerate(self.lenses):
            power += (self.number + 1) * (i + 1) * lens.focal_length
        return power

    def __repr__(self) -> str:
        rtn = f"\nBox {self.number}: \n"
        for lens in self.lenses:
            rtn += f"[{lens.label} {lens.focal_length}]  "
        return rtn


def dash(command: str, dash_idx: int, boxes: dict[int, Box]):
    label = command[:dash_idx]
    box_number = hash_label(label)
    box = boxes[box_number]
    box.remove_lens(label)


def equals(command: str, equals_idx: int, boxes: dict[int, Box]):
    label = command[:equals_idx]
    focal_length = int(command[equals_idx + 1 :])
    box_number = hash_label(label)
    box = boxes[box_number]
    box.add_lens(label, focal_length)


def part2():
    input = open("./input.txt", "r").read()
    commands = input.split(",")

    boxes: dict[int, Box] = {}
    for i in range(256):
        boxes[i] = Box(number=i)

    for command in commands:
        equals_idx = command.find("=")
        dash_idx = command.find("-")
        if dash_idx >= 0:
            dash(command, dash_idx, boxes)
        elif equals_idx >= 0:
            equals(command, equals_idx, boxes)
        else:
            raise AssertionError("could not find a - or =")

    total = 0
    for box in boxes.values():
        total += box.focusing_power
    print(total)


if __name__ == "__main__":
    part1()
    part2()
