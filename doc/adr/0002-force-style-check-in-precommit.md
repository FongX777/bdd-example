# 2. Force Style Check in Precommit

Date: 2022-05-21

## Status

Accepted

## Context

I want to make sure my python code is formatted correctly and follow the PEP8 guide.
Also, I want other collaborators can follow the same guide and don't break the coding style.

## Decision

I decided to install `pre-commit` to make sure code in every commit is formatted correctly.

Tools I've installed in `.pre-commit-config.yaml`:

- `pre-commit-hooks` fix some editor's style
- `mirrors-isort` sorts imports
- `autoflake` removes unused imports and unused variables from Python code.
- `flake8` checks Python code for style errors.
- `mirrors-yapf` re-formats code according to PEP8.

**NOTE1**: the order of the tools is important, because they might be conflict.

**NOTE2**: don't forget to run `pre-commit install --install-hooks` overwrite current pre-commit behavior
in `.git/hooks/pre-commit`

## Consequences

## References

- [pre-commit](https://pre-commit.com/)
- [用 pre-commit 提升程式碼品質 | My.APOLLO](https://myapollo.com.tw/zh-tw/pre-commit-the-best-friend-before-commit/)
