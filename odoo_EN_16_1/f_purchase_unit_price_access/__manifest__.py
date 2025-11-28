# -*- coding: utf-8 -*-
{
    'name': "Purchase Unit Price Access",

    'summary': """ This module for purchase unit price access""",

    'description': """
        - Add access on unit price in purcahse order
    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'license': 'AGPL-3',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','falak_product_prices_history'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/f_groups_access.xml',
        'views/f_purchase_order_inherit.xml',

    ],

}
