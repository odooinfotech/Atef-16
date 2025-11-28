from odoo import models, fields, api, _


class FProgressInfoWizard(models.TransientModel):
    _name = 'f.progress.info.wizard'
    _description = 'Progress Info Wizard'

    f_commission_role = fields.Many2one('f.commission.role', string='Commission Role')
    f_commission_period = fields.Many2one('f.commission.period', string='Commission Period')

    def f_get_progress_info(self):
        domain = [('f_commission_role_ids', 'in', self.f_commission_role.ids)]
        if self.f_commission_period.f_recurring:
            domain += ['|', ('f_commission_period_id', '=', self.f_commission_period.id),
                       ('f_recurring', '=', self.f_commission_period.f_recurring)]
        else:
            domain += [('f_commission_period_id', '=', self.f_commission_period.id)]
        setups = self.env['f.commission.setup'].search(domain)
        for setup in setups:
            result = self.env['f.setup.progress.info'].sudo().search([('f_commission_role', '=', self.f_commission_role.id),('f_commission_period', '=', self.f_commission_period.id), ('f_commission_setup_id', '=', setup.id)])
            if result:
                result.f_calculate_commission()
            else:
                vals = {
                    'f_commission_setup_id': setup.id,
                    'f_commission_period': self.f_commission_period.id,
                    'f_commission_role': self.f_commission_role.id
                }
                result =self.env['f.setup.progress.info'].sudo().create(vals)
                result.f_calculate_commission()

        action = self.env['ir.actions.actions']._for_xml_id('f_commission_management.f_setup_progress_info_action')
        action['domain'] = [('f_commission_role', '=', self.f_commission_role.id), ('f_commission_period', '=', self.f_commission_period.id)]
        return action