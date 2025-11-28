# -*- coding: utf-8 -*-
# from odoo import http


# class FContactBalanceCustoms(http.Controller):
#     @http.route('/f_contact_balance_customs/f_contact_balance_customs/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_contact_balance_customs/f_contact_balance_customs/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_contact_balance_customs.listing', {
#             'root': '/f_contact_balance_customs/f_contact_balance_customs',
#             'objects': http.request.env['f_contact_balance_customs.f_contact_balance_customs'].search([]),
#         })

#     @http.route('/f_contact_balance_customs/f_contact_balance_customs/objects/<model("f_contact_balance_customs.f_contact_balance_customs"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_contact_balance_customs.object', {
#             'object': obj
#         })
