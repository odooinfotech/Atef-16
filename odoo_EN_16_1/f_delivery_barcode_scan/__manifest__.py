# -*- coding: utf-8 -*-
{
    'name': 'Delivery Barcode Scanning',
    'summary': """
     
    """,
    'description': """
     .
    """,
    'author': 'Falaka Solutions',
    'license': 'OPL-1',
    'category': 'Warehouse',
    'sequence': '10',
    'version': '16',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [

            'f_delivery_barcode_scan/static/src/js/barcode.js',
        ],
    },
    'images': ['static/description/logo.jpg'],
    'application': True,
    'currency': 'EUR',
}

