"""Shared text helpers: spoken-word count, tag stripping, numerals."""
import re

TAG = re.compile(r"\[[^\]]+\]")

def strip_tags(t):
    return re.sub(r"\s+", " ", TAG.sub(" ", t)).strip()

def spoken_words(t):
    """Words as a listener hears them. An acronym is one word per letter (SKU is three), a part name
    like SKU-3 is four, and a number with a unit counts as the words it is read as, roughly."""
    n = 0
    for w in strip_tags(t).replace("...", " ").split():
        w = w.strip(".,;:!?“”’'\"()")
        if not w: continue
        for part in re.split(r"[-/]", w):
            if not part: continue
            if re.fullmatch(r"[A-Z]{2,5}", part):
                # spelled letter by letter (LVDS, RGB), unless it is said as a word (MIPI, ASIC): two vowels
                n += 1 if len(re.findall(r"[AEIOU]", part)) >= 2 else len(part)
            elif re.fullmatch(r"[\d,]+(\.\d+)?", part): n += number_words(part)
            else: n += 1
    return n

def number_words(tok):
    """Words a number is read as: 3,840 is 'three thousand eight hundred forty' (5), 3.3 is 'three point three' (3),
    1280 is 'one thousand two hundred eighty' (5). Counting every number as one or two words made a dense
    scene read 118 wpm while it ran at pace (measured on SKU-8, 2026-10-03)."""
    whole, _, frac = tok.replace(",", "").partition(".")
    def w(n):
        if n == 0: return 1
        c = 0
        for scale in (1_000_000, 1000, 100):
            if n >= scale: c += w(n // scale) + 1; n %= scale
        if n >= 20: c += 1; n %= 10
        if n: c += 1
        return c
    return w(int(whole or 0)) + (1 + len(frac) if frac else 0)

def numerals(t):
    return set(re.findall(r"\d+(?:\.\d+)?", strip_tags(t)))
