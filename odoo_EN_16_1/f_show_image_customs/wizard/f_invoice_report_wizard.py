from odoo import models, tools, api, fields, _


class FInvoiceReportWizard(models.Model):
    _name = "f.invoice.report.wizard"
    _description = "Invoice Report Wizard"

    f_show_image = fields.Boolean('Show Product Image')

    def f_print_invoice_report(self):
        invoice_ids = self.env['account.move'].browse(self.env.context.get('active_ids'))
        invoice_ids.write({
            'f_show_image': self.f_show_image,
        })
        return self.env.ref('account.account_invoices').report_action(invoice_ids.ids)