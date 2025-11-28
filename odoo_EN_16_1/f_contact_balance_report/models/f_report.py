from odoo import models, tools, api, fields, _
from datetime import datetime,timedelta,date

class F_contact_balances_Report(models.Model):
    _name = "f.contatc.balance.report"
    _description = "Contacts Balances Report"
    _auto = False
    id = fields.Integer("Partner Id", readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    tags_ids = fields.Many2many(related='partner_id.category_id', string='Tags', readonly=True)
    company_id = fields.Many2one('res.company', string="Company", readonly=True)
    company_currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    balance = fields.Monetary('Balance', currency_field='company_currency_id', readonly=True)
    ref = fields.Char("Ref", readonly=True)
    city = fields.Char("City", readonly=True)
    city_id = fields.Many2one('res.city', string="City ID", readonly=True)
    mobile = fields.Char("Mobile", readonly=True)
    user_id = fields.Many2one('res.users', readonly=True, string='SalesPerson')
    check_bounce = fields.Monetary('Bounced Checks', currency_field='company_currency_id', readonly=True)
    balance_check_bounce = fields.Monetary('Balance With BC', currency_field='company_currency_id', readonly=True)




    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
           select max(a.id) as id from product_product a
           """ % (self._table))
