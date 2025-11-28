# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import expression

## inherit product.product model 
class FProductProduct_Inherit(models.Model):
    _inherit = "product.product"
    

    #Change product name search to include  barcode.
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        #print('search')
        if operator == 'ilike' and not (name or '').strip():
                domain = []
        elif operator in ('ilike', 'like', '=', '=like', '=ilike'):
             domain = expression.AND([
                    args or [],
                    ['|','|', ('default_code', operator, name),('name', operator, name),('barcode', operator, name)]
                    ])
             #print('domain',domain)
             return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
        return super(FProductProduct_Inherit, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)




class FProductTemplateInherit(models.Model):
    _inherit ='product.template'
    
    fprodbrand = fields.Many2one('f.prod.brand',string='Brand')
    fprodcategory = fields.Many2one('f.prod.category',string='Category')
    fprodsubcategory = fields.Many2one('f.prod.sub.category',string='Sub Category')
    fprodfamily = fields.Many2one('f.prod.family',string='Product Family')
    fprodidentity = fields.Many2one('f.prod.identity',string='Product Identity')
   
    fproducername =fields.Many2one('f.prod.producername',string="Producer Name")
    fexternalid =fields.Char(string="External Id")
    fprodtarget =fields.Many2many('f.prod.target',string=" Product Target") 
     
    
     
    #barcode = fields.Char('Barcode', copy=True,compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode')
  
     
    @api.onchange('fprodcategory')
    def _f_onchange_prod_category(self):
        self.fprodsubcategory=False
        domain = [('fprodcategory', '=', self.fprodcategory.id)]    
        return {'domain':{'fprodsubcategory':domain}}
    
class FProdBrand(models.Model):
    _name = 'f.prod.brand'
    _rec_name= 'fprodbrand_name'
    fprodbrand_name = fields.Char(string = 'Brand Name')
    

class FProdCategory(models.Model):
    _name = 'f.prod.category'
    _rec_name= 'fprodcategory_name'
    
    fprodcategory_name = fields.Char(string = 'Category Name')
    fprodsubcategory = fields.One2many('f.prod.sub.category','fprodcategory',string='Sub Category')     

class FProdSubCategory(models.Model):
    _name = 'f.prod.sub.category'
    _rec_name= 'fprodsubcategory_name'
    
    fprodsubcategory_name = fields.Char(string = 'Category Name') 
    fprodcategory         = fields.Many2one('f.prod.category',string='Category')
    
class FProdFamily(models.Model):
    _name = 'f.prod.family'
    _rec_name= 'fprodfamily_name'
    fprodfamily_name = fields.Char(string = 'Product Family Name')     

class FProdIdentity(models.Model):
    _name = 'f.prod.identity'
    _rec_name= 'fprodidentity_name'
    
    fprodidentity_name = fields.Char(string = 'Product Identity Name')     

class FProdProducerName(models.Model):
    _name = 'f.prod.producername'
    _rec_name= 'fprodproducer_name'
    
    fprodproducer_name = fields.Char(string = 'Product Producer Name')     


class FProdTarget(models.Model):
    _name = 'f.prod.target'
    _rec_name= 'fprodtarget_name'
    
    fprodtarget_name = fields.Char(string = 'Product Target Name')     


    
