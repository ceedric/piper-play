# Piper Play 🎭🪨

**Turn a written script into a performance with many voices, using free, open-source text-to-speech.**

You write something like this:

```
NARRATOR: The stage is dark. Somewhere, water is moving.
A: Hello? Is anyone here?
...
B: Just me. And the river.
```

And Piper Play gives you back **one audio file** where every character has their own voice, with pauses where you asked for them.

I'm Ceedric, an artist. I made this for my own performance work and I'm sharing it because the tools that helped me were shared with me first. 💛

<!-- VIDEO PLACEHOLDER: a short "hello, here's what this does" video (30-60 seconds), maybe with a clip of the finished audio. -->
> 🎥 **Video: What this is and what it sounds like** *(coming soon)*

---

## Before you start: a few honest words

- **You don't need to be "a tech person."** If you can write a script and follow a recipe, you can do this.
- **Nothing here costs money, and nothing here watches you.** Piper runs entirely on your own computer. Your words are not uploaded anywhere. No account, no subscription, no AI company reading your script.
- **You can't break your computer by following these steps.** The worst thing that usually happens is an error message, and error messages are just the computer saying "I didn't understand." We'll go through the common ones together below.
- **Go at your own pace.** Take breaks. Come back tomorrow. The steps will still be here.

### What is "open source"?

Open source means the people who made a tool let everyone see how it works, use it, change it, and share it. Piper was made by people who wanted good voices to be free for everyone. This script is open source too. If you change it to fit your work, that's not breaking the rules, that's the whole point. 🌱

---

## Two ways to use this

**🖱️ The double-click way (least typing).** Install Python once (Part 2), download this project as a ZIP and unzip it, then double-click **Make My Play**. It walks you through everything else with simple questions: it installs Piper for you, helps you download voices, asks which voice each character should have, and tells you roughly how long it will take. Jump to [The double-click way](#the-double-click-way).

**⌨️ The terminal way.** Parts 1 to 8 below walk you through doing it by typing commands. It takes a little longer to learn, and it's worth it: once the terminal stops feeling scary, a lot of other free tools open up to you. The videos are here to keep you company.

You can start with one and switch to the other any time. They make exactly the same audio.

---

## What's in this folder

| File | What it is |
|---|---|
| `Make My Play (Mac).command` | Double-click this on a Mac. |
| `Make My Play (Windows).bat` | Double-click this on Windows. |
| `make_my_play.py` | The step-by-step helper the double-click files start. |
| `piper_play.py` | The script that does the work. You'll only edit the top part, if at all. |
| `examples/my-first-play.txt` | A tiny practice script so you can test everything works. |
| `examples/from-screenplay-to-piper.md` | Fifteen short before-and-after examples from a real screenplay, showing the choices you make by hand. |
| `README.md` | This guide. |

---

## Part 1: Meeting the terminal

<!-- VIDEO PLACEHOLDER: Ceedric opening the terminal for the first time and typing one harmless command. -->
> 🎥 **Video: Opening the terminal together** *(coming soon)*

The **terminal** is a window where you type instructions to your computer instead of clicking. It looks plain and a bit old-fashioned. That's okay. It's just a text conversation with your computer.

**How to open it:**

- **Mac:** Press `Command (⌘)` + `Space`, type `Terminal`, press `Enter`.
- **Windows:** Click Start, type `PowerShell`, press `Enter`.
- **Linux:** You probably already know, but `Ctrl` + `Alt` + `T` works on most.

**Try saying hello.** Type this and press `Enter`:

```
echo hello
```

The computer says `hello` back. You just used the terminal. 🎉

**A few things that are good to know:**

- In this guide, anything in a grey box is something you can type (or copy and paste) into the terminal, then press `Enter`.
- On Mac, paste with `Command` + `V`. In Windows PowerShell, right-click to paste.
- When something is working, the terminal might show nothing for a while. That's normal. Wait until you see the blinking cursor again.
- If you ever feel stuck in the middle of something, press `Ctrl` + `C`. It means "stop" and it's always safe.

---

## Part 2: Install Python (only once)

Piper and this script are written in a language called **Python**. You need it installed once.

**Check if you already have it:**

- **Mac / Linux:** `python3 --version`
- **Windows:** `python --version`

If you see something like `Python 3.11.4`, you're set. Skip to Part 3.

If you see an error instead:

- **Mac / Windows:** Download Python from [python.org/downloads](https://www.python.org/downloads/) and install it like any other app.
  - **Windows only:** on the first screen of the installer, tick the box that says **"Add python.exe to PATH"**. This one box saves a lot of trouble.
- **Linux:** `sudo apt install python3 python3-pip`

Close the terminal and open a new one, then check the version again.

> **Windows note:** everywhere this guide says `python3` or `pip3`, type `python` or `pip` instead.

---

## Part 3: Make a home for your project

<!-- VIDEO PLACEHOLDER: Ceedric making the folder and moving into it with cd. -->
> 🎥 **Video: Making a project folder and moving into it** *(coming soon)*

Let's make a folder for your voices and scripts. Then we'll tell the terminal to "stand inside" that folder.

```
mkdir piper-play
cd piper-play
```

- `mkdir` means **make directory** (a directory is a folder).
- `cd` means **change directory**. It's like walking into a room.

From now on, every time you open a new terminal to work on your play, type `cd piper-play` first so you're in the right room.

**Now put the files in.** Download this project (green **Code** button at the top of this page, then **Download ZIP**), unzip it, and move `piper_play.py` and the `examples` folder into your new `piper-play` folder.

> 💡 **Where is that folder?** It's in your home folder. On Mac, open Finder and press `Command` + `Shift` + `H`. On Windows, it's in `C:\Users\YourName`.

---

## Part 4: Install Piper (only once)

```
pip3 install piper-tts
```

You'll see a lot of text scroll by. That's the computer downloading and setting things up. When the cursor comes back, test it:

```
piper --help
```

If you see a list of options, Piper is installed. 🎉

---

## Part 5: Download some voices

<!-- VIDEO PLACEHOLDER: Ceedric downloading voices and listening to samples. -->
> 🎥 **Video: Choosing and downloading voices** *(coming soon)*

Each voice is a small file you download once. Make sure you're inside your `piper-play` folder (`cd piper-play`), then run:

```
python3 -m piper.download_voices en_US-lessac-medium
python3 -m piper.download_voices en_US-amy-medium
python3 -m piper.download_voices en_US-ryan-medium
```

Each voice arrives as two files that belong together, like `en_US-amy-medium.onnx` and `en_US-amy-medium.onnx.json`. Leave them in this folder.

**Want to hear other voices first?** Listen to every Piper voice at the [Piper voice samples page](https://rhasspy.github.io/piper-samples/). There are voices in many languages and accents. Download any of them the same way, using its name.

---

## Part 6: Make your first performance

```
python3 piper_play.py examples/my-first-play.txt my-first-play.wav
```

You'll see each line appear as it gets spoken. At the end it says:

```
Done! Combined audio saved to: my-first-play.wav
```

Open your `piper-play` folder and double-click `my-first-play.wav`. You're listening to your first multi-voice piece. 🎭

<!-- VIDEO PLACEHOLDER: Ceedric running the script and playing the result. -->
> 🎥 **Video: Running it and hearing it for the first time** *(coming soon)*

### The double-click way

<!-- VIDEO PLACEHOLDER: Ceedric double-clicking Make My Play and answering its questions. -->
> 🎥 **Video: Making a play without typing commands** *(coming soon)*

1. Make sure Python is installed (Part 2). That's the only thing you need to do first.
2. Download this project (green **Code** button, then **Download ZIP**) and unzip it. That unzipped folder is your project folder. Keep your scripts and voices in it.
3. Double-click **Make My Play (Mac)** or **Make My Play (Windows)**.

A window opens and asks you a few questions, one at a time:

- **Which script?** Type the number next to the script you want and press `Enter`, or drag your own `.txt` file into the window.
- **Which voice for each character?** It finds every character in your script and suggests a voice for each one. Press `Enter` to keep a voice, or type the number of a different voice from the list. You never need to type character names. Two characters can share a voice. If you want more voices than you have, it can download them for you.
- **How long will it take?** It gives you a rough guess, then a better one once it has done a few lines. For example, a play with about 190 lines (around 2,000 words) took about 2.5 minutes on my laptop. You can do something else while it works.

It remembers your cast in a small file next to your script (like `my-play.cast.json`), so next time you can just press `Enter`. It never overwrites an audio file you already made. It saves a new one with `-2` on the end instead.

**The first time you double-click it, your computer may be cautious.** That's a good thing. It's protecting you from files downloaded from the internet. This is a plain text file you can open and read, and you only have to do this once:

- **Mac:** if it says it "can't be opened" or "Apple could not verify" it, click **Done**. Then open **System Settings → Privacy & Security**, scroll down, and click **Open Anyway** next to "Make My Play (Mac)". On older Macs, you can instead hold `Control`, click the file, choose **Open**, then **Open** again.
- **Mac, if it says you don't have permission:** open Terminal in this folder and run `chmod +x "Make My Play (Mac).command"`, then double-click again.
- **Windows:** if a blue box says "Windows protected your PC", click **More info**, then **Run anyway**.

---

## Part 7: Writing your own script

Use any plain text editor (TextEdit on Mac in **Format → Make Plain Text** mode, Notepad on Windows). Save it as a `.txt` file in your `piper-play` folder.

**The rules are small:**

1. **One line = one person speaking.** Write the character's name, a colon, then what they say.
   ```
   NARRATOR: The lights come up.
   A: Is anyone there?
   ```
2. **Pauses go on their own line**, by themselves:

   | Type this | You get |
   |---|---|
   | `...` | a short beat (0.3 seconds) |
   | `___` | a pause, like after a question (1 second) |
   | `SCENE BREAK` | a longer pause for a new scene (2 seconds) |

   Stack them for longer silences. Three `SCENE BREAK` lines in a row is six seconds of quiet.
3. **Blank lines are ignored**, so space things out however feels good to read.
4. **One voice at a time.** Each line plays after the one before it finishes, so voices can't overlap or speak in unison.

**Little tricks you can hear in the practice script** (`examples/my-first-play.txt`):

| In the script | What it does |
|---|---|
| `A: Hello? Is anyone here?` then `___` on the next line | A one-second pause after a question, so it has room to land |
| `B: Just me. And the river...` | `...` at the **end of a line** makes the voice trail off |
| `...` on a line by itself | A short beat of silence (that's different from `...` at the end of a sentence) |
| `A: Ohh-kayy...` | Spelled the way it should sound, stretched out and trailing off |
| `A: And bones?` | A one-word line like `Bones?` can come out clipped, so a small word in front gives it something to lean on |

For more, see [From screenplay to Piper script](examples/from-screenplay-to-piper.md).

**Starting from a screenplay you already wrote?** See [From screenplay to Piper script](examples/from-screenplay-to-piper.md). It shows fifteen short examples from a real play of what needs translating by hand: character names, stage directions, spelling for sound, using non-English voices for accents, and more.

Then run it with your file's name:

```
python3 piper_play.py my-script.txt my-script.wav
```

---

## Part 8: Choosing your cast

> 🖱️ **Using the double-click way?** You don't need to edit anything. It asks you which voice each character should have. This part is for the terminal way.

Open `piper_play.py` in your text editor. Near the top you'll see a section that looks like this:

```python
VOICES = {
    "NARRATOR": "en_US-lessac-medium",
    "A": "en_US-amy-medium",
    "B": "en_US-ryan-medium",
    ...
}
```

The name on the **left** is what you type in your script. The name on the **right** is the Piper voice. You can:

- **Rename characters:** change `"A"` to `"RAVEN"`, then write `RAVEN: ...` in your script. Use capital letters and underscores instead of spaces (`OLD_WOMAN`, not `Old Woman`).
- **Change a voice:** swap the right side for any voice you've downloaded.
- **Add a character:** copy a line, change both sides, and keep the comma at the end.

You can also change how long the pauses are in the `SILENCE_MARKERS` section just below it.

---

## When Piper says a word wrong

Piper is good, but it learned mostly from English and a few other colonial languages. It will often stumble on names, place names, and words from Indigenous languages. That's a limit of the tool, not of your words. Some tricks that help:

- **Spell it the way it sounds:** `See-drick` instead of `Cedric`.
- **Break it into syllables with hyphens:** `Ax-el`.
- **Spell out letters** for acronyms: `B. D. S.`
- **Write numbers as words:** `twenty-three` instead of `23`.
- **Add or remove a comma** right after the word to change the pacing.
- **Test one word quickly** instead of running the whole script:
  ```
  echo 'testword' | piper --model en_US-amy-medium --output_file test.wav
  ```

For words that matter deeply, consider recording a real voice for those lines and mixing it in. Some words deserve a human. 🪶

---

## If something goes wrong

Error messages look scary, but they're usually telling you something simple. Here are the common ones:

| You see | What it means | Try this |
|---|---|---|
| `command not found: python3` | Python isn't installed, or on Windows it's called `python` | See Part 2 |
| `command not found: piper` | Piper isn't installed yet | `pip3 install piper-tts`, then open a new terminal |
| `Could not find script file` | The terminal is in a different folder from your script | `cd piper-play`, and check the file name spelling |
| `Warning: 'X' is not in the VOICES list` | Your script uses a character name the script doesn't know | Add it to `VOICES` (Part 8) or fix the spelling |
| `Skipping line (no ':' found)` | A line has no `Name:` at the start | Add a name and colon, or make it a pause marker |
| `Error synthesizing line` | A voice in your cast hasn't been downloaded | Download it (Part 5) into your `piper-play` folder |

Still stuck? That's normal and okay. [Ask for help here](../../issues/new/choose). There's a short form that asks what you typed and what you saw. You'll need a free GitHub account to post. There are no silly questions here.

---

## Sharing what you make

If you make something with this, I'd love to hear it. [Share it here](../../issues/new/choose).

This project uses the [MIT License](LICENSE), which means you're free to use it, change it, share it, and teach it to others, even in paid work. The only ask is that you keep the license note with the code. Want to help make it better? See [Joining in](CONTRIBUTING.md).

## Credits and thank you

**Piper Play is a small helper that sits on top of Piper. It does not contain or change any of Piper's own code.** All of the voice magic is Piper's.

- **[Piper](https://github.com/OHF-Voice/piper1-gpl)**, the free, local text-to-speech engine, created by Michael Hansen and now looked after by the [Open Home Foundation](https://www.openhomefoundation.org/). The [original Piper repository](https://github.com/rhasspy/piper) is where it started.
- **The Piper voices**, and the people whose recorded voices made them possible. Each voice has its own license and credits, listed in its `MODEL_CARD` on [Hugging Face](https://huggingface.co/rhasspy/piper-voices). Please check them before publishing or selling work made with a voice.
- **Carmen Argote**, co-writer of *A Rock Performance*, the piece this tool was made for.
- Everyone who learned something hard and then made it easier for the next person.

---

<p align="center">
  <img src="images/qr-code.png" alt="QR code linking to this page" width="180"><br>
  <em>Scan to come back to this page.</em>
</p>
