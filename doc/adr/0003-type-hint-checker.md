# 3. Type Hint Checker

Date: 2022-05-21

## Status

Accepted

## Context

Since python is a dynamically typed language, it's safer to use extra type hinting tools to check the type of the
variables.

There are lots of type hinting tools:

- mypy
- pyre
- pytype
- ...

## Decision

I decided to install

1. [mypy](https://mypy.readthedocs.io/en/stable/) is a linter to check the type of the variables.
   => mypy is more senior than pyre and pytype.
2. [pydantic](https://pydantic-docs.helpmanual.io/) prevents the error-typed variables in compile time.

### 1. Install mypy

```bash
pip install mypy
```

Add setting to `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

### 2. Install pydantic

```bash
$ pip install pydantic
```

## Consequences

N/A

## References

- [Type hints cheat sheet (Python 3) - mypy 0.950 documentation](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html#cheat-sheet-py3)
