"""
Iterative Deepening Search (IDS) for the 8-puzzle.

Runs depth-limited DFS with limits 0, 1, 2, ... until the goal is found.
Complete and optimal (unit step cost) with O(b*d) memory.
"""

from puzzle import GOAL, get_neighbors, get_start_state, is_solvable, print_solution

CUTOFF = "cutoff"


def depth_limited_search(state, goal, limit, path, on_path, counter):
    """
    Recursive DFS bounded by `limit`.
    Returns a list of moves, CUTOFF, or None (no solution within limit).
    `on_path` holds states on the current path to avoid cycles.
    """
    counter[0] += 1
    if state == goal:
        return []
    if limit == 0:
        return CUTOFF

    cutoff_occurred = False
    for move, nxt in get_neighbors(state):
        if nxt in on_path:
            continue
        on_path.add(nxt)
        result = depth_limited_search(nxt, goal, limit - 1, path, on_path, counter)
        on_path.remove(nxt)

        if result == CUTOFF:
            cutoff_occurred = True
        elif result is not None:
            return [move] + result
    return CUTOFF if cutoff_occurred else None


def iterative_deepening_search(start, goal=GOAL, max_depth=31):
    """Returns (moves, nodes_expanded). 31 is the max depth of any solvable 8-puzzle."""
    counter = [0]
    for limit in range(max_depth + 1):
        result = depth_limited_search(start, goal, limit, [], {start}, counter)
        if result != CUTOFF:
            return result, counter[0]
    return None, counter[0]


if __name__ == "__main__":
    start = get_start_state()
    if not is_solvable(start):
        print("This puzzle is not solvable.")
    else:
        solution, nodes = iterative_deepening_search(start)
        print(f"Solution depth : {len(solution)}")
        print(f"Nodes visited  : {nodes}")
        print(f"Moves          : {' -> '.join(solution)}\n")
        print_solution(start, solution)
