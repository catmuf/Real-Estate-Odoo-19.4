# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    """Real Estate Property Type Model.

    Represents property categories (e.g., Residential, Commercial, Apartment).
    Supports drag-and-drop sequencing and provides a stat button linking to offers.
    """
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"  # Sort by manual handle sequence first, then alphabetically

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(string="Sequence", default=1)  # Used by the widget="handle" for manual reordering

    # -------------------------------------------------------------------------
    # RELATIONAL FIELDS
    # -------------------------------------------------------------------------
    # Inverse relation: all properties categorized under this type
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    # Inverse relation: all offers made on properties belonging to this type
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    # -------------------------------------------------------------------------
    # COMPUTED FIELDS
    # -------------------------------------------------------------------------
    # Total count of offers linked to properties of this type, displayed on the form stat button
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offers Count")

    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS (New nomenclature: models.Constraint)
    # -------------------------------------------------------------------------
    # In Odoo saas-19.4 / 20.0+, models.Constraint replaces the deprecated _sql_constraints.
    # Enforces database-level uniqueness on the property type name.
    _check_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique",
    )

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        """Computes the total number of offers associated with this property type."""
        for record in self:
            record.offer_count = len(record.offer_ids)
