# -*- coding: utf-8 -*-
{
    'name': "Product Barcode Label ",

    'summary': """
        Custom product Label 
      
""",

    'description': """
       
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','account'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
         'views/f_product_label_report.xml',
         'views/f_res_company_inherit_view.xml',
         'report/report_template.xml',
         'report/report_pdf.xml',
         'views/f_label_with_qty_wizard.xml',
         'views/f_inherit_produc.xml',
         'views/f_label_with_qty_wizard_invoices.xml',
     
    ],
    # only loaded in demonstration mode
  
}
