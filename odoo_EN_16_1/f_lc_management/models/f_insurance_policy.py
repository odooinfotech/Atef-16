# -*- coding: utf-8 -*-

from odoo import models, fields, api


class F_Insurance_Policy_Class(models.Model):
    _name = 'f.insurance.policy'
    _rec_name='f_insuramce_name'
    _description = 'Insurance Polisy Details '
    f_insuramce_name =fields.Char(string="Insurance Policy Name")