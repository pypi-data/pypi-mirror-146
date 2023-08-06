# Alice-CI

Continous Integration framework with the goal of using the exact same code in CI and local env. Steps can be defined in yaml files, for syntax see the docs. Runs on LInux and Windows, Mac should work too, but not yet tested.

## Usage

Install with pip:
```
pythom3 -m pip install alice-ci
```

To run:

```
pythom3 -m alice [-i <ci.yaml>] STEPS
```