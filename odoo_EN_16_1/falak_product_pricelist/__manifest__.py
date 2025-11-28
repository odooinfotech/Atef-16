# -*- coding: utf-8 -*-
{
    'name': "falak_product_pricelist",

    'summary': """
         new five prices fields on product
       add these prices to pricelist""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Falak Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','account'],

    # always loaded
    'data': [
        'views/f_inherit_products.xml',
#         'views/f_inherit_pricelist.xml',
        
    ],
    
    

}
