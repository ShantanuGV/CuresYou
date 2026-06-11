#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from river_engine.layout import set_layout_seed
from river_engine.pipeline import RiverWordPipeline


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate continuous satellite river typography from a word.",
    )
    parser.add_argument(
        "word",
        nargs="?",
        default=None,
        help="Word or name to render (optional; prompts if omitted)",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Output scale multiplier (default: 1.0)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Overlay river/letter points, entry/exit, and bridges",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for overlap/underlap layout (default: different each run)",
    )
    return parser.parse_args(argv)


def read_name(args: argparse.Namespace) -> str:
    if args.word:
        return args.word.strip()
    name = input("Enter the name: ").strip()
    return name


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    word = read_name(args)
    if not word:
        print("Error: name cannot be empty.", file=sys.stderr)
        return 1

    set_layout_seed(args.seed)
    pipeline = RiverWordPipeline(output_scale=args.scale, debug=args.debug)
    try:
        out_path = pipeline.generate(word)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {out_path}")
    print("Wrote output.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
