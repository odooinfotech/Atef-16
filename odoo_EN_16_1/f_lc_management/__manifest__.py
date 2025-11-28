# -*- coding: utf-8 -*-
{
    'name': "LC Letter of Credit Management",

    'summary': """
        LC Management Module""",

    'description': """
    """,
    'license': 'LGPL-3',
    'author': "Falak Solutions",
   # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','account'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'Data/f_seq_number.xml',
        'views/f_purchase_order_inherit.xml',
        'views/f_purchase_lockups_views.xml',
        'views/f_purchase_order_config_menue.xml',
        'views/f_lc_details_view.xml',
       # 'views/f_shipping_details_view.xml',
    ],
 
}
