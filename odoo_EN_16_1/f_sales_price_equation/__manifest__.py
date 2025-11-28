# -*- coding: utf-8 -*-
{
    'name': "Falak Sales Pricing Equations",

    'summary': """ This Module to allow set new price depends on Landed Cost and Purchases""",

    'description': """ 
        - create pricing equation model (Name, Factor)
        - create product pricing model (Name, Equation, Status)
        - create landed pricing line model (Product, Quantity, New Cost, Unit New Cost, Landed Cost, Unit Old Cost, Deference, Def. With Vat, Current Price, New Price)
        - add security data for these 3 models 
        - create sequance and archive action for product pricing model
        - create pricing equation views (Tree, Action, Menu)
        - create product pricing views (Tree, Form, Actions, Menu)
        - create get_product, compute, confirm methods
        - do the same things for purchase and allow user to choose purchase type (Internal, External)
    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'stock_landed_costs','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/f_product_pricing_data.xml',
        'data/f_pricing_type_date.xml',
        'views/f_pricing_equation_views.xml',
        'views/f_product_pricing_views.xml',
    ],

}

