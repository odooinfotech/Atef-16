from odoo import models, fields, api,_

class FAccountMoveLineInherit(models.Model):      
    _inherit = 'account.move.line'#
  
    f_prod_family_id = fields.Many2one(related = 'product_id.product_tmpl_id.f_product_family')
    f_prod_identity_id = fields.Many2one(related = 'product_id.product_tmpl_id.fprodidentity')
    