# -*- coding: utf-8 -*-
{
    'name': "Falak Commission Management",

    'summary': """ This Module to manage commission calculations""",

    'description': """
        
    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','f_product_family','account','account_accountant','contacts'],

    # always loaded
    'data': [
        'data/f_groups.xml',
        'security/ir.model.access.csv',
        'wizards/f_progress_info_wizard.xml',
        'wizards/f_commission_report_wizard.xml',
        'reports/f_commission_report.xml',
        'views/f_commission_base_views.xml',
        'views/f_collection_type.xml',
        'views/f_commission_role.xml',
        'views/f_commission_period.xml',
        'views/f_aged_balance_matrix.xml',
        'views/f_commission_result.xml',
        'views/f_collections_adjustment.xml',
        'views/f_account_move_inherit.xml',
        'views/f_account_payment_inherit.xml',
        'views/f_res_partner_inherit.xml',
        'views/f_commission_setup.xml',
        'views/f_commission_calculation.xml',
        'views/f_setup_progress_info.xml',
    ],
}
