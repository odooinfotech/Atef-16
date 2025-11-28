from odoo import models, fields, api
from odoo.tools import float_compare
from odoo.addons import decimal_precision as dp

# #This Class is added allow creating invoices including items with 0 price
# class FSaleOrderInherit(models.Model):
#     _inherit = "sale.order"
#     
#     def _get_invoiceable_lines(self, final=False):
#         
#         invoiceable_line_ids =   super(FSaleOrderInherit, self)._get_invoiceable_lines(final)
#         
#         print('result',invoiceable_line_ids)
#         for line in self.order_line:    
#             if line.qty_to_invoice <= 0 and line.f_bonus_qty > 0  and line not in invoiceable_line_ids:
#                 invoiceable_line_ids += line
#         
#         print('result',invoiceable_line_ids)
#         return invoiceable_line_ids


class FSaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"
    
    #old to be removed
    #bonus_qty = fields.Float('Bonus Qty', digits=dp.get_precision('Product Unit of Measure'))
    
    
    f_bonus_qty = fields.Float('Bonus Qty', digits='Product Unit of Measure',default = 0)
    
    
    def _get_qty_procurement(self,previous_product_uom_qty=False):
        print('previous_product_uom_qty>>>>>>>>>>>>>>>>',previous_product_uom_qty)
        qty = super(FSaleOrderLineInherit, self)._get_qty_procurement(previous_product_uom_qty)
        print('previous_product_uom_qty_1',previous_product_uom_qty,qty,qty - self.f_bonus_qty)
        return qty - self.f_bonus_qty
 
    def write(self, values):
        lines = self.env['sale.order.line']
        if 'f_bonus_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            lines = self.filtered(
                lambda r: r.state == 'sale' and not r.is_expense and float_compare(r.f_bonus_qty + r.product_uom_qty , r.product_uom_qty + values['f_bonus_qty'] , precision_digits=precision) == -1)
        previous_product_uom_qty = {line.id:line.f_bonus_qty + line.product_uom_qty for line in lines}
        res = super(FSaleOrderLineInherit, self).write(values)
        if lines:
            lines.with_context(previous_product_uom_qty=previous_product_uom_qty)._action_launch_stock_rule()
        return res

    @api.onchange('product_id')
    def product_id_change(self):
     #   res = super(FSaleOrderLineInherit, self).product_id_change()
        if self.product_id:
            self.f_bonus_qty =  0
      #  return res
 
       
    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity', 'untaxed_amount_to_invoice')
    def _compute_qty_invoiced(self):
        """
        Compute the quantity invoiced. If case of a refund, the quantity invoiced is decreased. Note
        that this is the case only if the refund is generated from the SO and that is intentional: if
        a refund made would automatically decrease the invoiced quantity, then there is a risk of reinvoicing
        it automatically, which may not be wanted at all. That's why the refund has to be created from the SO
        """
        for line in self:
            qty_invoiced = 0.0
            for invoice_line in line._get_invoice_lines():
                if invoice_line.move_id.state != 'cancel':
                    if invoice_line.move_id.move_type == 'out_invoice':
                        qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
                        qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.f_bonus_qty, line.product_uom)
                    elif invoice_line.move_id.move_type == 'out_refund':
                        qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
                        qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.f_bonus_qty, line.product_uom)
            line.qty_invoiced = qty_invoiced

    def _prepare_invoice_line(self, **optional_values):
        
        res = super(FSaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        
        print('_prepare_invoice_line res =',res)
        print('self',self)
        
        sale_demand_qty= 0.0 
        sale_bonus_qty = 0.0 
        delivered_qty  = 0.0
        invoiced_qty   = 0.0
        to_inv_qty     = 0.0 
        bonus_qty      = 0.0
        
        total_prev_inv_bonus = 0.0
        total_prev_inv_qty   = 0.0
        
        
        sale_demand_qty   = self.product_uom_qty
        sale_bonus_qty = self.f_bonus_qty
        delivered_qty  = self.qty_delivered
        invoiced_qty   = self.qty_invoiced
        
        sys_to_inv_qty = self.qty_to_invoice
        
       
        
        
        print('sale_demand_qty',sale_demand_qty)
        print('sale_bonus_qty',sale_bonus_qty)
        print('delivered_qty',delivered_qty)
        print('invoiced_qty',invoiced_qty)
        print('sys_to_inv_qty',sys_to_inv_qty,self.qty_to_invoice)
        
        #print('diff_qty',diff_qty)
        
        #total_prev_inv_bonus  = 
        print('self.invoice_lines',self.invoice_lines)
        
        if sale_bonus_qty > 0:
            #GET previous invoiced and bonused quantities
            for invoice_line in self.invoice_lines:
                    if invoice_line.move_id.state != 'cancel':
                        print(invoice_line.move_id.move_type)
                        if invoice_line.move_id.move_type == 'out_invoice':
                            print('out_invoice')
                            total_prev_inv_qty   += invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, self.product_uom)
                            print(invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, self.product_uom))
                            print('total_prev_inv_qty',total_prev_inv_qty)
                            total_prev_inv_bonus += invoice_line.product_uom_id._compute_quantity(invoice_line.f_bonus_qty, self.product_uom)
                            print(invoice_line.product_uom_id._compute_quantity(invoice_line.f_bonus_qty, self.product_uom))
                        
                        elif invoice_line.move_id.move_type == 'out_refund':
                            print('out_refund')
                            total_prev_inv_qty   -= invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, self.product_uom)
                            print(invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, self.product_uom))
                           
                            total_prev_inv_bonus -= invoice_line.product_uom_id._compute_quantity(invoice_line.f_bonus_qty, self.product_uom)
                            print(invoice_line.product_uom_id._compute_quantity(invoice_line.f_bonus_qty, self.product_uom))
                            print('total_prev_inv_qty',total_prev_inv_qty)
            print('total_prev_inv_bonus',total_prev_inv_bonus)
            print('total_prev_inv_qty',total_prev_inv_qty)
                
            diff_qty    = (delivered_qty - invoiced_qty)
            #calculate actual bonus qty to invoice 
            if  diff_qty > 0 : 
                if sale_bonus_qty - total_prev_inv_bonus > 0 : 
                    if diff_qty + total_prev_inv_qty-sale_demand_qty >0 :
                        bonus_qty = min((diff_qty + total_prev_inv_qty-sale_demand_qty),(sale_bonus_qty - total_prev_inv_bonus))
                        print('1')
                            
                
            elif total_prev_inv_bonus >0 :
                if (total_prev_inv_qty + diff_qty) <= sale_demand_qty :                     
                    # This line is commented as a workaround
                    bonus_qty = 0 #-1* min(abs(abs(abs(diff_qty)-(total_prev_inv_bonus +total_prev_inv_qty))- sale_demand_qty), total_prev_inv_bonus,abs(diff_qty))
                    print('3')
                    
                else :
                    bonus_qty = 0
                    print('5')
            print('bonus_qty',bonus_qty)
            
            
            to_inv_qty = diff_qty - bonus_qty
            
            if to_inv_qty ==0 :
                res['f_bonus_qty'] = bonus_qty
            else :
                res['f_bonus_qty'] = abs(bonus_qty)
                
            res['quantity']    = to_inv_qty
            
            if (self.f_bonus_qty + self.product_uom_qty) >0 and to_inv_qty <0:
                
                res['price_unit'] = (self.price_unit *self.product_uom_qty) /(self.f_bonus_qty + self.product_uom_qty )
            
            
        print('result after calculation',res)
        return res






