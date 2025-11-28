from odoo import fields, models, api, _,tools
from datetime import datetime,timedelta,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT



class FthermalCustStatdetailedreport(models.TransientModel):
    _name= 'f.detailed.customer.thermal'
    _description = "Thermla Customer Statement Wizard"
    


