# -*- coding: utf-8 -*-
# from odoo import http


# class FalakProfitReport(http.Controller):
#     @http.route('/falak_profit_report/falak_profit_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/falak_profit_report/falak_profit_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('falak_profit_report.listing', {
#             'root': '/falak_profit_report/falak_profit_report',
#             'objects': http.request.env['falak_profit_report.falak_profit_report'].search([]),
#         })

#     @http.route('/falak_profit_report/falak_profit_report/objects/<model("falak_profit_report.falak_profit_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('falak_profit_report.object', {
#             'object': obj
#         })
