from greedy_search.grid import Cell, Grid, Position, iter_positions, get_neighbors, set_cell


def spread_fire(grid: Grid) -> None:
    """Expands fire by one BFS step to all 4-connected passable neighbors."""
    new_fire: list[Position] = [
        neighbor
        for pos, cell in iter_positions(grid)
        if cell == Cell.FIRE
        for neighbor in get_neighbors(grid, pos)
        if grid[neighbor[0]][neighbor[1]] == Cell.EMPTY
    ]

    for pos in new_fire:
        set_cell(grid, pos, Cell.FIRE)
