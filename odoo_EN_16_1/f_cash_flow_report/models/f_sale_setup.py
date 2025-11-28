# -*- coding: utf-8 -*-

from odoo import models, fields, api,_,tools

class f_typesso_setup_wizard(models.Model):
    _name = 'f.sale.forcaste.types'
    _rec_name = 'name'
    _description = "Sale Forecasted Types"
    name = fields.Char('Name')


class f_sale_setup_wizard(models.Model):
    _name = 'f.sale.setup.amount'
    _description = "Sale Forecasted Data"
    
    
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    type_id = fields.Many2one('f.sale.forcaste.types',string= 'Type') 
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
