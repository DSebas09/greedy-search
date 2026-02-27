# renderer.py
import pygame
from greedy_search.grid import Cell, Grid

# --- Constants ---
CELL_SIZE: int = 32
HUD_HEIGHT: int = 40
FONT_SIZE: int = 20

COLORS: dict[Cell, tuple[int, int, int]] = {
    Cell.EMPTY:    (30, 30, 30),
    Cell.WALL:     (80, 80, 80),
    Cell.FIRE:     (220, 80, 20),
    Cell.AGENT:    (50, 180, 255),
    Cell.EXIT:     (50, 220, 100),
    Cell.EXPLORED: (60, 60, 90),
}

_HUD_BG   = (10, 10, 10)
_HUD_FG   = (200, 200, 200)
_GRID_LINE = (15, 15, 15)


def init_renderer(grid_size: int) -> tuple[pygame.Surface, pygame.font.Font]:
    """Initializes Pygame and returns (surface, font)."""
    pygame.init()
    size = (grid_size * CELL_SIZE, grid_size * CELL_SIZE + HUD_HEIGHT)
    surface = pygame.display.set_mode(size, pygame.DOUBLEBUF)
    pygame.display.set_caption("Escape from Burning Building")
    return surface, pygame.font.SysFont("monospace", FONT_SIZE)


def draw_grid(surface: pygame.Surface, grid: Grid) -> None:
    """Draws every cell of the grid onto the surface."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, COLORS[cell], rect)
            pygame.draw.rect(surface, _GRID_LINE, rect, 1)


def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    seed: int,
    turn: int,
    status: str,
) -> None:
    """Draws the HUD bar at the bottom with seed, turn count and status."""
    hud_y = surface.get_height() - HUD_HEIGHT
    pygame.draw.rect(surface, _HUD_BG, (0, hud_y, surface.get_width(), HUD_HEIGHT))
    text = font.render(f"Seed: {seed}   Turn: {turn}   {status}", True, _HUD_FG)
    surface.blit(text, (10, hud_y + 10))


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
