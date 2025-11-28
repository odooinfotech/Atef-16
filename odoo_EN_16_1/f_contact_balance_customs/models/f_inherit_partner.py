# -*- coding: utf-8 -*-

from odoo import models, fields, api


class f_inheritpartners(models.Model):
    _inherit = 'res.partner'
    
    f_balance = fields.Monetary(string='Total Balance',compute="f_balanceget_partner_fields",currency_field='currency_id',search="f_search_balance")
    
   
    
    
    def f_balanceget_partner_fields(self):
        partner_ids = self.ids
        if not partner_ids:
            return
        
        # Use read_group to aggregate balances efficiently
        balances = self.env['account.move.line'].read_group(
            domain=[
                ('move_id.state', '=', 'posted'),
                ('move_id.company_id', '=', self.env.company.id),
                ('account_id.account_type', 'in', ('asset_receivable', 'liability_payable')),
                ('partner_id', 'in', partner_ids)
            ],
            fields=['partner_id', 'balance:sum'],
            groupby=['partner_id']
        )

        # Create a mapping of partner_id -> balance
        balance_dict = {b['partner_id'][0]: b['balance'] for b in balances}

        # Assign computed values
        for partner in self:
            partner.f_balance = balance_dict.get(partner.id, 0.0)

    
        # for rec in self:
        #     self.env.cr.execute("""
        #                         select partner_id, sum(xbalance)as credit from (
        #                             select  partner_id, xbalance
        #                             from (
        #                             select p.id as partner_id,

        #                               COALESCE(SUM(aml.debit - aml.credit ),0)as xbalance
        #                             from account_move_line aml,
        #                                 account_move am , 
        #                                 account_account ac, 
        #                                 res_partner p
        #                             where aml.move_id = am.id
        #                             AND am.state = 'posted'
        #                             and am.company_id = %s

        #                             AND  ac.id = aml.account_id
        #                               and  ac.account_type IN ('asset_receivable','liability_payable')
        #                             AND p.id = aml.partner_id

        #                             group by p.id
        #                             ) s1 
        #                             ) s2 
        #                             where
        #                              partner_id =%s

        #                             group by partner_id

        #                         """ % (self.env.company.id, rec.id))

        #     total_balance = 0
        #     credit_result = self.env.cr.fetchone()
        #     if credit_result:
        #         total_balance = credit_result[1]


        #     rec.f_balance = total_balance
            #rec.f_balance = rec.sudo().credit - rec.sudo().debit
          
            
            
    def f_search_balance(self,  operator,value):
        if operator == '=':
            operator = '=='

        partners = self.env['account.move.line'].read_group(
            domain=[
                ('move_id.state', '=', 'posted'),
                ('move_id.company_id', '=', self.env.company.id),
                ('account_id.account_type', 'in', ('asset_receivable', 'liability_payable'))
            ],
            fields=['partner_id', 'balance:sum'],
            groupby=['partner_id']
        )
    
        # Ensure 'partner_id' exists and is not a boolean
        partner_ids = [
            p['partner_id'][0] for p in partners 
            if isinstance(p.get('partner_id'), tuple) and eval(f"{p.get('balance', 0)} {operator} {value}")
        ]
    
        return [('id', 'in', partner_ids)]
