# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
# Changed by Falak

{
    'name': 'Export Products with Images | Export Images for Products',
    'version': '16.0.0.0',
    'category' : 'Sales',
    'summary': 'Export product images in excel Export product images in zip export image for product download product images export product with images in excel export product in excel export image as zip export product image in excel download image as zip download image',
    'description': """
	The Export Products with Images odoo app helps users to export your products with detailed information and high-quality images, this app also include a wide range of product details like the product's price, name, category etc.
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    "price": 20,
    "currency": 'EUR',
    'depends': ['base','sale_management'],
    'data': [
            'security/ir.model.access.csv',
            'security/security.xml',
            "wizard/export_products_images_wizard_view.xml",
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/AM4m-mF_OWw',
    "images":['static/description/Banner.gif'],
}
