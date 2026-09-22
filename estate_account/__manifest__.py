# -*- coding: utf-8 -*-
{
    # Module technical and display information
    'name': 'Estate Account',
    'version': '1.0',
    'category': 'Real Estate',
    'author': 'Catmuf',
    'summary': 'Link module between Real Estate and Invoicing',
    'description': """
        Real Estate Account link module developed following Chapter 13 of the Odoo Developer Tutorial.
        Integrates the Real Estate module with the Invoicing (account) application:
        - Inherits estate.property model
        - Automatically creates customer invoices when properties are sold
        - Invoices 6% commission on selling price and 100.00 administrative fees
    """,

    # Link module dependencies: both 'estate' and 'account' are required
    'depends': [
        'estate',
        'account',
    ],

    'data': [],

    # Configuration flags
    'installable': True,
    'application': False,  # Link module, not a standalone application
    'license': 'LGPL-3',
}
