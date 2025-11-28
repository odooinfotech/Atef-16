# -*- coding: utf-8 -*-
{
    'name': "Show Contact Balance",

    'summary': """
        show credit balance on partner and sale order
        """,

    'description': """
     
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','contacts','account','falak_multi_payments_base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/f_inherit_sale_order.xml',
         'views/f_inherit_res_partner.xml',
         'views/f_inherit_account_move.xml',
         'views/f_inherit_multipay.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
