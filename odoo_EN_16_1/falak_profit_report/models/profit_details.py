from odoo import models, tools, api, fields



class f_falak_profit_details(models.Model):
    _name = 'f.profit.details'
    _description = "Profit Details"
    
    _auto = False
    
    
    
   # config_id = fields.Many2one('pos.config', string="Point Of Sale", readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    #analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True)
   # type = fields.Char(string='Type', readonly=True)
    rev_qty = fields.Float(string='Rev Qty', digits=0, readonly=True)
    rev_bal = fields.Monetary(string='Rev Total',  readonly=True)
    exp_qty = fields.Float(string='Purch Qty', digits=0, readonly=True)
    exp_bal = fields.Monetary(string='Purch Total',  readonly=True)
    beginv_qty = fields.Float(string='Beg.Inv Qty', digits=0, readonly=True)
    beginv_bal = fields.Monetary(string='Beg.Inv Total',  readonly=True)
    endinv_qty = fields.Float(string='End.Inv Qty', digits=0, readonly=True)
    endinv_bal = fields.Monetary(string='End.Inv Total',  readonly=True)
    
    cogs = fields.Monetary(string='COGS',  readonly=True)
    profit = fields.Monetary(string='Profit',  readonly=True)
    
    company_id = fields.Many2one('res.company', string="Company", readonly=True)

    barcode = fields.Char(string="Barcode", readonly=True)
    
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True)
    
    

    def init(self):


        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
        select max(a.id) as id from product_product a
        
        
        """ % (self._table))
