from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from odoo.exceptions import Warning as UserWarning
import logging
_logger = logging.getLogger('mrp create')

class FMassManProducts(models.Model):
    _name ='f.mass.man.products'
    _description = 'Mass Manufacturing Products'
    _rec_name='f_product_id'
    
    
   
    _sql_constraints = [
         ('prod_uniq', 'unique(f_product_id,f_man_planning_id,f_work_center)', 'Product is already added !'),]
    
    f_mrp_production =fields.Many2one('mrp.production',string="Mrp Production")
    f_mass_man_id =fields.Many2one('f.mass.man',string="Mass Manufacturing")
    f_product_id =fields.Many2one('product.product',string="Product" , required= True , domain ="[('product_tmpl_id.type', '=', 'product'),('f_is_manufactured', '=', True)]",copy=True)
    f_quantity =fields.Float(string="Quantity" ,default=1.0,copy=True)
    product_uom_category_id = fields.Many2one(related='f_product_id.uom_id.category_id',copy=True)  
    f_product_uom = fields.Many2one('uom.uom',string='UOM', domain="[('category_id', '=', product_uom_category_id)]",copy=True,required=True)
    f_work_center_group = fields.Many2one('mrp.workcenter.management',string='Work Center Group',related='f_product_id.f_mrp_wcg')
    f_work_center =fields.Many2one('mrp.workcenter',string="Work Center",domain="[('workcenter_group_id', '=', f_work_center_group)]")  
    company_id = fields.Many2one('res.company',string="Company")
    f_shift = fields.Many2one('f.shift',string='shift')

    @api.onchange('f_product_id')
    def default_uom(self):
        self.f_product_uom = self.f_product_id.uom_id.id
        
        
    def get_mo_values(self,rec,operation_ids,bill_of_material):
            if rec.f_work_center :
                work_center= rec.f_work_center.id 
            elif operation_ids :
                work_center = operation_ids[0][2]['workcenter_id']
            else :
                work_center = False
            return {   
                   'origin': rec.f_mass_man_id.f_mass_man_name,          
                   'product_id':rec.f_product_id.id,
                   'product_qty':rec.f_quantity,
                   'product_uom_id' :rec.f_product_uom.id,
                   'date_planned_start' :rec.f_mass_man_id.f_date,
                   'f_actual_production_date' :rec.f_mass_man_id.f_date,
                   'date_planned_finished':rec.f_mass_man_id.f_date,
                   'f_mass_man_id':rec.f_mass_man_id.id,
                   'user_id' : rec.f_mass_man_id.f_responsible.id,                  
                   'bom_id':bill_of_material.id,
                   #'workorder_ids':operation_ids,
                   #'workcenter_id': work_center,
                    'workcenter_id': rec.f_work_center.id,

                    }
    
    def create_man_order(self):
        new_orders = False
        boms = []
        boms_empty = False
        for rec in self:
            man_order = None
            if rec.f_quantity > 0:
                operation_ids = []
                bill_of_material = self.env['mrp.bom'].sudo().search([
                    ('product_tmpl_id', '=', rec.f_product_id.product_tmpl_id.id), ('f_default_bom', '=', True)])
                if bill_of_material:
                    man_order = rec.env['mrp.production'].sudo().search([('product_id', '=', rec.f_product_id.id),
                                                                         ('f_mass_man_id', '=', rec.f_mass_man_id.id),
                                                                         ('state', '!=', 'cancel')])
                    if not man_order:
                        mo_values = self.get_mo_values(rec, operation_ids, bill_of_material)

                        man_order = rec.env['mrp.production'].sudo().create(mo_values)
                        #_logger.info("///////////////////////////////////////////////////////////")
                        #_logger.info(man_order)

                        man_order.action_confirm()
                        new_orders = True
            if not man_order:
               # _logger.info("///////////////////////////////////////////////////////////")
                #_logger.info(bill_of_material)
                boms.append(rec.f_product_id.default_code + " " + rec.f_product_id.name)
                boms_empty = True
        warning_message = "Failed to create a manufacturing order for these products: "
        for bom in boms:
            warning_message += "(" + bom + ") "
        #_logger.info("///////////////////////////////////////////////////////////")
        #_logger.info(warning_message)

        if boms_empty:
            _logger.info("///////////////////////////////////////////////////////////")
            res = {
                'type': 'ir.actions.act_window',
                'name': _('Warning'),
                'res_model': 'f.mrp.production.warning.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {
                    'default_f_warning_Message': warning_message,
                    'default_f_mass_man_id': self[0].f_mass_man_id.id,
                }
            }
            return res

        elif new_orders:
            res = {
                'type': 'ir.actions.act_window',
                'name': 'Manufacturing Order',
                'view_mode': 'tree,form',
                'res_model': 'mrp.production',
                'domain': [('f_mass_man_id', '=', self[0].f_mass_man_id.id)],

            }
            return res
        return True
