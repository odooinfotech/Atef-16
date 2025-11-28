# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpBomOverhead(models.Model):
    _name = 'mrp.bom.overhead'
    _description = 'MRP BOM Overhead'

    bom_id = fields.Many2one('mrp.bom', 'BoM', ondelete='cascade', index=True, copy=False)
    production_id = fields.Many2one('mrp.production', 'Production', ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one('product.product', domain="[('is_overhead', '=', True)]", string="Products")
    overhead_parameters = fields.Selection([('percent', 'Percent(%)'),
                                            ('amount_div_by_final_qty', 'Amount/ Final QTY'),
                                            ('amount_div_by_duration', 'Amount/ Duration'),
                                            ], string="Overheads", default='percent')
    overhead_cost = fields.Float(string="Cost")
