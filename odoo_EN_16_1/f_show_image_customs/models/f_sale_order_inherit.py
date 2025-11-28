from odoo import models, tools, api, fields, _


class FSalesOrderInherit(models.Model):
    _inherit = "sale.order"

    f_show_image = fields.Boolean('Show Product Image')
