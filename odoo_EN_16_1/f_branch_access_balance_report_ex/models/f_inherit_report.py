# -*- coding: utf-8 -*-

from odoo import fields, models, api, _, tools


class FconyactCurrreport(models.Model):
    _inherit =  "f.contatc.balance.report"

    f_related_branch = fields.Many2one('f.comp.branches',string='Branch', readonly=True)



class FwizconyactCurrreport(models.TransientModel):
    _inherit =  "f.partner.allb.balance.wizard"

    def _f_select(self):
        return super(FwizconyactCurrreport,self)._f_select() + ',  part.f_related_branch as f_related_branch '

