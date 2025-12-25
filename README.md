# LongTVQA+ Dataset

This repository contains the **LongTVQA+** dataset in JSON format. LongTVQA+ differs from the original TVQA dataset in three ways:

1. The questions in TVQA+ are a subset of TVQA (The Big Bang Theory).
2. TVQA+ provides frame-level bounding box annotations for visual concept words in questions and correct answers.
3. TVQA+ has refined timestamp annotations.

Please refer to the TVQA+ paper for more details.

## Files

- `LongTVQA_plus_train.json` — training split (23,545 QA samples)
- `LongTVQA_plus_val.json` — validation split (3,017 QA samples)
- `LongTVQA_plus_subtitle_clip_level.json` — clip-level subtitles indexed by video clip (4,198 clips)
- `LongTVQA_plus_subtitle_episode_level.json` — episode-level subtitles indexed by episode (220 episodes)

## QA JSON format

Each entry in `LongTVQA_plus_train.json` and `LongTVQA_plus_val.json` is a dictionary with the following fields:

| Key | Type | Description |
| --- | --- | --- |
| `qid` | int | Question ID (same as in TVQA). |
| `q` | str | Question text. |
| `a0` ... `a4` | str | Five multiple-choice answers. |
| `answer` | str | Correct answer key (`"a0"`-`"a4"`). |
| `ts` | list | Refined timestamp annotation, e.g. `[0, 5.4]` indicates the localized span starts at 0s and ends at 5.4s. |
| `episode_name` | str | Episode ID (e.g. `s01e02`). |
| `occur_clip` | str | Video clip name. Format: `{show_name_abbr}_s{season}e{episode}_seg{segment}_clip_{clip}`; e.g. `friends_s06e12_seg02_clip_16`. Episodes typically have two segments split by the opening song. Clips for **The Big Bang Theory** omit `{show_name_abbr}` (e.g. `s05e02_seg02_clip_00`). |
| `bbox` | dict | Bounding boxes for annotated frames (3 FPS). Keys are frame numbers. Values are lists of boxes with `img_id`, `top`, `left`, `width`, `height`, and `label`. |

### QA sample

```json
{
  "answer": "a1",
  "qid": 134094,
  "ts": [5.99, 11.98],
  "a1": "Howard is talking to Raj and Leonard",
  "a0": "Howard is talking to Bernadette",
  "a3": "Howard is talking to Leonard and Penny",
  "a2": "Howard is talking to Sheldon , and Raj",
  "q": "Who is Howard talking to when he is in the lab room ?",
  "episode_name": "s05e02",
  "occur_clip": "s05e02_seg02_clip_00",
  "a4": "Howard is talking to Penny and Bernadette",
  "bbox": {
    "14": [
      {
        "img_id": 14,
        "top": 153,
        "label": "Howard",
        "width": 180,
        "height": 207,
        "left": 339
      },
      {
        "img_id": 14,
        "top": 6,
        "label": "lab",
        "width": 637,
        "height": 354,
        "left": 3
      }
    ],
    "20": [],
    "26": [],
    "32": [],
    "38": []
  }
}
```

## Subtitles JSON format

Two subtitle files are provided for different use cases:

| File | Key | Value | Description |
| --- | --- | --- | --- |
| `LongTVQA_plus_subtitle_clip_level.json` | `vid_name` | str | Clip-level subtitle text with utterances separated by `<eos>`. |
| `LongTVQA_plus_subtitle_episode_level.json` | `episode_name` | str | Episode-level subtitle text with clip markers like `<seg01_clip_00>` and utterances separated by `<eos>`. |

### Subtitles sample

```json
{
  "s09e14_seg02_clip_04": "Sheldon : That  's a risk I  'm willing to take ! <eos> Amy : Well , this is so nice . <eos> ..."
}
```
