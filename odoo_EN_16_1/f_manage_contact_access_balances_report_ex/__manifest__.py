# -*- coding: utf-8 -*-
{
    'name': "f_manage_contact_access_balances_report_ex",

    'summary': """
              add contact access on partner balance report """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Falak Solutions",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','falak_extra_security','f_contact_balance_report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
      # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
     #   'demo/demo.xml',
    #],
}
