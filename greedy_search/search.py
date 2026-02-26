# search.py
import heapq
from greedy_search.grid import Cell, Grid, Position, get_neighbors, get_cell, is_passable, find_position

# --- Constants ---
FIRE_PENALTY: int = 50


def _fire_penalty(grid: Grid, pos: Position) -> int:
    """Returns FIRE_PENALTY if any neighbor of pos is on fire, else 0."""
    return FIRE_PENALTY if any(
        get_cell(grid, n) == Cell.FIRE
        for n in get_neighbors(grid, pos)
    ) else 0


def _heuristic(grid: Grid, pos: Position, goal: Position) -> int:
    """h(n) = manhattan(n, EXIT) + fire_penalty(n)."""
    r, c = pos
    gr, gc = goal
    return abs(r - gr) + abs(c - gc) + _fire_penalty(grid, pos)


def greedy_next_step(grid: Grid) -> Position | None:
    """
    Runs Greedy Best-First Search from AGENT to EXIT.
    Returns the next Position the agent should move to, or None if no path exists.
    """
    start = find_position(grid, Cell.AGENT)
    goal = find_position(grid, Cell.EXIT)

    if start is None or goal is None:
        return None

    # (h(n), position, path)
    heap: list[tuple[int, Position, list[Position]]] = []
    heapq.heappush(heap, (_heuristic(grid, start, goal), start, [start]))
    visited: set[Position] = {start}

    while heap:
        _, current, path = heapq.heappop(heap)

        if current == goal:
            return path[1] if len(path) > 1 else None

        for neighbor in get_neighbors(grid, current):
            cell = get_cell(grid, neighbor)
            if neighbor not in visited and is_passable(cell):
                visited.add(neighbor)
                h = _heuristic(grid, neighbor, goal)
                heapq.heappush(heap, (h, neighbor, path + [neighbor]))

    return None  # No path found — agent is trapped
