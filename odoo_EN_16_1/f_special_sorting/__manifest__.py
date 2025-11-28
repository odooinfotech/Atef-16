# -*- coding: utf-8 -*-
{
    'name': "Special Lines Sorting",

    'summary': """
		""",

    'description': """

    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'license': 'LGPL-3',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','account'],

    # always loaded
    'data': [
        'views/f_inherit_sale_view.xml',
        'views/f_account_move_inherited.xml',
        'views/f_stock_picking_inherit.xml',
        'views/f_purchase_order_inherit.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
