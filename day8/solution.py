from dataclasses import dataclass
from functools import cache


@dataclass
class Node:
    key: str
    left: str
    right: str

    @classmethod
    def from_str(cls, string: str) -> "Node":
        """
        AAA = (BBB, CCC) --> Node(key=AAA, left=BBB, right=CCC)
        """
        key, pair = string.split("=")
        key = key.strip()
        pair = pair.strip().replace("(", "").replace(")", "")
        left, right = pair.split(",")
        return cls(key, left, right.strip())


def part1():
    input = open("./input.txt").read()
    instruction_str, node_block = input.split("\n\n")
    nodes = [Node.from_str(line) for line in node_block.splitlines()]
    node_mapping = {n.key: n for n in nodes}
    steps = 0
    current_node_key = "AAA"
    while current_node_key != "ZZZ":
        for instruction in instruction_str:
            current_node = node_mapping[current_node_key]
            match instruction:
                case "R":
                    current_node_key = current_node.right
                case "L":
                    current_node_key = current_node.left
                case _:
                    raise ValueError(f"unexpected instruction {instruction}")
            steps += 1
    print(steps)


def part2():
    input = open("./input.txt").read()
    instruction_str, node_block = input.split("\n\n")
    nodes = [Node.from_str(line) for line in node_block.splitlines()]
    node_mapping = {n.key: n for n in nodes}
    start_nodes = [key for key in node_mapping.keys() if key[-1] == "A"]

    class NodePath:
        def __init__(
            self, start_node_key: str, current_node_key: str, steps: set[int]
        ) -> None:
            self.start_node_key = start_node_key
            self.current_node_key = current_node_key
            self.steps = steps
            self.total_steps = 0

    start_nodes_to_paths = {
        x: NodePath(start_node_key=x, current_node_key=x, steps=set())
        for x in start_nodes
    }

    def steps_are_equal(start_nodes_to_paths: dict[str, NodePath]) -> bool:
        step_counts = [x.steps for x in start_nodes_to_paths.values()]
        first_set = step_counts[0]
        # print(step_counts)
        for count in first_set:
            if all(count in c_set for c_set in step_counts):
                print(count)
                return True
        return False

    @cache
    def steps_to_next_z(current_node_key: str) -> tuple[int, str]:
        steps = 0
        while current_node_key[-1] != "Z" or steps == 0:
            for instruction in instruction_str:
                steps += 1
                current_node = node_mapping[current_node_key]
                match instruction:
                    case "R":
                        current_node_key = current_node.right
                    case "L":
                        current_node_key = current_node.left
                    case _:
                        raise ValueError(f"unexpected instruction {instruction}")
        return steps, current_node_key

    while not steps_are_equal(start_nodes_to_paths):
        for node_path in start_nodes_to_paths.values():
            steps_taken, end_node_key = steps_to_next_z(node_path.current_node_key)
            node_path.total_steps += steps_taken
            node_path.steps.add(node_path.total_steps)
            node_path.current_node_key = end_node_key


if __name__ == "__main__":
    part1()
    part2()
