# -*- coding: utf-8 -*-
{
    'name': "Falak Locations Dimensions",

    'summary': """ This module for locations capacity of goods, used and free space. Smart treatment of arrival goods PL and default locations""",

    'description': """
        - add fields (length, width, height, total volume, remaining volume, full volume) in product, packaging, and locations.

        - add parent location on the product to select one of its children to receive it.
        
        - New button in picking when click it the system will show a new wizard containing each product with the suggested location.
        
        - when validating the receipt, location volume will decrease the remaining volume and increase the full volume by the product or packaging volume amount.
        
        - in the sale order when creating a delivery order and validating it, location volume will increase the remaining volume and decrease the full volume by the product or packaging volume.
    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/f_location_suggestion_wizard.xml',
        'views/f_product_template_inherit.xml',
        'views/f_product_packaging_inherit.xml',
        'views/f_stock_location_inherit.xml',
        # 'views/f_product_product_inherit.xml',
        'views/f_stock_picking_inherit.xml',
    ],

}
