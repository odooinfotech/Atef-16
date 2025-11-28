from odoo import models, fields, api
class FSPAccountMoveInherit(models.Model):
    _inherit = "account.move"

    def _set_default_sp(self):
        if self.partner_id:
            invoice_user_id = self.partner_id.user_id.id
        else:
            invoice_user_id = self._uid
        return invoice_user_id

    invoice_user_id = fields.Many2one('res.users', copy=True, tracking=True,
                                      string='Salesperson',
                                      default=_set_default_sp)
    @api.onchange('partner_id')
    def set_user_id(self):
        for rec in self:
            if self.partner_id:
                rec.invoice_user_id = self.partner_id.user_id.id