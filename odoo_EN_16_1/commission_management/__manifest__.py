# -*- coding: utf-8 -*-
{
    'name': "Commission Management",

    'summary': """
     """,

    'description': """
       
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','f_product_family','account','account_accountant','contacts'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/f_groups.xml',
        'views/f_comm_menue.xml',
        'views/f_commission_management.xml',
        'views/f_comission_period.xml',
        'views/f_comission_calculation.xml',
        'views/f_res_partner_inherit.xml',
        'views/f_comm_collection_rules.xml',
        'views/f_account_payment_inherit.xml',
        'views/f_account_move_inherit.xml',
        'views/f_commission_groups_setup.xml',
        'views/f_calculation_logs.xml',
    ],
}
