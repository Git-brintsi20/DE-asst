# freshcart-pipelines

**Assignment: From Git to Gold** — Data Engineering, 100 marks + 10 bonus.

This repository contains four interconnected components of a modern data platform:

| Folder | Contents | Assignment Part |
|--------|----------|-----------------|
| `elt/` | FreshCart ELT notebook (Snowflake bronze → silver → gold) | Part B |
| `iris_project/` | Mage ML pipeline (Iris classifier with block tests) | Part C |
| `stream/` | RabbitMQ dispatcher and driver scripts | Part D |
| `tests/` | pytest test for the CI pipeline | Part A |
| `.github/workflows/` | GitHub Actions CI workflow | Part A |

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your credentials — **never commit `.env`**.

## Running the pipeline

- **Part B (ELT):** Open `elt/freshcart_elt.ipynb` in Google Colab and run top to bottom.
- **Part C (Mage):** `mage run iris_project iris_classifier --test`
- **Part D (Stream):**
  ```bash
  python stream/dispatcher.py &
  python stream/driver.py Ravi "bangalore.koramangala.*"
  python stream/driver.py Priya "bangalore.indiranagar.*"
  python stream/driver.py Control "bangalore.#"
  ```
- **Tests:** `pytest tests/`

## Repository structure

```
freshcart-pipelines/
├── README.md
├── .gitignore
├── requirements.txt
├── elt/
│   └── freshcart_elt.ipynb
├── iris_project/
│   ├── data_loaders/load_iris.py
│   ├── transformers/prepare_data.py
│   ├── transformers/train_model.py
│   ├── transformers/evaluate_model.py
│   ├── data_exporters/save_results.py
│   └── pipelines/iris_classifier/metadata.yaml
├── stream/
│   ├── dispatcher.py
│   └── driver.py
├── tests/
│   └── test_prepare_data.py
└── .github/workflows/ci.yml
```

## GitHub repo
https://github.com/Git-brintsi20/DE-asst
