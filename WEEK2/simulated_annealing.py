"""
Simulated Annealing for the 8-puzzle.

Cost  : Manhattan distance to the goal (0 means solved).
Step  : pick a random neighbor.
Accept: always if better; otherwise with probability exp(-delta / T).
Cool  : T <- T * cooling_rate (geometric schedule).

Simulated annealing is a local search: it is NOT guaranteed to find a
solution or the shortest one, so random restarts are used.
"""

import math
import random

from puzzle import (
    GOAL,
    get_neighbors,
    get_start_state,
    is_solvable,
    manhattan_distance,
    print_solution,
)


def simulated_annealing(start, goal=GOAL, t_start=10.0, t_min=0.01,
                        cooling_rate=0.995, steps_per_temp=50):
    """
    One annealing run.
    Returns (solved, final_state, path_of_moves, steps_taken).
    """
    state, path = start, []
    cost = manhattan_distance(state, goal)
    temperature = t_start
    steps = 0

    while temperature > t_min and cost > 0:
        for _ in range(steps_per_temp):
            move, candidate = random.choice(get_neighbors(state))
            delta = manhattan_distance(candidate, goal) - cost
            steps += 1

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                state, cost = candidate, cost + delta
                path.append(move)
                if cost == 0:
                    break
        temperature *= cooling_rate

    return cost == 0, state, path, steps


def solve_with_restarts(start, goal=GOAL, max_restarts=50):
    """Repeat annealing from the start state until a run reaches the goal."""
    total_steps = 0
    for attempt in range(1, max_restarts + 1):
        solved, state, path, steps = simulated_annealing(start, goal)
        total_steps += steps
        if solved:
            return path, attempt, total_steps
    return None, max_restarts, total_steps


if __name__ == "__main__":
    start = get_start_state()
    if not is_solvable(start):
        print("This puzzle is not solvable.")
    else:
        solution, attempts, steps = solve_with_restarts(start)
        if solution is None:
            print(f"No solution found in {attempts} restarts ({steps} steps).")
        else:
            print(f"Solved on attempt {attempts} ({steps} total steps).")
            print(f"Path length (not necessarily shortest): {len(solution)} moves\n")
            print_solution(start, solution)
