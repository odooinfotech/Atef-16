from odoo import models, fields, api


class FAccountInvReportInheritD(models.Model):
    _inherit = "account.invoice.report"
    
    partner_shipping_id = fields.Many2one('res.partner' , string="Delivery Address")
    
    def _select(self):
        return super(FAccountInvReportInheritD, self)._select() + """  ,move.partner_shipping_id  """
