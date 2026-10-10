"""m2b command-line entry point. Wires pipeline stages together."""

from __future__ import annotations

import argparse
import sys

from mumble_to_bars import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="m2b", description="mumble audio -> rap lyrics")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract", help="extract a vowel template from an audio file")
    extract.add_argument("audio", help="path to audio file")

    evaluate = sub.add_parser("eval", help="evaluate vowel extraction against a manifest")
    evaluate.add_argument("--manifest", default="eval/manifest.jsonl")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(f"m2b {args.command}: not implemented yet", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
