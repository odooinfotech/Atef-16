# -*- coding: utf-8 -*-
{
    'name': "Manual Exchange Rate",

    'summary': """
    
	Ability to set exchange rate manually in :
	    - Journal Entry """,

    'description': """
      
    """,

    'author': "Falak Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','account_accountant','account'],

    # always loaded
    'data': [
        'views/f_inherit_account_move.xml',
        
    ],
    'auto_install': True,
    'installable': True,
    'application': True,
    
   
}
