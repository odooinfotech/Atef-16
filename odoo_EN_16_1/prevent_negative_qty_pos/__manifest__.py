# -*- coding: utf-8 -*-
{
    'name': "Prevent Negative Qty POS",

    'summary': """
        prevent_sell_negative_qty on  POS""",

    'description': """
        
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','account','point_of_sale','sale','pos_sale','stock_barcode','stock','product'],

    # always loaded
    'data': [    
	       'views/pos_res_config_settigns.xml',
    ],
    # only loaded in demonstration mode

    'assets': {
     'point_of_sale.assets': [
        # 'prevent_negative_qty_pos/static/src/js/models.js',
            'prevent_negative_qty_pos/static/src/js/prevent_sell.js',
        ],
     }
}
