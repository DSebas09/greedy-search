from greedy_search.grid import Cell, Grid, Position, get_neighbors, get_cell, set_cell


def spread_fire(grid: Grid) -> None:
    """Expands fire by one BFS step to all 4-connected passable neighbors."""
    fire_cells: list[Position] = [
        (r, c)
        for r, row in enumerate(grid)
        for c, cell in enumerate(row)
        if cell == Cell.FIRE
    ]

    new_fire: list[Position] = [
        neighbor
        for pos in fire_cells
        for neighbor in get_neighbors(grid, pos)
        if get_cell(grid, neighbor) == Cell.EMPTY
    ]

    for pos in new_fire:
        set_cell(grid, pos, Cell.FIRE)
