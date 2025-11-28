from odoo import models, tools, api, fields ,_
from lxml import etree
from odoo.http import request



class f_falak_profit_details(models.Model):
    _name = 'f.aging.details'
    _auto = False
    _description = "Aging Details"

    
    
    
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    company_id = fields.Many2one('res.company', string="Company", readonly=True)
    name = fields.Char(string="Product Name", readonly=True)
    barcode = fields.Char(string="Barcode", readonly=True)
    default_code= fields.Char(string="Internal Ref", readonly=True)
  
    total_cost = fields.Float(string='Total Cost', digits=0, readonly=True)
    on_hand_quantity = fields.Float(string='Total Quantity',  readonly=True)
    days = fields.Float(string='Interval1', digits=0, readonly=True)
    cost0 = fields.Float(string='Interval1 Cost', digits=0, readonly=True)
    days1 = fields.Float(string='Interval2', digits=0, readonly=True)
    cost1 = fields.Float(string='Interval2 Cost', digits=0, readonly=True)
    days2 = fields.Float(string='Interval3', digits=0, readonly=True)
    cost2 = fields.Float(string='Interval3 Cost', digits=0, readonly=True)
    days3 = fields.Float(string='Interval4', digits=0, readonly=True)
    cost3 = fields.Float(string='Interval4 Cost', digits=0, readonly=True)
    days4= fields.Float(string='Interval5', digits=0, readonly=True)
    cost4 = fields.Float(string='Interval5 Cost',digits=0,  readonly=True)
    days5 = fields.Float(string='Interval6', digits=0, readonly=True)
    cost5 = fields.Float(string='Interval6 Cost',  digits=0,readonly=True)
    days6= fields.Float(string='Interval7', digits=0, readonly=True)
    cost6 = fields.Float(string='Interval7 Cost', digits=0,readonly=True)

    def init(self):

        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
         select max(a.id) as id from product_product a


         """ % (self._table))

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        wizard_record = request.env['f.product.aging'].search([])[-1]
        days = wizard_record.breakdown_days
        day1 = list()
        day1.append('''%s - %s'''% (0,days ))
        day2 = list()
        day2.append('''%s - %s'''% (days+1,days*2 ))
        day3 = list()
        day3.append('''%s - %s'''% ((days*2)+1,days*3 ))
        day4 = list()
        day4.append('''%s - %s'''% ((days*3)+1,days*6 ))
        day5 = list()
        day5.append('''%s - %s'''% ((days*6)+1,days*8 ))
        day6 = list()
        day6.append('''%s - %s'''% ((days*8)+1,days*12 ))
        day7 = list()
        day7.append('''>  %s'''% (days*12 ))
        
     
        
        if view_type == 'tree' :
                for node in arch.xpath("//tree//field[@name='days']"):
                    node.set('string', _('(%s)') % (day1))
                for node in arch.xpath("//tree//field[@name='days1']"):
                    node.set('string', _('(%s)') % (day2))    
                for node in arch.xpath("//tree//field[@name='days2']"):
                    node.set('string', _('(%s)') % (day3))
                for node in arch.xpath("//tree//field[@name='days3']"):
                    node.set('string', _('(%s)') % (day4))    
                for node in arch.xpath("//tree//field[@name='days4']"):
                    node.set('string', _('(%s)') % (day5))    
                for node in arch.xpath("//tree//field[@name='days5']"):
                    node.set('string', _('(%s)') % (day6))    
                for node in arch.xpath("//tree//field[@name='days6']"):
                    node.set('string', _('(%s)') % (day7))    
                
        return arch, view
    
    
    

    
    
    
