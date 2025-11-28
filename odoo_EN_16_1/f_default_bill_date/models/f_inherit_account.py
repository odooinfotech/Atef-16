from odoo import models, tools, api, fields,_

class FIinheritaccountmovedate(models.Model):
    _inherit = "account.move"
    
    
    @api.model
    def _get_default_invoice_date(self):
        print("xxxxxxx")
        return fields.Date.context_today(self) if self._context.get('default_move_type', 'entry') in ('in_invoice', 'in_refund', 'in_receipt','out_invoice','out_refund') else False

#default=_get_default_invoice_date

    
    invoice_date = fields.Date(string='Invoice/Bill Date', readonly=True, index=True, copy=False,
        states={'draft': [('readonly', False)]}
        )


    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
                    if 'invoice_date' not in values or values.get('invoice_date')  == False:
                        values['invoice_date'] = fields.Date.today()

                    
        return super().create(vals_list)


    
    
    
