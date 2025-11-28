# -*- coding: utf-8 -*-
from odoo import http

# class PrintJournalEnteries(http.Controller):
#     @http.route('/print_journal_enteries/print_journal_enteries/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/print_journal_enteries/print_journal_enteries/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('print_journal_enteries.listing', {
#             'root': '/print_journal_enteries/print_journal_enteries',
#             'objects': http.request.env['print_journal_enteries.print_journal_enteries'].search([]),
#         })

#     @http.route('/print_journal_enteries/print_journal_enteries/objects/<model("print_journal_enteries.print_journal_enteries"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('print_journal_enteries.object', {
#             'object': obj
#         })