# BREAKS.md
# Every real error that happened during this project — cause and fix.
# Used for Part E (half-page reflection). DO NOT invent stories.

---

## Break 1 — ModuleNotFoundError: No module named 'mage_ai'

**When:** 2026-11-15, while running `pytest tests/` locally (Part A3)

**What happened:**
`tests/test_prepare_data.py` imports `prepare_data.transform`.
`prepare_data.py` used an `if 'transformer' not in globals()` guard to avoid importing Mage.
But the guard used `globals()` *at module level before the decorator was applied*, so it evaluated to True immediately and tried to `from mage_ai.data_preparation.decorators import transformer` anyway.
Since `mage-ai` is not installed locally, the import failed with:
```
ModuleNotFoundError: No module named 'mage_ai'
```

**How we found it:**
Running `python -m pytest tests/ -v` showed the import traceback pointing to line 10 of `prepare_data.py`.

**Fix:**
Replaced the `if not in globals()` guard with a `try/except ImportError` that provides no-op decorator functions when Mage is not installed:
```python
try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn
```
After the fix: `1 passed in 0.66s` ✅

**What I learned:**
Python's `globals()` at module load time does not know about decorators that will be applied later. The correct pattern for "importable outside Mage" is `try/except ImportError`.

---

*More breaks will be added as they happen.*
