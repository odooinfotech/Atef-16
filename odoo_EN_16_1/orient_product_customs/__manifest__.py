# -*- coding: utf-8 -*-
{
    'name': "Orient Products Customizations",

    'summary': """
        Orient Customizations on products 
        
        """,

    'description':  """
        Orient Customizations on products 
        
        """,

      'author': "Falak Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','product_expiry'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/f_product_template_view_inherit.xml',
        'views/f_products_custom_lockups.xml',
        'views/f_products_category_view.xml',
        'views/f_products_brand_view.xml',
        'views/f_products_family_view.xml',
        'views/f_prod_identity_group.xml',
        'views/f_prod_producer_name_view.xml',
        'views/f_prod_target_view.xml',
    ],
 
}
