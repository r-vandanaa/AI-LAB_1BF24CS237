"""
8-Puzzle Problem: formulation + helpers shared by all solvers.

State   : tuple of 9 ints (row-major), 0 represents the blank.
Actions : move the blank Up / Down / Left / Right.
Goal    : (1, 2, 3, 4, 5, 6, 7, 8, 0)
Cost    : 1 per move.

Run this file directly to solve a puzzle using plain BFS.
"""

from collections import deque

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# (name, row change, column change) applied to the blank tile
MOVES = (("Up", -1, 0), ("Down", 1, 0), ("Left", 0, -1), ("Right", 0, 1))


def is_solvable(state):
    """A 3x3 puzzle is solvable iff the number of inversions is even."""
    tiles = [t for t in state if t != 0]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


def get_neighbors(state):
    """Return a list of (move_name, next_state) pairs."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    neighbors = []
    for name, dr, dc in MOVES:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            swap = r * 3 + c
            new = list(state)
            new[blank], new[swap] = new[swap], new[blank]
            neighbors.append((name, tuple(new)))
    return neighbors


def misplaced_tiles(state, goal=GOAL):
    """Heuristic h1: number of tiles not in their goal position."""
    return sum(1 for s, g in zip(state, goal) if s != 0 and s != g)


def manhattan_distance(state, goal=GOAL):
    """Heuristic h2: sum of horizontal + vertical distances to goal positions."""
    goal_pos = {tile: divmod(i, 3) for i, tile in enumerate(goal)}
    total = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        r, c = divmod(i, 3)
        gr, gc = goal_pos[tile]
        total += abs(r - gr) + abs(c - gc)
    return total


def print_state(state):
    for i in range(0, 9, 3):
        print(" ".join(str(t) if t else "_" for t in state[i:i + 3]))
    print()


def print_solution(start, moves):
    """Replay a list of move names from the start state."""
    state = start
    print("Initial state:")
    print_state(state)
    for step, move in enumerate(moves, 1):
        state = dict(get_neighbors(state))[move]
        print(f"Step {step}: {move}")
        print_state(state)


def read_state(prompt):
    """Read 9 space-separated digits (0 = blank) from the user."""
    while True:
        try:
            values = tuple(int(x) for x in input(prompt).split())
            if sorted(values) == list(range(9)):
                return values
        except ValueError:
            pass
        print("Enter the digits 0-8 exactly once, separated by spaces.")


def get_start_state():
    """Ask for a start state; press Enter to use a default example."""
    default = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    text = input("Enter start state (9 digits, 0 = blank) or press Enter for default: ").strip()
    if not text:
        return default
    try:
        values = tuple(int(x) for x in text.split())
        if sorted(values) == list(range(9)):
            return values
    except ValueError:
        pass
    print("Invalid input, using default.")
    return default


def bfs(start, goal=GOAL):
    """Breadth-first search: returns the shortest list of moves, or None."""
    if start == goal:
        return []
    frontier = deque([(start, [])])
    visited = {start}
    while frontier:
        state, path = frontier.popleft()
        for move, nxt in get_neighbors(state):
            if nxt in visited:
                continue
            if nxt == goal:
                return path + [move]
            visited.add(nxt)
            frontier.append((nxt, path + [move]))
    return None


if __name__ == "__main__":
    start = get_start_state()
    if not is_solvable(start):
        print("This puzzle is not solvable.")
    else:
        solution = bfs(start)
        print(f"Solved in {len(solution)} moves: {' -> '.join(solution)}\n")
        print_solution(start, solution)
