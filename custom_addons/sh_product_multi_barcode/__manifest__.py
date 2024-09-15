# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Product Multi Barcode',
    'author': 'Softhealer Technologies',
    'website': "https://www.softhealer.com",
    "support": "support@softhealer.com",
    'version': '0.0.2',
    'category': 'Extra Tools',
    "summary": "Product Multiple Barcode Product Various Barcode Generator Product Many Barcodes Product Multi Barcode Different Product Barcodes Generate Various Product Barcodes Search Product Multiple Barcode Find Product Multiple Barcode Odoo multi barcode for products Multiple barcode for product search Product based on barcode Generate multiple barcodes Product multiple barcodes Multiple barcodes for product",
    'description': """Mainly the use of this module, you can create a multiple barcode for each of product. Also you can search that product in product selection lines like in sale order, purchase order, invoices, bills, operation lines.
 Product Multiple Barcode Odoo, Product Various Barcode Generator Odoo
 
 Create Many Barcode Of Product Module, Make Product Multi Barcode, Produce Different Barcodes Of Product, Generate Various Product Barcodes, Search Product Multiple Barcode, Find Product Multiple Barcode Odoo.
 
 Product Many Barcodes Module, Product Multi Barcode App, Different Product Barcodes, Generate Various Product Barcodes, Search Product Multiple Barcode, Find Product Multiple Barcode Odoo.""",
    'depends': [
        'base_setup',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
    ],
    'images': ['static/description/background.png'],
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "20",
    "currency": "EUR"
}
