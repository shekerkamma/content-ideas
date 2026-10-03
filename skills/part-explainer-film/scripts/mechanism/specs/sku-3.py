"""SKU-3 hi-rel PMIC: mechanism scenes over the gated narration. Every figure is on the product page."""
from lib import chain, stat, wave, rails, items, compose

SCENES = {
 "open": {"scene": "The 28 V bus: surges and spikes rise above it, then the ceiling every rail needs appears",
          "build": lambda p, at: wave(p, at, "surge", [("spike", "surges"), ("clamp", "rail")], label="28 V BUS · 80 V SURGES · 100 V SPIKES")},
 "b1": {"scene": "A surge hits the input; conditioning clamps it to a safe ceiling",
        "build": lambda p, at: wave(p, at, "surge", [("spike", "surges"), ("clamp", "clamps")], label="INPUT CONDITIONING · CLAMP · IDEAL DIODE · UVLO + OVLO")},
 "b2": {"scene": "Switching cycles run; buck, cycle-by-cycle limit and a downstream short light in turn",
        "build": lambda p, at: compose(wave(p, at, "square", [("draw", "buck")], y=330, h=240, label="SWITCHING · 500 kHz TO 2 MHz"),
                                       chain(p, at, [("Buck", "peak current mode"), ("Current limit", "every cycle"), ("Short downstream", "cannot run away")],
                                             light=[(0, "buck"), (1, "limiting"), (2, "short")], y=650, h=140, ns="c"))},
 "b3": {"scene": "Four rails rise one after another, each with its power-good tick",
        "build": lambda p, at: rails(p, at, [("5 V", .9, "5"), ("3.3 V", .66, "3.3"), ("1.8 V", .42, "1.8"), ("1.2 / 0.9 V", .26, "1.2")])},
 "b4": {"scene": "Each rail reports power-good inside its window before the sequencer releases the next",
        "build": lambda p, at: chain(p, at, [("Rail 1", "power-good"), ("Rail 2", "waits"), ("Rail 3", "waits"), ("Rail 4", "waits")],
                                     light=[(0, "reports"), (1, "window"), (2, "sequencer"), (3, "next")])},
 "b5": {"scene": "Current sense, error amp and PWM comparator close the inner loop; the margin target appears",
        "build": lambda p, at: compose(stat(p, at, "> 60°", "PHASE MARGIN TARGET · −55 TO +125 °C", "minus", size=140),
                                       chain(p, at, [("Current sense", "sense-FET + amp"), ("Error amp", "type-III comp"), ("PWM comp", "slope comp")],
                                             light=[(0, "current"), (1, "inner"), (2, "loop")], y=600, h=150, ns="c"))},
 "b6": {"scene": "Three copies of the sequencer state; a particle strikes one, the vote keeps the order",
        "build": lambda p, at: chain(p, at, [("Copy A", "sequencer state"), ("Copy B", "sequencer state"), ("Copy C", "sequencer state"), ("Vote", "2 of 3 · TMR")],
                                     light=[(0, "because"), (2, "because"), (1, "strike", "err"), (3, "triple")], packet=False)},
 "close": {"scene": "Three open questions appear in turn, then the ask", "kicker": "WHAT IS STILL UNPROVEN",
           "build": lambda p, at: items(p, at, [("Clamping a 100 V, 50 ms surge", "surge"), ("Loop margins across −55 to +125 °C", "loop"),
                                                ("Upset spacing between the voting bits", "upset")])},
}
