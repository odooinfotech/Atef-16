from odoo import models, tools, api, fields, _
from lxml import etree
from odoo.http import request


class f_falak_loc_qtycost_details(models.Model):
    _name = 'f.loc.qty.cost.details'
    _description = "Location qtys - cost report"
    _auto = False

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    is_zero_qtys = fields.Integer( string='Zero Qtys', readonly=True)
    qty_from_loc = fields.Float(string="Qty /From Date", readonly=True)
    cost_from_loc = fields.Float(string="Val.Cost /From Date", readonly=True)
    cost_stan_from_loc = fields.Float(string="Standard Cost /From Date", readonly=True)

    qty_to_loc = fields.Float(string="Qty /To Date", readonly=True)
    cost_to_loc = fields.Float(string="Val.Cost /To Date", readonly=True)
    cost_stan_to_loc = fields.Float(string="Standard Cost /To Date", readonly=True)