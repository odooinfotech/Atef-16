# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class InherritSaleReportD(models.Model):
    _inherit = "sale.report"
    
    delivery_address = fields.Many2one('res.partner',string = 'Delivery Address')
    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['delivery_address'] = "s.partner_shipping_id"
        
        
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """, s.partner_shipping_id"""
        return res
    
