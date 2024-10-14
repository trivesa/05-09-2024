   {
       'name': 'Custom Product Label with QR Code',
       'version': '1.0',
       'depends': ['product', 'barcodes'],
       'data': [
           'security/ir.model.access.csv',
           'views/report_product_label.xml',
       ],
       'license': 'LGPL-3',
       'installable': True,
       'application': False,
       'auto_install': False,
   }
