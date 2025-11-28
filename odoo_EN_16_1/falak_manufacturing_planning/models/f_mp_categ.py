from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta


class FMPCategory(models.Model):
    _name ='f.mp.categ'
    _description = 'Manufacturing Plan Category'
    _rec_name='f_categ_name'
    
    
    f_categ_name = fields.Char(string="MP Category")

    