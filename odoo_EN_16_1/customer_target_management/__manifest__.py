# -*- coding: utf-8 -*-
{
    'name': "Customer Target Management",

    'summary': """
    """,

    'description': """
       
    """,

    'author': "Falak Solutions",
    #'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','contacts','mail','account_accountant','product','stock','f_product_family'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/f_groups.xml',
        'data/f_scheduled_action.xml',
        'views/f_customer_target.xml',
    ],
    
}
