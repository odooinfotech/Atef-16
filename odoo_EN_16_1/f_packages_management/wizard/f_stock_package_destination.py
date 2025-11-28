# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class FChooseDestinationLocation(models.TransientModel):
    _name = 'f.stock.package.destination'
    _description = 'Stock Package Destination'

    f_picking_id = fields.Many2one('stock.picking', required=True)
    f_move_line_ids = fields.Many2many('stock.move.line', 'Products', compute='_f_compute_move_line_ids', required=True)
    f_location_dest_id = fields.Many2one('stock.location', 'Destination location', required=True)
    f_filtered_location = fields.One2many(comodel_name='stock.location', compute='_f_filter_location')

    @api.depends('f_picking_id')
    def _f_compute_move_line_ids(self):
        for destination in self:
            destination.f_move_line_ids = destination.f_picking_id.move_line_ids.filtered(lambda l: l.qty_done > 0 and not l.result_package_id)

    @api.depends('f_move_line_ids')
    def _f_filter_location(self):
        for destination in self:
            destination.f_filtered_location = destination.f_move_line_ids.mapped('location_dest_id')

    def f_action_done(self):
        # set the same location on each move line and pass again in action_put_in_pack
        self.f_move_line_ids.location_dest_id = self.f_location_dest_id
        return self.f_picking_id.f_action_put_in_pack()
