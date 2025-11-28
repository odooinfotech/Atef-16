# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools,_


class falak_customer_statementdetails_report(models.Model):
    _name = 'f.customer.detailed.report'
    _description = "Customer Detailed statement "
    #_auto = False
    _order = "f_report_date asc ,f_last_upadeton asc , id asc"

    acum_balance = fields.Monetary('Total Balance', readonly=True, default=0, currency_field='company_currency')
    f_initial_balance = fields.Monetary('Beginning Balance', readonly=True, default=0,
                                        currency_field='company_currency')
    
    
    
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    state = fields.Selection([('paid', 'Paid'), ('done', 'Done'), ('posted', 'Posted')], readonly=True)
    date = fields.Date(string='Date', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    company_currency = fields.Many2one('res.currency', string='Company Currency', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    product_list = fields.Text('Product List', readonly=True)
    f_user_id = fields.Many2one('res.users', string='Report User', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journals', readonly=True)
    amount_total = fields.Monetary('Sale Order Amount', help="Sale Order Amount", readonly=True)
    balance = fields.Monetary('Credit Payment', readonly=True)
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True)
    employee_name = fields.Char( string='Employee', readonly=True)
    f_last_upadeton = fields.Datetime(string='Created On', readonly=True)
    account_type = fields.Char(string='Account Type', readonly=True)
    amount_cuurency = fields.Monetary('Amount Currency', readonly=True,currency_field='currency_id')
   # type= fields.Char(string="Type", readonly=True)
    type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_refund', 'Customer Credit Note'),
        ('in_refund', 'Vendor Credit Note'),
        ('entry', 'Journal Entry'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
        ('beg_bal', 'Beg. Balance'),
        ('inbound', 'Customer Receipt'),
        ('outbound', 'Vendor Payment'),
        ('pos_order', 'POS Order'),
        ('pos_paym', 'POS Payment'),
        ], readonly=True)
    
    debt=fields.Monetary('Debit', readonly=True , default=0,currency_field='company_currency')
    credit = fields.Monetary('Credit', readonly=True , default=0,currency_field='company_currency')
    ref = fields.Char(string="Ref", readonly=True)
    
    check_bounce=fields.Monetary('Total Check Bounce', readonly=True , default=0,currency_field='company_currency')
    f_note = fields.Text("Notes")
    
    
    f_report_date = fields.Date(string = 'Reporting Date')


    # def init(self):
    #     tools.drop_view_if_exists(self._cr, self._table)
    #     self.env.cr.execute("""CREATE or REPLACE VIEW %s as
    #      select max(a.id) as id from product_product a
    #
    #
    #      """ % (self._table))

#     @property
#     def _table_query(self):
#         return '%s ' % (self._query())
    
    


