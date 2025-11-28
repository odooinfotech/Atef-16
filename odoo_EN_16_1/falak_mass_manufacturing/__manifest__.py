# -*- coding: utf-8 -*-
{
    'name': "Falak Mass Manufacturing",

    'summary': """
      Falak Mass Manufacturing
      
      """,

    'description': """

    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','mrp','product','uom','falak_manufacturing_planning','falak_mrp_definition'],

    # always loaded
    'data': [
        'Data/f_seq_number.xml',
        'security/ir.model.access.csv',
        'report/f_report_man_orders_products_templates.xml',
        'wizards/f_mrp_production_warning_view.xml',
        'wizards/f_mrp_production_report_view.xml',
        'views/f_mrp_production_inherit.xml',    
        'views/f_mass_man_products.xml',
        'views/f_mass_manufacturing.xml',
        'report/f_report_man_orders_products.xml',
        
    ],
    
}
