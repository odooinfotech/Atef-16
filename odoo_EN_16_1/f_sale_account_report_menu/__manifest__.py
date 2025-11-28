# -*- coding: utf-8 -*-
{
    'name': "f_sale_account_report_menu",

    'summary': """
        New Custom report menu in sale""",

    'description': """
      
    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
 
}
