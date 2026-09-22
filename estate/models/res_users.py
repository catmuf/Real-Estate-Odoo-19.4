# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    """Model extension for res.users (Salespersons).

    Adds a One2many relation to display all available properties assigned to the user.
    """
    _inherit = "res.users"

    # Inverse relationship to estate.property.user_id, filtered to available properties only
    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        string="Real Estate Properties",
        domain=[("state", "in", ["new", "offer_received"])],
    )

