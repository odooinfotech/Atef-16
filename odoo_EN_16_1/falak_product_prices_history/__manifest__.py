# -*- coding: utf-8 -*-
{
    'name': "Falak Product Prices History",

    'summary': """
        Products Sales/Purchasing Prices History
        """,

    'description': """
        This Modules shows :
        - Product Prices History in Sales Orders Lines 
        - Product Prices History in Purchase Orders Lines
        - Product Prices History in Products 
        
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','purchase','stock','account','hide_product_cost'],

    # always loaded
    'data': [
        
         'security/ir.model.access.csv',        
         'wizard/f_product_price_history_wizard.xml',
         'wizard/f_so_price_history_wizard.xml',
         'wizard/f_po_price_hitory_wizard.xml',
         'wizard/f_am_price_history_wizard.xml',
         'wizard/f_product_purchase_price_history_wizard.xml',
         'views/f_res_settings_inherit.xml',
         'views/f_so_line_tree_view_inherit.xml',
         'views/f_po_line_tree_view_inherit.xml',
         'views/f_product_view_inherit.xml',
         'views/f_product_view_inherit.xml',
         'views/f_legacy_price_history.xml',
         'views/f_am_line_tree_view_inherit.xml',
    ],

}