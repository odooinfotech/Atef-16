# -*- coding: utf-8 -*-
{
    'name': "Falak Packages Management",

    'summary': """ This Module to manage the operations of transfer with packages""",

    'description': """
        In the Packages Model:
            - add a Boolean Flag "Printed" This flag determines if the label is printed or not
            - Once the print button is clicked for this package from any screen this flag should be set to true.
        In the Transfer screen in inventory and barcode Modules add the following:
            - Add a new button in the view to print the packages' Labels that weren't printed before
            - Once this button is clicked the printed flag on the package will be set to True
        In the Inventory -> product Definition-> packaging, 
            - Add a new boolean field to the product packaging line named "delivery packaging", this field will be used for packages Auto generation.
        In the Transfer line 
            - if the product has packaging, 
                then when we press on "put in pack" Action the system should create a package for each product packaging as described above
            - Other Packaging without the "delivery packaging" flag will be ignored and the put-in pack should work as standard behavior.
        Read package barcode in batch operation from barcode model:
            - group batch by contact in barcode view.
            - choose a batch for the chosen contact this will show you all packages for this contact in different deliveries.
            - when finishing reading barcodes Validate batch, this will validate all delivery orders in this batch.
            - add customer name in batch kanban view.
            - add packages search in batch transfer search.
            - add customer name in packages and batches form views.
            - ability to delete done or edit done qty after scan package barcode from batch transfer.
    """,

    'author': "Falak Solutions",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','stock_picking_batch','stock_barcode_picking_batch','stock_barcode'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/f_product_packaging_inherit.xml',
        'views/f_stock_quant_package_inherit.xml',
        'views/f_stock_picking_batch_inherit.xml',
        'report/f_package_label_action.xml',
        'report/f_package_label_template.xml',
        'views/f_stock_picking_inherit.xml',
        'wizard/f_stock_package_destination_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'f_packages_management/static/src/**/*.js',
            'f_packages_management/static/src/**/*.xml',
        ],
    }

}
