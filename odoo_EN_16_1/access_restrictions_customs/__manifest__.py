{
    'name': 'Falak Access Restrictions Customs',
    'summary': """Managing user login hours and session expiration.""",
    'version': '16.0.1.0.0',
    'depends': ['base','mail','access_restriction_by_ip'],
    'license': 'LGPL-3',
    'author': "Falak Solutions",
    'data': [
        'data/f_logout_schedule_action.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
