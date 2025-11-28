# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.



import json
import time
from ast import literal_eval
from datetime import date, timedelta
from collections import defaultdict

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_datetime, format_date, groupby
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class StockMove(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        """Call `_action_done` on the `stock.move` of the `stock.picking` in `self`.
        This method makes sure every `stock.move.line` is linked to a `stock.move` by either
        linking them to an existing one or a newly created one.

        If the context key `cancel_backorder` is present, backorders won't be created.

        :return: True
        :rtype: bool
        """
        self._check_company()

        todo_moves = self.sudo().move_ids.filtered(lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
        for picking in self:
            if picking.owner_id:
                picking.sudo().move_ids.sudo().write({'restrict_partner_id': picking.owner_id.id})
                picking.sudo().move_line_ids.sudo().write({'owner_id': picking.owner_id.id})
        todo_moves.sudo()._action_done(cancel_backorder=self.env.context.get('cancel_backorder'))
        self.write({'date_done': fields.Datetime.now(), 'priority': '0'})

        # if incoming/internal moves make other confirmed/partially_available moves available, assign them
        done_incoming_moves = self.sudo().filtered(lambda p: p.picking_type_id.code in ('incoming', 'internal')).move_ids.filtered(lambda m: m.state == 'done')
        done_incoming_moves.sudo()._trigger_assign()

        self._send_confirmation_email()
        return True




# from odoo import fields, models,_
# from odoo.osv import expression

# class StockMove(models.Model):
#     _inherit = "stock.move"

#     def _trigger_assign(self):
#         """ Check for and trigger action_assign for confirmed/partially_available moves related to done moves.
#             Disable auto reservation if user configured to do so.
#    """
#         if not self or self.env['ir.config_parameter'].sudo().get_param('stock.picking_no_auto_reserve'):
#             return

#         domains = []
#         for move in self:
#             domains.append([('product_id', '=', move.product_id.id), ('location_id', '=', move.location_dest_id.id)])
#         static_domain = [('state', 'in', ['confirmed', 'partially_available']),
#                          ('procure_method', '=', 'make_to_stock'),
#                          ('reservation_date', '<=', fields.Date.today())]
#         # add sudo
#         moves_to_reserve = self.sudo().env['stock.move'].sudo().search(expression.AND([static_domain, expression.OR(domains)]),
#                                                          order='reservation_date, priority desc, date asc, id asc')
#         # add sudo
#         moves_to_reserve.sudo()._action_assign()
