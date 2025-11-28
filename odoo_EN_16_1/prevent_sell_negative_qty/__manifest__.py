# -*- coding: utf-8 -*-
{
    'name': "prevent_sell_negative_qty",

    'summary': """
      prevent_sell_negative_qty on  sales   """,

    'description': """
        Long description of module's purpose
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
    'depends': ['base','account','sale','stock_barcode','stock','product','f_bonus_management'],

    # always loaded
    'data': [
        'security/f_access_group.xml',
        'views/sales_res_config_settings_inherit.xml',
        
        'views/transfer_res_config_settings_inherit.xml',
        
    ],
   
    
}
