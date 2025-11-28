# -*- coding: utf-8 -*-
{
    'name': "Falak Purchase Logistics",

    'summary': """
       this modules also for purchase order planning customization""",

    'description': """
    we should create the shipp seq and create the shipp stages manually
    """,

    'author': "Falak Solutions",
    #'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '16.0',
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,
    'depends': ['base','mail','purchase','f_lc_management','product','base_automation', 'documents'],

    'data': [
        'security/ir.model.access.csv',
        'security/f_record_rules.xml',
        'data/f_workspaces_data.xml',
        'data/f_groups.xml',
        'views/f_res_settings_inherit.xml',
        'views/f_account_move_inherit.xml',
        'views/f_account_incoterm_inherit.xml',
        'views/f_shipping_dates_history.xml',
        'views/f_purchase_planning.xml',
        'views/f_purchase_order_inherit.xml',
        'views/f_purchase_lockups_views.xml',
        'views/f_purchase_order_config_menue.xml',
        'views/f_container_details.xml',
        'views/f_class_template.xml',
        'views/f_classification_approval.xml',
        'views/f_shipping_details_view.xml',
        'views/f_res_partner_view_inherit.xml',
        'views/f_res_users_inherit.xml',
        'views/f_product_template_inherit.xml',
        'data/f_sequence_data.xml',
        'data/f_shipping_stages.xml',
        'data/f_automated_actions.xml',
        'data/f_contact_tags.xml',
        'data/f_data.xml',
        'views/f_res_country_inherit.xml',
        'report/f_shipping_report_template.xml',
        'report/f_shipping_report_action.xml',
        'wizards/f_approval_message_wizard.xml',
    ],
  
}
