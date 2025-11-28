# -*- coding: utf-8 -*-
from odoo import models, api, fields
import logging
_logger = logging.getLogger('mrp create')


class F_Mrp_Production_Warning_Wizard(models.TransientModel):
    _name = 'f.mrp.production.warning.wizard'
    _description = "MRP Production Warning"
    
    f_warning_Message = fields.Char(' ',readonly=True)
    f_mass_man_id =fields.Many2one('f.mass.man',string="Mass Manufacturing")
    
    def f_mrp_orders(self):
        return {
                'type': 'ir.actions.act_window',
                'name':'Manufacturing Order',
                'view_mode': 'tree,form',
                'res_model': 'mrp.production',
                'domain':[('f_mass_man_id','=',self.f_mass_man_id.id)],
                            
            }  