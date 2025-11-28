from odoo import models, fields, api
from datetime import date


class FCustomerContactInherit(models.Model):
    _inherit = "res.partner"

    # sequence = fields.Integer(string='Sequence', default=0)
    f_route = fields.Many2one("f.customer.routes", string="Route")
    f_frequency = fields.Integer(string='Frequency')
    f_frequency_unit = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years')
    ], string='Frequency Unit', default='weeks')

    def update_visits(self):
        for rec in self:
            visits = self.env['f.visits'].sudo().search([('f_customer', '=', rec.id),
                                                         ('f_date', '>', date.today()),
                                                         ('state', '=', 'draft')])
            visits.unlink()
            self.env['f.visits'].sudo().create_visits()


