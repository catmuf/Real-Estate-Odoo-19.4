# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    """Real Estate Property Model.

    Represents a property listing for sale, tracking physical characteristics,
    pricing, status progression, associated offers, and assigned salespersons.
    """
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"  # Default sorting: latest created properties first

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,  # Do not duplicate availability date when copying a record
        default=lambda self: fields.Date.today() + relativedelta(months=3),  # Default available in 3 months
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
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

    # Reserved Odoo fields for special behaviors
    active = fields.Boolean(string="Active", default=True)  # Allows archiving records instead of deleting
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    # -------------------------------------------------------------------------
    # RELATIONAL FIELDS
    # -------------------------------------------------------------------------
    # Many properties belong to one property type (e.g., Residential, Commercial)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # Buyer partner set automatically when an offer is accepted
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    # Salesperson assigned to the property (defaults to the current user)
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    # Categorization tags (Many2many: a property can have multiple tags)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # Bidding offers made on this property (One2many: inverse of property_id in estate.property.offer)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # -------------------------------------------------------------------------
    # COMPUTED FIELDS
    # -------------------------------------------------------------------------
    # Calculated total area summing living area and garden area
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")

    # Dynamically calculated highest offer price among received offers
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS (New nomenclature: models.Constraint)
    # -------------------------------------------------------------------------
    # In Odoo saas-19.4 / 20.0+, the legacy '_sql_constraints' list attribute was
    # deprecated and removed in favor of declarative 'models.Constraint' class attributes.
    # These create database-level CHECK / UNIQUE constraints in PostgreSQL.

    # Enforce strictly positive expected price (> 0)
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive",
    )

    # Enforce non-negative selling price (>= 0)
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive",
    )

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """Computes the total surface area by combining living and garden areas."""
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        """Calculates the highest price offered among all active offers for the property."""
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------
    @api.onchange("garden")
    def _onchange_garden(self):
        """Automatically pre-fills default garden area and orientation when the garden

        checkbox is enabled, or clears them when disabled.
        """
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # -------------------------------------------------------------------------
    # ACTION METHODS (State Transitions)
    # -------------------------------------------------------------------------
    def action_sold(self):
        """Marks the property as 'sold'. Cannot sell a canceled property."""
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        """Marks the property as 'canceled'. Cannot cancel an already sold property."""
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            record.state = "canceled"
        return True

    # -------------------------------------------------------------------------
    # PYTHON CONSTRAINTS
    # -------------------------------------------------------------------------
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_constraint(self):
        """Validates that when a selling price is registered (> 0), it cannot be

        lower than 90% of the expected price. Uses float_compare to avoid
        floating-point rounding discrepancies.
        """
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
