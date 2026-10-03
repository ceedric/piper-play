# From screenplay to Piper script: what you have to translate by hand

A screenplay is written for **people** to read. Piper is a voice that will say **exactly** what's on the page, out loud, in order. So when you turn a screenplay into a Piper script, you have to make some choices by hand. The script can't make them for you. They're creative choices too, and that's the fun part.

The fifteen examples below are short excerpts from *A Rock Performance* by Carmen Argote & Cedric Tai. Each one shows the **screenplay** (what a person reads) next to the **Piper script** (what the computer reads).

---

## 1. One character, many names, one voice

The script only knows the name in front of the colon. It has no idea that "the wife" and "Carmen" are the same person. You make that connection. In this play, Carmen is first a wife opening the door, then later goes by her name. She's **always voice A**.

| Screenplay | Piper script |
|---|---|
| <pre>CARMEN<br>Honey! The guests are here!<br>A husband and wife open the door…</pre> | <pre>A: Honey! The guests are here!</pre> |

> 💡 **Tip:** before you start, make a little cast list on paper: *Carmen = A, Cedric = B*, and so on. Then you never have to wonder which letter someone was.

## 2. The name goes on the same line as the words

| Screenplay | Piper script |
|---|---|
| <pre>CEDRIC<br>What?</pre> | <pre>B: What?</pre> |

If you forget, the script tells you: `Skipping line (no ':' found)`.

## 3. A stage direction, said out loud

Piper can't act, so for every stage direction you decide: say it, turn it into silence, or cut it. This one is said by the narrator.

| Screenplay | Piper script |
|---|---|
| <pre>CARMEN<br>From there.<br>(Points at the ground right where they are)</pre> | <pre>A: From there.<br>NARRATOR: Points at ground right where they are</pre> |

## 4. A stage direction, turned into silence (or cut)

| Screenplay | Piper script |
|---|---|
| <pre>(…nothing happens for three beats)</pre> | <pre>&#95;&#95;&#95;<br>&#95;&#95;&#95;<br>&#95;&#95;&#95;</pre> |

Three one-second pauses, stacked. Directions that only work for the eyes, like someone making coffee in the background, can simply be left out.

## 5. Give questions room to land

On stage, an actor pauses after a big question. Piper goes straight to the next line unless you tell it not to. A `___` on its own line after a question adds a one-second pause.

| Screenplay | Piper script |
|---|---|
| <pre>CEDRIC<br>Are rocks alive?<br>(Rubs their stomach)<br>We have gut bacteria…</pre> | <pre>B: Are rocks alive?<br>&#95;&#95;&#95;<br>B: We have gut bacteria…</pre> |

## 6. Timing with `...`

A list of words on one line comes out rushed. Putting each one on its own line, with a short `...` beat between them, lets each word settle.

| Screenplay | Piper script |
|---|---|
| <pre>CARMEN<br>Sedimentary… Grounding… Land spirits…</pre> | <pre>A: Sedimentary.<br>...<br>A: Grounding…<br>...<br>A: Land spirits…</pre> |

## 7. Very short lines need a little company

A line that's only one word can come out clipped, as if the voice was cut off. Adding a small word in front, or trailing punctuation, gives Piper enough to work with. The words don't match the screenplay exactly, and that's on purpose.

| Screenplay | Piper script |
|---|---|
| <pre>CARMEN<br>like teeth<br>CEDRIC<br>Bones?</pre> | <pre>A: Like teeth…<br>B: And Bones?</pre> |

## 8. A scene heading becomes a pause and a narrator line

`INT.`, `EXT.`, `CUT TO:` and `FADE OUT.` are instructions for a camera. In audio they become pauses, plus a narrator line if the listener needs to know where they are.

| Screenplay | Piper script |
|---|---|
| <pre>CUT TO:<br>EXT. ON A ROCK WALK</pre> | <pre>SCENE BREAK<br>NARRATOR: On a Rock walk<br>SCENE BREAK</pre> |

## 9. Spell it the way it should *sound*

The screenplay is spelled correctly. The Piper script is spelled for the ear. These look like typos, but each one is on purpose.

| Screenplay | Piper script | Why |
|---|---|---|
| 2,000 years | Two thousand years | numbers are safer as words |
| soil | soyyl | Piper said it too short |
| Cedric | See-drick | names are often mispronounced |
| Bourgeois | Bor-joh | French name, English voice |

> 🪶 For words in Indigenous languages, respelling may never feel right, and that's worth honouring. Some words deserve a human voice. You can record those lines yourself and mix them in later.

## 10. Only one voice at a time

**This way of making a script can't overlap voices.** Every line plays after the one before it finishes. Nobody can interrupt, talk over someone, or speak in unison. When the screenplay has characters speaking together, you choose who says each part, in order.

| Screenplay | Piper script |
|---|---|
| <pre>CEDRIC & CARMEN<br>You never—<br>See?<br>I do! I am!</pre> | <pre>B: You never<br>A: See?<br>B: I do! I yam!</pre> |

If overlap really matters to your piece, you can make separate audio files for each voice and layer them in a free audio editor like [Audacity](https://www.audacityteam.org/).

## 11. A non-English voice can give a character an "accent"

Piper has voices in many languages. If you give a character a non-English voice and feed it English words, it reads them using its own language's sound rules. That can give a character a distinct accent. In this play, THE ARTIST uses an Arabic (Jordan) voice:

```python
VOICES = {
    ...
    "E": "ar_JO-kareem-medium",   # THE ARTIST
}
```

Be warned: this can also come out garbled rather than "accented but clear." Test a few lines first. The next two examples show how much respelling it can still take.

## 12. Accent voices still need phonetic spelling

The Arabic voice didn't know how to say many English words. Spelling them the way they should sound fixed that.

| Screenplay | Piper script |
|---|---|
| <pre>THE ARTIST<br>The elements are all here, but it needs<br>the fire to begin.</pre> | <pre>E: The elements are alll hearr, but it needs<br>   the fyyre to begin.</pre> |

## 13. Stretch vowels by doubling letters

Doubled or tripled letters made the voice hold a sound longer, so short words didn't get swallowed.

| Screenplay | Piper script |
|---|---|
| <pre>THE ARTIST<br>Only in art can you feed the non-human…</pre> | <pre>E: Only in ahrrt can you feeed the nahn-human.</pre> |
| harmony | harmon-ee |
| figures | fig-yers |

## 14. Two characters can say the same word differently

Respelling isn't only about fixing mistakes. Here, Cedric says a Spanish word the English way, and Carmen corrects him. The two spellings make that difference audible.

| Screenplay | Piper script |
|---|---|
| <pre>CEDRIC<br>Where is this… Canyon-ito?<br>CARMEN<br>Cañoncito. In Spanish, "cito" is used to<br>make something diminutive.</pre> | <pre>B: Where is this… Can-yon-ito?<br>A: Can-yon-see-toh, in Spanish, cito is used<br>   to make something diminutive.</pre> |

## 15. Hyphens hold words together

Hyphens tell Piper to treat a few words as one unit, or split a word where you want the stress to fall.

| Screenplay | Piper script | Why |
|---|---|---|
| Lord of the Rings | lord-of-the-rings | said as one title, not three separate words |
| Colonialism | Co-lonialism | puts the stress where it belongs |

---

## A checklist for your own script

Before you run `piper_play.py` on something you've written:

- [ ] Every character has **one** letter or name, used the same way every time.
- [ ] Every name in your script is in the `VOICES` list in `piper_play.py`.
- [ ] Every speaking line looks like `NAME: words`.
- [ ] You've decided, for each stage direction: say it, make it silence, or cut it.
- [ ] Big questions have a `___` after them.
- [ ] Scene changes are `SCENE BREAK` (or a short NARRATOR line).
- [ ] Long speeches are broken into a few lines, so the voice has places to breathe.
- [ ] One-word lines have a little word or punctuation to lean on.
- [ ] If you used a non-English voice for an accent, you listened for words it couldn't say and respelled them.
- [ ] Names, numbers and non-English words are spelled the way they should sound.
- [ ] You listened once and fixed the words that came out wrong. (Everyone does this. It's part of the process.)
