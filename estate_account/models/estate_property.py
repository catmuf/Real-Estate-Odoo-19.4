# -*- coding: utf-8 -*-
from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    """Inherits estate.property to add automated customer invoicing upon sale."""
    _inherit = "estate.property"

    def action_sold(self):
        """Overrides action_sold to automatically generate a customer invoice

        for the buyer when the property is marked as sold:
        1. Calls super() to validate and transition state to 'sold'.
        2. Creates an account.move of type 'out_invoice' (Customer Invoice).
        3. Adds two invoice lines:
           - 6% of selling price as property sale commission
           - 100.00 administrative fees
        """
        # Execute standard action_sold first (validates state transitions and sets state to 'sold')
        res = super().action_sold()

        for record in self:
            if not record.buyer_id:
                raise UserError("A buyer must be set before selling and invoicing the property.")

            # Create Customer Invoice in the account.move model
            self.env["account.move"].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": f"Property Sale Commission (6%): {record.name}",
                                "quantity": 1.0,
                                "price_unit": record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1.0,
                                "price_unit": 100.00,
                            }
                        ),
                    ],
                }
            )

        return res
