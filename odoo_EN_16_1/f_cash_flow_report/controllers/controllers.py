# -*- coding: utf-8 -*-
# from odoo import http


# class FCashFlowReport(http.Controller):
#     @http.route('/f_cash_flow_report/f_cash_flow_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_cash_flow_report/f_cash_flow_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_cash_flow_report.listing', {
#             'root': '/f_cash_flow_report/f_cash_flow_report',
#             'objects': http.request.env['f_cash_flow_report.f_cash_flow_report'].search([]),
#         })

#     @http.route('/f_cash_flow_report/f_cash_flow_report/objects/<model("f_cash_flow_report.f_cash_flow_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_cash_flow_report.object', {
#             'object': obj
#         })
