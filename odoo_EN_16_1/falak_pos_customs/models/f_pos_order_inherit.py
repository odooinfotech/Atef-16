from odoo import api, fields, models, _


class FPosOrderInherit(models.Model):
    _inherit = 'pos.order'

    is_have_partner_edit_group = fields.Boolean(
        string='Is in Custom Partner Edit Group',
        compute='_compute_is_have_partner_edit_group',
        store=False
    )

    @api.depends('user_id')
    def _compute_is_have_partner_edit_group(self):
        custom_group = self.env.ref('falak_pos_customs.f_pos_order_partner_edit_group')
        for order in self:
            order.is_have_partner_edit_group = custom_group in order.env.user.groups_id
