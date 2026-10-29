# Chapter 7: Three factories and the shared processor
*Whitepaper §7–8.2*

## Core Idea
One design method runs across three factories that form a sequence, not alternatives, and seven of ten chips share one deliberately minimal RISC-V processor so tools, start-up code, debug and verification are written once. Every feature the processor lacks is chosen to guarantee worst-case timing.

## Frameworks Introduced
- **One method, three factories (a sequence with three jobs)**:
  - **sky130, SkyWater (USA)**: proven; the 130 nm test chip on Deepgrid's flow; cheap first silicon for digital chips. DONE.
  - **SG13G2, IHP (Germany)**: free 130 nm SiGe with 350 GHz transistors; 77/24 GHz radar and fast data links; the only free kit that can make chip 7. PLANNED.
  - **Indian 180 nm, SCL Mohali**: military-approved factory; design, manufacture, screening and approval in India; answers "where is it made?". PLANNED.
  - Stated exception: camera sensors need the paid TowerJazz TS13 kit, a deliberate limited exception for Indian image sensors.
- **One processor across the range (DGridRiscV)**: Deepgrid's product version of the VexiiRiscv generator; properties read from the generated code, not a wish list.
- **Every missing feature is a decision** (determinism over average speed):
  - **No caches**: a cache turns a guaranteed worst case into an average; wrong for motor loops, sequencers and safety monitors. Chip 1's sub-1 µs hardware loop only means something because nothing in the path can miss.
  - **No branch prediction**: same reason plus area; control loops are short and data-dominated.
  - **No FPU**: fixed-point everywhere is smaller, faster and bit-identical across screened and commercial chips; floating-point lives as a separate engine on the test chip.
  - **No compressed instructions**: memory is on-chip and sized to the job; removing the feature removes a fetch alignment case.
  - **PMP instead of an MMU**: bare-metal or small RTOS code needs secure boot, application and safety monitor isolated, at a fraction of MMU area.
- **Why 200 MHz is enough, and what it is not**: the processor is a controller, not a calculator. Heavy work runs in dedicated hardware (motor pipeline, meter filters, pixel pipeline, radar processing) sized by parallel lanes, not MHz. 200 MHz is a processor-and-bus target, not a per-chip promise: chip 6 (comparator + watchdog) and chip 5 (line driver) do not need it, and each chip will publish its own measured speed.

## Key Concepts
- **RV32IM_Zicsr**: base integer ISA + multiply/divide + CSRs (misa = 0x40001100 in generated code).
- **Machine mode only**: no supervisor or user privilege levels.
- **Pipeline**: 2 fetch stages, 6 execute stages; one lane, one instruction at a time.
- **Cacheless AXI4**: 32-bit AXI4 ports for instruction fetch and data access, no cache.
- **PMP regions**: physical memory protection for software isolation.
- **Fixed-point maths**: deterministic arithmetic identical across chip grades.

## Mental Models
- Think of **the processor as the conductor, not the orchestra**.
- Use **"a cost you always pay is easier to plan for than one you usually avoid"**.
- Treat **"where is it made?" as the defence buyer's real question**, answered by SCL.

## Anti-patterns
- **Quoting 200 MHz as a spec for every chip**: it is the processor target, unmeasured.
- **Adding caches or branch prediction to control silicon for benchmark speed**.
- **Treating the three factories as interchangeable**: each has a distinct job.

## Reference Tables

| DGridRiscV property | Value | Evidence in generated code |
|---|---|---|
| Instruction set | RV32IM_Zicsr | misa constant 0x40001100 |
| Privilege | machine mode only | PrivilegedPlugin |
| Execution | one instruction at a time, in order | single lane |
| Pipeline | 2 fetch + 6 execute stages | fetch ctrls 0..1, execute ctrl 0..5 |
| Multiply/divide | hardware | MulPlugin + DivPlugin |
| Shifter | full barrel, one cycle | BarrelShifterPlugin |
| Memory protection | PMP regions | PmpPlugin |
| Fetch / data | no cache, 32-bit AXI4 | FetchCachelessAxi4Plugin / LsuCachelessAxi4Plugin |
| Branch prediction | none | no BtbPlugin or RasPlugin |
| Floating point | none | FPU decode tied off |
| Compressed | none, 4-byte only | not set in misa |

| Factory | Job | Status |
|---|---|---|
| sky130 (SkyWater) | proven flow, cheap digital first silicon | DONE |
| SG13G2 (IHP) | SiGe radar and fast links | PLANNED |
| SCL Mohali 180 nm | Indian origin, screening, IDDM | PLANNED |

## Worked Example
**Defending "no cache" to a reviewer who reads it as a gap:**
1. State the requirement: chip 1's hardware control loop must respond in under 1 µs every time.
2. Show the failure: a cache miss makes an access far slower than average, breaking the worst case.
3. State the design: the core fetches from closely attached memory with a fixed access time.
4. Tie to value: the sub-1 µs figure is only meaningful because no element in the path can miss.
5. Generalise: the same logic removes branch prediction and justifies fixed-point.

## Key Takeaways
1. Factories are sequential jobs: prove (sky130), reach 77 GHz (IHP), make in India (SCL).
2. One processor across seven chips is how a small team builds a range.
3. Each omitted processor feature trades average speed for a guaranteed worst case.
4. Heavy computation belongs in dedicated hardware sized by lanes.
5. Publish per-chip measured speeds; never one 200 MHz number for all.

## Connects To
- **ch01**: SCL as the IDDM enabler.
- **ch03**: the unpublished timing analysis behind 200 MHz.
- **ch09**: dual DGridRiscV in the lockstep MCU.
- **ch10**: the IHP/CMOS radar split.
