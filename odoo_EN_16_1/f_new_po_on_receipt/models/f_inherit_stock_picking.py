#-*- coding: utf-8 -*-

from odoo import models, fields, api,_


class f_purchase(models.Model):
    _inherit = 'purchase.order'

    f_virtual_pick = fields.Many2one('stock.picking', string='Receiving Transfer ',copy=False)


class f_picking_type(models.Model):
    _inherit = 'stock.picking.type'

    f_virtual_operation = fields.Boolean('Is Virtual Operation ',help='When True , in transfer new button appear to create draft purchase order')
    f_virtual_pick = fields.Many2one('stock.picking.type',string='Picking on Purchase Order ' ,copy=False)



class f_picking(models.Model):
    _inherit = 'stock.picking'


    f_virtual_po= fields.Many2one('purchase.order', string='Purchase Order ',copy=False)
    f_virtual_operation = fields.Boolean(
        related='picking_type_id.f_virtual_operation',
        readonly=True,copy=False)

    f_create_po_done = fields.Boolean('Po Created',copy=False)

    def f_create_draft_po_order(self):
        currency_id =  self.partner_id.property_purchase_currency_id.id
        if currency_id :
            final_currency_id = currency_id
        else :
            final_currency_id = self.env.company.currency_id.id
            
            


        currency_id =  self.partner_id.property_purchase_currency_id.id


        if currency_id :


            final_currency_id = currency_id


        else :


            final_currency_id = self.env.company.currency_id.id

        po = self.env['purchase.order'].create({

            "partner_id": self.partner_id.id,

            "currency_id": final_currency_id,
            "picking_type_id": self.picking_type_id.f_virtual_pick.id,
           # "dest_address_id": self.partner_id.id,
            "f_virtual_pick":self.id,
            "origin":self.origin

        })



        for rec in self.move_ids:
            self.env['purchase.order.line'].create({
                'order_id': po.id,
                'product_id': rec.product_id.id,
                'name': rec.product_id.name,
                'product_qty': rec.product_uom_qty,
                'product_uom': rec.product_uom.id,
            #    'price_unit': rec.product_id.standard_price,
                'taxes_id': False,

            })


            self.f_virtual_po = po.id
            self.f_create_po_done = True


        # message = (''' New Purchase Order :  %s - [%s]''' % (
        #     po.name,  po.id))
        # self.sudo().message_post(body=message, author_id=self.env.user.partner_id.id, message_type="comment",
        #                             subtype_xmlid="mail.mt_comment")
