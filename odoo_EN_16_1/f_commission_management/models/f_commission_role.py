from odoo import models, fields, api, _


class FCommissionRole(models.Model):
    _name = 'f.commission.role'
    _description = 'Commission Role'
    _rec_name = 'f_name'

    f_name = fields.Char(string='Name', required=True)
    f_sales_persons = fields.Many2many('res.users', string='Salespersons', required=True)
    f_responsible = fields.Many2one('res.users', string='Responsible', required=True)

    def f_show_progress_info(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Progress Info',
            'view_mode': 'form',
            'res_model': 'f.progress.info.wizard',
            'target': 'new',
            'context': {
                'default_f_commission_role': self.id
            },
        }