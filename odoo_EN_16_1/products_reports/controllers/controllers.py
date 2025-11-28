# -*- coding: utf-8 -*-
# from odoo import http


# class ProductsReports(http.Controller):
#     @http.route('/products_reports/products_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/products_reports/products_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('products_reports.listing', {
#             'root': '/products_reports/products_reports',
#             'objects': http.request.env['products_reports.products_reports'].search([]),
#         })

#     @http.route('/products_reports/products_reports/objects/<model("products_reports.products_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('products_reports.object', {
#             'object': obj
#         })
