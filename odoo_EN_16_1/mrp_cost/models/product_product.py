# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    

    def button_bom_weight(self):
        MrpBoMLines = self.env['mrp.bom.line'].search([('bom_id.product_tmpl_id', '=', self.product_tmpl_id.id)])
        [line._onchange_coefficent_parameters() for line in MrpBoMLines]

    
    def compute_bom_cost(self):
        self.mapped('product_tmpl_id').compute_bom_cost()

    def f_action_cost_analysis(self):
        self.mapped('product_tmpl_id').f_action_cost_analysis()
