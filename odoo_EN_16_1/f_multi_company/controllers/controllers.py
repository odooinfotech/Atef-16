# -*- coding: utf-8 -*-
# from odoo import http


# class FMultiCompany(http.Controller):
#     @http.route('/f_multi_company/f_multi_company', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_multi_company/f_multi_company/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_multi_company.listing', {
#             'root': '/f_multi_company/f_multi_company',
#             'objects': http.request.env['f_multi_company.f_multi_company'].search([]),
#         })

#     @http.route('/f_multi_company/f_multi_company/objects/<model("f_multi_company.f_multi_company"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_multi_company.object', {
#             'object': obj
#         })
