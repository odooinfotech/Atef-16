# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': " Manufacturing Overhead",
    'summary': "Manufacturing Cost of OverHeads, Employee Time Sheet Cost Calculations\
                Same Opertions with Multi Workcenter,Cost of OverHeads Percent On Total Cost operations and\
                calculate the cost of valuation of finished manufacturing product" ,
    'version': "15.0.1.0",
    'category': "Customizations",
    'description': """
    Task Id: 2758801 
    1.Manufacturing OverHeads Cost Calculations :
      Manufacturing OverHeads Cost Calculations based on below the OverHeads
        1.1 Percent '%'
        1.2 Amount/ Final QTY
        1.3 Amount/ Duration
    and also added the Cost of OverHeads Calculation details into the MRP Cost Analysis Report.
    2.Calcualte the Cost of Employee Timesheet Cost
    3.Calcualte the Cost of OverHeads Percent Total Cost
    4.Same Operations with Multi Workcenters Configurations
    5.Calculate the Cost Valuation of finished manufacturing product along with Cost of operations, Cost of Overheads,
      Cost of Employee Timesheet Cost
    6.Added the Shift on Production Order
    7.Added the Workcentergroup on Workcenter.
    """,
    'author': 'Falak Solutions',
    'license': 'LGPL-3',
    #'website': "http://www.odoo.com",
    'depends': ['product', 'mrp', 'mrp_account_enterprise', 'hr_timesheet','falak_mrp_definition','hide_product_cost'],
    'data': [
        'security/ir.model.access.csv',
        'data/f_compute_bom_cost_scheduled.xml',
        'data/f_groups.xml',
        'report/f_product_mrp_cost_analysis_action.xml',
        'report/f_product_mrp_cost_analysis_template.xml',
        'views/product_views.xml',
        'views/mrp_bom_view.xml',
        'views/mrp_production_views.xml',
        'views/mrp_workorder_view.xml',
        'views/f_mrp_config_menues.xml',
        'report/mrp_cost_structure.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'assets': {
        'web.report_assets_common': [
            'mrp_cost/static/src/scss/f_product_cost_analysis_report.scss',
        ],
    }
}
