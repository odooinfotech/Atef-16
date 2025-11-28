from odoo import api, fields, models, _


class fSaleStockMove(models.Model):
    _inherit = 'stock.move'




    def _get_source_document(self):
        res = super()._get_source_document()
        return self.sudo().sale_line_id.sudo().order_id.sudo() or res
