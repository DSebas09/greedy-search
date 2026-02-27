import sys
import pygame
from greedy_search.grid import Cell, Grid, Position, set_cell, find_position, get_cell
from greedy_search.fire import spread_fire
from greedy_search.search import greedy_next_step
from greedy_search.generator import generate_level, GRID_SIZE
from greedy_search.renderer import init_renderer, render_frame


def _apply_move(grid: Grid, next_pos: Position) -> None:
    agent_pos = find_position(grid, Cell.AGENT)
    if agent_pos:
        set_cell(grid, agent_pos, Cell.EXPLORED)
    set_cell(grid, next_pos, Cell.AGENT)


def _agent_is_burning(grid: Grid) -> bool:
    pos = find_position(grid, Cell.AGENT)
    return pos is not None and get_cell(grid, pos) == Cell.FIRE


def _handle_events() -> str:
    """Returns 'restart', 'advance', or 'none'."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "restart"
            if event.key == pygame.K_RIGHT:
                return "advance"
    return "none"


def _wait_for_input(surface: pygame.Surface, font: pygame.font.Font,
                    grid: Grid, seed: int, turn: int, status: str,
                    accept: set[str]) -> str:
    """Blocks until one of the accepted actions is triggered."""
    while True:
        render_frame(surface, font, grid, seed, turn, status)
        action = _handle_events()
        if action in accept:
            return action


def run(surface: pygame.Surface, font: pygame.font.Font, seed: int | None = None) -> None:
    grid, used_seed = generate_level(seed)
    print(f"Seed: {used_seed}")

    turn: int = 0
    status: str = "Running..."

    while True:
        render_frame(surface, font, grid, used_seed, turn, status)

        if status in ("ESCAPED!", "TRAPPED"):
            _wait_for_input(surface, font, grid, used_seed, turn, status, {"restart"})
            return

        action = _handle_events()
        if action == "restart":
            return

        next_pos = greedy_next_step(grid)

        if next_pos is None:
            status = "TRAPPED"
            continue

        cell_at_next = get_cell(grid, next_pos)

        if cell_at_next == Cell.EXIT:
            _apply_move(grid, next_pos)
            status = "ESCAPED!"
            continue

        _apply_move(grid, next_pos)

        if _agent_is_burning(grid):
            status = "TRAPPED"
            continue

        spread_fire(grid)

        if _agent_is_burning(grid):
            status = "TRAPPED"
            continue

        turn += 1
        action = _wait_for_input(surface, font, grid, used_seed, turn, status, {"advance", "restart"})
        if action == "restart":
            return


if __name__ == "__main__":
    seed_arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    surface, font = init_renderer(GRID_SIZE)
    while True:
        run(surface, font, seed_arg)
        seed_arg = None
