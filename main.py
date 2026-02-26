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


def run(seed: int | None = None) -> None:
    grid, used_seed = generate_level(seed)
    surface, font = init_renderer(GRID_SIZE)
    clock = pygame.time.Clock()

    turn: int = 0
    status: str = "Running..."

    while True:
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                run()  # restart with new random level
                return

        # --- Render current state ---
        render_frame(surface, font, grid, used_seed, turn, status)

        # --- End conditions ---
        if status in ("ESCAPED!", "TRAPPED"):
            time.sleep(2)
            run()
            return

        # --- Greedy step ---
        next_pos = greedy_next_step(grid)

        if next_pos is None:
            status = "TRAPPED"
            continue

        # --- Check win before moving ---
        if get_cell(grid, next_pos) == Cell.EXIT:
            _apply_move(grid, next_pos)
            status = "ESCAPED!"
            continue

        # --- Move agent ---
        _apply_move(grid, next_pos)

        # --- Check fire collision after move ---
        agent_pos = find_position(grid, Cell.AGENT)
        if agent_pos and any(
            get_cell(grid, n) == Cell.FIRE
            for n in [agent_pos]
        ):
            status = "TRAPPED"
            continue

        # --- Spread fire ---
        spread_fire(grid)

        # --- Check if agent cell caught fire ---
        agent_pos = find_position(grid, Cell.AGENT)
        if agent_pos and get_cell(grid, agent_pos) == Cell.FIRE:
            status = "TRAPPED"
            continue

        turn += 1
        clock.tick(1 / TURN_DELAY * 60)
        time.sleep(TURN_DELAY)


if __name__ == "__main__":
    seed_arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run(seed_arg)
