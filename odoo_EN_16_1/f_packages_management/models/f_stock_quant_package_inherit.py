# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FStockQuantPackageInherit(models.Model):
    _inherit = 'stock.quant.package'

    f_printed = fields.Boolean(string='Printed', default=False, copy=False)

    f_partner = fields.Many2many('res.partner', string='Customer', compute='_f_compute_package_partners')

    f_partner_char = fields.Char(string='Customer')
    f_product_char = fields.Char(string='Product Description')
    f_product_id = fields.Many2one('product.product', string='Product')

    def _f_compute_package_partners(self):
        for record in self:
            domain = ['|', ('result_package_id', 'in', record.ids), ('package_id', 'in', record.ids)]
            stock_move_lines = self.env['stock.move.line'].search(domain)
            picking_ids = stock_move_lines.mapped('picking_id')

            # Use read_group to group pickings by partner_id
            group_by_fields = ['partner_id']
            groups = self.env['stock.picking'].read_group([('id', 'in', picking_ids.ids)], ['partner_id'],
                                                          group_by_fields)
            record.f_partner = []
            name = ''
            for group in groups:
                if group['partner_id']:
                    record.f_partner = [(4, group['partner_id'][0])]
                    name += group['partner_id'][1] + ', '
            record.f_partner_char = name

    def f_print_package(self):
        return (self.env.ref('f_packages_management.f_action_package_label_barcode').
                report_action(self))
