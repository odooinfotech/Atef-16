# -*- coding: utf-8 -*-
{
    'name': "Falak Product Prices History POS EXT", 

    'summary': """
        This Module is added to include the POS orders in the proces history on product and 
        sales orders level 
        """,

    'description': """
         
        
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale','falak_product_prices_history'],

    # always loaded
    'data': [
        
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
