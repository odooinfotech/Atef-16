
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _,tools
from datetime import datetime,timedelta,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Finheritpartners(models.Model):
    _inherit = 'res.partner'

    def f_open_balancereport(self):
        action = {
            'name': _('Summary Partner Balance  Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'f.partner.breif.balance.wizard',
            'target': 'new',
        }
            
        return action  

