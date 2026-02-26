from enum import IntEnum
from typing import TypeAlias


class Cell(IntEnum):
    EMPTY = 0
    WALL = 1
    FIRE = 2
    AGENT = 3
    EXIT = 4
    EXPLORED = 5


# --- Type aliases ---
Position: TypeAlias = tuple[int, int]
Grid: TypeAlias = list[list[Cell]]

# --- Constants ---
PASSABLE: frozenset[Cell] = frozenset({Cell.EMPTY, Cell.AGENT, Cell.EXIT, Cell.EXPLORED})
_DIRECTIONS: tuple[Position, ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


def create_grid(size: int) -> Grid:
    return [[Cell.EMPTY] * size for _ in range(size)]


def in_bounds(grid: Grid, pos: Position) -> bool:
    r, c = pos
    n = len(grid)
    return 0 <= r < n and 0 <= c < n


def get_cell(grid: Grid, pos: Position) -> Cell:
    r, c = pos
    return grid[r][c]


def set_cell(grid: Grid, pos: Position, state: Cell) -> None:
    r, c = pos
    grid[r][c] = state


def get_neighbors(grid: Grid, pos: Position) -> list[Position]:
    r, c = pos
    return [
        (r + dr, c + dc)
        for dr, dc in _DIRECTIONS
        if in_bounds(grid, (r + dr, c + dc))
    ]


def is_passable(cell: Cell) -> bool:
    return cell in PASSABLE


def find_position(grid: Grid, target: Cell) -> Position | None:
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == target:
                return r, c
    return None
