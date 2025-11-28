# -*- coding: utf-8 -*-
# from odoo import http


# class FDefaultBillDate(http.Controller):
#     @http.route('/f_default_bill_date/f_default_bill_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_default_bill_date/f_default_bill_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_default_bill_date.listing', {
#             'root': '/f_default_bill_date/f_default_bill_date',
#             'objects': http.request.env['f_default_bill_date.f_default_bill_date'].search([]),
#         })

#     @http.route('/f_default_bill_date/f_default_bill_date/objects/<model("f_default_bill_date.f_default_bill_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_default_bill_date.object', {
#             'object': obj
#         })
