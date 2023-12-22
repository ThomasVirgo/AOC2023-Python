import re
from dataclasses import dataclass
from enum import Enum
from typing import Callable


class Outcome(Enum):
    ACCEPTED = "A"
    REJECTED = "R"


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_str(cls, string: str) -> "Part":
        nums = re.findall(r"\d+", string)
        nums = [int(num) for num in nums]
        return cls(*nums)

    @property
    def total_rating(self) -> int:
        return self.x + self.m + self.a + self.s


class Criteria:
    def __init__(
        self, rule: str, result: str, category: str, comparator: str, value: int
    ) -> None:
        self.rule = rule
        self.result = result
        self.category = category
        self.comparator = comparator
        self.value = value

    @classmethod
    def from_str(cls, string: str) -> "Criteria":
        """
        a<2006:qkq --> Criteria(rule="a<2006", result="qkq")
        """
        rule, result = string.split(":")
        category = rule[0]
        comparator = rule[1]
        value = int(rule[2:])
        return cls(rule, result, category, comparator, value)

    def does_part_pass_criteria(self, part: Part) -> bool:
        part_value = getattr(part, self.category)
        if self.comparator == "<":
            return part_value < self.value
        elif self.comparator == ">":
            return part_value > self.value
        else:
            raise ValueError(f"unknown comparator {self.comparator}")


class Workflow:
    def __init__(self, label: str, criteria: list[Criteria], result: str) -> None:
        self.label = label
        self.criteria = criteria
        self.result = result

    @classmethod
    def from_str(cls, string: str) -> "Workflow":
        label, criteria = string.split("{")
        criteria = criteria.replace("}", "").split(",")
        end = criteria.pop()
        criteria = [Criteria.from_str(c) for c in criteria]
        return cls(label, criteria, end)

    def run_part(self, part: Part) -> str:
        for criteria in self.criteria:
            if criteria.does_part_pass_criteria(part):
                return criteria.result
        return self.result

    def __repr__(self) -> str:
        return f"label={self.label} criteria={self.criteria} result={self.result}"


def run_workflow_on_part(
    part: Part, workflow: Workflow, workflow_label_to_workflow: dict[str, Workflow]
) -> Outcome:
    result = workflow.run_part(part)
    if result == "A":
        print("accepted")
        return Outcome.ACCEPTED
    elif result == "R":
        print("rejected")
        return Outcome.REJECTED
    else:
        return run_workflow_on_part(
            part, workflow_label_to_workflow[result], workflow_label_to_workflow
        )


def part1():
    input = open("./input.txt", "r").read()
    workflows, parts = input.split("\n\n")
    parts = [Part.from_str(string) for string in parts.splitlines()]
    workflows = [Workflow.from_str(string) for string in workflows.splitlines()]
    workflow_label_to_workflow: dict[str, Workflow] = {w.label: w for w in workflows}
    starting_workflow = workflow_label_to_workflow["in"]
    total = 0
    for part in parts:
        outcome = run_workflow_on_part(
            part, starting_workflow, workflow_label_to_workflow
        )
        print(outcome)
        if outcome == Outcome.ACCEPTED:
            total += part.total_rating
    print(total)


if __name__ == "__main__":
    part1()
