# ABAP Unit Testing Guidelines

Source: Vincit `GUIDELINES_UNITTEST.md`. When generating or refactoring logic, automatically create or update accompanying ABAP Unit tests according to these standards:

1. **Class Decorators** — always declare test classes with `FOR TESTING DURATION SHORT RISK LEVEL HARMLESS`.
2. **Behavioral Structuring** — structure test methods using the AAA pattern:
   - **Arrange (Given)** — set up mock data structures and local configurations.
   - **Act (When)** — trigger exactly one call to the Component Under Test (CUT).
   - **Assert (Then)** — run focused assertions using `cl_abap_unit_assert`.
3. **No Database Dependencies** — if a method requires DB records, refactor the dependency out via an interface layer, or use a test injection constructor. Do not write tests that execute native `SELECT` statements on real tables.
4. **Naming Template** — name test methods using the pattern: `method_given_scenario_expect_outcome`.

## Example

```abap
CLASS lcl_test_discount_engine DEFINITION FOR TESTING
  DURATION SHORT
  RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    DATA mo_cut TYPE REF TO zcl_discount_engine. " Component Under Test

    METHODS setup.
    METHODS calculate_given_vip_expect_20_pct FOR TESTING.
    METHODS calculate_given_new_expect_0_pct FOR TESTING.
ENDCLASS.

CLASS lcl_test_discount_engine IMPLEMENTATION.
  METHOD setup.
    " Arrange: Create instance before every test cycle
    mo_cut = NEW #( ).
  ENDMETHOD.

  METHOD calculate_given_vip_expect_20_pct.
    " Act
    DATA(lv_discount) = mo_cut->get_rate( iv_customer_type = 'VIP' ).

    " Assert
    cl_abap_unit_assert=>assert_equals(
      act = lv_discount
      exp = '0.20'
      msg = 'VIP customers must receive a baseline 20% discount rate.' ).
  ENDMETHOD.

  METHOD calculate_given_new_expect_0_pct.
    " Act
    DATA(lv_discount) = mo_cut->get_rate( iv_customer_type = 'NEW' ).

    " Assert
    cl_abap_unit_assert=>assert_initial(
      act = lv_discount
      msg = 'New customers should start with a 0% discount.' ).
  ENDMETHOD.
ENDCLASS.
```
