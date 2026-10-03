"""SKU-5 transceiver: mechanism scenes over the gated narration. Every figure is on the product page."""
from lib import chain, stat, wave, items, compose

SCENES = {
 "open": {"scene": "A differential pair runs; a ground shift moves it, and the link holds",
          "build": lambda p, at: wave(p, at, "diff", [("draw", "transceiver"), ("shift", "miswiring")], label="A / B · DIFFERENTIAL PAIR · GROUND SHIFT")},
 "b1": {"scene": "A thin logic skin hands over to analog blocks on thick-oxide devices",
        "build": lambda p, at: chain(p, at, [("Logic IF", "1.8 V core"), ("Pre-driver", "analog"), ("Output stage", "5 V thick-oxide")],
                                     light=[(0, "core"), (1, "analog"), (2, "thick")])},
 "b2": {"scene": "Edges are drawn with a shaped slope; reach comes from the edge, not the rate",
        "build": lambda p, at: wave(p, at, "slew", [("draw", "edges")], label="SLEW-SHAPED EDGES · TRIMMED 3 V/ns")},
 "b3": {"scene": "Up to 256 nodes; two operating points, fast and short or slow and long",
        "build": lambda p, at: compose(stat(p, at, "256", "NODES · HALF DUPLEX", "256", size=140),
                                       chain(p, at, [("20 Mbps", "short run"), ("83 kbps", "1.2 km")], light=[(0, "fast"), (1, "slow")],
                                             packet=False, y=600, h=150, ns="c"))},
 "b4": {"scene": "An open bus reaches the receiver; hysteresis turns it into a known idle state",
        "build": lambda p, at: chain(p, at, [("Bus A / B", "dead or open"), ("Receiver", "30 mV hysteresis"), ("Logic", "reads a known state")],
                                     light=[(0, "dead"), (1, "hysteresis"), (2, "known", "safe")])},
 "b5": {"scene": "The same path lights again for the CAN-FD channel",
        "build": lambda p, at: chain(p, at, [("Logic IF", "channel 2"), ("Pre-driver", "shaped edges"), ("Output stage", "CANH / CANL"), ("Clock recovery", "40 MHz")],
                                     light=[(0, "second"), (1, "repeats"), (2, "can"), (3, "clock")])},
 "b6": {"scene": "A fault reaches a pin; its own protection shuts the channel down",
        "build": lambda p, at: chain(p, at, [("Bus pin", "A / B · CANH / CANL"), ("ESD + EMC", "±15 kV target"), ("Channel", "shut down")],
                                     light=[(0, "pin"), (1, "protection"), (2, "short", "err")])},
 "close": {"scene": "Three open questions appear in turn, then the ask", "kicker": "WHAT IS STILL UNPROVEN",
           "build": lambda p, at: items(p, at, [("ESD structures that hold ±15 kV", "esd"), ("Reaching 256 nodes, and at what impedance", "silicon"),
                                                ("The first discontinued part it replaces", "bring")])},
}
