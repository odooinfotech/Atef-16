# -*- coding: utf-8 -*-
# from odoo import http


# class FMoCostAnalysis(http.Controller):
#     @http.route('/f_mo_cost_analysis/f_mo_cost_analysis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_mo_cost_analysis/f_mo_cost_analysis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_mo_cost_analysis.listing', {
#             'root': '/f_mo_cost_analysis/f_mo_cost_analysis',
#             'objects': http.request.env['f_mo_cost_analysis.f_mo_cost_analysis'].search([]),
#         })

#     @http.route('/f_mo_cost_analysis/f_mo_cost_analysis/objects/<model("f_mo_cost_analysis.f_mo_cost_analysis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_mo_cost_analysis.object', {
#             'object': obj
#         })
