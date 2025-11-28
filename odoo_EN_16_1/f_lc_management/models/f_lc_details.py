# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FLCManagement(models.Model):
    _name = 'f.lc.management'
    _description = 'LC Management'
    _inherit = ['mail.thread']
    _rec_name="f_lc_name"
     
    f_purchase_id =fields.Many2one('purchase.order',string="Purchase Order")
    #lc Details
    f_lc_name =fields.Char(string="LC Name" ,default='New' ,required=True ,index=True ,copy=False)
    
    @api.model
    def create(self, vals):
        vals['f_lc_name'] = self.env['ir.sequence'].next_by_code('f.lc.management')
        return super(FLCManagement, self).create(vals)
    
    f_lc_number =fields.Char(string="LC Number")
    f_lc_date=fields.Date(string="LC Date")
    
    #Insurance details
    f_insurance_name =fields.Many2one('res.partner',string="Insurance Name")
    f_insurance_policy =fields.Many2one('f.insurance.policy',string="Insurance Policy")
    f_insurance_attachment =fields.Binary(string="Insurance Attachment")
  
    file_name_insurance = fields.Char(string='Insurance File')

    
    
    
    f_lc_currency= fields.Many2one(comodel_name='res.currency',string='LC Currency')
    f_notes =fields.Char(string="Notes")
    f_account_journal =fields.Many2one('account.journal',string="Account Journal")
    f_debit_account =fields.Many2one('account.account',string="Debit Account")
    f_credit_account =fields.Many2one('account.account',string="Credit Account")
    
    
    #Bank Details 
    f_bank_name =fields.Many2one('res.bank',string="Bank Name")
    f_bank_account_no= fields.Char(string="Bank Account Number")
    

   
    
    
    

    
