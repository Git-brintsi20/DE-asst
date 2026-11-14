# PREDICTIONS.md
# Committed BEFORE running the relevant code cells.
# After the run, actual results are added next to predictions.
# Wrong predictions are KEPT and explained in "What I got wrong".

---

## B4 — SCD2 / Idempotency predictions
**Committed:** before running the Arjun event cell in the notebook.

Event being added: CUST-02 (arjun.k@yahoo.in) moves to Gold, effective_from = 2026-08-15.

| Quantity | My prediction (before run) | Actual after run | Correct? |
|----------|---------------------------|------------------|----------|
| Rows for CUST-02 in dim.customers_scd2 | **2** (one Silver row up to 2026-08-14, one Gold row from 2026-08-15 onward) | PENDING USER | — |
| Tier used for ORD-1002 (order_date 2026-09-01) | **Gold** (because 2026-09-01 is after 2026-08-15, so the Gold row covers it) | PENDING USER | — |
| Loyalty points for ORD-1002 | **PENDING USER** (depends on amount_inr and Gold multiplier from ref table) | PENDING USER | — |
| Total loyalty points in gold | **Higher than 126** (the previous baseline; ORD-1002 earns more points at Gold multiplier) | PENDING USER | — |
| Number of gold rows whose published_at changed | **1** (only ORD-1002's row changes because its tier/points changed; the others are unaffected) | PENDING USER | — |

**Reasoning:**
- Arjun's existing row (Silver from some earlier date) covers ORD-1001 (2026-09-01 is after the new Gold date, so both ORD-1001 and ORD-1002 fall in the Gold period — wait, ORD-1001 is Priya, not Arjun).
- Arjun is CUST-02. ORD-1002 belongs to Arjun (arjun.k@yahoo.in). Its order_date is 2026-09-01.
- If the Gold period starts 2026-08-15, then 2026-09-01 is inside it → Arjun gets Gold multiplier for ORD-1002.
- SCD2 builds one row per tier period. Before this event, Arjun had 1 row (whatever tier he started with). Adding the Gold event creates a second row starting 2026-08-15, closing the previous row on 2026-08-14.
- gold.fct_orders uses MERGE + row_hash. ORD-1002's row_hash changes (tier changed → multiplier changed → loyalty_points changed → row_hash changes) → published_at is updated for that one row. No other order belongs to Arjun, so only 1 gold row changes.

---

## D1 — Routing table predictions
**Committed:** before writing or running dispatcher.py / driver.py.

Drivers and patterns:
| Driver  | Binding pattern          |
|---------|--------------------------|
| Ravi    | bangalore.koramangala.*  |
| Priya   | bangalore.indiranagar.*  |
| Arjun   | bangalore.*.ride         |
| Meena   | bangalore.*.food         |
| Karthik | chennai.tnagar.food      |
| Control | bangalore.#              |

Pattern rules: `*` = exactly one word, `#` = zero or more words.

| # | Routing key                    | My prediction — receiving queues      |
|---|-------------------------------|---------------------------------------|
| 1 | bangalore.koramangala.food    | Ravi, Meena, Control                  |
| 2 | bangalore.indiranagar.ride    | Priya, Arjun, Control                 |
| 3 | bangalore.whitefield.ride     | Arjun, Control                        |
| 4 | chennai.tnagar.food           | Karthik                               |
| 5 | chennai.whitefield.ride       | *dropped* (no driver matches Chennai non-tnagar-food) |
| 6 | bangalore.koramangala         | Control only                          |

**Reasoning for Question 6 (bangalore.koramangala — only 2 words):**
- `bangalore.koramangala.*` (Ravi): `*` must match EXACTLY one word, but there is no third word → ❌ no match.
- `bangalore.indiranagar.*` (Priya): wrong zone AND no third word → ❌.
- `bangalore.*.ride` (Arjun): `*` matches koramangala (one word) but then expects `.ride` as a third word — there is no third word → ❌.
- `bangalore.*.food` (Meena): same problem — no third word → ❌.
- `chennai.tnagar.food` (Karthik): different city → ❌.
- `bangalore.#` (Control): `#` matches ZERO or more words, so `bangalore.koramangala` = `bangalore` + `#`→`koramangala` → ✅ matches.
- **Only Control receives this message.**

**What I got wrong:** (fill in after running)

---
*This file was last updated: 2026-11-15 (before any code ran for B4 or D1)*
