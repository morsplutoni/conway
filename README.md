# Conway's Game of Life (Python)

A minimal, terminal-based implementation of Conway's Game of Life in Python. It includes:
- A core engine with wrap-around (toroidal) boundaries
- A simple CLI to run simulations in your terminal
- A few built-in patterns (random, glider, blinker)

Requirements:
- Python 3.8+

Quickstart:
- Preferred invocation: `python3 -m src.main` (ensures package-relative imports work)
- Glider demo: `python3 -m src.main --width 40 --height 20 --steps 200 --pattern glider`
- Random world: `python3 -m src.main --width 60 --height 30 --steps 500 --pattern random --density 0.25`
- Blinker: `python3 -m src.main --width 20 --height 10 --steps 100 --pattern blinker`

Controls:
- Press Ctrl-C to stop the simulation.

CLI options (common):
- `--width` and `--height`: grid size
- `--steps`: number of steps to run (default 200)
- `--interval`: seconds between frames (default 0.1)
- `--pattern`: one of `random`, `glider`, or `blinker` (default `random`)
- `--density`: for random initialization, fraction of live cells (0.0-1.0, default 0.2)

Notes:
- The grid wraps around edges (toroidal world), which keeps the simulation lively without special boundary logic.
- No external dependencies are required.
