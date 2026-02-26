# generator.py
from __future__ import annotations

import random
from collections import deque

from greedy_search.grid import (
    Cell, Grid, Position,
    create_grid, set_cell, get_cell,
    get_neighbors, is_passable, find_position,
    iter_positions,
)

# --- Constants ---
GRID_SIZE: int = 20
WALL_DENSITY: float = 0.25
FIRE_SOURCES: int = 3
MIN_DISTANCE: int = 8


def _manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _empty_positions(grid: Grid) -> list[Position]:
    return [pos for pos, cell in iter_positions(grid) if cell == Cell.EMPTY]


def _place_far_from(
    grid: Grid,
    state: Cell,
    origin: Position,
    min_dist: int,
    exclude: set[Position],
) -> Position | None:
    candidates = [
        pos for pos in _empty_positions(grid)
        if pos not in exclude and _manhattan(origin, pos) >= min_dist
    ]
    if not candidates:
        return None
    pos = random.choice(candidates)
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


def _try_build_level(rng_seed: int) -> Grid | None:
    random.seed(rng_seed)
    grid = create_grid(GRID_SIZE)

    for pos, _ in iter_positions(grid):
        if random.random() < WALL_DENSITY:
            set_cell(grid, pos, Cell.WALL)

    occupied: set[Position] = set()

    agent_pos = _place_far_from(grid, Cell.AGENT, (0, 0), 0, occupied)
    if agent_pos is None:
        return None
    occupied.add(agent_pos)

    exit_pos = _place_far_from(grid, Cell.EXIT, agent_pos, MIN_DISTANCE, occupied)
    if exit_pos is None:
        return None
    occupied.add(exit_pos)

    for _ in range(FIRE_SOURCES):
        fire_pos = _place_far_from(grid, Cell.FIRE, agent_pos, MIN_DISTANCE // 2, occupied)
        if fire_pos is None:
            return None
        occupied.add(fire_pos)

    return grid


def generate_level(seed: int | None = None) -> tuple[Grid, int]:
    """Generates and validates a level. Returns (grid, seed)."""
    current_seed = seed if seed is not None else random.randint(0, 999_999)

    while True:
        grid = _try_build_level(current_seed)
        if grid is not None and _is_solvable(grid):
            return grid, current_seed
        current_seed = random.randint(0, 999_999)
