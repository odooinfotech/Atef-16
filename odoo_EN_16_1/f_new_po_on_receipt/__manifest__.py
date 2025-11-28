# -*- coding: utf-8 -*-
{
    'name': "f_new_po_on_receipt",

    'summary': """
        Enable  create new po from transfer when certain opertaion type applied""",

    'description': """

    """,

    'author': "falak-solutions",
   # 'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','stock'],

    # always loaded
    'data': [
        'views/f_inherit_picking.xml',
    ],

}
