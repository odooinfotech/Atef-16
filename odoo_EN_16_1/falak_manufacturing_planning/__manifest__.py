# -*- coding: utf-8 -*-
{
    'name': "Falak Manufacturing Planning",

    'summary': """
        Manufacturing Planning Customs""",

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
    'depends': ['base','mrp','product','uom','falak_mrp_definition','hr'],

    # always loaded
    'data': [
        'Data/f_seq_number.xml',
        'Data/f_mrp_planning_departments.xml',
        'security/ir.model.access.csv',
        'wizard/f_min_qty_prods_wizard.xml',
        'wizard/f_planning_wizard_report_view.xml',
        #'wizard/f_set_actual_date_wizard.xml',
        'views/f_res_config_setting_inherit.xml',
        'views/f_mrp_production_inherit.xml',
        'views/f_man_products.xml',
        'views/f_bill_of_material_inherit.xml',
        'views/f_manufacturing_planning.xml',
        'views/f_stock_orderpoint_inherit.xml',
        'views/f_mp_category.xml',
        'views/f_product_template_inherit.xml',
        'report/f_man_planning_report_template.xml',
        'report/f_mo_plan_products_report.xml',
    ],
    
}
