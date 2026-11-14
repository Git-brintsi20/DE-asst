# WORKLOG.md
# Every action is logged here: what was done, which file it came from,
# what actually ran, and what is still pending for the user.

---

## 2026-11-15 — Phase 0: Inventory complete

### Files read
| File | Location | Purpose |
|------|----------|---------|
| `Assignment_DE.docx` | `material/` | Full assignment text, all parts A–E + Bonus |
| `freshcart_elt_simple_(1).ipynb` | `material/07-10-2026/` | FreshCart ELT notebook (used for Part B) |
| `Maze_ML_PipeLine.ipynb` | `Latest/Latest/28-10-2026/` | Mage ML pipeline notebook (used for Part C) |
| `freshcart_elt_flowchart.html` | `material/07-10-2026/` | ELT flowchart HTML |
| Various HTML slides | `material/30-09-2026/` | ETL/ELT/orchestration lecture slides |

### Key identifiers extracted from notebooks
- SQL steps: `SQL_00_SETUP`, `SQL_10_ORDERS_CLEAN`, `SQL_20_ORDERS_DEDUP`, `SQL_30_CUSTOMERS_SCD2`, `SQL_31_FX_DAILY`, `SQL_32_PINCODE_GEO`, `SQL_40_GOLD`
- Functions: `write_landing()`, `load_file()`, `run_pipeline()`, `quality_checks()`
- Tables: `bronze.orders_raw`, `silver.orders_checked`, `silver.orders_clean`, `silver.orders_dedup`, `silver.orders_enriched`, `dim.customers_scd2`, `ref.fx_daily`, `ref.pincode_geo`, `gold.fct_orders`, `quarantine.orders`
- Mage blocks: `load_iris`, `prepare_data`, `train_model`, `save_results`, `evaluate_model`
- Mage metadata: `iris_project/pipelines/iris_classifier/metadata.yaml`

---

## 2026-11-15 — Part A: Repo structure created

### What ran
- Created `c:\Users\HARSHI\Downloads\freshcart-pipelines\` with full structure
- Wrote: `.gitignore`, `README.md`, `requirements.txt`, `.env.example`
- Wrote: `.github/workflows/ci.yml` (Python 3.12, pytest on every push)
- Wrote: `tests/test_prepare_data.py` (exact test from assignment)
- Wrote: `iris_project/` with all 5 blocks + `metadata.yaml`
- Wrote: `stream/dispatcher.py` and `stream/driver.py`
- Copied: `elt/freshcart_elt.ipynb` from `material/07-10-2026/`

### Local pytest result
```
tests/test_prepare_data.py::test_split_is_80_20 PASSED   [100%]
1 passed in 0.66s
```
Source: ran `python -m pytest tests/ -v` locally ✅

### Git log (5 commits)
```
8910e06 ci: add pytest test for prepare_data and GitHub Actions CI workflow (Part A3)
9f2a593 feat(stream): add dispatcher.py and driver.py with ACK/NACK (Part D)
9a8cf6c feat(ml): add Mage iris_project — 4 blocks, evaluate branch, metadata.yaml (Part C)
e1d9d59 feat(elt): add FreshCart ELT notebook (Part B)
8d3fb96 chore: skeleton, .gitignore, README, requirements
```

### Pushed to
https://github.com/Git-brintsi20/DE-asst

---

## PENDING USER actions

### 1. Snowflake credentials (URGENT — needed before Part B can run)
Create `.env` in the repo root (copy `.env.example`) and fill in:
```
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
```
**DO NOT commit `.env`** — it is in `.gitignore`.

### 2. Run FreshCart notebook in Google Colab (Part B)
- Open `elt/freshcart_elt.ipynb` in Colab
- Run top to bottom
- Screenshots needed: (see ASSIGNMENT_CHECKLIST.md)

### 3. GitHub Actions green run (Part A3)
- After push: go to https://github.com/Git-brintsi20/DE-asst/actions
- Screenshot the green (✅) run

### 4. GitHub Actions red run (Part A3)
- Temporarily change `test_size=0.2` to `test_size=0.3` in `prepare_data.py`
- Commit and push → screenshot the red (❌) run
- Revert and push again → screenshot the green (✅) fix run

### 5. Mage pipeline run (Part C)
- In Colab (from Mage notebook): `mage run iris_project iris_classifier --test`
- Run with max_depth 1–5 using `--runtime-vars`
- Screenshot the Mage UI graph showing evaluate_model branch

### 6. RabbitMQ stream (Part D)
- Install RabbitMQ in Colab: `apt-get install -y rabbitmq-server`
- Run dispatcher + 3+ drivers for 2 minutes
- Screenshot console logs

### 7. Report PDF (Part E)
- I need: your roll number and full name
- Then I produce `RollNo_Name_Pipelines.pdf`
