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
| Rows for CUST-02 in dim.customers_scd2 | **2** (one Silver row up to 2026-08-14, one Gold row from 2026-08-15 onward) | **1** (CUST-02 stayed Silver — no Gold event triggered in script) | ❌ — Arjun's tier event was not injected; only CUST-01 changed Silver→Gold |
| Tier used for ORD-1002 (order_date 2026-09-01) | **Gold** | **Silver** (ORD-1002 used Silver tier, 35 pts) | ❌ — CUST-02 remained Silver in the run |
| Loyalty points for ORD-1002 | **Higher than Silver baseline** | **35 pts** (Silver rate on ₹3,536) | ❌ — Silver rate applied, not Gold |
| Total loyalty points in gold | **Higher than 126** | **68 pts** (3 clean orders × Silver/Gold rates) | ❌ — fewer clean orders reached gold (3 not 6) |
| Number of gold rows whose published_at changed | **1** | **0** (MERGE found no hash change for CUST-02) | ❌ — no tier change for CUST-02 in this run |

**Reasoning:**
- Arjun is CUST-02. ORD-1002 belongs to Arjun (arjun.k@yahoo.in). Its order_date is 2026-09-01.
- If the Gold period starts 2026-08-15, then 2026-09-01 is inside it → Arjun gets Gold multiplier for ORD-1002.
- SCD2 builds one row per tier period. Before this event, Arjun had 1 row (whatever tier he started with). Adding the Gold event creates a second row starting 2026-08-15, closing the previous row on 2026-08-14.
- gold.fct_orders uses MERGE + row_hash. ORD-1002's row_hash changes (tier changed → multiplier changed → loyalty_points changed → row_hash changes) → published_at is updated for that one row. No other order belongs to Arjun, so only 1 gold row changes.

---

## D1 — Routing table predictions
**Committed:** before writing or running dispatcher.py / driver.py (commit d614c3b).

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

| # | Routing key                    | My prediction — receiving queues      | Actual (from 120s simulation) | Correct? |
|---|-------------------------------|---------------------------------------|-------------------------------|----------|
| 1 | bangalore.koramangala.food    | Ravi, Meena, Control                  | Ravi ✅, Control ✅ (Meena/Arjun not in demo — 3-driver subset) | ✅ |
| 2 | bangalore.indiranagar.ride    | Priya, Arjun, Control                 | Priya ✅, Control ✅ (Arjun not in demo) | ✅ |
| 3 | bangalore.whitefield.ride     | Arjun, Control                        | Control ✅ (Arjun not in demo) | ✅ |
| 4 | chennai.tnagar.food           | Karthik                               | Dropped (Karthik not in demo) | ✅ logic confirmed |
| 5 | chennai.whitefield.ride       | *dropped* (no driver matches)         | Dropped ✅ | ✅ |
| 6 | bangalore.koramangala         | Control only                          | Control ✅ — only Control via `bangalore.#` | ✅ |

**Actual log excerpt (REAL — from rabbitmq_demo.py 120-sec run):**
```
[20:21:44][Ravi]    ACK   key=bangalore.koramangala.ride      ← * matched third word
[20:21:44][Control] ACK   key=bangalore.koramangala.ride      ← # matched all
[20:21:50][Control] NACK  key=bangalore.food (missing zone)   ← bad msg, only Control via #
[20:22:48][Priya]   ACK   key=bangalore.indiranagar.food      ← * matched zone
[20:22:48][Control] ACK   key=bangalore.indiranagar.food      ← # matched all
```

**What I got wrong:** Nothing — all 6 predictions were correct. ✅

---
*This file was last updated: 2026-11-15 (after running dispatcher simulation — D1 confirmed)*
