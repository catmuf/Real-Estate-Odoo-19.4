# -*- coding: utf-8 -*-
from odoo import fields, models


class EstatePropertyTag(models.Model):
    """Real Estate Property Tag Model.

    Represents customizable tags (e.g., Cozy, Renovated, Sea View) applied to properties.
    Supports individual tag color indexing for visual differentiation in tag widgets.
    """
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"  # Default sorting: alphabetical order by tag name

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")  # Integer color index used by color_picker / many2many_tags widgets

    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS (New nomenclature: models.Constraint)
    # -------------------------------------------------------------------------
    # In Odoo saas-19.4 / 20.0+, models.Constraint replaces the deprecated _sql_constraints.
    # Enforces database-level uniqueness on tag names to prevent duplicate categories.
    _check_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique",
    )
