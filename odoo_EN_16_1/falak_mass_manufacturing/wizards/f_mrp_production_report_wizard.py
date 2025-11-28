# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger('mrp create')


class F_Mrp_Production_Report_Wizard(models.TransientModel):
    _name = 'f.mrp.production.report.wizard'
    _description = "MRP Production Report"
    
    f_Production_date = fields.Date('Actual Production Date',required=True)
    
    
    def f_set_date(self):
        mo_orders = self.env['mrp.production'].search([('f_actual_production_date','=',self.f_Production_date),('state','=','done')])
        report_rec = self.env['f.report.man.orders.products'].sudo().search([])
        for rec in report_rec:
            rec.unlink()
        product_groups = []
        sum = {}
        # _logger.info("//////////////////////////////////////////////////////////////")
        # _logger.info("start")
        for mrp in mo_orders:
            # _logger.info("//////////////////////////////////////////////////////////////")
            # _logger.info(mrp)
            if mrp.product_id.id in product_groups:
                sum[mrp.product_id.id] += mrp.product_qty
            
            else:
                product_groups.append(mrp.product_id.id)
                sum[mrp.product_id.id] = mrp.product_qty
            
                
        for product in product_groups:
            # _logger.info("//////////////////////////////////////////////////////////////")
            # _logger.info(product)
            values = {
                    'f_user_id': self.env.user.id,
                    'f_product_id': product,
                    'f_production_qty': sum[product],
                    'f_order_date': self.f_Production_date,
                    }
            self.env['f.report.man.orders.products'].create(values)
        # _logger.info("//////////////////////////////////////////////////////////////")
        # _logger.info("end")    
        report_rec = self.env['f.report.man.orders.products'].sudo().search([])
        if report_rec: 
            # report_action = self.env['ir.actions.report'].create({
            #     'id': 'action_report_man_orders_products',
            #     'name': 'Manufacturing Order Products Report',
            #     'model': 'f.report.man.orders.products',
            #     'type': 'ir.actions.report',
            #     'report_type': 'qweb-pdf',
            #     'report_name': 'falak_mass_manufacturing.report_mo_details',
            #     'report_file': 'falak_mass_manufacturing.report_mo_details',
            #     'print_report_name' : "Manufacturing Orders",
            #     'binding_model_id': self.env['ir.model'].sudo().search([('name','=','f.report.man.orders.products')]).id,
            #     'binding_type': 'report',
            #
            # })
            
            
            return self.env.ref('falak_mass_manufacturing.action_report_man_orders_products').report_action(report_rec.ids)
            #data = report_action.report_action(report_rec)
            
            
            #return data
        else:
            raise ValidationError("There isn't a done manufacturing order in this DATE ")
    
    
    
    
        
        
        
