# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Minimal, terminal-based Python implementation of Conway’s Game of Life.
- No external dependencies. Code lives under src/.
- Entry point is a CLI that renders generations in the terminal and advances the world on a timer.

Common commands
- Run (preferred invocation to ensure package-relative imports work):
  - Help: `python3 -m src.main --help`
  - Glider demo: `python3 -m src.main --width 40 --height 20 --steps 200 --pattern glider`
  - Random world: `python3 -m src.main --width 60 --height 30 --steps 500 --pattern random --density 0.25`
  - Blinker: `python3 -m src.main --width 20 --height 10 --steps 100 --pattern blinker`
- Build: not applicable (no packaging/build configuration present).
- Lint: not configured in this repo.
- Tests: none present in this repo.

CLI parameters (most used)
- `--width`, `--height`: grid size (defaults 40x20)
- `--steps`: number of generations to run (default 200)
- `--interval`: seconds between frames (default 0.1)
- `--pattern`: `random` | `glider` | `blinker` (default `random`)
- `--density`: for `random`, fraction of live cells in [0.0, 1.0] (default 0.2)

High-level architecture
- Core engine (src/life.py)
  - Life: dataclass modeling the world with wrap-around (toroidal) edges.
  - State: `self.live` is a set of live cell coordinates (x, y).
  - Neighboring: uses 8 fixed offsets; coordinates wrap via `_wrap(x, y)`.
  - Initialization:
    - `randomize(density)`: fills live cells with given probability.
    - `set_pattern(name, x_offset?, y_offset?)`: seeds built-in patterns (`glider`, `blinker`) centered by default.
  - Evolution:
    - `step()`: counts neighbors around current live cells and applies Conway’s rules to produce the next generation.
  - Rendering:
    - `render(live_char="█", dead_char=" ")`: returns a string frame of the current grid.
- CLI / runtime (src/main.py)
  - Parses arguments and constructs `Life(width, height)`.
  - Initializes state from `--pattern` (or `random` with `--density`).
  - Clears the terminal between frames and prints `life.render(...)`.
  - Advances with `life.step()` and sleeps for `--interval` seconds until `--steps` are done or interrupted.

Notes for agents
- Prefer `python3 -m src.main` over executing the file path directly to keep relative imports valid.
- There are no repository-defined linters, test runners, or packaging files. If you add them in the future (e.g., pytest, ruff), document the exact commands here.

Referenced docs
- Key usage details are also summarized in README.md; this file focuses on the non-obvious parts (correct invocation and big-picture architecture).