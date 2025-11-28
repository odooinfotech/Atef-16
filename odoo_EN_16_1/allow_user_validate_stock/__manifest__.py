# -*- coding: utf-8 -*-
{
    'name': "allow_user_validate_stock",

    
    'summary': """
        allow_inventory/user_validate_stock""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Falak-solution",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','stock','stock_barcode','web'],
    #'qweb': ['static/src/xml/*.xml'],

    # always loaded
    'data': [
       #  'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'allow_user_validate_stock/static/src/**/*.js',
            #'allow_user_validate_stock/static/src/**/*.xml',
        ],
    },
}
