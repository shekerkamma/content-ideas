# Clip narration — the four embedded simulator videos

One block per clip, written to the clip's own runtime and to what is on screen
at that moment. Not a reading of the slide beside it: the rail already says what
to watch, so the narration says what it *means*.

Voice: Microsoft David (en-US), rate -1. Local, free, deterministic.

---

**ddrive** · 78.0 s · Smart Truck (AD2 kit), slide 23
This is the D-DRIVE perception stack running against three road profiles in sequence. What you are looking at is not a recording of a drive. The vehicle model is solved in real time: five hundred and fifty kilograms, a two point one metre wheelbase, and a tyre friction coefficient of nought point seven five. Steering angle and lateral acceleration follow from that physics, not from an animation path. The centre panel is the planner's bird's-eye view, and it redraws from the fused object list rather than from the scene. On the right, the perception rail names each object it has classified and gives its range in metres — a motorbike, an auto-rickshaw, a pedestrian. Watch the scenario change from market street, to single carriageway highway, to the deliberate stress test. The same stack handles all three. Nothing is reloaded between them, and no parameters are re-tuned. That is the point of the demonstration: one perception pipeline, on one chip, across the road conditions an Indian commercial vehicle actually meets.

---

**forklift** · 72.1 s · AD1 Indoor L4 kit, slide 17
This is the indoor autonomy stack running a real warehouse floor. Indoors is where the silicon closes the loop rather than advising: the vehicle steers, accelerates and brakes itself. The truck is running an inbound put-away task. A twenty-four metre LiDAR at five hertz and a fifty-seven degree camera fuse into the occupancy view on the right. The red ring travelling with the truck is the safety zone. It is not decoration — it gates the speed, and when a person enters it the vehicle stops and speaks. You will hear that alert. The alert policy is configurable per site: horn, voice, both, or silent, because that is an operations decision and not ours to make. Now the pick run, and then the peak-hour floor, which is the scenario that decides whether a site can actually run this. Workers, peer vehicles, trolleys and spills all have to be resolved, and recovery is explicit: the truck reroutes after a set stuck time rather than waiting for someone to notice.

---

**yard** · 53.3 s · Seaport AGV, slide 55
This is a working twin of a container terminal, built for the PS18 programme. Three things have to be proven here. First, positioning. Watch the two confidence bars as the vehicle enters the container canyon: satellite positioning degrades under the quay cranes, and the fusion estimate holds. Seven centimetres in the open, twenty-two centimetres under the crane. Second, navigation — congestion-aware routing between the stacks, with obstacle-safe stops in mixed traffic. Third, scheduling. The dispatch toggle switches between first-in-first-out and predictive arrival time, and crane idle moves in response — the number a terminal operator is paid on. Note the badge: shadow mode. It advises before it is given control, which is how a port adopts this.

---

**sentinel** · 48.9 s · Defence D-HUMR, slide 74
This is the same fusion stack pointed outward instead of forward — the PS16 perimeter console. Radar, thermal and camera tracks along the fence line are classified individually, and then correlated. Watch two separate contacts become one threat: a vehicle loitering on the access road, and a person who dismounts and approaches the fence. Neither would raise an alarm alone. The ladder on the right is the escalation state — loiter, approach, breach risk — so the operator sees intent forming rather than an alarm at the moment of breach. The console states its reasoning in words. And the feature that matters most is restraint: benign tracks are held, never escalated. False alarm rate is what gets a perimeter system switched off.

---

**truck** · 37.8 s · Smart Mirror Tower / AD2 kit, slide 24
This is the sensor architecture of the truck kit — the first system that runs on the box. Two mirror towers retrofit above the existing wing mirrors, each carrying a thermal camera, a road-facing camera and a one hundred and twenty degree truck-side camera. Two more cameras sit in the cab: a forward dashcam for event recording, and a driver-monitoring camera for fatigue. Front and rear four-D radar give range and velocity at both ends, in rain, dust and glare. Watch the coverage cones sweep. Where they overlap is where a cyclist or an animal is picked up and held across frames. The claim the layout is making is a simple one: no quarter of a heavy truck is left unobserved.

---

**cube** · 36.3 s · Chipset OEM B2B, slide 30
Two units computing exactly the same arithmetic, with different geometry. On the left, the flat eight-by-eight matrix unit as it runs today on the FPGA: sixty-four multiply-accumulates per cycle, with the K reduction iterated in software, so it takes eight cycles to consume one tile. On the right, the eight-by-eight-by-eight cube that the twenty-eight nanometre part carries. K becomes hardware depth, so all eight layers fire simultaneously. Five hundred and twelve multiply-accumulates per cycle, one tile retired per cycle. Watch the tile counters diverge as they run: that gap is the eight-times figure, shown rather than asserted. And this is the operation that forces a custom chip, because the cube together with per-core memory access does not fit on the FPGA.

---

**problem** · 51.9 s · A100 compute box 4ch PCIe, slide 43
Two runs of the same workload, separated only by how memory is reached. On the left, the arrangement as it stands today: eight processing cores behind a single data engine. That engine fetches one descriptor at a time, so seven cores wait while one is fed. Watch the utilisation column on the left — it never clears twelve percent, and most of the cores sit at almost nothing for the whole run. On the right, the same silicon. The same multiply-accumulate count, the same twenty-eight nanometre process, the same clock. The only change is that every core now owns its own load engine and pulls from banked static memory in parallel. All eight climb to around fifty-nine percent and hold there. Nothing has been added but the path to memory. The frame that costs four hundred and seventy milliseconds today lands in about eighty-five.
