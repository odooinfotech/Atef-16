# -*- coding: utf-8 -*-
{
    'name': "Falak Product Prices History POS Access Branch ",

    'summary': """
       
        """,

    'description': """
        This Modules shows :
            Add Access on prices history based on branch with pos    
    """,

    'author': "Falak Solutions",
    #'website': "http://falak-solutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','f_multi_branches_pos_ext','falak_product_prices_history_branch_ext','falak_product_prices_history_POS'],

    # always loaded
    'data': [

    ],

}