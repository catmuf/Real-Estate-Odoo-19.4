# Architecture & Design

This page provides the architectural blueprints, entity-relationship diagrams, and state machine workflows for the Real Estate application suite.

---

## 1. System Architecture

```mermaid
graph TD
    subgraph Client["Client Tier (Web Browser)"]
        Browser["User Browser"]
        OWLClient["OWL UI Framework"]
        QWebCards["QWeb Kanban Renderers"]
    end

    subgraph Server["Application Server Tier (Odoo 19.4)"]
        Dispatcher["HTTP / JSON-RPC Dispatcher"]
        Security["Access Security (ir.access)"]
        ORM["Odoo ORM (Python Models)"]
        Modules["Module Layer (estate & estate_account)"]
    end

    subgraph Data["Database Tier (PostgreSQL)"]
        Postgres[("PostgreSQL 14+")]
        SQLConstraints["Database Constraints (CHECK / UNIQUE)"]
    end

    Browser -->|HTTP/JSON-RPC| Dispatcher
    Dispatcher --> Security
    Security --> ORM
    ORM --> Modules
    Modules --> ORM
    ORM --> Postgres
    Postgres --> SQLConstraints
```

---

## 2. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    ESTATE_PROPERTY ||--o{ ESTATE_PROPERTY_OFFER : "receives"
    ESTATE_PROPERTY }o--|| ESTATE_PROPERTY_TYPE : "typed as"
    ESTATE_PROPERTY }o--o{ ESTATE_PROPERTY_TAG : "categorized with"
    ESTATE_PROPERTY }o--|| RES_USERS : "salesperson"
    ESTATE_PROPERTY }o--o| RES_PARTNER : "buyer"
    ESTATE_PROPERTY_OFFER }o--|| RES_PARTNER : "bidder"
    ACCOUNT_MOVE ||--o{ ACCOUNT_MOVE_LINE : "invoiced lines"
    ESTATE_PROPERTY ..> ACCOUNT_MOVE : "creates upon sale"

    ESTATE_PROPERTY {
        integer id PK
        string name
        text description
        string postcode
        date date_availability
        float expected_price
        float selling_price
        integer bedrooms
        integer living_area
        integer facades
        boolean garage
        boolean garden
        integer garden_area
        string garden_orientation
        boolean active
        string state
        integer total_area
        float best_price
    }

    ESTATE_PROPERTY_TYPE {
        integer id PK
        string name
        integer sequence
        integer offer_count
    }

    ESTATE_PROPERTY_TAG {
        integer id PK
        string name
        integer color
    }

    ESTATE_PROPERTY_OFFER {
        integer id PK
        float price
        string status
        integer validity
        date date_deadline
    }

    ACCOUNT_MOVE {
        integer id PK
        integer partner_id FK
        string move_type
    }

    ACCOUNT_MOVE_LINE {
        integer id PK
        string name
        float quantity
        float price_unit
    }
```

---

## 3. Property Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> New : Record Creation
    New --> Offer_Received : Offer Created (create hook)
    Offer_Received --> Offer_Accepted : Salesperson Accepts Offer
    New --> Canceled : Cancel Button
    Offer_Received --> Canceled : Cancel Button
    Offer_Accepted --> Canceled : Cancel Button
    Offer_Accepted --> Sold : Sold Button
    Sold --> [*] : Invoiced via estate_account
    Canceled --> [*] : Non-deletable if unlinked
```

---

## 4. Cross-Module Invoicing Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as Real Estate Agent
    participant Form as Property Form View
    participant Prop as estate.property
    participant Acct as estate_account (Override)
    participant Move as account.move (Invoicing)

    User->>Form: Clicks "Sold"
    Form->>Acct: action_sold()
    Acct->>Prop: super().action_sold()
    Prop->>Prop: Check state != 'canceled'
    Prop->>Prop: Set state = 'sold'
    Prop-->>Acct: return True
    Acct->>Acct: Check buyer_id exists
    Acct->>Move: create({partner_id: buyer.id, move_type: 'out_invoice', invoice_line_ids: [...]})
    Note over Move: Creates Line 1: 6% Commission<br/>Creates Line 2: 100.00 Admin Fee
    Move-->>Acct: Invoice Created (Draft)
    Acct-->>Form: Complete
```
