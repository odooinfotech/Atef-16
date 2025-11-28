# -*- coding: utf-8 -*-
{
    'name': "f_custom_aging_report",

    'summary': """
        Product Aging In Inventory""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','report_xlsx'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        'views/f_aging_details.xml',
        'views/f_aging_wizard.xml',
        'views/f_report_file_xls.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
