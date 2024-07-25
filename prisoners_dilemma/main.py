from math import factorial
from time import sleep
from typing import Literal

from rich.progress import Progress, TaskID, BarColumn, TextColumn, MofNCompleteColumn

from prisoners_dilemma.agents import tit_for_tat, random

AGENTS: list = [random, tit_for_tat]


def main():
    results: dict[str, int] = {}

    progress = Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), MofNCompleteColumn())
    tasks: dict[str, TaskID] = {}
    for agent in AGENTS:
        agent_name = agent.__name__.split(".")[-1]
        tasks[agent_name] = progress.add_task(agent_name, total=factorial(len(AGENTS)) * 200 * 5)
    progress.start()

    combinations = _get_combinations(AGENTS)
    for combination in combinations:
        # One Game
        agent1 = AGENTS[combination[0]]
        agent2 = AGENTS[combination[1]]
        agent1_points, agent2_points = _play_game(agent1, agent2)

        agent1_name = agent1.__name__.split(".")[-1]
        agent2_name = agent2.__name__.split(".")[-1]

        # Save stats
        if agent1_name not in results:
            results[agent1_name] = 0
        results[agent1_name] += agent1_points
        if agent2_name not in results:
            results[agent2_name] = 0
        results[agent2_name] += agent2_points
        # Update progress
        progress.update(tasks[agent1_name], completed=results[agent1_name])
        progress.update(tasks[agent2_name], completed=results[agent2_name])
        sleep(1)

    progress.stop()

    # Sort results
    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    print("\nResults:")
    for agent_name, points in results.items():
        print(f" - {agent_name:<15}: {points}")


def _play_game(agent1, agent2) -> tuple[int, int]:
    agent1_actions: list[Literal["C", "D"]] = []
    agent2_actions: list[Literal["C", "D"]] = []
    agent1_points = 0
    agent2_points = 0

    for _ in range(200):
        agent1_action = agent1.act(agent1_actions, agent2_actions)
        agent2_action = agent2.act(agent2_actions, agent1_actions)

        agent1_round_points, agent2_round_points = _get_points_for_actions(agent1_action, agent2_action)
        agent1_points += agent1_round_points
        agent2_points += agent2_round_points

        agent1_actions.append(agent1_action)
        agent2_actions.append(agent2_action)

    return agent1_points, agent2_points


def _get_points_for_actions(action1: Literal["C", "D"], action2: Literal["C", "D"]) -> tuple[int, int]:
    if action1 == "C" and action2 == "C":
        return 3, 3
    if action1 == "C" and action2 == "D":
        return 0, 5
    if action1 == "D" and action2 == "C":
        return 5, 0
    if action1 == "D" and action2 == "D":
        return 1, 1

    raise ValueError(f"Invalid actions: {action1}, {action2}")


def _get_combinations(elements: list) -> tuple[tuple[int, int], ...]:
    combinations = []
    for i in range(len(elements)):
        for j in range(i, len(elements)):
            combinations.append((i, j))

    return tuple(combinations)


if __name__ == "__main__":
    main()
