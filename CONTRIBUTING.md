# Contributing

EveSite Forge is currently an early reference implementation.

Before proposing a new site type or interactive module:

1. state the public meaning it exposes;
2. define its structured input fields;
3. provide a non-interactive fallback;
4. identify evidence and limitation requirements;
5. add at least one reference example;
6. keep the core generator free of unnecessary runtime dependencies.

Run before opening a pull request:

```bash
python tests/validate_examples.py
python scripts/build_all.py
```
