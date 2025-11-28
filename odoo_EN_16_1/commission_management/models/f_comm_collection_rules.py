from odoo import models, fields, api

class FCollectionModel(models.Model):
     _name = 'f.comm.collection.rules'
     
     f_customer_type = fields.Selection([('retail','Retail'),('whole','Whole Sales')], default = 'whole',required = True, string = "Customer Type")  
     f_operator = fields.Selection([('between','Between'),('less','<='),('great','>=')],string = 'Debit%')
     f_debit_from = fields.Float(string = 'Debit From',required = True, default = 0) 
     f_debit_to = fields.Float(string = 'Debit To',required = True , default = 0)
     f_collection_com = fields.Float(string = 'Percentage',required = True, default = 0)
     
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    