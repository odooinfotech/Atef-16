# -*- coding: utf-8 -*-


from odoo import _, api, fields, models
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero


class allow_user_validate_stocktrans(models.Model):
    _inherit = "stock.picking"
    
    


    def button_validate(self):
        if not self.user_has_groups('allow_user_validate_stock.f_admintransfvalid_group_id'):
            raise UserError(_("Only User with group 'Inventory/Transfer Validate' can validate an inventory transfer."))
        
        return super(allow_user_validate_stocktrans, self).button_validate()


class allow_user_validate_stock(models.Model):
    _inherit = "stock.quant"
    
    def action_set_inventory_quantity_to_zero(self):
        if not self.user_has_groups('allow_user_validate_stock.f_adminadjvalid_group_id'):
            raise UserError(_("Only User with group 'Inventory/Adj Validate' can Cancel an inventory adjustment."))
        
        return super(allow_user_validate_stock, self).action_set_inventory_quantity_to_zero()



    def action_apply_inventory(self):
        # if not self.exists():
        #     return
        # self.ensure_one()
        # #falak - allow group user to validate stock
        if not self.user_has_groups('allow_user_validate_stock.f_adminadjvalid_group_id'):
            raise UserError(_("Only User with group 'Inventory/Adj Validate' can validate an inventory adjustment."))
        # if self.state != 'confirm':
        #     raise UserError(_(
        #         "You can't validate the inventory '%s', maybe this inventory "
        #         "has been already validated or isn't ready.", self.name))
        # inventory_lines = self.line_ids.filtered(lambda l: l.product_id.tracking in ['lot', 'serial'] and not l.prod_lot_id and l.theoretical_qty != l.product_qty)
        # lines = self.line_ids.filtered(lambda l: float_compare(l.product_qty, 1, precision_rounding=l.product_uom_id.rounding) > 0 and l.product_id.tracking == 'serial' and l.prod_lot_id)
        # if inventory_lines and not lines:
        #     wiz_lines = [(0, 0, {'product_id': product.id, 'tracking': product.tracking}) for product in inventory_lines.mapped('product_id')]
        #     wiz = self.env['stock.track.confirmation'].create({'inventory_id': self.id, 'tracking_line_ids': wiz_lines})
        #     return {
        #         'name': _('Tracked Products in Inventory Adjustment'),
        #         'type': 'ir.actions.act_window',
        #         'view_mode': 'form',
        #         'views': [(False, 'form')],
        #         'res_model': 'stock.track.confirmation',
        #         'target': 'new',
        #         'res_id': wiz.id,
        #     }
        # self._action_done()
        # self.line_ids._check_company()
        # self._check_company()
        return super(allow_user_validate_stock, self).action_apply_inventory()
