from odoo import models, fields, api


class FstsCheckSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    f_show_bounce_checks_stat = fields.Boolean(string='Show bounce Checks on Statement Report')


    def get_values(self):
        res = super(FstsCheckSetting, self).get_values()

        res.update(
            f_show_bounce_checks_stat=self.env['ir.config_parameter'].sudo().get_param(
                'f_customer_detailed_statement.f_show_bounce_checks_stat'),

        )

        return res

    def set_values(self):
        super(FstsCheckSetting, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        f_show_bounce_checks_stat = self.f_show_bounce_checks_stat or False
        param.sudo().set_param('f_customer_detailed_statement.f_show_bounce_checks_stat', f_show_bounce_checks_stat)





