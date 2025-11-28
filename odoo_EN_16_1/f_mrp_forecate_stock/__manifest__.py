# -*- coding: utf-8 -*-
{
    'name': "f_mrp_forecate_stock",

    'summary': """
       mrp extend forecaste report for contact security issue """,

    'description': """
        
    """,

    'author': "falak-solutions",
    'license': 'OPL-1',
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','f_sale_stock_forcaste','mrp','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
       # 'views/views.xml',
       # 'views/templates.xml',
    ],
}
