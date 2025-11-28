# # -*- coding: utf-8 -*
# # Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo.upgrade import util

def migrate(cr, version):
    cr.execute( """ALTER TABLE res_company ADD COLUMN  IF NOT EXISTS f_show_headerinstatemnt BOOLEAN ;""")
    util.records.remove_view(cr, xml_id='f_customer_detailed_statement.f_inherit_company_show_header')


