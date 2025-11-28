# -*- coding: utf-8 -*-

from odoo import fields, models, api, _, tools
from datetime import datetime, timedelta, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class FixlsnheritCustStatdetailedreport(models.TransientModel):
    _inherit = 'f.detailed.customer'

    f_report = fields.Selection(
        selection_add=[('xls', 'Excel')],
    )

    def generate_salereport(self):
        res = super(FixlsnheritCustStatdetailedreport, self).generate_salereport()
        if self.f_report == 'xls':
            return self.env.ref('f_statament_payment_report_xlsx_ex.f_custstatdetaild_report_xls').report_action(self)
        return res

