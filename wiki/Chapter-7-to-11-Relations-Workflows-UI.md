# Chapters 7 to 11: Relations, Business Logic & Polish

This section covers relational modeling, dynamic field calculations, state machine workflows, constraints, and advanced UI enhancements.

---

## Chapter 7: Relations Between Models
- **Goal**: Connect properties with property types, tags, offers, salespersons, and buyers.
- **New Models Created**:
  1. `estate.property.type`:
     - `name` (`Char`, required)
     - `sequence` (`Integer`, default=1)
     - `property_ids` (`One2many` to `estate.property`)
  2. `estate.property.tag`:
     - `name` (`Char`, required)
     - `color` (`Integer`)
  3. `estate.property.offer`:
     - `price` (`Float`)
     - `status` (`Selection`: accepted, refused)
     - `partner_id` (`Many2one` to `res.partner`)
     - `property_id` (`Many2one` to `estate.property`)
- **Commit**: `574d33b Chapter 7: Relations Between Models`

---

## Chapter 8: Computed Fields and Onchanges
- **Goal**: Implement dynamic field recalculations.
- **Implementation**:
  - `total_area`:
    ```python
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    ```
  - `best_price`:
    ```python
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0
    ```
  - `_onchange_garden`:
    ```python
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
    ```
  - Two-way compute/inverse for offer deadline:
    - Modifying `validity` recalculates `date_deadline`.
    - Modifying `date_deadline` recomputes `validity`.
- **Commit**: `1d397d6 Chapter 8: Computed Fields And Onchanges`

---

## Chapter 9: Ready For Some Action? (Workflows)
- **Goal**: Implement state transition actions and validation.
- **Implementation**:
  - **`action_sold`**: Sets property state to `'sold'`. Raises `UserError` if the property is already canceled.
  - **`action_cancel`**: Sets property state to `'canceled'`. Raises `UserError` if the property is already sold.
  - **`action_accept` on Offer**:
    - Ensures no other offer is already accepted.
    - Sets offer status to `'accepted'`.
    - Sets property's `buyer_id` and `selling_price`.
    - Sets property state to `'offer_accepted'`.
  - **`action_refuse` on Offer**: Sets status to `'refused'`.
- **Commit**: `c7fe7e9 Chapter 9: Ready For Some Action?`

---

## Chapter 10: Constraints (SQL & Python)
- **Goal**: Prevent data inconsistencies.
- **Implementation**:
  - **Database Constraints (`models.Constraint`)**:
    - `estate.property`: `CHECK(expected_price > 0)`
    - `estate.property`: `CHECK(selling_price >= 0)`
    - `estate.property.offer`: `CHECK(price > 0)`
    - `estate.property.type`: `UNIQUE(name)`
    - `estate.property.tag`: `UNIQUE(name)`
  - **Python Constraint (`@api.constrains`)**:
    ```python
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_constraint(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
    ```
- **Commit**: `9c808aa Chapter 10: Constraints`

---

## Chapter 11: Add The Sprinkles
- **Goal**: Add visual enhancements, interactive widgets, and semantic styling.
- **Implementation**:
  - `widget="statusbar"` on `state`.
  - `widget="color_picker"` on `color` in tags.
  - `widget="many2many_tags"` with `options="{'color_field': 'color'}"`.
  - `widget="handle"` on `sequence` in property types for drag-and-drop reordering.
  - Smart Button on Property Type with `widget="statinfo"` displaying `offer_count`.
  - Inline editing (`editable="bottom"`) on offers and tags.
  - List row decorations (`decoration-success`, `decoration-bf`, `decoration-muted`, `decoration-danger`).
- **Commit**: `bac2b85 Chapter 11: Add The Sprinkles`
