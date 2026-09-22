# Chapters 1 to 6: Core Application Setup

This section covers the foundational construction of the Real Estate module, from scaffolding and ORM model creation to security access rights, window actions, menus, and basic view architectures.

---

## Chapter 1: Architecture Overview
- **Goal**: Understand the 3-tier architecture: PostgreSQL, Odoo server, and the web client.
- **Concepts**:
  - Addon discovery via `addons_path` in `odoo.conf`.
  - The registry loads models dynamically at startup.

---

## Chapter 2: A New Application
- **Goal**: Initialize the module structure.
- **Files Created**:
  - `estate/__init__.py`: Package entrypoint importing `models`.
  - `estate/__manifest__.py`:
    ```python
    {
        'name': 'Real Estate',
        'version': '1.0',
        'category': 'Real Estate',
        'author': 'Catmuf',
        'summary': 'Real estate advertisement module',
        'depends': ['base'],
        'data': [],
        'installable': True,
        'application': True,
        'license': 'LGPL-3',
    }
    ```
- **Commit**: `3a3daad Chapter 2: A New Application`

---

## Chapter 3: Models and Basic Fields
- **Goal**: Create the primary database table `estate_property`.
- **Implementation**:
  ```python
  class EstateProperty(models.Model):
      _name = "estate.property"
      _description = "Real Estate Property"

      name = fields.Char(string="Title", required=True)
      description = fields.Text(string="Description")
      postcode = fields.Char(string="Postcode")
      date_availability = fields.Date(string="Available From")
      expected_price = fields.Float(string="Expected Price", required=True)
      selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
      bedrooms = fields.Integer(string="Bedrooms")
      living_area = fields.Integer(string="Living Area (sqm)")
      facades = fields.Integer(string="Facades")
      garage = fields.Boolean(string="Garage")
      garden = fields.Boolean(string="Garden")
      garden_area = fields.Integer(string="Garden Area (sqm)")
      garden_orientation = fields.Selection(
          selection=[
              ("north", "North"),
              ("south", "South"),
              ("east", "East"),
              ("west", "West"),
          ],
          string="Garden Orientation",
      )
  ```
- **Commit**: `b644772 Chapter 3: Models And Basic Fields`

---

## Chapter 4: Security – A Brief Introduction
- **Goal**: Grant access permissions to standard users.
- **Implementation (`estate/security/ir.access.csv`)**:
  ```csv
  id,name,model_id:id,group_id:id,operation,domain
  access_estate_property,estate.property,model_estate_property,base.group_user,crud,
  ```
- **Commit**: `8e450cd Chapter 4: Security - A Brief Introduction`

---

## Chapter 5: Finally, Some UI To Play With
- **Goal**: Add default values, reserved attributes, window actions, and menus.
- **Implementation**:
  - Added field defaults:
    - `bedrooms = 2`
    - `date_availability = fields.Date.today() + relativedelta(months=3)`
    - `active = fields.Boolean(default=True)` (archive support)
    - `state = fields.Selection(default='new')`
  - Created Window Action:
    ```xml
    <record id="estate_property_action" model="ir.actions.act_window">
        <field name="name">Properties</field>
        <field name="res_model">estate.property</field>
        <field name="view_mode">list,form</field>
    </record>
    ```
  - Created 3-level Menu Hierarchy in `views/estate_menus.xml`:
    - Root: `Real Estate`
    - Level 1: `Advertisements`
    - Action Item: `Properties`
- **Commit**: `93714c6 Chapter 5: Finally, Some UI To Play With`

---

## Chapter 6: Basic Views
- **Goal**: Build custom List, Form, and Search views.
- **Implementation (`estate/views/estate_property_views.xml`)**:
  - **List View (`<list>`)**:
    Displays tabular properties with title, postcode, bedrooms, living area, expected price, selling price, and availability date.
  - **Form View (`<form>`)**:
    Header title, two-column `<group>`, and `<notebook>` tab for Description.
  - **Search View (`<search>`)**:
    Quick filters for title, postcode, living area with filter domain `[('living_area', '>=', self)]`, custom "Available" filter, and group by postcode.
- **Commit**: `61d8e85 Chapter 6: Basic Views`
