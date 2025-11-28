
# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self, res_ids=None, data=None):
        print("2222222222222222test")
        # Overridden so that the print > invoices actions raises an error
        # when trying to print a miscellaneous operation instead of an invoice.
        if self.model == 'account.move' and res_ids:
            invoice_reports = (self.env.ref('print_journal_enteries.f_ar_template_account_journal_entrey'), self.env.ref('print_journal_enteries.f_en_template_account_journal_entrey'))
            if self in invoice_reports:
                moves = self.env['account.move'].browse(res_ids)
                if any( move.move_type != 'entry' for move in moves):
                    print("2222222222222222222222")
                    raise UserError(_("Only Journal Entry could be printed."))
                
                
                
                
        return super()._render_qweb_pdf(res_ids=res_ids, data=data)
    
    
    