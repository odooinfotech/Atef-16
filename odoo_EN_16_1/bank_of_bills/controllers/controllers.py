# -*- coding: utf-8 -*-
from odoo import http

# class TaxReport(http.Controller):
#     @http.route('/tax_report/tax_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax_report/tax_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax_report.listing', {
#             'root': '/tax_report/tax_report',
#             'objects': http.request.env['tax_report.tax_report'].search([]),
#         })

#     @http.route('/tax_report/tax_report/objects/<model("tax_report.tax_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax_report.object', {
#             'object': obj
#         })