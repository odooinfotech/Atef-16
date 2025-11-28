# -*- coding: utf-8 -*-
{
    'name': "f_statament_payment_report_xlsx_ex",

    'summary': """
       add excel report to statament """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Falak Solutions",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report_xlsx','f_partner_statemment_payment_ext'],

    # always loaded
    'data': [
        'views/f_repert_xls.xml',
    ],

}
