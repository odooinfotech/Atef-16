from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class FCancelWizard(models.Model):
    _name = 'f.cancel.wizard'
    _description = "Cancel Wizard"


    f_visit = fields.Many2one("f.visits",string="Visit")
    f_reason_cancel = fields.Text(string="Reason of cancel",required=True)

    def save(self):
        self.f_visit.state='cancel'
            
