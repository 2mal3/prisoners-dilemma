from typing import Literal
from random import choice


def act(me_actions: list[Literal["C", "D"]], you_actions: list[Literal["C", "D"]]) -> Literal["C", "D"]:
    return choice(["C", "D"])
