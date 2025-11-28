# -*- coding: utf-8 -*-
{
    'name': "Set Partner Sales Person",

    'summary': """
""",

    'description': """

    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'license': 'LGPL-3',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
