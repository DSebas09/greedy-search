# main.py
import sys
import time
import pygame
from greedy_search.grid import Cell, Grid, Position, set_cell, find_position, get_cell
from greedy_search.fire import spread_fire
from greedy_search.search import greedy_next_step
from greedy_search.generator import generate_level, GRID_SIZE
from greedy_search.renderer import init_renderer, render_frame

# --- Constants ---
TURN_DELAY: float = 0.3  # seconds between turns


def _apply_move(grid: Grid, next_pos: Position) -> None:
    """Moves agent to next_pos and marks previous cell as EXPLORED."""
    agent_pos = find_position(grid, Cell.AGENT)
    if agent_pos:
        set_cell(grid, agent_pos, Cell.EXPLORED)
    set_cell(grid, next_pos, Cell.AGENT)


def _check_status(grid: Grid, next_pos: Position | None) -> str:
    """Returns current game status string."""
    if next_pos is None:
        return "TRAPPED"
    agent_pos = find_position(grid, Cell.AGENT)
    if agent_pos is not None:
        if get_cell(grid, agent_pos) == Cell.EXIT:
            return "ESCAPED!"
    return "Running..."


def _wait_for_restart(surface: pygame.Surface, font: pygame.font.Font, grid: Grid, used_seed: int, turn: int, status: str) -> None:
    """Freezes the final frame until the player presses R."""
    while True:
        render_frame(surface, font, grid, used_seed, turn, status)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return


def _wait_for_next_turn(surface: pygame.Surface, font: pygame.font.Font, grid: Grid, used_seed: int, turn: int, status: str) -> bool:
    """Waits for arrow key. Returns False if user wants to restart."""
    while True:
        render_frame(surface, font, grid, used_seed, turn, status)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    return True   # advance one turn
                if event.key == pygame.K_r:
                    return False  # restart


def run(surface: pygame.Surface, font: pygame.font.Font, seed: int | None = None) -> None:
    grid, used_seed = generate_level(seed)
    print(f"Seed: {used_seed}")

    turn: int = 0
    status: str = "Running..."

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                run(surface, font)
                return

        render_frame(surface, font, grid, used_seed, turn, status)

        if status in ("ESCAPED!", "TRAPPED"):
            _wait_for_restart(surface, font, grid, used_seed, turn, status)
            run(surface, font)
            return

        next_pos = greedy_next_step(grid)

        if next_pos is None:
            status = "TRAPPED"
            continue

        if get_cell(grid, next_pos) == Cell.EXIT:
            _apply_move(grid, next_pos)
            status = "ESCAPED!"
            continue

        _apply_move(grid, next_pos)

        agent_pos = find_position(grid, Cell.AGENT)
        if agent_pos and get_cell(grid, agent_pos) == Cell.FIRE:
            status = "TRAPPED"
            continue

        spread_fire(grid)

        agent_pos = find_position(grid, Cell.AGENT)
        if agent_pos and get_cell(grid, agent_pos) == Cell.FIRE:
            status = "TRAPPED"
            continue

        turn += 1
        if not _wait_for_next_turn(surface, font, grid, used_seed, turn, status):
            run(surface, font)
            return


if __name__ == "__main__":
    seed_arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    surface, font = init_renderer(GRID_SIZE)
    run(surface, font, seed_arg)
