# Writing narration for the Founder Voice (Holt delivery)

Read before authoring step 3. The source direction is `Holt_Voice_Direction.md` (a thoughtful
executive speaking to a small room: curiosity in the opening, sober clarity on what is unproven,
conviction in the close).

## Text rules eleven_v3 actually honours

| Want | Write | Measured |
|---|---|---|
| A phrase pause (0.25-0.45 s) | a comma | voice leaves ~0.06-0.15 s; `extend_pauses.py` opens it to 0.32 s if the scene runs fast |
| A sentence pause (0.55-0.85 s) | a full stop | ~0.13-0.9 s |
| A transition (1.0-1.3 s) | an ellipsis `...` | 1.2-1.6 s |
| Emotion | `[thoughtful]` open · `[serious]` unproven · `[confident]` close | one per scene, two in the close, four in the film |
| Never | `[pause]`, `[short pause]`, `[long pause]` | ran 1.7-1.8 s and dragged the take to 126 wpm |
| Never | SSML `<break time>` | v3 ignores it (multilingual_v2 honours it but reads flat) |

## Numbers and names

- Write numerals with their unit word ("28 volt", "minus 55 to 125 degrees"); the gate traces numerals.
- A count the source states may be a word ("four rails"). Part names as written: `SKU-3` reads correctly.
- Spoken-word pace counts an acronym as one word per letter (SKU-3 is four).

## Shape of a scene

- Open (≈25 words): the problem in the listener's world, then the tension. `[thoughtful]`.
- Beat (15-25 words): what this block does for the system, in plain verbs. Not its part list.
- Close (≈45 words): what is not yet proven, then the ask. `[serious]` ... `[confident]`.

## SKU-3 pilot, for reference (gated clean)

> [thoughtful] Avionics power starts on a 28 volt bus. One that carries 80 volt surges, and 100 volt
> spikes... Yet every rail on the board must still come up in order.

> First, the surges stop at the door. The input stage clamps them, refuses a reversed supply, and
> shuts out any bus that drifts outside its range.

> [serious] None of this is silicon yet. Every figure is a target. The surge clamp, the loop margins,
> the upset spacing. All of it must still be proven... [confident] So bring us your bus profile.
> Bring your rail list. And we will tell you exactly what SKU-3 must prove.
