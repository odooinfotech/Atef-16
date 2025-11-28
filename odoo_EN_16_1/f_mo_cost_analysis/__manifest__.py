# -*- coding: utf-8 -*-
{
    'name': "Falak MO Costnalysis",

    'summary': """
       """,

    'description': """
       
    """,

    'author': "Falak Solutions",
    'license': 'LGPL-3',
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','mrp'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        'views/f_inherit_products.xml',
        'views/f_mo_cost_analysis_report.xml',
       
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
