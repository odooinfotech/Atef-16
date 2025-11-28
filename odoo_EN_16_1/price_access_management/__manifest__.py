# -*- coding: utf-8 -*-
{
    'name': "PriceAccessManagement",

    'summary': """
       this module for give an access to edit prices in invoices & sales""",

    'description': """
    """,

    'author': "Falak Solutions",
   # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','account','sale'],

    # always loaded
    'data': [
        'Data/f_groups.xml',
        #'security/ir.model.access.csv',
        'views/f_prices_access_invoices_man.xml',
        'views/f_prices_access_sales_man.xml',
        'views/f_settings_inherit.xml',

    ],

}
