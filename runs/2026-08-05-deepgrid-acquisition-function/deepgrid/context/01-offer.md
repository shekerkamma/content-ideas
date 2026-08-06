# Offer

Status: draft — **requires founder approval on pricing before outbound use**

## What we sell

A certified ADAS **function**, not a chip and not a bundle. Five product lines on one 28nm
**chiplet-based package** — six chiplets (A100 / R100 / T100 / D100 / S100 / H100) in one
package, not one die. Say "package" or "SoC", never "six-chiplet die": a die does not contain
chiplets and a technical evaluator will catch it in the first meeting.

**AIS-184 is correct** for driver monitoring — it is a different standard from AIS-162 (AEBS)
and AIS-188. It is not a typo; do not "correct" it.

| Line | What it actually is | ASP | Model | Sold to |
|---|---|---|---|---|
| **AD0 basic** | Smart mirror / 360° surround. Cameras replace mirrors; driver drives everything. | ₹0.50L | Product sale | Retrofit entry — establishes the account and the data-rights clause |
| **AD0 Tower** ⚠ | **Smart Mirror Tower pod: 3× 8MP GMSL2 cameras + 4D 77GHz radar + thermal + DMS + in-cab compute.** Installed in hours, driver in seat. | ₹2.3L | Product sale | Light-fleet (5t) retrofit; buyer is the fleet owner or GM-Operations owning the safety/insurance P&L — one signer, no committee |
| **AD2** | Full truck ADAS kit — compute + software + sensors. Driver drives; the kit warns and can brake. **The mandate product.** | ₹2.0–2.5L | Product sale | Fleets, OEM line-fit |
| **AD3** | The AD2 kit rented instead of sold, on a fleet subscription. Same hardware, different contract. | ₹0.66 Cr/yr ⚠ | Design partner only, FY28+ | Fleets that will not take capex |
| **AD4 Heavy** | **Driverless** heavy transport AGV, >5T, on private land. No driver in the cab. | ₹3.50 Cr | **Design partner only** | Plants, mines, industrial campuses |
| **AD4 Seaport** | **Driverless** container-yard AGV — moves containers between stack and quay. No driver in the cab. | ₹0.45 Cr | **Design partner only** | Container terminals, intermodal yards |

**AD0→AD2 is driver assistance. AD3 is the same thing rented. AD4 is driverless.** These are
different buyers, different sales cycles and different proof burdens. Never present them as a
single price range — the ₹0.50L-to-₹3.5 Cr spread is a product ladder, not a discount band.

### What is real today, by line

| Line | Evidence state | FY27 | FY32 plan |
|---|---|---|---|
| AD0 | Perception proven on FPGA (40 fps YOLOv11n) | ₹0.05 Cr | ₹270 Cr / 54,000 units |
| AD2 | **Claim outruns silicon** — needs the SoC and AIS-162/188 | ₹2.50 Cr | ₹450 Cr / 18,000 units |
| AD3 | Nothing. Plan only, from FY28 | — | ₹66 Cr / 100 units |
| AD4 Heavy | Nothing. No site, no reference | — | ₹105 Cr / 30 units |
| AD4 Seaport | Nothing. No site, no reference | — | ₹22.65 Cr / 50 units |

⚠ **AD3 unresolved.** ₹0.66 Cr/yr against an AD2 outright sale of ₹2.0–2.5L is ~26× annual
rent on identical hardware. One of those two numbers is wrong. Do not quote AD3 pricing until
the founder resolves it.

Source: BP-1A India plan, ADAS product-line table. ADAS total ₹2.55 Cr FY27 → ₹913.65 Cr FY32.

> **⚠ The sellable-product problem.** AD2 is called the mandate product and carries ₹2.50 Cr
> of FY27 revenue — but AIS-162/188 is not held, and 02-icp.md puts fleets on "validate, do
> not forecast" precisely because certified AEBS does not exist until 2027. **So the one
> product designated as sellable has no segment cleared to buy it today.** What is actually
> sellable right now is AD0 to government/PSU buyers, where eligibility rather than
> certification is the gate. Say that plainly rather than forecasting AD2 into FY27.

> **Selling rule.** AD0 and AD2 are what you sell. AD3 and AD4 are what you *win design
> partners for* — never quote them as available. AD3 and AD4 together are ₹193.65 Cr of the FY32
> ₹913.65 Cr (21%) and **none of it exists today**. Within AD4, Heavy is ₹105 Cr of ₹127.65 Cr
> (82%). Treat any AD3/AD4 conversation as discovery, not pipeline.

### ⚠ Two products are both called AD0

BP-1A carries **₹0.50L** in the ADAS product table and **₹2.3L** for the Smart Mirror Tower
retrofit kit — 4.6× apart. They are not the same thing: the Tower carries 4D radar, thermal
and DMS; the basic line is cameras replacing mirrors. **Confirm with the founder which one is
being quoted before any AD0 outbound.** Quoting ₹0.50L and delivering a ₹2.3L pod, or the
reverse, is how a first deal dies.

## How to price it

### AD0 Tower vs a ₹35,000 camera box — the price defence

This is the comparison AD0 actually faces, and it is winnable on content, not on adjectives.
A ₹35,000 box is cameras and a recorder. The Tower adds **4D 77GHz radar** (works in dust,
fog, night, and no camera box has it), **thermal**, and **driver monitoring** — the AIS-184
addressable function. Price the radar and the DMS. Let the camera view and the recording ride
free, because that is what the cheap box does adequately.

Do not say "we are better cameras". Say: *ask them what happens at night in dust, and ask
them whether it watches the driver.*

### AD2 — the same doctrine, one level up

**Quote AEBS and DMS by function. Let the warning functions ride free.**

- Certified AEBS (AIS-162) requires radar, brake actuation and proving-ground homologation.
  A ₹30,000 camera box cannot deliver it at any price. This carries the price.
- Driver monitoring (AIS-184 addressable) is hard to approximate. This carries the price.
- LDW / BSD / warnings are what the cheap box does adequately. Giving them away costs
  nothing and removes the buyer's strongest comparison.

Selling the bundle forces a ₹2.3L-versus-₹30,000 comparison on the box's terms. Do not.

## What is included

Compute module, perception software, sensor suite, drive-by-wire CAN actuator interface,
installation (15–35 min per vehicle).

⚠ **AIS-140 telematics via the S100 chiplet is NOT included today.** S100 is a chiplet in a
package that has not taped out; the only evidenced silicon is DGS001 on Artix-7 class FPGA,
and 04-proof.md carries no AIS-140 entry. It is a post-ASIC roadmap item. Do not offer it to
a fleet mid-AIS-140-rollout, however tempting the hook.

## What is not included

AIS-162/188 certification — **held as a path via NATRAX, not held today**. Insurance
outcomes. Any accident-reduction guarantee. Fleet management software.

## What the client must do

Provide vehicle access for installation, a site contact, and — for pilots — a measurement
baseline. Every contract carries a data-rights clause; the data moat is only real if it is
contractually secured.

## Typical result and timeline

Not yet evidenced at fleet scale. Do not quote a payback period, a premium reduction, or an
accident-reduction figure. See `04-proof.md` for what may be claimed.

## Unit economics (internal only — never quote to a buyer)

- Kit gross margin at ASIC phase: **72%**. Do not quote a blended figure.
- Die cost $3.876 at 1M units; loaded at plan volumes ≈ $22/die effective. **These differ 5.7×
  and the bridge is not documented. Never quote either externally — mixing the two is exactly
  the error that retired the 12.9× claim.**
- Team opex ₹4–6 Cr/yr, covered by 400–600 kits/yr.
