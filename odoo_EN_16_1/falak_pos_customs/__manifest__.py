# -*- coding: utf-8 -*-
{
    'name': "Falak POS Customs",

    'description': """
    This module for pos customization
    """,

    'author': "Falak Solutions",
    'category': 'Uncategorized',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'point_of_sale'],

    # always loaded
    'data': [
        'data/f_pos_order_partner_group.xml',
        'views/f_pos_order_inherit.xml',
    ],
}
