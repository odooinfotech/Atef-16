# -*- coding: utf-8 -*-
{
    'name': "Falak Customer Detailed Statement",

    'summary': """
        This Module includes a customized Customer Detailed Statement in PDF and Excel/View 
        Formats  
        Also includes Thermal Statement 

        
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
    'depends': ['base','account','check_management','contacts','f_access_categ','f_sale_account_report_menu'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/f_res_config_inherit.xml',
        'views/f_inherit_account_move.xml',
          
         'views/f_statement_pdfwizard.xml',
          'views/f_statement_view.xml',
          'views/f_statement_thermal_view.xml',
          'report/f_statement_report_pdf.xml',
          'report/f_statement_report_thermal_pdf.xml',
           'report/report_file_thermal.xml',
        'report/report_file.xml',
        'views/f_inherit_partner.xml',
       'views/f_sale_order_view_inherit.xml',
       
    ],
   
}
