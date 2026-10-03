#!/usr/bin/env python3
"""
make_my_play.py

A friendly, step-by-step helper for piper_play.py. You don't need to
type any commands: double-click "Make My Play (Mac).command" or
"Make My Play (Windows).bat" and this program will:

    1. Check that Piper is installed (and offer to install it).
    2. Let you pick your script.
    3. Find every character in it and help you choose a voice for each
       one (characters can share a voice, and you can download more).
    4. Remember your cast for next time.
    5. Tell you roughly how long it will take, then make the .wav file.

It uses the same script format and pause markers as piper_play.py,
so everything in the README still applies.
"""

import json
import os
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.chdir(HERE)  # voices, scripts and audio all live in this folder

import piper_play  # noqa: E402  (uses the same parsing and pause rules)

TEMP_DIR = HERE / "piper_temp_lines"

# Average speed, measured on Ceedric's own play: 188 lines took about
# 2.5 minutes, so roughly 0.8 seconds per line. Most of that time is
# Piper starting up for each line, so the number of lines matters more
# than how long each line is.
SECONDS_PER_LINE = 150 / 188

# A few voices to suggest when someone wants more. Any voice name from
# https://rhasspy.github.io/piper-samples/ also works.
SUGGESTED_VOICES = [
    ("en_US-lessac-medium", "English (US), calm, clear"),
    ("en_US-amy-medium", "English (US), bright"),
    ("en_US-ryan-medium", "English (US), deeper"),
    ("en_US-kristin-medium", "English (US), warm"),
    ("en_US-hfc_female-medium", "English (US)"),
    ("en_US-hfc_male-medium", "English (US)"),
    ("en_US-joe-medium", "English (US)"),
    ("en_GB-jenny_dioco-medium", "English (UK)"),
    ("en_GB-alan-medium", "English (UK)"),
    ("en_GB-southern_english_female-low", "English (UK, southern)"),
    ("es_MX-claude-high", "Spanish (Mexico)"),
    ("es_ES-davefx-medium", "Spanish (Spain)"),
    ("fr_FR-siwis-medium", "French"),
    ("ar_JO-kareem-medium", "Arabic (Jordan)"),
]


# ---------------------------------------------------------------------
# Small helpers for talking with the person
# ---------------------------------------------------------------------

def say(text=""):
    print(text, flush=True)


def heading(text):
    say()
    say("-" * 60)
    say(text)
    say("-" * 60)


def about(seconds):
    return f"about {friendly_time(seconds)}"


def ask(prompt, default=None):
    """Ask a question, then wait for an answer on the "> " line.
    Pressing Enter on its own gives the default, if there is one."""
    if prompt:
        say(prompt)
    try:
        answer = input("> ").strip()
    except EOFError:
        answer = ""
    return answer or (default or "")


def ask_yes_no(prompt, default=True):
    enter_means = "yes" if default else "no"
    while True:
        answer = ask(f"{prompt}\n(Type y for yes or n for no, then press Enter."
                     f" Pressing Enter on its own means {enter_means}.)").lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        say("  Please type y for yes or n for no.")


def ask_number(prompt, low, high, default=None):
    while True:
        answer = ask(prompt, str(default) if default else None)
        if answer.isdigit() and low <= int(answer) <= high:
            return int(answer)
        say(f"  Please type one of the numbers from the list ({low} to {high}).")


def friendly_time(seconds):
    seconds = max(0, int(round(seconds)))
    if seconds <= 1:
        return "1 second"
    if seconds < 60:
        return f"{seconds} seconds"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        word = "minute" if minutes == 1 else "minutes"
        return f"{minutes} {word} {secs} seconds" if secs else f"{minutes} {word}"
    hours, minutes = divmod(minutes, 60)
    return f"{hours} hours {minutes} minutes"


# ---------------------------------------------------------------------
# Step 1: is Piper installed?
# ---------------------------------------------------------------------

def check_piper():
    try:
        import piper  # noqa: F401
        return True
    except ImportError:
        pass

    heading("Piper isn't installed yet")
    say("Piper is the free voice engine this uses. It runs on your")
    say("computer and doesn't send your words anywhere.")
    if not ask_yes_no("Install it now?"):
        say("Okay. You can install it later. See Part 4 of the README.")
        return False

    say("\nInstalling... lots of text may scroll by. That's normal.\n")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "piper-tts"]
    )
    if result.returncode != 0:
        say("\nThe install didn't finish. See Part 4 of the README,")
        say("or ask for help on the project page. You didn't break anything.")
        return False
    say("\nPiper is installed.")
    return True


# ---------------------------------------------------------------------
# Step 2: pick a script
# ---------------------------------------------------------------------

NOT_SCRIPTS = {"requirements.txt", "license.txt"}


def find_scripts():
    found = []
    for folder in (HERE, HERE / "examples", HERE / "scripts"):
        if folder.is_dir():
            for path in sorted(folder.glob("*.txt")):
                if path.name.lower() not in NOT_SCRIPTS:
                    found.append(path)
    return found


def clean_dragged_path(text):
    """A file dragged into the window can arrive with quotes or
    backslashes around spaces. Tidy that up."""
    text = text.strip().strip("'\"")
    if os.name != "nt":
        text = text.replace("\\ ", " ")
    return Path(text).expanduser()


def pick_script():
    heading("Step 1 of 3: Choose your script")
    scripts = find_scripts()
    if scripts:
        say("I found these scripts in your folder:\n")
        for i, path in enumerate(scripts, 1):
            try:
                n = len(find_characters(path))
                voices = f"   ({n} character{'' if n == 1 else 's'})"
            except (OSError, UnicodeDecodeError):
                voices = ""
            say(f"  {i}. {path.relative_to(HERE)}{voices}")
        say("\nTo choose a script, type the number next to it, then press Enter.")
        say("(Or drag a different .txt file into this window, then press Enter.)")
    else:
        say("I didn't find any .txt scripts in this folder.")
        say("Drag your script file into this window and press Enter.")

    while True:
        answer = ask("")
        if answer.isdigit() and scripts and 1 <= int(answer) <= len(scripts):
            return scripts[int(answer) - 1]
        if answer:
            path = clean_dragged_path(answer)
            if path.is_file():
                return path
            say(f"  I couldn't find a file at: {path}")
        else:
            say("  Please type the number next to your script, then press Enter.")


# ---------------------------------------------------------------------
# Step 3: characters and cast
# ---------------------------------------------------------------------

def find_characters(script_path):
    """Return {NAME: number_of_lines} in the order names first appear,
    using the same rules as piper_play.py."""
    markers = {m.upper() for m in piper_play.SILENCE_MARKERS}
    counts = {}
    with open(script_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip().replace("…", "...")
            if not line or line.upper() in markers or ":" not in line:
                continue
            name, text = line.split(":", 1)
            name = name.strip().upper()
            if name and text.strip():
                counts[name] = counts.get(name, 0) + 1
    return counts


def downloaded_voices():
    return sorted(p.stem for p in HERE.glob("*.onnx")
                  if (HERE / f"{p.name}.json").exists())


def download_voice(name):
    say(f"\nDownloading {name}...")
    result = subprocess.run(
        [sys.executable, "-m", "piper.download_voices", name], cwd=HERE
    )
    if result.returncode == 0 and (HERE / f"{name}.onnx").exists():
        say(f"Got it: {name}")
        return True
    say(f"I couldn't download '{name}'. Check the spelling against the")
    say("voice samples page, and check your internet connection.")
    return False


def offer_downloads(have):
    """Let the person download more voices. Returns the updated list."""
    while True:
        heading("Download more voices")
        say("Listen to every voice first at:")
        say("  https://rhasspy.github.io/piper-samples/\n")
        for i, (name, about) in enumerate(SUGGESTED_VOICES, 1):
            mark = " (already have it)" if name in have else ""
            say(f"  {i:2}. {name:36} {about}{mark}")
        say("\nTo download a voice, type the number next to it, then press Enter.")
        say("(You can also type the full name of any voice from the samples page.)")
        say("When you have all the voices you want, just press Enter.")
        answer = ask("")
        if not answer:
            return downloaded_voices()
        if answer.isdigit() and 1 <= int(answer) <= len(SUGGESTED_VOICES):
            answer = SUGGESTED_VOICES[int(answer) - 1][0]
        download_voice(answer)
        have = downloaded_voices()


def cast_file_for(script_path):
    return script_path.with_suffix(".cast.json")


def load_saved_cast(script_path):
    path = cast_file_for(script_path)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
    return None


def save_cast(script_path, cast):
    path = cast_file_for(script_path)
    try:
        path.write_text(json.dumps(cast, indent=2), encoding="utf-8")
        say(f"\nI saved this cast in {path.name}, so next time you can reuse it.")
    except OSError:
        pass


def show_cast(cast, counts):
    for name, voice in cast.items():
        lines = counts.get(name, 0)
        say(f"  {name:16} -> {voice}   ({lines} lines)")


def choose_cast(script_path, counts):
    heading("Step 2 of 3: Choose a voice for each character")

    names = list(counts)
    say(f"Your script has {len(names)} character"
        f"{'' if len(names) == 1 else 's'}:\n")
    for name in names:
        say(f"  {name:16} {counts[name]} lines")

    have = downloaded_voices()
    saved = load_saved_cast(script_path)
    if saved and all(saved.get(n) in have for n in names):
        say("\nLast time you used this cast:\n")
        show_cast({n: saved[n] for n in names}, counts)
        if ask_yes_no("\nUse the same cast again?"):
            return {n: saved[n] for n in names}

    say(f"\nYou have {len(have)} voice{'' if len(have) == 1 else 's'} downloaded.")
    if len(have) < len(names):
        say("Characters can share a voice, or you can download more so")
        say("everyone sounds different.")
    if not have or ask_yes_no("Download more voices first?", default=not have):
        have = offer_downloads(have)
    if not have:
        say("\nYou'll need at least one voice. See Part 5 of the README.")
        return None

    # Suggest a starting voice for each character: whatever piper_play.py
    # already says, otherwise spread the downloaded voices around.
    cast = {}
    for i, name in enumerate(names):
        suggested = piper_play.VOICES.get(name)
        if suggested not in have:
            suggested = have[i % len(have)]
        cast[name] = suggested

    while True:
        say("\nYour voices:\n")
        for i, voice in enumerate(have, 1):
            say(f"  {i}. {voice}")
        say("\nNow I'll go through your characters one at a time and show the")
        say("voice I picked for each one. You don't need to type any names.")
        say("  - To keep the voice, just press Enter.")
        say("  - To change it, type the number of a different voice from the")
        say("    list above, then press Enter.")
        say("Two characters can share the same voice.")
        for name in names:
            default = have.index(cast[name]) + 1
            say(f"\n{name} ({counts[name]} lines) will use voice "
                f"{default}: {cast[name]}")
            pick = ask_number("Press Enter to keep it, or type a different "
                              "voice number:", 1, len(have), default)
            cast[name] = have[pick - 1]

        say("\nYour cast:\n")
        show_cast(cast, counts)
        if ask_yes_no("\nHappy with this cast?"):
            save_cast(script_path, cast)
            return cast


# ---------------------------------------------------------------------
# Step 4: make the audio, with a time estimate
# ---------------------------------------------------------------------

def output_path_for(script_path):
    out = script_path.with_suffix(".wav")
    n = 2
    while out.exists():
        out = script_path.with_name(f"{script_path.stem}-{n}.wav")
        n += 1
    return out


def synthesize(voice, text, out_path):
    # Runs Piper through Python itself, so it works even when the
    # "piper" command isn't on this computer's PATH.
    result = subprocess.run(
        [sys.executable, "-m", "piper", "--model", voice,
         "--output_file", str(out_path)],
        input=text, text=True, encoding="utf-8", capture_output=True,
        cwd=HERE,
    )
    if result.returncode != 0:
        say(f"    Piper had trouble with this line:\n{result.stderr.strip()}")
        return False
    return True


def make_audio(script_path, cast):
    heading("Step 3 of 3: Making your audio")
    piper_play.VOICES = dict(cast)
    items = piper_play.parse_script(script_path)
    speech = [it for it in items if it["type"] == "speech"]
    if not speech:
        say("I couldn't find any lines to speak. Check that lines look like")
        say("  NAME: what they say")
        return None

    guess = len(speech) * SECONDS_PER_LINE
    out_path = output_path_for(script_path)
    say(f"Your script has {len(speech)} lines to speak.")
    say(f"Each line takes about {SECONDS_PER_LINE:.1f} seconds on average, so this")
    say(f"should take {about(guess)}. (Slower computers take longer, and I'll")
    say("update the estimate as I go.)")
    say(f"The audio will be saved as: {out_path.name}")
    say("You can leave this window open and do something else.")
    say("To stop at any time, press Ctrl + C.\n")
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir()

    start = time.monotonic()
    done_lines = 0
    entries = []  # ("speech", path) or ("silence", seconds)
    for i, item in enumerate(items):
        if item["type"] == "silence":
            entries.append(("silence", item["duration"]))
            continue

        # After a few lines, use this computer's own average speed.
        per_line = SECONDS_PER_LINE
        if done_lines >= 3:
            per_line = (time.monotonic() - start) / done_lines
        when = f"{about((len(speech) - done_lines) * per_line)} left"

        preview = item["text"] if len(item["text"]) <= 50 else item["text"][:47] + "..."
        say(f"[{done_lines + 1}/{len(speech)}] {when}  |  "
            f"{item['character']}: {preview}")

        path = TEMP_DIR / f"{i:04d}_{item['character']}.wav"
        if synthesize(cast[item["character"]], item["text"], path):
            entries.append(("speech", path))
        done_lines += 1

    first = next((p for kind, p in entries if kind == "speech"), None)
    if first is None:
        say("\nNo audio was made. Scroll up to see what Piper said.")
        return None
    with wave.open(str(first), "rb") as f:
        params = f.getparams()

    paths = []
    for i, (kind, value) in enumerate(entries):
        if kind == "speech":
            paths.append(value)
        else:
            paths.append(piper_play.make_silence(value, params, i, TEMP_DIR))

    piper_play.combine_wavs(paths, out_path)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    say(f"That took {friendly_time(time.monotonic() - start)}.")
    return out_path


def open_file(path):
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(path)])
        elif os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(path)])
    except OSError:
        say(f"Your file is here: {path}")


# ---------------------------------------------------------------------

def main():
    say("=" * 60)
    say("  Make My Play")
    say("  Turn your script into a multi-voice audio performance.")
    say("=" * 60)

    if not check_piper():
        return

    script_path = pick_script()
    counts = find_characters(script_path)
    if not counts:
        say("\nI couldn't find any characters. Each spoken line should look")
        say("like:   NAME: what they say")
        return

    cast = choose_cast(script_path, counts)
    if not cast:
        return

    out_path = make_audio(script_path, cast)
    if out_path and ask_yes_no("\nPlay it now?"):
        open_file(out_path)
    say("\nSee notes for more advanced tips and tricks:")
    say("  examples/from-screenplay-to-piper.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        say("\n\nStopped. Nothing is broken; you can run it again any time.")
