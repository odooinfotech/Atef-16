from odoo import models, tools, api, fields, _


class FSalesReportWizard(models.Model):
    _name = "f.sales.report.wizard"
    _description = "Sales Report Wizard"

    f_show_image = fields.Boolean('Show Product Image')

    def f_print_sales_report(self):
        sale_ids = self.env['sale.order'].browse(self.env.context.get('active_ids'))
        sale_ids.write({
            'f_show_image': self.f_show_image,
        })
        return self.env.ref('sale.action_report_saleorder').report_action(sale_ids.ids)