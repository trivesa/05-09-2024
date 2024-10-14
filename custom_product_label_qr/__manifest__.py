{
    'name': 'Custom Product Label with QR Code',
    'version': '17.0.1.0.0',  # 根据您的 Odoo 版本调整
    'category': 'Inventory',
    'summary': 'Add QR code to product labels',
    'description': """
        This module adds a QR code to product labels using sh_product_qrcode_generator.
    """,
    'author': 'TRIVESA',
    'website': 'https://www.milanomodamaison.it',
    'depends': [
        'product',
        'barcodes',
        'base_setup',
        'sh_product_qrcode_generator'
    ],
    'data': [
        'views/report_product_label.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
