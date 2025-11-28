# -*- coding: utf-8 -*-
{
    'name': "f_contact_balance_report",

    'summary': """
      Contact Balances tree view """,

    'description': """
    new tree view for contact balances
    """,

    'author': "Falak Solutions",
    'sequence': 100,
    'installable': True,
   # 'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','account','check_management','base_address_extended','f_sale_account_report_menu'],

    # always loaded
    'data': [
         'security/ir_rule.xml',
         'security/ir.model.access.csv',
         'data/f_groups.xml',
         'wizard/f_report_xizard_view.xml',
         'views/f_report_view.xml',

    ],
 
}
