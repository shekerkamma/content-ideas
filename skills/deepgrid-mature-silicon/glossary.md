# DeepGrid Semi — Silicon Architecture & Defence Glossary

**AEC-Q100** — Automotive Electronics Council standard specifying stress test qualification for automotive integrated circuits (Grade 0: -40°C to +150°C, Grade 1: -40°C to +125°C). (Ch 1, 2, 5, 10)

**AFE (Analog Front End)** — Integrated analog circuitry including low-noise amplifiers, active mixers, PGA, and ADCs that digitize sensor or antenna signals. (Ch 3, 8, 13)

**ASIL (Automotive Safety Integrity Level)** — Risk classification scheme defined by ISO 26262. ASIL-D represents the highest level of functional safety integrity requiring redundant lockstep cores and sub-2-cycle fault latching. (Ch 2, 5, 10, 12)

**AXI-REALM** — Real-time bus interconnect monitoring and bandwidth regulation QoS unit that prevents lower-priority host traffic from starving safety-critical hardware accelerators. (Ch 12)

**BCD (Bipolar-CMOS-DMOS)** — Mixed-signal semiconductor manufacturing process combining Bipolar (precise analog), CMOS (high-density digital logic), and DMOS (high-voltage power switching). (Ch 2, 4, 7)

**Brokaw Bandgap** — A precision voltage reference circuit topology utilizing the temperature compensation of base-emitter voltage differences in bipolar transistors, achieving 10–12 ppm/°C drift. (Ch 4, 7)

**CFAR (Constant False Alarm Rate)** — Adaptive thresholding algorithm implemented in hardware on radar basebands to detect real targets amid background clutter and thermal noise. (Ch 8)

**CORDIC (Coordinate Rotation Digital Computer)** — Hardware iterative arithmetic algorithm computing trigonometric, hyperbolic, and polar transformations with minimal gate count and sub-microsecond latency. (Ch 2)

**DICE (Dual Interlocked Storage Cell)** — Radiation-tolerant latch topology featuring four cross-coupled nodes that provides single-event upset (SEU) immunity without full triple modular redundancy. (Ch 4)

**DGridRiscV** — DeepGrid's proprietary 32-bit (RV32IM) and 64-bit (RV64GCH) in-order RISC-V processor cores designed with zero recurring IP licensing footprints. (Ch 2, 3, 5, 10, 11, 12)

**DO-160 / DO-254** — RTCA standards governing environmental conditions / airborne hardware design assurance for civil and military aircraft electronics. (Ch 4, 8)

**EKF (Extended Kalman Filter)** — Non-linear sensor fusion algorithm running at 30 Hz in hardware on the D100 SoC to fuse IMU kinematics with optical flow feature tracking for GPS-denied navigation. (Ch 11)

**EVITA Full** — European secure on-board vehicle architecture standard defining the highest tier of hardware security module (HSM) with asymmetric cryptography and secure boot. (Ch 10, 12)

**FOC (Field-Oriented Control)** — Mathematical vector control method for brushless motors that decouples stator magnetic field and rotor flux for maximum torque efficiency and dynamic response. (Ch 2, 5)

**LDMOS (Laterally Diffused Metal Oxide Semiconductor)** — Asymmetric high-voltage planar power transistor technology integrated on 130nm CMOS for robust $\pm$15 kV ESD line drivers. (Ch 6)

**MIL-STD-883K** — United States military standard defining test methods, screening flows, and environmental controls for microelectronics used in defence and aerospace systems. (Ch 1, 4, 7, 8)

**PIL (Positive Indigenisation List)** — Indian Ministry of Defence procurement mandate banning the import of specific defence line-items to enforce domestic sourcing. (Ch 1, 9, 14)

**ReRAM (Resistive Random-Access Memory)** — Non-volatile memory technology operating by changing resistance across a solid-state dielectric, utilized as an embedded flash alternative on open PDKs. (Ch 2)

**SEU (Single-Event Upset)** — Radiation or particle-induced state change in a memory cell or latch mitigated by SECDED ECC, DICE latches, and temporal lockstep skew. (Ch 4, 5, 12)

**SiP (System-in-Package)** — Packaging technology enclosing multiple distinct semiconductor dies (wire-bonded and flip-chip) onto a single organic BGA substrate. (Ch 1, 13)

**TCON (Timing Controller)** — Digital logic block generating row/column clock strobes and gamma voltage synchronization for flat-panel liquid crystal displays. (Ch 9)

**TMR (Triple Modular Redundancy)** — Fault-tolerant voting architecture using three parallel hardware instances and a 2-out-of-3 majority voter. (Ch 4, 12)

**TSN (Time-Sensitive Networking)** — IEEE 802.1 standards suite (including 802.1Qbv time-aware shaper) providing deterministic bounded latency over standard Ethernet. (Ch 10)
