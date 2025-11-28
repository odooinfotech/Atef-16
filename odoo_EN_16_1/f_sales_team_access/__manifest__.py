# -*- coding: utf-8 -*-
{
    'name': "Falak Sales Team Access",

    'description': """
        group the user will be able to see the sales orders that the user is within the sales team
    """,

    'author': "Falak Solutions",

    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sale_management', 'contacts', 'account', 'account_accountant'],

    # always loaded
    'data': [
            'security/f_sales_team_access_security.xml',
            'views/views.xml',
            'data/f_group_sales_team_access.xml',
    ],
   
}
