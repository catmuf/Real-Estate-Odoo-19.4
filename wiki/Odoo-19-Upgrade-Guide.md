# Odoo 19+ Modernization & Upgrade Guide

This guide details the major framework differences between Odoo 14–17 and Odoo 19.4 (saas-19.4 / 20.0), and how this codebase was developed to strictly adhere to current and future Odoo architectural standards.

---

## 1. `models.Constraint` vs Deprecated `_sql_constraints`

In legacy Odoo versions, database constraints were defined as a list of 3-element tuples on the model:
```python
# DEPRECATED AND REMOVED IN ODOO 19+
_sql_constraints = [
    ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
    ('check_name', 'UNIQUE(name)', 'The name must be unique'),
]
```

### The Modern Odoo 19+ Way:
In modern Odoo, constraints are instantiated as declarative class attributes using `models.Constraint`:
```python
_check_expected_price = models.Constraint(
    "CHECK(expected_price > 0)",
    "The expected price must be strictly positive",
)

_check_selling_price = models.Constraint(
    "CHECK(selling_price >= 0)",
    "The selling price must be positive",
)

_check_name = models.Constraint(
    "UNIQUE(name)",
    "The name must be unique",
)
```

**Advantages**:
- Can be cleanly inherited and overridden in child modules without string-matching tuple lists.
- Directly integrated into Odoo's modern table object manager (`odoo/orm/table_objects.py`).

---

## 2. Unified Security Model (`ir.access.csv`)

In Odoo 19.4+, access controls have been unified under the `ir.access` model:
```csv
id,name,model_id:id,group_id:id,operation,domain
access_estate_property,estate.property,model_estate_property,base.group_user,crud,
```
Attempting to load legacy `ir.model.access.csv` files raises `KeyError: 'ir.model.access'` on fresh databases.

---

## 3. Search View RelaxNG Schema Validation

Inside `<search>` views, `<group>` elements represent layout containers for filters and cannot contain `string="..."` or `expand="0"`:

```xml
<!-- INVALID IN ODOO 19 (Raises RelaxNG validation error) -->
<group string="Group By" expand="0">
    <filter string="Postcode" name="postcode" context="{'group_by': 'postcode'}"/>
</group>

<!-- VALID MODERN SYNTAX -->
<group>
    <filter string="Postcode" name="group_by_postcode" context="{'group_by': 'postcode'}"/>
</group>
```

Filter names must also avoid colliding with actual field names to avoid domain lookup ambiguities.

---

## 4. QWeb Kanban Card Architecture

In Odoo 19+, the root Kanban card template is named `card`:
```xml
<!-- Legacy syntax -->
<t t-name="kanban-box"> ... </t>

<!-- Modern Odoo 19+ standard -->
<t t-name="card"> ... </t>
```
All fields used inside conditionals (`t-if="record.state.raw_value == ..."`) must be explicitly declared before `<templates>` if they are not directly rendered as `<field>`.
