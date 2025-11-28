from odoo import models, tools, api, fields,_

class FIjournalentryline(models.Model):
    _inherit = "account.move.line"
    
    f_partner_ref = fields.Char(
       related='partner_id.ref',
        copy = False,
        string='Partner Ref'
    )

class FIjournalentry(models.Model):
    _inherit = "account.move"
    
    f_exclude_entry = fields.Boolean('Exclude Entry', default=False)
    f_note = fields.Text("Notes")
    
    f_partner_ref = fields.Char(
       related='partner_id.ref',
        copy = False,
        string='Partner Ref'
    )


    invoice_product_list = fields.Text('Invoice Product list')
  
    # @api.depends('invoice_line_ids', 'invoice_line_ids.product_id', 'invoice_line_ids.product_id.name', 'invoice_line_ids.quantity', 'invoice_line_ids.price_unit')
    # def _compute_product_list(self):
    #     for inv in self:
    #         invoice_product_list = list()
    #         if inv.journal_id.type == 'general':
    #             inv.invoice_product_list = inv.ref
    #         if inv.journal_id.type in ('sale','purchase'):
    #
    #             for o_line in inv.invoice_line_ids:
    #                     if o_line.product_id:
    #                         invoice_product_list.append('''%s(%s * %s)'''% (o_line.product_id.name, o_line.quantity, o_line.price_unit))
    #                     if not(o_line.product_id) and o_line.name:
    #                         invoice_product_list.append('''%s(%s * %s)'''% (o_line.name, o_line.quantity, o_line.price_unit))
    #             inv.invoice_product_list = '\n'.join(invoice_product_list).strip(' + ')
