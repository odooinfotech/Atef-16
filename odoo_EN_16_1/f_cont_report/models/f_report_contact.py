from odoo import tools
from odoo import models, fields, api,_


class fpartnerbalances_pdf_template(models.AbstractModel):
    _name = 'report.f_cont_report.report_contact_details'
    _description = 'Balance Details'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('111')
        data = dict(data or {})
        
        return {
            'data': data,
        }


class FPartnerGeneralBalances_pdf_template(models.AbstractModel):
    _name = 'report.f_cont_report.report_contact_general_details'
    _description = 'Balance General Details'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('111')
        data = dict(data or {})

        return {
            'data': data,
        }
