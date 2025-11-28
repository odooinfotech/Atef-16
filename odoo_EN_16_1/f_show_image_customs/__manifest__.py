# -*- coding: utf-8 -*-
{
    'name': "Show Image Customization",

    'summary': """ This module created for display image in sales and invoices lines and reports """,

    'description': """
        Add product Image
            1. In sale order lines
            2. In quotation/order report
            3. In invoice lines
            4. Invoice report
    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'license': 'LGPL-3',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/f_sales_report_wizard.xml',
        'wizard/f_invoice_report_wizard.xml',
        'views/f_sale_order_line_inherit.xml',
        'views/f_account_move_line_inherit.xml',
        'reports/f_sale_report_template_inherit.xml',
        'reports/f_report_invoice_inherit.xml',
    ],

}
