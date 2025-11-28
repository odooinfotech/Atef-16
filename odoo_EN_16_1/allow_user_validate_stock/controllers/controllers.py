# -*- coding: utf-8 -*-
# from odoo import http


# class AllowUserValidateStock(http.Controller):
#     @http.route('/allow_user_validate_stock/allow_user_validate_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/allow_user_validate_stock/allow_user_validate_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('allow_user_validate_stock.listing', {
#             'root': '/allow_user_validate_stock/allow_user_validate_stock',
#             'objects': http.request.env['allow_user_validate_stock.allow_user_validate_stock'].search([]),
#         })

#     @http.route('/allow_user_validate_stock/allow_user_validate_stock/objects/<model("allow_user_validate_stock.allow_user_validate_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('allow_user_validate_stock.object', {
#             'object': obj
#         })
