# Escape from Burning Building - Greedy Search Algorithm

A visual simulation of the **Greedy Best-First Search** algorithm applied to
a dynamic pathfinding problem. An agent must escape a burning building before
the fire — which spreads every turn — cuts off all viable routes.

Built with Python and Pygame for an Artificial Intelligence course project.

---

## Demo

| State | Color |
|---|---|
| Agent | 🔵 Blue `(50, 180, 255)` |
| Exit | 🟢 Green `(50, 220, 100)` |
| Fire | 🟠 Orange `(220, 80, 20)` |
| Wall | ⬜ Gray `(80, 80, 80)` |
| Explored | 🔷 Dark Blue `(60, 60, 90)` |
| Empty | ⬛ Dark `(30, 30, 30)` |

---

## How It Works

- The **agent** uses Greedy Best-First Search, recalculating `h(n)` every turn
- The **fire** expands via BFS to all 4-connected empty neighbors each turn
- The **heuristic** is: `h(n) = Manhattan(n, EXIT) + fire_penalty(n)`
  - `fire_penalty`: adds `+50` if any neighbor of candidate `n` is on fire
- The **grid** is procedurally generated and validated for solvability before
  each run — invalid levels are automatically discarded and regenerated

---

## Project Structure

```
greedy-search/
│
├── greedy_search/
│ ├── grid.py # 2D grid matrix and cell states
│ ├── fire.py # Fire BFS propagation logic
│ ├── search.py # Greedy Best-First Search algorithm
│ ├── generator.py # Procedural generation + BFS solvability validation
│ ├── renderer.py # Pygame rendering (grid + HUD)
│ └── main.py # Main loop and module coordination
│
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (package manager)

Install uv if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
````

## Getting Started

```bash
git clone https://github.com/DSebas09/greedy-search.git
cd greedy-search
uv sync
```

### Run with random seed

```bash
python main.py 
```

### Run with a specific seed (for reproducibility):

```bash
python main.py 482910
```