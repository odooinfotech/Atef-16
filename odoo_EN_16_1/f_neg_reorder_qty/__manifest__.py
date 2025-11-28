# -*- coding: utf-8 -*-
{
    'name': "Falak Negative Reorder Qty",

    'summary': """
      products  qtys less than min re-ordering rule qty""",

    'description': """
        
    """,

    'author': "Falak Solutions",
    'license': 'LGPL-3',
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','location_access'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        'views/f_reorder_neg_qty.xml',
        'views/f_reording_wizard.xml',
    ],
   
}
