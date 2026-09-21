# -*- coding: utf-8 -*-
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Property Type", required=True)

    _check_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique",
    )

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property type name must be unique"),
    ]
