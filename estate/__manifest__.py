# -*- coding: utf-8 -*-
{
    # Module technical and display information
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'author': 'Catmuf',
    'summary': 'Real estate advertisement module',
    'description': """
        Real Estate module developed following the Odoo Developer Tutorial (Server Framework 101).
        Provides property management, offer tracking, property types, tags, and automated business workflows.
    """,

    # Core dependencies: only 'base' is required for standard ORM and security functionality
    'depends': [
        'base',
    ],

    # Data files loaded in order during installation and upgrades:
    # 1. Security access rights (ir.access.csv for Odoo saas-19.4 / 20.0 unified security)
    # 2. Model UI views (list, form, search views and window actions)
    # 3. Top-level and sub-level navigation menus
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],

    # Module configuration flags
    'installable': True,    # Allows module to be installed from the Apps menu
    'application': True,    # Displays the module as a top-level application in the Apps list
    'license': 'LGPL-3',    # Open source license identifier
}
