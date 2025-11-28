# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FContainerSize(models.Model):
    _name ='f.container.size'
    _rec_name ='f_name'
    _description = 'Container Size'
    
    f_name =fields.Char(string="Name")
    


class FPaymentsTerms(models.Model):
    _name ='f.payment.terms'
    _rec_name ='f_payment_name'
    _description = 'Payment Terms'

    f_payment_name =fields.Char(string="Payment Term Name")
    
    
class FShippingLines(models.Model):
    _name ='f.shipping.line'
    _rec_name ='f_ship_line_name'
    _description = 'Shipping Line'
    
    f_ship_line_name =fields.Char(string="Shipping Line Name")
    
    
class FPurchasePorts(models.Model):
    _name ='f.purchase.ports'
    _rec_name ='f_port_name'
    _description = 'Purchase Report'
    
    f_port_name =fields.Char(string="Port Name")    
    
    f_port_type = fields.Selection([('loading', 'Loading'),
                                    ('discharge', 'Discharge'),
                                    ('both','Both')],string='Type Loading / Discharge')
    
    f_shipping_period = fields.Integer(string="Shipping Period")
    
    
    
    
    
