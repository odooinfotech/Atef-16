from odoo import models, fields, api


class FResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one(domain=[])


class FSaleOrderInherited(models.Model):
    _inherit = "sale.order"

    user_id = fields.Many2one(domain=[])


class FAccountMoveInherited(models.Model):
    _inherit = "account.move"

    invoice_user_id = fields.Many2one(domain=[])


class FCrmTeamInherited(models.Model):
    _inherit = 'crm.team'

    member_ids = fields.Many2many(domain=[])
