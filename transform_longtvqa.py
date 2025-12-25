#!/usr/bin/env python3
"""Transform LongTVQA+ train/val JSON schema.

Changes per entry:
- Add `episode_name` extracted from the `vid_name` (e.g. "s05e02").
- Rename `vid_name` to `occur_clip`.
- Rename `answer_idx` to `answer` with the value prefixed by "a" (e.g. "a2").
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

EPISODE_PATTERN = re.compile(r"s\d{2}e\d{2}")


def extract_episode_name(vid_name: str) -> str:
    match = EPISODE_PATTERN.search(vid_name)
    if match:
        return match.group(0)
    return vid_name[:6]


def transform_entry(entry: dict[str, Any]) -> dict[str, Any]:
    if "vid_name" not in entry:
        raise KeyError("Missing vid_name in entry")
    episode_name = extract_episode_name(entry["vid_name"])

    answer_idx = entry.get("answer_idx")
    if answer_idx is None:
        raise KeyError("Missing answer_idx in entry")
    answer = f"a{answer_idx}"

    transformed = dict(entry)
    transformed["episode_name"] = episode_name
    transformed["occur_clip"] = transformed.pop("vid_name")
    transformed["answer"] = answer
    transformed.pop("answer_idx", None)
    return transformed


def transform_file(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"Expected list in {input_path}, got {type(data)!r}")

    transformed: list[dict[str, Any]] = [transform_entry(item) for item in data]

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(transformed, handle, ensure_ascii=False, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transform LongTVQA+ train/val JSON files.")
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        default=[
            Path("LongTVQA_plus_train.json"),
            Path("LongTVQA_plus_val.json"),
        ],
        help="Input JSON files to transform (defaults to train/val).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("transformed_json"),
        help="Directory to write transformed JSON files.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite input files instead of writing new ones.",
    )
    return parser.parse_args()


def iter_pairs(inputs: Iterable[Path], output_dir: Path, in_place: bool) -> Iterable[tuple[Path, Path]]:
    for input_path in inputs:
        output_path = input_path if in_place else output_dir / input_path.name
        yield input_path, output_path


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for input_path, output_path in iter_pairs(args.inputs, args.output_dir, args.in_place):
        transform_file(input_path, output_path)


if __name__ == "__main__":
    main()
