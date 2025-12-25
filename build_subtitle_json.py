#!/usr/bin/env python3
"""Build derived subtitle JSON files from LongTVQA_plus_subtitles.json.

Outputs:
1) Clip-level subtitles: {"s09e14_seg02_clip_04": "...sub_text..."}
2) Episode-level subtitles: {"s09e14": "<seg01_clip_01>...</seg01_clip_01>..."}
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

CLIP_PATTERN = re.compile(
    r"^(?P<episode>s\d{2}e\d{2})_seg(?P<segment>\d{2})_clip_(?P<clip>\d{2})$"
)


@dataclass(frozen=True)
class ClipKey:
    episode: str
    segment: int
    clip: int


def parse_clip_name(clip_name: str) -> ClipKey:
    match = CLIP_PATTERN.match(clip_name)
    if not match:
        raise ValueError(f"Unexpected clip name format: {clip_name}")
    return ClipKey(
        episode=match.group("episode"),
        segment=int(match.group("segment")),
        clip=int(match.group("clip")),
    )


def build_clip_level(subtitles: Dict[str, dict]) -> Dict[str, str]:
    return {clip_name: payload.get("sub_text", "") for clip_name, payload in subtitles.items()}


def build_episode_level(subtitles: Dict[str, dict]) -> Dict[str, str]:
    grouped: Dict[str, list[Tuple[ClipKey, str]]] = {}
    for clip_name, payload in subtitles.items():
        clip_key = parse_clip_name(clip_name)
        grouped.setdefault(clip_key.episode, []).append((clip_key, payload.get("sub_text", "")))

    episode_level: Dict[str, str] = {}
    for episode, entries in grouped.items():
        entries.sort(key=lambda item: (item[0].segment, item[0].clip))
        parts = [
            f"<seg{clip_key.segment:02d}_clip_{clip_key.clip:02d}>{text}</seg{clip_key.segment:02d}_clip_{clip_key.clip:02d}>"
            for clip_key, text in entries
        ]
        episode_level[episode] = "".join(parts)

    return episode_level


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build clip/episode subtitle JSON outputs.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("LongTVQA_plus_subtitles.json"),
        help="Path to the subtitles JSON file.",
    )
    parser.add_argument(
        "--clip-output",
        type=Path,
        default=Path("subtitle_clip_level.json"),
        help="Output path for clip-level subtitles.",
    )
    parser.add_argument(
        "--episode-output",
        type=Path,
        default=Path("subtitle_episode_level.json"),
        help="Output path for episode-level subtitles.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with args.input.open("r", encoding="utf-8") as handle:
        subtitles = json.load(handle)

    if not isinstance(subtitles, dict):
        raise ValueError("Expected subtitles JSON to be a dictionary keyed by clip name.")

    clip_level = build_clip_level(subtitles)
    episode_level = build_episode_level(subtitles)

    with args.clip_output.open("w", encoding="utf-8") as handle:
        json.dump(clip_level, handle, ensure_ascii=False, indent=2)

    with args.episode_output.open("w", encoding="utf-8") as handle:
        json.dump(episode_level, handle, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
