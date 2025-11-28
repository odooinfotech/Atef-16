from odoo import models, fields, api, _


class FCommissionReportWizard(models.TransientModel):
    _name = 'f.commission.report.wizard'
    _description = 'Commission Report Wizard'

    f_commission_period_ids = fields.Many2many('f.commission.period', string='Commission Period')
    f_team_commission = fields.Boolean(string='Team Commission')

    def f_get_report_info(self):
        roles = self.env['f.commission.role'].sudo().search([('f_responsible', '=', self.env.user.id)])
        if self.f_team_commission:
            roles = self.env['f.commission.role'].sudo().search([('f_responsible', 'in', roles.f_sales_persons.ids)])
        for period in self.f_commission_period_ids:
            result = self.env['f.commission.result'].sudo().search([('f_commission_role_id', 'in', roles.ids),('f_commission_period_id', '=', period.id)])
            if result:
                self.env['f.commission.report'].sudo().search(
                    [('f_commission_result', '=', False), ('f_user_id', '=', self.env.user.id), ('f_commission_period', '=', period.id)]).unlink()
                for res in result:
                    report = self.env['f.commission.report'].sudo().search([('f_commission_result', '=', res.id), ('f_user_id', '=', self.env.user.id)])
                    if not report:
                        vals = {
                            'f_commission_setup_id': res.f_commission_setup_id.id,
                            'f_commission_period': period.id,
                            'f_commission_role': res.f_commission_role_id.id,
                            'f_commission_value': res.f_commission_percent,
                            'f_commission_target': res.f_commission_target,
                            'f_total_amount': res.f_total_amount,
                            'f_commission_amount': res.f_commission_amount,
                            'f_user_id': self.env.user.id,
                            'f_commission_result': res.id
                        }
                        report = self.env['f.commission.report'].sudo().create(vals)
            else:
                domain = [('f_commission_role_ids', 'in', roles.ids)]
                if period.f_recurring:
                    domain += ['|', ('f_commission_period_id', '=', period.id),
                               ('f_recurring', '=', period.f_recurring)]
                else:
                    domain += [('f_commission_period_id', '=', period.id)]
                setups = self.env['f.commission.setup'].search(domain)
                for setup in setups:
                    for role in roles:
                        if role in setup.f_commission_role_ids:
                            result = self.env['f.commission.report'].sudo().search([('f_commission_role', '=', role.id),('f_commission_period', '=', period.id), ('f_commission_setup_id', '=', setup.id), ('f_user_id', '=', self.env.user.id)])
                            if result:
                                result.f_calculate_commission()
                            else:
                                vals = {
                                    'f_commission_setup_id': setup.id,
                                    'f_commission_period': period.id,
                                    'f_commission_role': role.id,
                                    'f_user_id': self.env.user.id
                                }
                                result =self.env['f.commission.report'].sudo().create(vals)
                                result.f_calculate_commission()

        action = self.env['ir.actions.actions']._for_xml_id('f_commission_management.f_commission_report_action')
        action['domain'] = [('f_user_id', '=', self.env.user.id), ('f_commission_period', 'in', self.f_commission_period_ids.ids), ('f_commission_role', 'in', roles.ids)]
        return action