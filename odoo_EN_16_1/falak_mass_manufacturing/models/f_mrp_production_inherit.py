# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
import itertools
import operator
import logging
_logger = logging.getLogger('mrp create')


class F_MassMrpProductionInherit(models.Model):
    _inherit ='mrp.production'
    
    f_mass_man_id =fields.Many2one('f.mass.man',string="Mass Manufacturing")
    
    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center', readonly=True,
                                    states={'draft': [('readonly', False)]}, check_company=True,
                                    help="""Allow users to pass specific workcenter and
                                    replace Related BOM work center from the header automatically
                                    """)
    f_actual_production_date = fields.Date(string='Actual Production Date',copy=True)
    
    def button_mark_done(self):
        for rec in self.move_raw_ids:
            if rec.product_uom_qty == 0:
                raise ValidationError(f"{rec.product_id.default_code} {rec.product_id.name} has zero consumption, please check it!  ")
            
        return super(F_MassMrpProductionInherit,self).button_mark_done()
    
    
    @api.onchange('bom_id')
    def _onchange_f_bom_id(self):
        self.total_cost_over_head_percent = self.bom_id.total_cost_over_head_percent
        
        
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            bom = self.env['mrp.bom'].sudo().search([('id','=',vals.get('bom_id'))])
            _logger.info("///////////////////////////////////////////////////////////")
            _logger.info(bom.id)
            if bom:
                bom = self.env['mrp.bom'].sudo().search([('id','=',vals.get('bom_id'))])
                vals['total_cost_over_head_percent'] = bom.total_cost_over_head_percent
                
        rec = super(F_MassMrpProductionInherit,self).create(vals_list)
                
        return rec
            
    
                
            
            
            