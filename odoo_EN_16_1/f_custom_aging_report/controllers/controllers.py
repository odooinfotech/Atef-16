# -*- coding: utf-8 -*-
# from odoo import http


# class FCustomAgingReport(http.Controller):
#     @http.route('/f_custom_aging_report/f_custom_aging_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_custom_aging_report/f_custom_aging_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_custom_aging_report.listing', {
#             'root': '/f_custom_aging_report/f_custom_aging_report',
#             'objects': http.request.env['f_custom_aging_report.f_custom_aging_report'].search([]),
#         })

#     @http.route('/f_custom_aging_report/f_custom_aging_report/objects/<model("f_custom_aging_report.f_custom_aging_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_custom_aging_report.object', {
#             'object': obj
#         })
