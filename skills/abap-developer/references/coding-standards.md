# ABAP Code Style Standard

Source: Vincit `GUIDELINES_ABAP.md`. Strictly adhere to the official SAP Clean ABAP style guide:
Reference: https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md

## Core Clean ABAP Directives

1. **Prefer Expression over Statement** — use internal table expressions, string templates, and modern constructor operators (`VALUE`, `REDUCE`, `FILTER`, `COND`, `SWITCH`) rather than legacy multi-line statements.
2. **Keep Methods Small** — methods should do exactly one thing. If a method exceeds 20–30 lines, refactor or split it.
3. **Descriptive Naming** — favor readable English names over cryptic abbreviations. Avoid excessive Hungarian notation if modern types make it obvious (e.g. `customers` instead of `lt_kna1`).
4. **No Obsolete Language Elements** — never use `MOVE`, `ADD`, `SUBTRACT`, `READ TABLE` (unless table expressions can't handle it), or `RANGES`.
5. **Fail Fast** — use class-based exceptions. Return early from methods using `RETURN` or `CHECK` instead of nesting deep `IF`/`ELSE` blocks.

## Class Preference

Prefer class-based ABAP (methods/classes) over reports/includes wherever possible — easier to unit test and keeps logic modular. See `unittest-guidelines.md` for the matching test generation rule.
