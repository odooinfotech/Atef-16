# # -*- coding: utf-8 -*
# # Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo.upgrade import util
#
def migrate(cr, version):
#     # hijza upgrade
         util.records.remove_view(cr, xml_id='f_bonus_management.report_invoice_document')
#
