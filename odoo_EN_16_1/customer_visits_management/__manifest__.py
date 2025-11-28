# -*- coding: utf-8 -*-
{
    'name': "Customer Visits Management",

    'summary': """
        This Module is used to Manage the customer visits by Sales Persons """,

    'description': """
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','sale','account','customer_target_management','f_partner_aging_balance_report'],

    # always loaded
    'data': [
        'data/f_scheduled_action.xml',
        'security/f_groups.xml',
        'security/ir.model.access.csv',
        'wizard/f_cancel_wizard.xml',
        'views/f_customer_contact.xml',
        'views/f_my_visits.xml',
        'views/f_customer_route.xml',
        'views/f_sale_order_inherit.xml',
        'views/f_account_move_inherit.xml',
        'views/f_account_payment_inherit.xml',
    ],
   
}
