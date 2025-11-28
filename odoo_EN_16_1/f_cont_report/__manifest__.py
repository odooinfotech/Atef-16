# -*- coding: utf-8 -*-
{
    'name': "Contacts Balance Report",

    'summary': """
       Contacts Report
        
        """,

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
    'depends': ['base','contacts','account','check_management','f_partner_credit_limit','f_header_onpartner_list_view'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/f_report_task_template.xml',
        'report/f_general_report_template.xml',
        'report/f_report_task.xml',
        'views/f_inherit_partners.xml',
        
    ],    
}
