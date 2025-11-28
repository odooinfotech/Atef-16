# -*- coding: utf-8 -*-
{
    'name': "f_sale_stock_forcaste",

    'summary': """
        super access to view sales numbers only in forcase report to prevent record rule access in falak extra serc module""",

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
    'depends': ['base','stock','sale_stock','falak_extra_security','stock_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
