# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class FStockPickingBatchInherit(models.Model):
    _inherit = "stock.picking.batch"

    f_partner = fields.Many2many('res.partner', string='Customer', compute='_f_compute_package_partners')

    f_partner_char = fields.Char(related='f_partner.name', store=True, string='Customer')

    def _f_compute_package_partners(self):
        for record in self:
            domain = [('id', 'in', record.picking_ids.ids)]
            picking_ids = self.env['stock.picking'].search(domain)

            # Use read_group to group pickings by partner_id
            group_by_fields = ['partner_id']
            groups = self.env['stock.picking'].read_group([('id', 'in', picking_ids.ids)], ['partner_id'],
                                                          group_by_fields)

            partner_ids = [group['partner_id'][0] for group in groups if group['partner_id']]
            record.f_partner = [(6, 0, partner_ids)]
