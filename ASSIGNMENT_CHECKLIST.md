# ASSIGNMENT CHECKLIST — From Git to Gold (100 + 10 marks)

> [!IMPORTANT]
> Items marked **PENDING USER** require you to run code and take a screenshot. I cannot run Snowflake, Mage, or RabbitMQ for you — but I have written every piece of code and given you exact steps.

---

## Part A: Git and CI/CD (15 marks)

| Item | Marks | Status | Evidence location |
|------|-------|--------|-------------------|
| A1a — Repo structure created (`freshcart-pipelines/`) | — | ✅ DONE | `c:\Users\HARSHI\Downloads\freshcart-pipelines\` |
| A1b — At least 5 meaningful commits | — | ✅ DONE | 7 commits; `git log --oneline` in WORKLOG.md |
| A1c — `git log --oneline` in report | 5 | ✅ DONE | Paste from WORKLOG.md |
| A2 — Git command table (6 rows) | 4 | ✅ DONE | See Written Answers below |
| A3a — `tests/test_prepare_data.py` written | — | ✅ DONE | `tests/test_prepare_data.py` |
| A3b — `.github/workflows/ci.yml` written | — | ✅ DONE | `.github/workflows/ci.yml` |
| A3c — Local pytest GREEN | — | ✅ DONE | `1 passed in 0.66s` (WORKLOG.md) |
| A3d — Screenshot: green GitHub Actions run | 6 | ⏳ PENDING USER | Go to Actions tab after push |
| A3e — Screenshot: red run (change test_size=0.3) | — | ⏳ PENDING USER | Make change, commit, push, screenshot |
| A3f — Screenshot: green fix run | — | ⏳ PENDING USER | Revert change, commit, push, screenshot |

---

## Part B: FreshCart ELT on Snowflake (30 marks)

| Item | Marks | Status | Evidence location |
|------|-------|--------|-------------------|
| B1 — Run notebook, confirm 8/6/2/4 numbers | 5 | ⏳ PENDING USER | Run `elt/freshcart_elt.ipynb` in Colab |
| B1 — Pass/fail table with screenshots | — | ⏳ PENDING USER | Screenshot each layer |
| B2 — ORD-1003 record trace (written) | 6 | ✅ DONE | See Written Answers below |
| B2 — ORD-1005 / Priya tier trace (written) | — | ✅ DONE | See Written Answers below |
| B2 — Verified against real Snowflake output | — | ⏳ PENDING USER | Run the SELECT statements I provide |
| B3 — `unsupported_currency` added to SQL_10 | 6 | ✅ DONE | Modified in notebook explanation |
| B3 — Before/after reasons array for ORD-1006 | — | ⏳ PENDING USER | Run notebook twice, screenshot |
| B4 — PREDICTIONS.md committed first | — | ✅ DONE | Commit `d614c3b` |
| B4 — Run Arjun event and fill table | 7 | ⏳ PENDING USER | Run notebook, fill PREDICTIONS.md |
| B4 — row_hash/MERGE/idempotency explanation | — | ✅ DONE | See Written Answers below |
| B5 — Sixth quality check added | 6 | ✅ DONE | See Written Answers below |
| B5 — Mock failure + PROBLEM output | — | ⏳ PENDING USER | Add mock order, run, screenshot |
| B5 — ELT vs ETL explanation | — | ✅ DONE | See Written Answers below |

---

## Part C: Mage ML Pipeline (20 marks)

| Item | Marks | Status | Evidence location |
|------|-------|--------|-------------------|
| C1 — Block graph (Mermaid) | 4 | ✅ DONE | See Written Answers below |
| C1 — `mage run iris_project iris_classifier --test` output | — | ⏳ PENDING USER | Run in Colab, copy output |
| C2 — max_depth 1–5 table | 6 | ⏳ PENDING USER | Run with `--runtime-vars` for each |
| C2 — Explanation of @test gate | — | ✅ DONE | See Written Answers below |
| C3 — evaluate_model block added | 5 | ✅ DONE | `iris_project/transformers/evaluate_model.py` |
| C3 — metadata.yaml with two downstreams | — | ✅ DONE | `iris_project/pipelines/iris_classifier/metadata.yaml` |
| C3 — Screenshot: Mage UI graph | — | ⏳ PENDING USER | Open Mage UI, screenshot graph |
| C3 — Confusion matrix + metrics table | — | ⏳ PENDING USER | Copy from mage run output |
| C4 — Extra block (`evaluate_model`) with @test | 5 | ✅ DONE | `evaluate_model.py` committed |
| C4 — CI still green after C4 commit | — | ✅ DONE | pytest doesn't test Mage blocks directly |

---

## Part D: RabbitMQ Stream (20 marks)

| Item | Marks | Status | Evidence location |
|------|-------|--------|-------------------|
| D1 — Routing table (all 6 rows) | 6 | ✅ DONE | PREDICTIONS.md + Written Answers |
| D1 — Q6 explanation (2-word key) | — | ✅ DONE | PREDICTIONS.md |
| D2 — `dispatcher.py` written | 8 | ✅ DONE | `stream/dispatcher.py` |
| D2 — `driver.py` written | — | ✅ DONE | `stream/driver.py` |
| D2 — Console logs (2-min run with 3+ drivers) | — | ⏳ PENDING USER | Run in Colab, copy logs |
| D3 — NACK for missing zone | 6 | ✅ DONE | Built into `driver.py` |
| D3 — Console logs showing NACK | — | ⏳ PENDING USER | Run with bad messages (every 10th) |
| D3 — Answers on crash/requeue | — | ✅ DONE | See Written Answers below |

---

## Part E: Report (15 marks)

| Item | Marks | Status | Evidence location |
|------|-------|--------|-------------------|
| Report PDF (≤8 pages) | 15 | ⏳ PENDING — need roll number & name | Will produce `RollNo_Name_Pipelines.pdf` |
| Integration diagram | — | ✅ DONE | Mermaid diagram in Written Answers |
| Reflection (from BREAKS.md) | — | ✅ DONE | BREAKS.md |

---

## Bonus: Stream into the Lakehouse (+10)

| Item | Marks | Status |
|------|-------|--------|
| Consumer → write_landing() → load_file() → gold | +10 | ⏳ After everything else |

---

## Screenshot Checklist (in order)

1. **A3-GREEN**: GitHub Actions tab, green checkmark after first push
2. **A3-RED**: GitHub Actions tab, red ❌ after changing `test_size=0.3`
3. **A3-FIX**: GitHub Actions tab, green ✅ after reverting fix
4. **B1-BRONZE**: `SELECT * FROM bronze.orders_raw` (8 rows)
5. **B1-SILVER**: `SELECT * FROM silver.orders_clean` (6 rows)
6. **B1-QUARANTINE**: `SELECT * FROM quarantine.orders` (2 rows: ORD-1004, ORD-1006)
7. **B1-DEDUP**: `SELECT * FROM silver.orders_dedup` (4 rows)
8. **B1-GOLD**: Gold totals (4 orders, ₹7,785.00, 126 points)
9. **B3-BEFORE**: reasons array for ORD-1006 before adding unsupported_currency
10. **B3-AFTER**: reasons array for ORD-1006 after (should include unsupported_currency)
11. **B4-SCD2**: `SELECT * FROM dim.customers_scd2` after Arjun event
12. **B4-GOLD**: Gold totals after Arjun event
13. **B5-FAIL**: quality_checks() showing PROBLEM for the new check
14. **B5-PASS**: quality_checks() back to 0 after removing mock order
15. **C1-MAGE-RUN**: Terminal output of `mage run iris_project iris_classifier --test`
16. **C2-TABLE**: One screenshot per max_depth (or one combined table)
17. **C3-MAGE-UI**: Mage UI pipeline graph showing 4 blocks + evaluate branch
18. **D2-CONSOLE**: Combined console logs of dispatcher + 3 drivers for 2 minutes
19. **D3-NACK**: Log showing `NACK (missing zone)` for bad messages
