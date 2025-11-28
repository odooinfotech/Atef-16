odoo.define('prevent_negative_qty_pos.models', function(require) {
	"use strict";
	
	const PosComponent = require('point_of_sale.PosComponent');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useState } = owl.hooks;
    const ProductScreen = require('point_of_sale.ProductScreen');
    
    
    var models = require('point_of_sale.models');
    
    models.load_models([
		
    	{
            model:  'stock.quant',
            fields: ['id', 'product_id', 'location_id', 'quantity'],
            domain: function(self) {return [['location_id', '=', self.env.pos.config.f_location[0]]]},
            loaded: function(self, products_quants){
         
            	self.products_quants = products_quants;
            	console.log(self.env.pos.config.f_location,"self.products_quants",self.products_quants)
            	
            },
        }
    	
    	
    	
    	
    	
    	],{'after': 'product.product'});
    
    
    
    
    
});	
    
    
    