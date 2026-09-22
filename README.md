# Real Estate Management System (Odoo 19.4)

[![Odoo Version](https://img.shields.io/badge/Odoo-19.4%20(saas--19.4)-714B67?logo=odoo&logoColor=white)](https://www.odoo.com)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

A modular, enterprise-grade Real Estate management application built for **Odoo 19.4** following the official **Odoo Developer Tutorial (*Server Framework 101*)** from Chapter 2 through Chapter 14.

This repository features both the core business application (`estate`) and the accounting link module (`estate_account`), completely modernized for Odoo 19+ standards (including `models.Constraint`, unified `ir.access`, and modern QWeb card templates).

---

## What is Odoo?

**[Odoo](https://www.odoo.com)** is an open-source, fully integrated suite of business management applications (ERP / CRM) designed to streamline and automate company workflows across sales, accounting, inventory, manufacturing, human resources, and project management.

### Key Architectural Pillars of Odoo:
1. **Model-View-Controller (MVC) Framework**:
   - **Models (PostgreSQL / Python ORM)**: Business logic, declarative relational fields (`Many2one`, `One2many`, `Many2many`), computed fields with automatic dependency tracking (`@api.depends`), and database-level validation.
   - **Views (XML / QWeb / OWL)**: Declarative UI rendering across Form, List, Search, Kanban, Pivot, Graph, and Calendar views.
   - **Controllers (HTTP / JSON-RPC / REST)**: Web controllers handling routing, portal interfaces, API endpoints, and client-server communication.
2. **Extreme Modularity & Inheritance**:
   - Applications are built as isolated, pluggable modules (addons).
   - Any module can extend or alter existing behavior without modifying upstream source code via Python class inheritance (`_inherit`), model delegation (`_inherits`), view XPaths, and method chaining (`super()`).
3. **Enterprise Security & Multitenancy**:
   - Fine-grained security layers combining Model Access Controls (`ir.access`), Record Rules (row-level filtering via domain criteria), and Field-Level Access Control.
4. **Rich Templating & Component System**:
   - Server-side and client-side templating powered by **QWeb**, alongside a modern reactive UI component framework powered by **OWL (Odoo Web Library)**.

---

## Repository Modules

This repository contains two decoupled modules:

### 1. `estate` (Real Estate Core)
The primary real estate advertisement application:
- **Property Management**: Track properties with pricing, address, surface areas, garage, garden, and availability dates.
- **Offer & Negotiation Flow**: Receive bids, calculate deadlines/validity dynamically, enforce price progression, and execute Accept/Refuse workflows.
- **Categorization**: Property types with drag-and-drop sequencing handle and property tags with customizable color palettes.
- **Views**:
  - **Kanban View**: Grouped by property type, drag-and-drop disabled, with conditional pricing display.
  - **List View**: Inline editing, optional columns, and semantic color decorations (`decoration-success`, `decoration-bf`, `decoration-muted`).
  - **Form View**: Dynamic statusbar, smart button stat counters, action buttons with state-based visibility, and notebook tabs.
  - **Search View**: Search by title, type, postcode, minimum living area filter domain, predefined filters, and grouping options.
- **Salesperson Integration**: Extends standard user profile (`res.users`) to display managed active properties.

### 2. `estate_account` (Invoicing Link Module)
A bridge module that connects `estate` with Odoo's core Invoicing (`account`) app:
- Listens to property sale transitions (`action_sold`).
- Automatically creates a draft Customer Invoice (`account.move` of type `out_invoice`) assigned to the property buyer.
- Invoices two distinct line items using `Command.create()`:
  1. **Commission**: 6% of the property's selling price.
  2. **Administrative Fee**: Flat 100.00 administrative fee.

---

## Tutorial Roadmap & Commit Progression

The repository follows a clean, sequential commit history corresponding to each tutorial chapter:

| Chapter | Title | Scope & Features |
|:---|:---|:---|
| **Ch. 2** | *A New Application* | Git setup, module manifest (`__manifest__.py`), category `"Real Estate"`, and entrypoint. |
| **Ch. 3** | *Models and Basic Fields* | `estate.property` model definition with scalar fields and ORM configuration. |
| **Ch. 4** | *Security - A Brief Intro* | Access control rules granting CRUD permissions to base users. |
| **Ch. 5** | *Finally, Some UI To Play With* | Default field values, window actions, and 3-level menu hierarchy. |
| **Ch. 6** | *Basic Views* | Custom Form, List, and Search view architectures. |
| **Ch. 7** | *Relations Between Models* | `estate.property.type`, `estate.property.tag`, and `estate.property.offer` with relational fields. |
| **Ch. 8** | *Computed Fields and Onchanges* | `@api.depends` total area and best price; `@api.onchange` garden area; inverse validity computation. |
| **Ch. 9** | *Ready For Some Action?* | Property state transitions (Sold/Cancel) and offer Accept/Refuse business workflows. |
| **Ch. 10** | *Constraints* | Database-level SQL constraints (`models.Constraint`) and Python constraints (`@api.constrains`). |
| **Ch. 11** | *Add The Sprinkles* | Editable lists, widgets (color picker, statusbar, handle), options, smart button stat counters, and decorations. |
| **Ch. 12** | *Inheritance* | CRUD overrides (`@api.ondelete`, `create`), model extension on `res.users`, and view inheritance on `base.view_users_form`. |
| **Ch. 13** | *Interact With Other Modules* | Decoupled link module `estate_account` generating automated customer invoices on sale. |
| **Ch. 14** | *A Brief History Of QWeb* | Property Kanban view with QWeb `<t t-name="card">`, default grouping, and conditional tags. |

---

## Modern Odoo 19+ Technical Highlights

### 1. `models.Constraint` vs Deprecated `_sql_constraints`
In Odoo saas-19.4 / 20.0+, the legacy `_sql_constraints` attribute was deprecated and removed. All database constraints are declared as class attributes:
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

### 2. Unified Access Rights (`ir.access.csv`)
Odoo 19.4 unified model access and rules into `ir.access`:
```csv
id,name,model_id:id,group_id:id,operation,domain
access_estate_property,estate.property,model_estate_property,base.group_user,crud,
access_estate_property_type,estate.property.type,model_estate_property_type,base.group_user,crud,
access_estate_property_tag,estate.property.tag,model_estate_property_tag,base.group_user,crud,
access_estate_property_offer,estate.property.offer,model_estate_property_offer,base.group_user,crud,
```

### 3. Modern Kanban Card Architecture
Uses Odoo 19's `<t t-name="card">` syntax with conditional rendering:
```xml
<kanban default_group_by="property_type_id" records_draggable="0">
    <field name="state"/>
    <templates>
        <t t-name="card">
            <div>
                <strong><field name="name"/></strong>
            </div>
            <div>
                Expected Price: <field name="expected_price"/>
            </div>
            <div t-if="record.state.raw_value == 'offer_received'">
                Best Price: <field name="best_price"/>
            </div>
            <div t-if="record.state.raw_value == 'offer_accepted'">
                Selling Price: <field name="selling_price"/>
            </div>
            <div>
                <field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
            </div>
        </t>
    </templates>
</kanban>
```

---

## Directory Structure

```text
Real-Estate-Odoo-19.4/
├── README.md
├── .gitignore
├── estate/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── estate_property.py
│   │   ├── estate_property_offer.py
│   │   ├── estate_property_tag.py
│   │   ├── estate_property_type.py
│   │   └── res_users.py
│   ├── security/
│   │   └── ir.access.csv
│   └── views/
│       ├── estate_menus.xml
│       ├── estate_property_offer_views.xml
│       ├── estate_property_tag_views.xml
│       ├── estate_property_type_views.xml
│       ├── estate_property_views.xml
│       └── res_users_views.xml
└── estate_account/
    ├── __init__.py
    ├── __manifest__.py
    └── models/
        ├── __init__.py
        └── estate_property.py
```

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Odoo 19.4 (saas-19.4 or compatible)

### Step 1: Clone Repository
```bash
git clone git@github.com:catmuf/Real-Estate-Odoo-19.4.git
```

### Step 2: Configure Addons Path
Add the repository path to your `odoo.conf`:
```ini
addons_path = /path/to/odoo/addons,/path/to/Real-Estate-Odoo-19.4
```

### Step 3: Install Modules
```bash
# Install core Real Estate application
python3 odoo-bin -c odoo.conf -d <your-database> -i estate

# Install Invoicing link module (automatically loads account module if not installed)
python3 odoo-bin -c odoo.conf -d <your-database> -i estate_account
```

### Step 4: Upgrading After Changes
```bash
python3 odoo-bin -c odoo.conf -d <your-database> -u estate,estate_account --stop-after-init
```

---

## License

This project is licensed under the **GNU Lesser General Public License v3.0 (LGPL-3)**.
