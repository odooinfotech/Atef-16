# -*- coding: utf-8 -*-
{
    'name': "Sales Margin Customization",

    'summary': """ This module for sale margin customization""",

    'description': """
        - Add access on margin field in sale order view
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
    'depends': ['base','sale','sale_margin','hide_product_cost'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/f_groups_access.xml',
        'views/f_sale_order_inherit.xml',

    ],

}
