# -*- coding: utf-8 -*-
# from odoo import http


# class FSaleStockForcaste(http.Controller):
#     @http.route('/f_sale_stock_forcaste/f_sale_stock_forcaste', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/f_sale_stock_forcaste/f_sale_stock_forcaste/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('f_sale_stock_forcaste.listing', {
#             'root': '/f_sale_stock_forcaste/f_sale_stock_forcaste',
#             'objects': http.request.env['f_sale_stock_forcaste.f_sale_stock_forcaste'].search([]),
#         })

#     @http.route('/f_sale_stock_forcaste/f_sale_stock_forcaste/objects/<model("f_sale_stock_forcaste.f_sale_stock_forcaste"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('f_sale_stock_forcaste.object', {
#             'object': obj
#         })
