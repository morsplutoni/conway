import argparse
import sys
import time
from typing import Optional

from .life import Life


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Conway's Game of Life (terminal)")
    p.add_argument("--width", type=int, default=40, help="grid width (default: 40)")
    p.add_argument("--height", type=int, default=20, help="grid height (default: 20)")
    p.add_argument("--steps", type=int, default=200, help="number of steps to run (default: 200)")
    p.add_argument("--interval", type=float, default=0.1, help="seconds between frames (default: 0.1)")
    p.add_argument(
        "--pattern",
        type=str,
        default="random",
        choices=["random", "glider", "blinker"],
        help="initial pattern (default: random)",
    )
    p.add_argument("--density", type=float, default=0.2, help="random fill density (0.0-1.0, default: 0.2)")
    return p.parse_args(argv)


def clear_screen() -> None:
    # ANSI clear + home
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    life = Life(width=args.width, height=args.height)

    if args.pattern == "random":
        life.randomize(density=args.density)
    else:
        life.set_pattern(args.pattern)

    try:
        for _ in range(max(0, args.steps)):
            clear_screen()
            print(life.render(live_char="█", dead_char="."))
            life.step()
            time.sleep(max(0.0, args.interval))
    except KeyboardInterrupt:
        # Gracefully exit on Ctrl-C
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
