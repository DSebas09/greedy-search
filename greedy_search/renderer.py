# renderer.py
import pygame
from greedy_search.grid import Cell, Grid, Position

# --- Constants ---
CELL_SIZE: int = 32
HUD_HEIGHT: int = 40

COLORS: dict[Cell, tuple[int, int, int]] = {
    Cell.EMPTY:    (30, 30, 30),
    Cell.WALL:     (80, 80, 80),
    Cell.FIRE:     (220, 80, 20),
    Cell.AGENT:    (50, 180, 255),
    Cell.EXIT:     (50, 220, 100),
    Cell.EXPLORED: (60, 60, 90),
}

FONT_SIZE: int = 20


def compute_window_size(grid_size: int) -> tuple[int, int]:
    """Returns (width, height) in pixels for the given grid size."""
    width = grid_size * CELL_SIZE
    height = grid_size * CELL_SIZE + HUD_HEIGHT
    return width, height


def draw_grid(surface: pygame.Surface, grid: Grid) -> None:
    """Draws every cell of the grid onto the surface."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, COLORS[cell], rect)
            pygame.draw.rect(surface, (15, 15, 15), rect, 1)  # grid line


def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    seed: int,
    turn: int,
    status: str,
) -> None:
    """Draws the HUD bar at the bottom with seed, turn count and status."""
    grid_height = (len(surface.get_size()) and surface.get_height()) - HUD_HEIGHT
    hud_rect = pygame.Rect(0, surface.get_height() - HUD_HEIGHT, surface.get_width(), HUD_HEIGHT)
    pygame.draw.rect(surface, (10, 10, 10), hud_rect)

    text = font.render(f"Seed: {seed}   Turn: {turn}   {status}", True, (200, 200, 200))
    surface.blit(text, (10, surface.get_height() - HUD_HEIGHT + 10))


def init_renderer(grid_size: int) -> tuple[pygame.Surface, pygame.font.Font]:
    """Initializes Pygame and returns (surface, font)."""
    pygame.init()
    width, height = compute_window_size(grid_size)
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Escape from Burning Building")
    font = pygame.font.SysFont("monospace", FONT_SIZE)
    return surface, font


def render_frame(
    surface: pygame.Surface,
    font: pygame.font.Font,
    grid: Grid,
    seed: int,
    turn: int,
    status: str,
) -> None:
    """Full render pass: clears screen, draws grid and HUD, flips buffer."""
    surface.fill((0, 0, 0))
    draw_grid(surface, grid)
    draw_hud(surface, font, seed, turn, status)
    pygame.display.flip()
