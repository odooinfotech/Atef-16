# -*- coding: utf-8 -*-
{
    'name': "f_branch_access_balance_report_ex",

    'summary': """
        add Partner Branch access on balance report""",

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

    # any module necessary for this one to work correctly
    'depends': ['base','stock','f_contact_balance_report','f_multi_branches_management'],

    # always loaded
    'data': [
         'security/ir_rule.xml',
        'views/f_inherit_report.xml',

    ],
  
}
