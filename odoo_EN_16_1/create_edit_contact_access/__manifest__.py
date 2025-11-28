# -*- coding: utf-8 -*-
{
    'name': "Falak Create Edit Contact Access",

    'summary': """
        this module for create edit contact access""",

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
    'depends': ['base','stock','purchase','sale'],

    # always loaded
    'data': [
        
        'security/ir.model.access.csv',
        
       # 'Data/f_groups.xml',
      #  'views/f_res_partner_inherit.xml',
    ],
  
}
