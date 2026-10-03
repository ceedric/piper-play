#!/usr/bin/env python3
"""
piper_play.py

Turns a script formatted like:

    NARRATOR: The stage is dark.
    A: Who's there?
    B: Just me.
    ***
    A: ...You sure?

into one combined .wav file, using a different Piper voice for each
character name, with support for three kinds of silence.

USAGE:
    python3 piper_play.py my_script.txt output.wav

SETUP (do this once):
    pip3 install piper-tts

    Then download each voice you plan to use, for example:
    python3 -m piper.download_voices en_US-amy-medium

    Voices get saved to your current folder as pairs of files:
    en_US-amy-medium.onnx and en_US-amy-medium.onnx.json

HOW TO EDIT THE CAST:
    Change the VOICES dictionary below. The key is the name you'll
    type in your script file (all caps, no spaces, use underscores),
    and the value is the Piper voice name.

HOW TO USE SILENCE / PAUSES:
    Put one of these on its own line, by itself, wherever you want a
    pause. They don't need a character name or colon.

        ...           -> a short beat (0.3 seconds)
        ___           -> a pause after a question (1 second)
        SCENE BREAK    -> a longer pause for a new scene (2 seconds)

    You can change the exact wording or timing in the SILENCE_MARKERS
    dictionary below.

TIPS FOR WORDS PIPER MISPRONOUNCES:
    Piper doesn't have a built-in way to correct pronunciation, but a
    few tricks usually work:
      - Respell it phonetically the way it sounds, not how it's
        spelled. You're already doing this ("See-drick" for Cedric).
      - Break a tricky word into syllables with hyphens: "Ax-el" 
        instead of "Axel" if it's coming out wrong.
      - Spell out acronyms letter by letter: "B. D. S." instead of
        "BDS" if it's trying to read it as a word.
      - Spell out numbers as words if it mangles digits.
      - Try removing or adding a comma right after the word — Piper
        uses punctuation to decide pacing and emphasis, so a stray
        comma can sometimes fix a stumble.
      - Test one line at a time instead of the whole script when
        you're troubleshooting a single word, it's much faster:
          echo 'testword' | piper --model en_US-amy-medium --output_file test.wav
"""

import sys
import wave
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------
# EDIT THIS SECTION to set your cast of characters and their voices.
# The name on the left is what you type in your script file.
# The name on the right must match a voice you've downloaded.
# ---------------------------------------------------------------------
VOICES = {
    "NARRATOR": "en_US-lessac-medium",
    "A": "en_US-amy-medium",
    "B": "en_US-ryan-medium",
    "C": "en_US-kristin-medium",
    "D": "en_US-hfc_female-medium",
    # Heads up: kareem is an Arabic (Jordan) voice and davefx is a
    # Spanish (Spain) voice. Feeding them English text will make them
    # try to pronounce English words using Arabic/Spanish sound rules,
    # which usually sounds broken rather than "accented but clear."
    # Keep them if that's the effect you want; swap them out if not.
    "E": "ar_JO-kareem-medium",
    "F": "es_ES-davefx-medium",
    # A British voice, for real contrast against the American cast above.
    "G": "en_GB-jenny_dioco-medium",
}
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# EDIT THIS SECTION to change silence markers or their durations
# (in seconds).
# ---------------------------------------------------------------------
SILENCE_MARKERS = {
    "...": 0.3,          # short beat
    "___": 1.0,          # pause after a question
    "SCENE BREAK": 2.0,  # new scene
}
# ---------------------------------------------------------------------

TEMP_DIR = Path("piper_temp_lines")


def parse_script(script_path):
    """
    Read the script file and split it into a list of items, each either:
        {"type": "speech", "character": ..., "text": ...}
        {"type": "silence", "duration": ...}
    """
    items = []
    with open(script_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            raw_line = raw_line.strip()
            if not raw_line:
                continue  # skip blank lines

            # Check for a silence marker first (case-insensitive match).
            # Also normalize the fancy single-character "…" ellipsis
            # (which Mac apps often auto-correct "..." into) down to
            # three plain periods, so either typed form works the same.
            normalized_line = raw_line.replace("\u2026", "...")
            matched_silence = None
            for marker, duration in SILENCE_MARKERS.items():
                if normalized_line.upper() == marker.upper():
                    matched_silence = duration
                    break
            if matched_silence is not None:
                items.append({"type": "silence", "duration": matched_silence})
                continue

            if ":" not in raw_line:
                print(f"Skipping line (no ':' found): {raw_line}")
                continue

            character, text = raw_line.split(":", 1)
            character = character.strip().upper()
            text = text.strip()
            if not text:
                continue
            if character not in VOICES:
                print(
                    f"Warning: '{character}' is not in the VOICES list. "
                    f"Skipping line: {raw_line}"
                )
                continue
            items.append({"type": "speech", "character": character, "text": text})
    return items


def synthesize_line(character, text, index, temp_dir):
    """Call piper on one line of dialogue and return the output wav path."""
    voice = VOICES[character]
    out_path = temp_dir / f"{index:04d}_{character}.wav"

    result = subprocess.run(
        ["piper", "--model", voice, "--output_file", str(out_path)],
        input=text,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print(f"Error synthesizing line {index} ({character}): {text}")
        print(result.stderr)
        return None

    return out_path


def make_silence(duration_seconds, params, index, temp_dir):
    """Create a silent wav file matching the given params."""
    out_path = temp_dir / f"{index:04d}_silence.wav"
    num_frames = int(duration_seconds * params.framerate)
    silent_frame = b"\x00" * (params.sampwidth * params.nchannels)

    with wave.open(str(out_path), "wb") as w:
        w.setparams(params)
        w.writeframes(silent_frame * num_frames)

    return out_path


def combine_wavs(wav_paths, output_path):
    """Concatenate a list of wav files into a single wav file."""
    if not wav_paths:
        print("No audio was generated, nothing to combine.")
        return

    with wave.open(str(wav_paths[0]), "rb") as first:
        params = first.getparams()

    with wave.open(str(output_path), "wb") as out_wav:
        out_wav.setparams(params)
        for path in wav_paths:
            with wave.open(str(path), "rb") as w:
                out_wav.writeframes(w.readframes(w.getnframes()))

    print(f"\nDone! Combined audio saved to: {output_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 piper_play.py <script.txt> <output.wav>")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not script_path.exists():
        print(f"Could not find script file: {script_path}")
        sys.exit(1)

    TEMP_DIR.mkdir(exist_ok=True)

    parsed_items = parse_script(script_path)
    if not parsed_items:
        print("No valid lines found in the script. Check your formatting.")
        sys.exit(1)

    print(f"Found {len(parsed_items)} items. Generating audio...\n")

    # First pass: synthesize all speech lines, remember silence spots.
    wav_entries = []  # list of (kind, path_or_duration)
    for i, item in enumerate(parsed_items):
        if item["type"] == "speech":
            print(f"[{i+1}/{len(parsed_items)}] {item['character']}: {item['text']}")
            wav_path = synthesize_line(item["character"], item["text"], i, TEMP_DIR)
            if wav_path:
                wav_entries.append(("speech", wav_path))
        else:
            print(f"[{i+1}/{len(parsed_items)}] (silence, {item['duration']}s)")
            wav_entries.append(("silence", item["duration"]))

    # Figure out audio params (sample rate etc.) from the first real
    # speech clip, so silence clips match.
    first_speech_path = next(
        (path for kind, path in wav_entries if kind == "speech"), None
    )
    if first_speech_path is None:
        print("No speech was generated, nothing to combine.")
        sys.exit(1)

    with wave.open(str(first_speech_path), "rb") as f:
        params = f.getparams()

    # Second pass: build silence files now that we know the params.
    final_paths = []
    for i, (kind, value) in enumerate(wav_entries):
        if kind == "speech":
            final_paths.append(value)
        else:
            silence_path = make_silence(value, params, i, TEMP_DIR)
            final_paths.append(silence_path)

    combine_wavs(final_paths, output_path)


if __name__ == "__main__":
    main()
