from odoo import models, fields, api


class F_Product_Template_Inherit(models.Model):
    _inherit='product.template'
    
    
    f_mrp_wcg =fields.Many2one('mrp.workcenter.management',string="Work Center Group")
    f_mrp_categ = fields.Many2one('f.mp.categ', string='MRP Category')
    f_mrp_category  =fields.Many2one('mrp.workcenter.management',string="Old Field Categ")
    
class F_Product_Product_Inherit(models.Model):
    _inherit='product.product'
    
    
    f_mrp_wcg =fields.Many2one('mrp.workcenter.management',string="Work Center Group",related = 'product_tmpl_id.f_mrp_wcg')
    f_mrp_categ = fields.Many2one('f.mp.categ', string='MRP Category',related = 'product_tmpl_id.f_mrp_categ')
    f_is_manufactured = fields.Boolean(string='Is Man?',default=True)
    
    
