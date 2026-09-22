# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    """Real Estate Property Offer Model.

    Represents purchase bids submitted by potential buyers for a specific property.
    Includes validity periods, automatic deadline calculation, and acceptance/refusal workflows.
    """
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"  # Default sorting: highest offered price first

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,  # Status is not duplicated when copying an offer record
    )

    # -------------------------------------------------------------------------
    # RELATIONAL FIELDS
    # -------------------------------------------------------------------------
    # Potential buyer partner making the offer
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    # Property being bid on
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    # Stored related field pointing to the property type through the linked property;
    # enables grouping and stat button aggregation on property type
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    # -------------------------------------------------------------------------
    # COMPUTED / INVERSE FIELDS (Validity & Deadline)
    # -------------------------------------------------------------------------
    # Validity duration in days (defaults to 7 days)
    validity = fields.Integer(string="Validity (days)", default=7)

    # Computed deadline date; modifying date_deadline calculates back into validity (inverse)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS (New nomenclature: models.Constraint)
    # -------------------------------------------------------------------------
    # In Odoo saas-19.4 / 20.0+, models.Constraint replaces the deprecated _sql_constraints.
    # Enforces database-level check ensuring offer prices are strictly positive.
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive",
    )

    # -------------------------------------------------------------------------
    # COMPUTE AND INVERSE METHODS
    # -------------------------------------------------------------------------
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        """Computes the offer deadline by adding validity days to the record's creation date

        (or today's date if the record is being newly composed).
        """
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """Inverse compute method: when the user manually picks a deadline date,

        recomputes the validity in days relative to the creation date.
        """
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline and create_date:
                record.validity = (record.date_deadline - create_date).days

    # -------------------------------------------------------------------------
    # ACTION METHODS (Accept / Refuse Workflows)
    # -------------------------------------------------------------------------
    def action_accept(self):
        """Accepts the offer:

        1. Ensures no other offer for the property has already been accepted.
        2. Sets this offer's status to 'accepted'.
        3. Updates the parent property's buyer to this partner.
        4. Updates the parent property's selling price to this offer price.
        5. Sets the parent property's state to 'offer_accepted'.
        """
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("An offer has already been accepted.")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        """Refuses the offer by marking its status as 'refused'."""
        for record in self:
            record.status = "refused"
        return True

    # -------------------------------------------------------------------------
    # CRUD OVERRIDES (Create Method)
    # -------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """Overrides create to:

        1. Prevent creating an offer with a price lower than an existing offer on the property.
        2. Set the property state to 'offer_received'.
        """
        for vals in vals_list:
            property_id = vals.get("property_id")
            if property_id:
                property_record = self.env["estate.property"].browse(property_id)
                for offer in property_record.offer_ids:
                    if vals.get("price", 0) < offer.price:
                        raise UserError("The offer must be higher than %.2f" % offer.price)
                property_record.state = "offer_received"
        return super().create(vals_list)

