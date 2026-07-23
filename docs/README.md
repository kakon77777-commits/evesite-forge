# EveSite Forge Documentation

## Core references

- [Theory Interface Schema v0.1](../examples/theory-interface/docs/Theory_Interface_Schema_v0.1.md)
- [The Interface Transformation of Theory v1.0](../examples/theory-interface/docs/Theory_Interface_Transformation_v1.0.md)
- [Game Wave Semantic Model v0.1](../examples/gwsm/docs/GWSM_v0.1.md)
- [GWSM Limitations & Unknowns](../examples/gwsm/docs/LIMITATIONS.md)

## Architecture

```text
Structured source
    ↓
Schema validation
    ↓
Site type selection
    ↓
Interaction modules
    ↓
Static projection
    ↓
Site-group registry and deployment
```

The authoritative structured sources for the current reference sites live under `examples/*/theory.json`. Generated websites are build artifacts and should not be edited as primary sources.
