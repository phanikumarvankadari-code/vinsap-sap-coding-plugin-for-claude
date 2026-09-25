# Package Hierarchy & Naming

Source: Vincit `GUIDELINES_ABAP.md`.

All transportable SAP objects belong inside the `ZMASTER` tree. Never create a top-level `Z*` package — once code leaves `$TMP` per `transport-guidelines.md` §3 it must land in a `ZMASTER_*` package.

```
ZMASTER                              Root, Structure pkg
├── ZMASTER_CORE                     Cross-cutting (DDIC / UTIL / INT)
└── ZMASTER_<AREA>                   Solution-area Structure pkg
    └── ZMASTER_<AREA><APP><LAYER>   Leaf development pkg
```

1. **Solution-area codes** — classical ECC module codes, not invented ones: `FI` Finance · `SD` Sales & Distribution · `MM` Materials Management · `PP` Production Planning · `LE` Logistics Execution · `HR` Human Resources · `AA` Asset Accounting · `CS` Customer Service · `CORE` shared (not a real module, cross-cutting only). Adding a new area requires the user's explicit approval.

2. **Layer codes** — use exactly these four, and only these: `DDIC` types & DDIC objects · `DB` CDS/AMDP/table access · `APP` business logic (no `SELECT`, no UI) · `UI` reports, OData/Fiori projections, ALV controllers.

3. **Layer dependency rule** — a package at layer `X` may consume only layers below it: `UI → APP → DB → DDIC`. `CORE` is reachable from any layer. Reverse access is forbidden and must not be unlocked via Use Access.

4. **Encapsulation flags** — every `ZMASTER_*` package must have *Package Use Access Controlled* = X and *Package Encapsulated* = X. Any cross-package consumer requires an explicit Use Access entry; surface the entry to the user before activation.

5. **One application per `<APP>` token** — a self-contained capability (a report, a Fiori app, a background job, an interface) lives under a single `<APP>` namespace with its own layer packages. Empty layers are *omitted*, never repurposed.

6. **Object-name prefix tracks the package** — objects carry the area+app token from their package. Examples:
   - Class in `ZMASTER_SD_OSOSTK_APP` → `ZCL_SD_OSOSTK_<role>`
   - Interface in same package → `ZIF_SD_OSOSTK_<role>`
   - CDS in `ZMASTER_SD_OSOSTK_DB` → `ZR_SdOsoStk_<entity>` (RAP root) / `ZC_SdOsoStk_<entity>` (consumer)
   - Report in `..._UI` → `ZADT_SD_OSOSTK_<name>`

7. **30-character cap** — SAP package names are capped at 30 chars. Abbreviate the `<APP>` token (max 8 chars, drop vowels if needed), never the `ZMASTER_<AREA>_` prefix.

8. **Application Component attribute** — set the *Application Component* on each `ZMASTER_<AREA>` structure pkg to the matching SAP standard (`SD-SLS`, `FI-GL`, `MM-PUR`, `PP-SFC`, `LO-MD`, `PA-PA`, …). Leaf packages inherit it; do not override at leaf level.

9. **Creation order** — when starting a new application, create packages bottom-up: `DDIC → DB → APP → UI`. Skipping straight to `UI` is forbidden; if `DB` or `APP` would be empty, omit them, do not collapse their contents upward.
