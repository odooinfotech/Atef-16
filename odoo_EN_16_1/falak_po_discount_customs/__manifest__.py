# -*- coding: utf-8 -*-
{
    'name': "Falak PO Discount Customs",

    'description': """
        Purchase order lines discount and full price customization
    """,

    'author': "Falak Solutions",
    'license': 'LGPL-3',
    'installable': True,
    'depends': ['base','mail','purchase', 'account', 'account_accountant'],

    'data': [
        'views/f_purchase_order_inherit.xml',
        'views/f_account_move_inherit.xml',
    ],
  
}
