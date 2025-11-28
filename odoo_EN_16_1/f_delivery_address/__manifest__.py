# -*- coding: utf-8 -*-
{
    'name': "Sales/Purchase Delivery Address ",

    'summary': """
		""",

    'description': """

    """,
    'license': 'LGPL-3',
    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    #'report_xlsx'
    'depends': ['base','sale','purchase'],

    # always loaded
    'data': [

         'views/f_so_inherit.xml',
         'views/f_po_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}
