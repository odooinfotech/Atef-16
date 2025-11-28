# -*- coding: utf-8 -*-
# from odoo import http


# class FalakProductBarcode(http.Controller):
#     @http.route('/falak_product_barcode/falak_product_barcode/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/falak_product_barcode/falak_product_barcode/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('falak_product_barcode.listing', {
#             'root': '/falak_product_barcode/falak_product_barcode',
#             'objects': http.request.env['falak_product_barcode.falak_product_barcode'].search([]),
#         })

#     @http.route('/falak_product_barcode/falak_product_barcode/objects/<model("falak_product_barcode.falak_product_barcode"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('falak_product_barcode.object', {
#             'object': obj
#         })
