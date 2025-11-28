from odoo import models, fields, api,_
from odoo.exceptions import UserError



class FSaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        
        if self.env['ir.config_parameter'].sudo().get_param('prevent_sell_negative_qty.f_prevent_sell'):
            print("1111111111111111")
            groups={}
            for a in self.order_line:
                print("sssss")
                dic_name = a.product_id.id
                if a.product_id.type == 'product':
                    if not groups.get(dic_name):
                        groups[dic_name] = {}
                        groups[dic_name].update({
                                'name': a.product_id.name,
                                'qty':a.product_uom_qty + a.f_bonus_qty,
                               
                                
                               
                            })
                    else:
                        groups[dic_name].update({
                            'qty': groups[dic_name].get('qty') + a.product_uom_qty+ a.f_bonus_qty,
                        })
                    
            print(groups,"qqqqqqqq")
            res=list()
            res2 = ''
            x = True
            loct = []
            for z in groups:
                
                print(groups[z]['qty'],"zzzzz",z)
             
                wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
                [('id', 'child_of', self.warehouse_id.lot_stock_id.id)],
                ['id'],
            )]    
                 
                #  [('id', 'child_of', self.warehouse_id.view_location_id.id)],  
            
                quants = self.env['stock.quant'].search([('product_id', '=', z),('location_id', 'in', wh_location_ids)])
                print(quants,"qqqqq")
                if len(quants) > 1:
                    quantity = 0.0
                    for quant in quants:
                        if self.env['ir.config_parameter'].sudo().get_param('prevent_sell_negative_qty.f_include_rese_sale'):
                            quantity += quant.quantity
                        else:
                            quantity += quant.available_quantity
                    if groups[z]['qty'] >0:
                        if groups[z]['qty'] > quantity:
                            x = x and False
                            res.append('''%s'''% (groups[z]['name']))
                            
                    print("qty",groups[z]['name'],quantity)
                else:
                    if self.env['ir.config_parameter'].sudo().get_param('prevent_sell_negative_qty.f_include_rese_sale'):
                        qty = quants.quantity
                    else:
                        qty = quants.available_quantity
                        
                    if groups[z]['qty'] > 0:
                        if groups[z]['qty'] > qty:
                            x = x and False
                            res.append('''%s'''% (groups[z]['name']))
                res2 = '\n'.join(res).strip(' + ')            
                
            if len(res) > 0 and  not self.env.user.has_group('prevent_sell_negative_qty.f_bypass_minus_transactions'):
                print("15555555555555555555555")
                raise UserError(_('Can not confirm Order Because The requested Qty for Products \n [%s] \n Is More than available Qty in the stock ...  \n Please Contact Your Manager',(res2)))
            
        return super(FSaleOrderInherit, self).action_confirm()    

