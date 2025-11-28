# -*- coding: utf-8 -*-
{
    'name': "Cash Flow Report",

    'summary': """
       """,

    'description': """
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale','purchase','f_access_categ','check_management'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
      
        'views/f_sale_setup.xml',
        'views/f_cash_basis.xml',
        'views/f_purchase_setup.xml',
        'views/f_cashflow_report.xml',
        'views/f_cash_flow_period.xml',
        'views/f_cash_flow_type.xml',
        'views/f_cash_period_subtype.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
