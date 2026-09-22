# Chapters 12 to 14: Inheritance, Accounting Integration & QWeb

This section covers Odoo's modular inheritance mechanisms, cross-module integration with Invoicing via a decoupled link module, and modern QWeb Kanban card templating.

---

## Chapter 12: Inheritance
- **Goal**: Alter standard behaviors and extend existing models and views.
- **Implementation**:
  1. **CRUD Method Extension**:
     - **On Delete Protection**:
       ```python
       @api.ondelete(at_uninstall=False)
       def _unlink_if_new_or_canceled(self):
           for record in self:
               if record.state not in ("new", "canceled"):
                   raise UserError("Only new and canceled properties can be deleted.")
       ```
     - **Create Hook on Offers**:
       ```python
       @api.model_create_multi
       def create(self, vals_list):
           for vals in vals_list:
               property_id = vals.get("property_id")
               if property_id:
                   property_record = self.env["estate.property"].browse(property_id)
                   for offer in property_record.offer_ids:
                       if vals.get("price", 0) < offer.price:
                           raise UserError("The offer must be higher than %.2f" % offer.price)
                   property_record.state = "offer_received"
           return super().create(vals_list)
       ```
  2. **Model Extension (`res.users`)**:
     Created `estate/models/res_users.py`:
     ```python
     class ResUsers(models.Model):
         _inherit = "res.users"

         property_ids = fields.One2many(
             "estate.property",
             "user_id",
             string="Real Estate Properties",
             domain=[("state", "in", ["new", "offer_received"])],
         )
     ```
  3. **View Inheritance (`res_users_views.xml`)**:
     Extends `base.view_users_form` by inserting a new notebook page:
     ```xml
     <record id="res_users_view_form" model="ir.ui.view">
         <field name="name">res.users.view.form.inherit.estate</field>
         <field name="model">res.users</field>
         <field name="inherit_id" ref="base.view_users_form"/>
         <field name="arch" type="xml">
             <xpath expr="//notebook" position="inside">
                 <page string="Real Estate Properties" name="real_estate_properties">
                     <field name="property_ids"/>
                 </page>
             </xpath>
         </field>
     </record>
     ```
- **Commit**: `84de37a Chapter 12: Inheritance`

---

## Chapter 13: Interact With Other Modules (Link Module)
- **Goal**: Create a decoupled bridge module to generate customer invoices upon property sales.
- **Module Architecture**:
  - Module directory: `estate_account`
  - Dependencies: `['estate', 'account']`
- **Implementation (`estate_account/models/estate_property.py`)**:
  ```python
  class EstateProperty(models.Model):
      _inherit = "estate.property"

      def action_sold(self):
          res = super().action_sold()

          for record in self:
              if not record.buyer_id:
                  raise UserError("A buyer must be set before selling and invoicing the property.")

              self.env["account.move"].create({
                  "partner_id": record.buyer_id.id,
                  "move_type": "out_invoice",
                  "invoice_line_ids": [
                      Command.create({
                          "name": f"Property Sale Commission (6%): {record.name}",
                          "quantity": 1.0,
                          "price_unit": record.selling_price * 0.06,
                      }),
                      Command.create({
                          "name": "Administrative Fees",
                          "quantity": 1.0,
                          "price_unit": 100.00,
                      }),
                  ],
              })
          return res
  ```
- **Commit**: `1fd720a Chapter 13: Interact With Other Modules`

---

## Chapter 14: A Brief History of QWeb (Kanban View)
- **Goal**: Build an interactive card-based Kanban board.
- **Implementation (`estate/views/estate_property_views.xml`)**:
  - Grouping and drag prevention: `default_group_by="property_type_id" records_draggable="0"`.
  - Modern Odoo 19 QWeb template syntax: `<t t-name="card">`.
  - Conditional rendering with `t-if`:
  ```xml
  <record id="estate_property_view_kanban" model="ir.ui.view">
      <field name="name">estate.property.kanban</field>
      <field name="model">estate.property</field>
      <field name="arch" type="xml">
          <kanban default_group_by="property_type_id" records_draggable="0">
              <field name="state"/>
              <templates>
                  <t t-name="card">
                      <div>
                          <strong>
                              <field name="name"/>
                          </strong>
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
      </field>
  </record>
  ```
  - Updated window action view modes:
    ```xml
    <field name="view_mode">kanban,list,form</field>
    ```
- **Commit**: `689494e Chapter 14: A Brief History Of QWeb`
