# -*- coding: utf-8 -*-
{
    'name': "Falak Bounus Management",

    'summary': """
	This Modules Manages the bonus in sales and invoicing process""",

    'description': """
      
    """,


    'author': "Falak Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_management', 'sale_stock', 'stock_account','account'],

    # always loaded
    'data': [
        #'security/f_groups.xml',
        #'views/f_inherit_account_move.xml',
        'views/f_account_move_inherit_view.xml',
        'views/f_sale_order_inherit_view.xml',
        'report/f_sales_report_inherit.xml',
        'report/f_invoice_report_inherit.xml',
        
    ],
   
}
