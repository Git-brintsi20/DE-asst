# Viva Cheat Sheet — 15 Most Likely Questions

> Short answers, plain language. Reread before the viva.

---

**1. After `git commit`, can your teammate see the code on GitHub?**
No. `git commit` saves to the *local* repo only (the `.git/` folder on your laptop). The teammate sees it only after `git push` uploads the commits to GitHub.

---

**2. What is the difference between `git add` and `git commit`?**
`git add` moves a file into the staging area — it's queued for the next commit but nothing is saved yet. `git commit` takes everything in the staging area and saves it as a permanent snapshot in the local repo with a unique hash.

---

**3. What does the GitHub Actions CI workflow do, and why is the red run useful?**
On every push: check out the code → install Python 3.12 + dependencies → run `pytest`. The red run proves the test actually catches the bug. If the test always passes, you can't trust it. By deliberately breaking `test_size=0.3`, you confirm the test is real.

---

**4. What is ELT and how does it differ from ETL? Why is ELT better for FreshCart?**
ETL transforms data *before* loading it; ELT loads raw data first, then transforms it *inside* the warehouse. For FreshCart, Snowflake's SQL is very fast — it's cheaper and faster to transform there than on a local server. Also, you keep the raw data in bronze so you can re-run the SQL if you fix a bug.

---

**5. What is the purpose of the bronze layer?**
It stores raw data exactly as received, with no cleaning. It acts as a permanent audit trail. If the cleaning SQL has a bug, you can fix it and re-replay from bronze without hitting the source API again.

---

**6. How does `QUALIFY ROW_NUMBER()` dedup ORD-1003?**
Both web and mobile records for ORD-1003 are grouped by `PARTITION BY order_id`. Inside that group, `ORDER BY updated_at DESC` puts the mobile record first (it has a later timestamp). `ROW_NUMBER() = 1` picks only the first row in each group — the mobile record with the amount. The web record (null amount, earlier timestamp) is discarded.

---

**7. What is SCD Type 2 and why does `dim.customers_scd2` use it?**
SCD2 (Slowly Changing Dimension Type 2) keeps a full history of changes. Each tier change creates a new row with `valid_from` and `valid_to` dates. This lets you answer "what tier was this customer on the date of this order?" — which is exactly what the point-in-time join in `SQL_40_GOLD` does.

---

**8. What is `row_hash` and why does it make gold idempotent?**
`row_hash` is a hash of all meaningful columns in a gold row. The MERGE compares the hash of the incoming data to the hash stored in gold. If they match, nothing is updated — the row is unchanged. If the hash changes (e.g. because loyalty_points changed), only that row is updated. This means you can run the pipeline 10 times and get the same result — it never duplicates rows or double-counts revenue.

---

**9. Why does bronze grow by 8 rows on every run but gold stays the same?**
`COPY INTO bronze.orders_raw` just appends — it keeps every file it receives. This is intentional: bronze is an append-only audit log. Gold uses MERGE with `row_hash`, so re-loading the same data produces no change in gold. Different design goals: bronze = never lose anything; gold = always reflect the current truth.

---

**10. How does a failing `@test` in Mage stop `save_results` from running?**
Mage runs blocks in dependency order. If `train_model`'s `@test` raises an exception, Mage marks `train_model` as failed and does not run any downstream blocks. `save_results` is downstream, so it never executes — `iris_predictions.csv` is never created. This is better than saving first because there is no bad file to clean up.

---

**11. What does `max_depth` control in the Decision Tree, and why does depth 1 fail?**
`max_depth` limits how many levels the tree can have. At depth 1 (a stump), the model can only make one binary split — it can't learn the complex boundaries between all three Iris species. Accuracy falls below 85%, the `@test` fails, and `save_results` doesn't run. At depth 3+ the model is complex enough to separate the classes and passes.

---

**12. What is a topic exchange in RabbitMQ, and what do `*` and `#` mean?**
A topic exchange routes messages by matching the routing key (like `bangalore.koramangala.food`) against each queue's binding pattern. `*` matches exactly one word (one dot-delimited segment). `#` matches zero or more words. Example: `bangalore.#` matches `bangalore`, `bangalore.koramangala`, and `bangalore.koramangala.food`.

---

**13. Why does `bangalore.koramangala` (2 words) only reach Control?**
Ravi's pattern `bangalore.koramangala.*` needs a third word — `*` can't match nothing. Arjun's `bangalore.*.ride` also needs a third word (`ride`). Control's `bangalore.#` matches zero or more words after `bangalore`, so `koramangala` counts. Only Control's queue receives the message.

---

**14. What happens if a driver crashes before sending an ACK?**
RabbitMQ tracks unacknowledged messages. When the driver's connection drops, the message is returned to the queue and re-delivered to the next available consumer. This guarantees *at-least-once* delivery — no message is lost just because a consumer crashed.

---

**15. What is a poison message and why is `requeue=False` safer?**
A poison message is one that always fails processing (e.g. missing a required field). With `requeue=True`, the bad message bounces back and is re-delivered endlessly — a loop that wastes resources and blocks good messages. With `requeue=False`, the bad message is discarded (or sent to a Dead-Letter Exchange for investigation), so the queue keeps moving.
