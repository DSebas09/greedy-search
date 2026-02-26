# generator.py
import random
from collections import deque
from greedy_search.grid import (
    Cell, Grid, Position,
    create_grid, set_cell, get_cell,
    get_neighbors, is_passable, find_position,
)


# --- Constants ---
GRID_SIZE: int = 20
WALL_DENSITY: float = 0.25
FIRE_SOURCES: int = 3
MIN_DISTANCE: int = 8


def _place_randomly(grid: Grid, state: Cell, exclude: set[Position]) -> Position:
    """Places a cell state in a random EMPTY position not in exclude."""
    size = len(grid)
    while True:
        pos = (random.randint(0, size - 1), random.randint(0, size - 1))
        if pos not in exclude and get_cell(grid, pos) == Cell.EMPTY:
            set_cell(grid, pos, state)
            return pos


def _is_solvable(grid: Grid) -> bool:
    """BFS check: can AGENT reach EXIT through passable cells (ignoring fire)?"""
    start = find_position(grid, Cell.AGENT)
    goal = find_position(grid, Cell.EXIT)
    if start is None or goal is None:
        return False

    visited: set[Position] = {start}
    queue: deque[Position] = deque([start])

    while queue:
        pos = queue.popleft()
        if pos == goal:
            return True
        for neighbor in get_neighbors(grid, pos):
            if neighbor not in visited and is_passable(get_cell(grid, neighbor)):
                visited.add(neighbor)
                queue.append(neighbor)

    return False


def _manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def generate_level(seed: int | None = None) -> tuple[Grid, int]:
    """Generates and validates a level. Returns (grid, seed)."""
    used_seed = seed if seed is not None else random.randint(0, 999_999)

    while True:
        random.seed(used_seed)
        grid = create_grid(GRID_SIZE)

        # Place walls
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if random.random() < WALL_DENSITY:
                    set_cell(grid, (r, c), Cell.WALL)

        # Place agent and exit with minimum distance
        occupied: set[Position] = set()
        agent_pos = _place_randomly(grid, Cell.AGENT, occupied)
        occupied.add(agent_pos)

        while True:
            exit_pos = _place_randomly(grid, Cell.EXIT, occupied)
            if _manhattan(agent_pos, exit_pos) >= MIN_DISTANCE:
                break
            set_cell(grid, exit_pos, Cell.EMPTY)  # retry

        occupied.add(exit_pos)

        # Place fire sources away from agent
        for _ in range(FIRE_SOURCES):
            while True:
                pos = _place_randomly(grid, Cell.FIRE, occupied)
                if _manhattan(agent_pos, pos) >= MIN_DISTANCE // 2:
                    occupied.add(pos)
                    break
                set_cell(grid, pos, Cell.EMPTY)  # retry

        if _is_solvable(grid):
            return grid, used_seed

        used_seed = random.randint(0, 999_999)  # regenerate with new seed
