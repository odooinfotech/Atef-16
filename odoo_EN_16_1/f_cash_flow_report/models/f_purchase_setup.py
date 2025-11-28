# -*- coding: utf-8 -*-

from odoo import models, fields, api,_,tools
from odoo.exceptions import UserError



class f_tpayypespurchase_setup_wizard(models.Model):
    _name = 'f.po.payment.forcaste.types'
    _rec_name = 'name'
    _description = "PO payment Forecasted types"
    name = fields.Char('Name')
    
    


class f_paymentpurchase_setup_wizard(models.Model):
    _name = 'f.po.payment.forcaste'
    _description = "PO Payments Forecasts"
    name = fields.Selection([('bank','Bank'),('cash','Cash'),('check','Check')],string='Name')
    f_name = fields.Many2one('f.po.payment.forcaste.types',string='Payment Method')
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    company_id = fields.Many2one('res.company', string='Company',  readonly=True,
        default=lambda self: self.env.company)
    
    currency_id = fields.Many2one('res.currency', string='Currency')
    
    
    purchase_id = fields.Many2one('purchase.order',string='PO Order')
    
    currency_rate = fields.Float(string ='Currency Rate',compute="_f_get_rate",store=True,digits=0, readonly=True)
    
    

            
    
    @api.depends('currency_id','date','company_id')
    def _f_get_rate(self):
        for x in self :
            print("111111111111")
            x.currency_rate = 1
            if x.date:
                if x.currency_id:
                    rate = self.env['res.currency']._get_conversion_rate(x.company_id.currency_id, x.currency_id, x.company_id, x.date)
                    print("111111111111",rate,"ratetet")
                    if rate:
                        x.currency_rate = rate
                        

    
    
class f_InheritPurchase(models.Model):
    _inherit = 'purchase.order'
    
    f_forcasted_ids = fields.One2many('f.po.payment.forcaste','purchase_id',string='Forcaste Payment')


class f_typespurchase_setup_wizard(models.Model):
    _name = 'f.po.forcaste.types'
    _rec_name = 'name'
    _description = "PO Forecasted Types"
    name = fields.Char('Name')


class f_purchase_setup_wizard(models.Model):
    _name = 'f.po.setup.amount'
    _description = "PO Forecasted Data"
    
    
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    type_id = fields.Many2one('f.po.forcaste.types',string= 'Type')
    company_id = fields.Many2one('res.company', string='Company',  readonly=True,
        default=lambda self: self.env.company)
    label = fields.Char('Label')
    currency_id = fields.Many2one('res.currency', string='Currency')
    
    currency_rate = fields.Float(string ='Currency Rate',compute="_f_get_rate",store=True,digits=0, readonly=True)
    
    

            
    
    @api.depends('currency_id','date','company_id')
    def _f_get_rate(self):
        for x in self :
            print("111111111111")
            x.currency_rate = 1
            if x.date:
                if x.currency_id:
                    rate = self.env['res.currency']._get_conversion_rate(x.company_id.currency_id, x.currency_id, x.company_id, x.date)
                    print("111111111111",rate,"ratetet")
                    if rate:
                        x.currency_rate = rate
                        
                        
