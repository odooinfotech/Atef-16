# -*- coding: utf-8 -*-
{
    'name': 'Barcode App Customization',
    'summary': 'Barcode App Customization',
    #'website': 'https://www.odoo.com',
    'version': '16.0.1.0.0',
    'author': 'Odoo Ps',
    'description': "TASK ID - 2723114",
    'category': 'Custom Development',
    'depends': ['stock_barcode'],
    'data': [
        'views/product_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
        'barcode_customization/static/src/**/*.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
