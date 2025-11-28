# -*- coding: utf-8 -*
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.upgrade import util

def migrate(cr, version):
   
    util.fields.remove_field(cr, 'sale.order', 'f_price_unit' )
