# -*- coding: utf-8 -*-
from odoo import models, api, fields
import logging
_logger = logging.getLogger('mrp create')


class F_Report_Man_Orders_Products(models.Model):
    _name = 'f.report.man.orders.products'
    _description = "MRP Production Report"
    
    f_user_id = fields.Many2one('res.users',string="Users",required=True)
    f_product_id = fields.Many2one('product.product',string="Product ID",required=True)
    f_product_name = fields.Char(string="Product Name",related="f_product_id.name",required=True)
    f_production_qty =fields.Float(string="Total Production QTY",required=True)
    f_on_hand_qty =fields.Float(string="On Hand QTY",related="f_product_id.qty_available",required=True)
    f_order_date = fields.Date(string="Orders Date",required=True)
    
    