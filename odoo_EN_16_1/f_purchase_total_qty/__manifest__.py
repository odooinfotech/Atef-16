# -*- coding: utf-8 -*-
{
    'name': "Falak Purchase Total QTY",

    'summary': """ This Module To display Total QTY for PO, Bill and receipts""",

    'description': """
        This Module To display Total QTY for PO, Bill and receipts
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
    'depends': ['base', 'purchase', 'account', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/f_purchase_order_inherit.xml',
        'views/f_account_move_inherit.xml',
        'views/f_stock_picking_inherit.xml',
    ],

}
