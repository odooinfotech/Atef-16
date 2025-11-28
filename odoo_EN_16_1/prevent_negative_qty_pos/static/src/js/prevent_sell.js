odoo.define('prevent_negative_qty_pos.prevent_sell', function(require) {
	"use strict";
	
	const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');
    const { Gui } = require('point_of_sale.Gui');
    const { _t } = require('web.core');
    
    
    
    
    
    var models = require('point_of_sale.models');
    
  //  models.load_fields("product.product", ['type']);
    
    
	const FpreventProductScreen = (ProductScreen) =>
    class extends ProductScreen {
    	
    	constructor() {
			super(...arguments);
		}
		
    	async _onClickPay() {
    		
    		console.log("****************************************",this.error,this.env.pos.db.get_orders())
    		var self = this;
    		let currentClient = this.currentOrder.get_partner();
    		console.log("this.currentOrder",this.env.pos.get_order())
    		var dict = {};
    		var prods = {};
    		let call_super = true;
    		var ss = {};
    		let location = this.env.pos.config.f_location;
    		
    		let order = this.env.pos.get_order();
    		var count_error = 0;

    			 order.orderlines.forEach(line => {
            if (line){
				var product =line.get_product();
						if(product.type == 'product'){
							if( line.get_quantity() > 0  && line.price > 0 ){
	  						var key = product.id;

    					if (!ss[key]){
    						ss[key]={}
    						ss[key] = line.quantity;


    					}
    					else{
    						ss[key] = ss[key] + line.quantity

    					}

							}
						}
				}


        });




    					
    					
    					var list = [];
    	    			for (var k in ss){
    					list.push(parseInt(k));
    	    		}
    	    			
    	    		try {await this.env.services.rpc({
    						model: 'stock.quant',
    						method: 'get_singles_product',
    						args: [currentClient ? currentClient.id : 0,location,ss,list,self.env.pos.config.f_include_rese_pos],
    					
    					}).then(function(output) {
    						console.log("our",output)
    						if(output.length != 0){
    							if(self.env.pos.config.pos_deny_order == true){
    								call_super = false; 
    								 self.showPopup('ErrorPopup',{
    		                         'title': _t('Warning'),
    		                         'body':  _t("The Ordered Qty of " + "(" + output + ")" + " is Greater than Available Qty."),
    		                         
    		                         
    		                         
    		                     });
    								return
    								}
    							else{
    								call_super = true; 
    								
    							}
    							
    							
    						}
    						else{
    							call_super = true; 
    							
    						}
    						
    					});
    			 
    		 }
    	    		 catch (error) {
              if (isConnectionError(error)) {
                  this.showPopup('ErrorPopup', {
                      title: this.env._t('Network Error'),
                      body: this.env._t('Cannot check qtys screen if offline.'),
                  });
              } else {
                  throw error;
              }
                     }
    	    		 
    	    		 if(call_super){
    						super._onClickPay();
    					}
    	    		 
    	    		 
    	    		 
    	    		
    	    		/*catch (error) {
    			 if ( error.message.code < 0) {
    				 
    				
    				 var orders = this.env.pos.db.get_orders()
    				 if (this.env.pos.db.get_orders().length > 0){
    					
    						  var orders_dict = {};
    						  for (var i in  orders) {
    							  for (const line of orders[i].data.lines) {
    								 
    								  var  key = line[2].product_id 
    								  if (!orders_dict[key]){
    								  
    								  orders_dict[key] = {
    									  product_id: line[2].product_id,
    									  product_name: line[2].full_product_name,
    									  product_qty: line[2].qty
    									};
    								  }
    								  
    								  else{
    									  orders_dict[key].product_qty  = orders_dict[key].product_qty  + line[2].qty
    								  }
    								  
    								 
    							  }
    						  }
    						  
    						  var  product_qtys_len= []
    						  for (var i_prod in ss){
    							  
    							  if(ss[i_prod] > 0 ){
    							  
    							  var prod_quant_qyu = self.env.pos.products_quants.filter(method => method.product_id[0] == i_prod);
    	        				
    	        				 if (i_prod in orders_dict ){
    	        					  if(orders_dict[i_prod].product_qty + ss[i_prod] > prod_quant_qyu[0].quantity){
										  product_qtys_len.push(orders_dict[i_prod].product_name)
										  
									  }
    	        					 
    	        				 }
    	        				 
    	        				 else{
    	        					 if(ss[i_prod] > prod_quant_qyu[0].quantity){
    	        						 product_qtys_len.push(prod_quant_qyu[0].product_id[1])
    	        					 }
    	        				 }
    							
    						  }
    						  }
    						  
    						
    						  
    						  
    						  if (product_qtys_len.length != 0){
    	        					 call_super = false; 
    								 self.showPopup('ErrorPopup',{
    		                         'title': _t('Warning'),
    		                         'body':  _t("The Ordered Qty of " + "(" + product_qtys_len + ")" + " is Greater than Available Qty."),
    		                         
    		                         
    		                         
    		                     });
    								return
    	        					 
    	        					 
    	        				 }
    						  
    						  
    						  self.showPopup('ErrorPopup',{
 		                         'title': _t('Warning'),
 		                         'body':  _t("No Internet Connection."),
 		                         
 		                         
 		                         
 		                     });
    						  if(call_super){
          						super._onClickPay();
          					}	
    					
    			
        				 
        			 }
        			 
        			 else{
        				var qunat = self.env.pos.products_quants
        				var  product_qtys= []
        				 for (var i in ss){
        					 if(ss[i] > 0 ){
        					 var prod_quant = self.env.pos.products_quants.filter(method => method.product_id[0] == i);
        					 if(ss[i] > prod_quant[0].quantity){
        						 product_qtys.push(prod_quant[0].product_id[1])
        					 }
        			
        				 }
        			 }
        				 
        				 if (product_qtys.length != 0){
        					 call_super = false; 
							 self.showPopup('ErrorPopup',{
	                         'title': _t('Warning'),
	                         'body':  _t("The Ordered Qty of " + "(" + product_qtys + ")" + " is Greater than Available Qty."),
	                         
	                         
	                         
	                     });
							return
        					 
        					 
        				 }
        				 
        				
        				 
        			
    						
        				  self.showPopup('ErrorPopup',{
		                         'title': _t('Warning'),
		                         'body':  _t("No Internet Connection."),
		                         
		                         
		                         
		                     });
        				  if(call_super){
        						super._onClickPay();
        					}	
        				 
        			 }
    				 
    				 
               
                 }
             }*/
    		
    		
    		
    	

				

    			
    			
    		
    		
            
        }
    	
    	
    	
    	
    	
    }
    	
    Registries.Component.extend(ProductScreen, FpreventProductScreen);
  

    return ProductScreen;


	
});	
	
	
	
	
	
	
	
	
	
	
	
	
	


