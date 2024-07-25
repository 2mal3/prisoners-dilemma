from typing import Literal


def act(me_actions: list[Literal["C", "D"]], you_actions: list[Literal["C", "D"]]) -> Literal["C", "D"]:
    if len(you_actions) == 0:
        return "C"
    last_you_action = you_actions[-1]
    return last_you_action
