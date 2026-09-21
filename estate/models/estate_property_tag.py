# -*- coding: utf-8 -*-
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _check_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique",
    )

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property tag name must be unique"),
    ]
