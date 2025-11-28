# -*- coding: utf-8 -*-
# from odoo import http


# class FLocationQtysCostReport(http.Controller):
#     @http.route('/f_location_qtys_cost_report/f_location_qtys_cost_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_location_qtys_cost_report/f_location_qtys_cost_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_location_qtys_cost_report.listing', {
#             'root': '/f_location_qtys_cost_report/f_location_qtys_cost_report',
#             'objects': http.request.env['f_location_qtys_cost_report.f_location_qtys_cost_report'].search([]),
#         })

#     @http.route('/f_location_qtys_cost_report/f_location_qtys_cost_report/objects/<model("f_location_qtys_cost_report.f_location_qtys_cost_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_location_qtys_cost_report.object', {
#             'object': obj
#         })
