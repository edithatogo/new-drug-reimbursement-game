# Python style

- Follow Ruff and the `ty`/basedpyright configuration in `pyproject.toml`.
- Run `ty check src` routinely and `basedpyright` before opening or
  updating a pull request.
- Use typed public APIs, standard exceptions, immutable defaults, and clear control flow.
- Group imports as standard library, third party, and local.
- Use `snake_case` for functions and variables, `PascalCase` for classes, and
  `UPPER_CASE` for constants.
- Give executable modules a `main()` entry point.
