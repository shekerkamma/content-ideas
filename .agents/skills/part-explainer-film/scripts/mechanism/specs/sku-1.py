"""SKU-1 BLDC controller: mechanism scenes over the gated narration. Every figure is on the product page."""
from lib import chain, stat, wave, items, compose

SCENES = {
 "open": {"scene": "Today's split: firmware loop and a separate gate driver; SKU-1 joins them on one die",
          "build": lambda p, at: chain(p, at, [("Firmware loop", "processor today"), ("Gate driver", "separate chip"), ("One die", "loop in hardware")],
                                       light=[(0, "brushless"), (1, "driver"), (2, "hardware")])},
 "b1": {"scene": "Commands reach the processor, which sets the loop up and steps aside; the hardware loop switches the gates",
        "build": lambda p, at: chain(p, at, [("Host", "speed · torque · brake"), ("Processor", "sets the loop up"), ("Hardware loop", "switches the gates")],
                                     light=[(0, "commands"), (1, "processor"), (2, "never")])},
 "b2": {"scene": "Three phase currents build from the torque command; the latency target appears",
        "build": lambda p, at: compose(stat(p, at, "< 1 µs", "LOOP LATENCY TARGET", "target", size=140),
                                       wave(p, at, "sine3", [("build", "torque")], y=540, h=300, label="THREE-PHASE DRIVE · FIXED HARDWARE"))},
 "b3": {"scene": "Seven PWM channels switch; the bridge rail figure appears",
        "build": lambda p, at: compose(stat(p, at, "120 V", "BRIDGE RAIL · FROM 5 V · 130 nm BCD", "120", size=140),
                                       wave(p, at, "square", [("draw", "seven")], y=560, h=260, label="PWM × 7 · UP TO 200 kHz"))},
 "b4": {"scene": "Rotor angle and phase current return to the regulator, with no firmware in between",
        "build": lambda p, at: chain(p, at, [("Rotor angle", "Hall · quadrature · encoder"), ("Phase current", "16-bit ADC"), ("Regulator", "PID · CORDIC")],
                                     light=[(0, "rotor"), (1, "current"), (2, "regulator")])},
 "b5": {"scene": "A fault arrives; protection shuts the gates; the trip stays latched",
        "build": lambda p, at: chain(p, at, [("Fault", "thermal · over-current · over-voltage"), ("Protection", "gates shut"), ("Latched", "until cleared")],
                                     light=[(0, "thermal", "err"), (1, "gates"), (2, "latched")])},
 "close": {"scene": "Three open questions appear in turn, then the ask", "kicker": "WHAT IS STILL UNPROVEN",
           "build": lambda p, at: items(p, at, [("ADC isolation from fast switching edges", "isolation"), ("The 1 µs deadline under bus load", "deadline"),
                                                ("ReRAM retention above 125 °C junction", "proven")])},
}
