from odoo import models, tools, api, fields,_

class FIinheritsaleorder(models.Model):
    _inherit = "sale.order"

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,copy=False,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))

    @api.depends('partner_id')
    def _compute_user_id(self):
        for order in self:
            order.user_id = order.partner_id.user_id or order.partner_id.commercial_partner_id.user_id or self.env.user

    @api.onchange('partner_id')
    def set_user_id(self):
        for rec in self:
            if self.partner_id:
                rec.user_id = self.partner_id.user_id.id

class FIinheritpurchaseorder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('partner_id')
    def set_user_id(self):
        for rec in self:
            if self.partner_id:
                rec.user_id = self.partner_id.user_id.id