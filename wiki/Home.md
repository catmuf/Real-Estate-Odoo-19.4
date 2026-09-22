# Real Estate Odoo 19.4 Developer Wiki

Welcome to the **Real Estate Odoo 19.4 Application Suite** documentation wiki. This wiki documents the end-to-end development of the third-party Real Estate suite built following Odoo's official **Server Framework 101** tutorial.

---

## 📚 Wiki Navigation

1. **[Architecture & Data Model](Architecture-and-Design)**
   - High-level 3-tier architecture
   - Entity-Relationship Diagram (ERD)
   - Property Lifecycle State Machine
   - Offer Acceptance Sequence Flow

2. **[Part 1: Core Application (Chapters 1 to 6)](Chapter-1-to-6-Core-Application)**
   - Chapter 1: Architecture Overview
   - Chapter 2: A New Application (Manifest, inits)
   - Chapter 3: Models and Basic Fields (`estate.property`)
   - Chapter 4: Security Access Rights (`ir.access.csv`)
   - Chapter 5: UI Configuration (Menus & Actions)
   - Chapter 6: Basic Views (List, Form, Search)

3. **[Part 2: Relations, Business Logic & Polish (Chapters 7 to 11)](Chapter-7-to-11-Relations-Workflows-UI)**
   - Chapter 7: Relational Models (`estate.property.type`, `tag`, `offer`)
   - Chapter 8: Computed Fields (`@api.depends`) & Onchanges (`@api.onchange`)
   - Chapter 9: Action Methods & State Transitions
   - Chapter 10: SQL Constraints (`models.Constraint`) & Python Constraints (`@api.constrains`)
   - Chapter 11: UI Sprinkles (Statusbar, Handle widget, Color picker, Smart buttons, Row decorations)

4. **[Part 3: Advanced Architecture & QWeb (Chapters 12 to 14)](Chapter-12-to-14-Inheritance-Accounting-QWeb)**
   - Chapter 12: Inheritance (CRUD `@api.ondelete`, `create()`, `res.users` extension, XPath view inheritance)
   - Chapter 13: Link Module `estate_account` (Cross-module integration with Invoicing via `Command.create()`)
   - Chapter 14: QWeb Templating & Kanban View (`<t t-name="card">`, `default_group_by`, conditional `t-if`)

5. **[Odoo 19.4 Modernization & Best Practices](Odoo-19-Upgrade-Guide)**
   - Transition from `_sql_constraints` to `models.Constraint`
   - Unified `ir.access.csv` security model
   - RelaxNG search view rules
   - QWeb `<t t-name="card">` vs legacy `<t t-name="kanban-box">`

---

## 🛠️ Modules in this Repository

| Module | Technical Name | Purpose | Depends |
|---|---|---|---|
| **Real Estate Core** | `estate` | Main application managing properties, offers, categories, and UI | `base` |
| **Invoicing Bridge** | `estate_account` | Link module automatically generating customer invoices upon property sale | `estate`, `account` |
