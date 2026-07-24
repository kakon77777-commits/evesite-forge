# EveSite Forge

**Schema-Driven Universal Site Generator**  
**結構驅動的通用網站生成器**

[Live site](https://kakon77777-commits.github.io/evesite-forge/) · [Theory Interface](https://kakon77777-commits.github.io/evesite-forge/sites/theory-interface/) · [GWSM](https://kakon77777-commits.github.io/evesite-forge/sites/gwsm/)

EveSite Forge turns structured theories, products, documents, observatories, and site-group definitions into governed public interfaces.

It began as **Theory Interface Generator v0.1** and now treats theory interfaces as the first reference site type rather than the boundary of the project.

## Core model

```text
Structured source
    ↓
Schema + site type + modules
    ↓
Generator and validator
    ↓
Deployable static site
    ↓
Site-group catalog and governance
```

## Current reference sites

- **The Interface Transformation of Theory** — maturity-ladder module.
- **Game Wave Semantic Model** — weighted-risk module.

The live catalog is deployed through GitHub Pages from `public/`.

## Build

```bash
python tests/validate_examples.py
python scripts/build_all.py
python -m http.server 8000 --directory public
```

Then open:

```text
http://localhost:8000/
http://localhost:8000/sites/theory-interface/
http://localhost:8000/sites/gwsm/
```

## Repository map

```text
core/           generator implementation
schemas/        structured contracts
site-types/     site-type definitions
modules/        interaction module registry
examples/       source data and authoritative documents
scripts/        build orchestration
public/         deployable root
registry/       site-group metadata
docs/           research and specification documents
tests/          validation
```

## Current boundary

v0.1 proves that one schema-driven generator can produce distinct theory sites with different interaction models. It does not yet prove that one schema can represent every knowledge domain or website family without loss.

## License

MIT License. Research documents retain attribution to their named authors and organizations.
