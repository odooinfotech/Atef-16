from odoo import api, fields, models, tools
        

class F_Account_Move_Line_Price_History(models.Model):
    _name = "f.account.move.line.price.history.a"
    _description = "Account Move line price history"
    _auto = False

    source= fields.Char(string='Source')
    f_account_move_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Account Move Line",
    )

    
    source_order_line_id = fields.Integer(
       # comodel_name='sale.order.line',
        string='Source order line', readonly=1
    )
    order_id = fields.Char( readonly=1
    )
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=1

    )
    source_order_date_order = fields.Datetime(string='Date', readonly=1
    )
    product_uom_qty = fields.Float(
        string='Qty', readonly=1

    )
    price_unit = fields.Float(
       string='Price', readonly=1

    )
    currency_id = fields.Many2one('res.currency',
        string='Currency', readonly=1

        )

    tax_id = fields.Many2many('account.tax',
        string='Tax', readonly=1,compute='_compute_tax'
        )
    
    
    discount_id = fields.Float(
        string  = 'Discount', readonly=1

        )
    
    
    price_after_disc=fields.Float(compute="get_price",string="Net Price", readonly=1)
    
    def _compute_tax(self):
        for rec in self:
            if rec.source == 'invoice':
                print(rec.source_order_line_id)
                account_move_lines = rec.env['account.move.line'].sudo().search([('id','=',rec.source_order_line_id)],limit=1)
                print(account_move_lines)
                rec.tax_id = account_move_lines.tax_ids.ids
            else:
                rec.tax_id = None
        
    def get_price(self):
        for d in self :
            if  d.discount_id:
                d.price_after_disc =  d.price_unit - d.price_unit   *((d.discount_id)/100)
                
            else:
                d.price_after_disc =  d.price_unit

                # Add button action in tree wizard view

    

    def f_set_price(self):
        print("dwsedf")
        account_move_line = self.env['account.move.line'].search([('id','=',self.f_account_move_line_id.id)])
        print(account_move_line)
        if account_move_line:
            account_move_line.price_unit = self.price_unit

    def init(self):

        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as
           select max(a.id) as id from product_product a
           """ % (self._table))
    
    
    
    
        
        
        
        
