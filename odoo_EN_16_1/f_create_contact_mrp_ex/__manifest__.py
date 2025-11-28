# -*- coding: utf-8 -*-
{
    'name': "f_create_contact_mrp_ex",

    'summary': """
     mrp extend -  this module for create edit contact access""",

    'description': """
      this module for create edit contact access - mrp ex
    """,

    'author': "Falak Solutions",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','create_edit_contact_access'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
   
    ],
 
}
