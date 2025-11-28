from odoo import models, fields, api
from odoo.osv import expression


class FProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    fprodidentity = fields.Many2one('f.prod.identity', string='Product Identity')
