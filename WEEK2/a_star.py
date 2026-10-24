"""
A* Search for the 8-puzzle.

f(n) = g(n) + h(n)
  g(n): number of moves from the start
  h(n): admissible heuristic (Manhattan distance or misplaced tiles)

Both heuristics are admissible, so A* returns an optimal solution.
"""

import heapq
from itertools import count

from puzzle import (
    GOAL,
    get_neighbors,
    get_start_state,
    is_solvable,
    manhattan_distance,
    misplaced_tiles,
    print_solution,
)

HEURISTICS = {"manhattan": manhattan_distance, "misplaced": misplaced_tiles}


def a_star(start, goal=GOAL, heuristic=manhattan_distance):
    """Returns (moves, nodes_expanded), or (None, nodes_expanded) if unsolvable."""
    tie_breaker = count()  # keeps heap ordering stable when f-values tie
    open_list = [(heuristic(start, goal), next(tie_breaker), 0, start)]
    best_g = {start: 0}
    parent = {start: (None, None)}  # state -> (previous state, move)
    closed = set()
    expanded = 0

    while open_list:
        _, _, g, state = heapq.heappop(open_list)
        if state in closed:
            continue
        closed.add(state)
        expanded += 1

        if state == goal:
            moves = []
            while parent[state][0] is not None:
                state, move = parent[state]
                moves.append(move)
            return moves[::-1], expanded

        for move, nxt in get_neighbors(state):
            new_g = g + 1
            if new_g < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_g
                parent[nxt] = (state, move)
                f = new_g + heuristic(nxt, goal)
                heapq.heappush(open_list, (f, next(tie_breaker), new_g, nxt))

    return None, expanded


if __name__ == "__main__":
    start = get_start_state()
    choice = input("Heuristic [manhattan/misplaced] (default manhattan): ").strip().lower()
    h = HEURISTICS.get(choice, manhattan_distance)

    if not is_solvable(start):
        print("This puzzle is not solvable.")
    else:
        solution, nodes = a_star(start, heuristic=h)
        print(f"Solution depth : {len(solution)}")
        print(f"Nodes expanded : {nodes}")
        print(f"Moves          : {' -> '.join(solution)}\n")
        print_solution(start, solution)
