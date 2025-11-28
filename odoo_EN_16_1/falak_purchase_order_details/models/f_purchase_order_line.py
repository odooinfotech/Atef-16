# -*- coding: utf-8 -*-

from odoo import models, fields, api

class F_Purchase_Order_Line_Inherit(models.Model):
     _inherit = 'purchase.order.line'
     _description = 'purchase_order_Line_details'
   
   
    #fields purchase order header
     f_po_name =fields.Char(related='order_id.name',string='Purchase Name')
     f_vendor= fields.Many2one('res.partner',related='order_id.partner_id',string='Vendor')
     
    
