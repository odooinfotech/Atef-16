# -*- coding: utf-8 -*-
{
    'name': "Falak Manufacturing Definitions",

    'summary': """
        Shift Definitions
        Work center groups def 
        """,

    'description': """
    """,

    'author': "Falak Solutions",
   # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'Data/f_seq_number.xml',
        'views/f_manufacturing_lockups_view.xml',
        'views/f_mrp_lookups_view.xml',
        'views/mrp_workcenter_view.xml',

    ],
   
}
