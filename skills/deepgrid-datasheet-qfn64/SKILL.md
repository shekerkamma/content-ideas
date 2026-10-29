---
name: deepgrid-datasheet-qfn64
description: "Hardware pinout, QFN-64 package definition, electrical characteristics, power supply sequencing, register maps, and PCB layout guidelines for DeepGrid Semi's DG32-LITE (CI2609) and DG32-2DOM (CI2612) SoCs on SkyWater sky130A (130 nm)."
---

# DeepGrid Semi — DG32-LITE & DG32-2DOM Datasheet Reference

**Part Numbers:** DG32-LITE (chipIgnite CI2609) · DG32-2DOM (chipIgnite CI2612)  
**Package:** 64-pin QFN ($9.0 \times 9.0\ \text{mm}$, 0.5 mm pitch, exposed paddle = VSS)  
**Process:** SkyWater sky130A (130 nm CMOS)  

---

## 1. Features & Architectural Comparison

| Feature | DG32-LITE (CI2609) | DG32-2DOM (CI2612) |
| :--- | :--- | :--- |
| **Die Size** | Standard OpenFrame Slot | $3400 \times 4500\ \mu\text{m}$ ($15.30\ \text{mm}^2$) |
| **CPU Cores** | 2x RV32IMC in Hardware Lockstep | 2x RV32IMC in Hardware Lockstep (Frozen) |
| **Core Clock** | 50 MHz (`CLK` pin 31) | 50 MHz (`CLK` pin 31) |
| **Fast Clock** | None | 114 MHz (`clk_fast_i`) for Attention Engine |
| **SRAM Memory** | 32 KB (16x sky130 macros, no ECC) | 32 KB main + 16 KB checker + K/V macros |
| **Boot ROM** | 64 KB baked std-cell ROM | 64 KB baked std-cell ROM |
| **External Flash** | QSPI quad-output-fast-read (0x6B) | QSPI quad-output-fast-read (0x6B) |
| **Motor Drive** | 3-phase center-aligned complementary PWM | 3-phase center-aligned complementary PWM |
| **ESC Engine** | 4-channel DShot (`0xC000_0000`) | 4-channel DShot (`0xC000_0000`) |
| **Analog Feedback**| On-die 8-bit diff SAR ADC (`0xDB`) | On-die 8-bit diff SAR ADC (`0xDB`) |
| **Hardware Trig** | CORDIC ($N=20$, sin/cos/atan2/mag) | CORDIC ($N=20$, sin/cos/atan2/mag) |
| **Attention Engine**| None (Error slave returns `SLVERR`) | Hardware INT8 Attention (`0xE000_0000`) |
| **Total Power** | ~0.43 W @ 50 MHz (tt 25 °C, 1.8 V) | ~0.43 W @ 50 MHz (Core) + Attn dynamic |

---

## 2. Complete 64-Pin QFN Pin Assignment

| Pin | Signal Name | Type | Description / Hardware Tie Rule |
| :---: | :--- | :---: | :--- |
| **1** | `vssa2` | Power | Ground |
| **2** | `ADC_VINN` | Analog | SAR ADC Negative Input, 0 to 1.8 V (diff pair with pin 62) |
| **3** | `PWM_AH` | Output | Phase A High-Side Gate Drive (or DShot CH0) |
| **4** | `PWM_AL` | Output | Phase A Low-Side Gate Drive |
| **5** | `PWM_BH` | Output | Phase B High-Side Gate Drive (or DShot CH1) |
| **6** | `PWM_BL` | Output | Phase B Low-Side Gate Drive |
| **7** | `PWM_CH` | Output | Phase C High-Side Gate Drive (or DShot CH2) |
| **8** | `PWM_CL` | Output | Phase C Low-Side Gate Drive |
| **9** | `vdda2` | Power | 3.3 V User Supply, unused — tie to 3.3 V |
| **10** | `vssd2` | Power | Ground |
| **11** | `PWM_TRIG` | Output | ADC Sample Trigger (pulses at center-aligned ripple null) |
| **12** | `ENC_A` | Input | Quadrature Encoder Phase A (2-flop sync, 3.3 V CMOS) |
| **13** | `ENC_B` | Input | Quadrature Encoder Phase B (2-flop sync, 3.3 V CMOS) |
| **14** | `ENC_Z` | Input | Quadrature Encoder Index Z (captures position & timestamp) |
| **15** | `HALL_A` | Input | Hall Sensor Input A |
| **16** | `HALL_B` | Input | Hall Sensor Input B |
| **17** | `vddio` | Power | 3.3 V Pad-Ring / ESD Supply — **REQUIRED** |
| **18** | `vccd` | Power | 1.8 V Harness Core Supply — **REQUIRED** |
| **19** | `N/C` | No Connect| Leave floating or no connect |
| **20** | `vssa` | Power | Ground |
| **21** | `resetb` | Input | Harness reset input, active low, 3.3 V (ANDed with pin 28) |
| **22** | `HALL_C` | Input | Hall Sensor Input C |
| **23** | `vssd` | Power | Ground |
| **24** | `TCK` | Input | JTAG Clock (weak internal pull-down) |
| **25** | `TMS` | Input | JTAG Mode Select (weak internal pull-up) |
| **26** | `TDI` | Input | JTAG Data In (weak internal pull-up) |
| **27** | `TDO` | Output | JTAG Data Out (driven only while shifting) |
| **28** | `RST_N` | Input | External Reset, active low (ANDed on-die with resetb & POR) |
| **29** | `vssio` | Power | Ground |
| **30** | `vdda` | Power | 3.3 V Harness Analog / POR Supply — **REQUIRED** |
| **31** | `CLK` | Input | System Clock, 3.3 V CMOS, 50 MHz design target |
| **32** | `QSPI_SCLK`| Output | QSPI Boot Flash Clock (SCLK = CLK / 2 = 25 MHz) |
| **33** | `QSPI_CSN0`| Output | QSPI Boot Flash Chip Select 0 (active low) |
| **34** | `QSPI_IO0` | Bidir | QSPI Flash Data Bit 0 (MOSI in 1-bit mode) |
| **35** | `QSPI_IO1` | Bidir | QSPI Flash Data Bit 1 (MISO in 1-bit mode) |
| **36** | `QSPI_IO2` | Bidir | QSPI Flash Data Bit 2 (WPn) |
| **37** | `QSPI_IO3` | Bidir | QSPI Flash Data Bit 3 (HOLDn) |
| **38** | `vssa1` | Power | Ground |
| **39** | `vssd1` | Power | Ground (User Area) |
| **40** | `vdda1` | Power | 3.3 V User Supply, unused — tie to 3.3 V |
| **41** | `QSPI_CSN1`| Output | QSPI Chip Select 1 (optional second device / PSRAM) |
| **42** | `UART0_TX` | Output | Console UART Transmit (boot banner emitted at 115200 8N1) |
| **43** | `UART0_RX` | Input | Console UART Receive (interactive monitor if flash blank) |
| **44** | `UART1_TX` | Output | Telemetry UART Transmit |
| **45** | `UART1_RX` | Input | Telemetry UART Receive |
| **46** | `SPI_SCLK` | Output | SPI Master Clock (up to 25 MHz) |
| **47** | `vdda1` | Power | 3.3 V User Supply, unused — tie to 3.3 V |
| **48** | `SPI_MOSI` | Output | SPI Master Data Out |
| **49** | `vccd1` | Power | 1.8 V User Area Supply: all DG32 logic, SRAM, SAR — **REQUIRED** |
| **50** | `SPI_MISO` | Input | SPI Master Data In |
| **51** | `SPI_CSN` | Output | SPI Master Chip Select (active low) |
| **52** | `vssa1` | Power | Ground |
| **53** | `I2C_SCL` | Bidir (OD)| I2C Master Clock (external pull-up 2.2k–4.7k to 3.3 V required)|
| **54** | `I2C_SDA` | Bidir (OD)| I2C Master Data (external pull-up 2.2k–4.7k to 3.3 V required) |
| **55** | `GPIO0` | Bidir | General-Purpose I/O 0 (atomic SET/CLR at `0xD300_000C/10`) |
| **56** | `vssio` | Power | Ground |
| **57** | `GPIO1` | Bidir | General-Purpose I/O 1 |
| **58** | `GPIO2` | Bidir | General-Purpose I/O 2 |
| **59** | `FAULT_N` | Output | Lockstep / Supervisor Fault, active low (trips <=2 cycles) |
| **60** | `RAIL_OK0` | Input | Rail Supervisor Input 0 (rail_ok[3:2] tied high internally) |
| **61** | `RAIL_OK1` | Input | Rail Supervisor Input 1 |
| **62** | `ADC_VINP` | Analog | SAR ADC Positive Input, 0 to 1.8 V (diff pair with pin 2) |
| **63** | `vccd2` | Power | 1.8 V User Supply, unused — tie to 1.8 V |
| **64** | `vddio` | Power | 3.3 V Pad-Ring / ESD Supply — **REQUIRED** |
| **EP** | `VSS` | Ground | Exposed Die Paddle — solder directly to solid ground plane |

---

## 3. Power Supply Sequencing & PCB Layout Rules
1. **Supply Voltage Rails:**
   - `vddio` (pins 17, 64) = 3.3 V $\pm$ 10%
   - `vdda` (pin 30) = 3.3 V $\pm$ 10%
   - `vccd` (pin 18) = 1.8 V $\pm$ 5%
   - `vccd1` (pin 49) = 1.8 V $\pm$ 5% (Main supply powering all logic, SRAM, and SAR ADC)
   - Unused rails (`vdda1`, `vdda2`, `vccd2`) must be tied to nominal voltages (3.3V / 1.8V) to ensure ESD diodes remain properly biased.
2. **Power-Up Sequence:**
   - Bring up 3.3 V (`vddio`, `vdda`) **before or coincident with** 1.8 V (`vccd`, `vccd1`). Never allow 1.8 V core to exceed 3.3 V I/O rail by $>0.3\ \text{V}$.
3. **Differential SAR ADC Layout:**
   - Pins 62 (`ADC_VINP`) and 2 (`ADC_VINN`) form a differential analog pair operating from 0 to 1.8 V. Route as a tightly coupled, length-matched differential microstrip over an unbroken ground plane away from noisy PWM gate traces (pins 3–8).
4. **Boot Flash Memory:**
   - Connect standard 3.3 V SPI/QSPI NOR flash (e.g. Winbond W25Q128 or Spansion S25FL) to pins 32–37.
   - Header magic required at flash offset `0x0000_0000`: `0xD632_B007` followed by a 32-bit image length.
