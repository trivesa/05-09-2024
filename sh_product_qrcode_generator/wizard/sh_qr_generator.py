import qrcode
import base64
from io import BytesIO
import logging

_logger = logging.getLogger(__name__)

# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ShProductQRCodeGeneratorWizard(models.TransientModel):
    _name = 'sh.product.qrcode.generator.wizard'
    _description = 'Product QR Code Generator Wizard'

    product_tmpl_ids = fields.Many2many(
        'product.template', string='Products', copy=False)
    product_var_ids = fields.Many2many(
        'product.product', string='Product Variants', copy=False)
    is_overwrite_existing = fields.Boolean("Overwrite QR code If Exists")

    @api.model
    def default_get(self, default_fields):
        rec = super(ShProductQRCodeGeneratorWizard, self).default_get(default_fields)
        # ... 保持现有代码不变 ...
        return rec

    def action_generate_qr_code(self):
        if self.user_has_groups('sh_product_qrcode_generator.group_sh_product_qr_code_generator'):
            # Product Template
            if self.product_tmpl_ids:
                for product in self.product_tmpl_ids:
                    if (not product.sh_qr_code or self.is_overwrite_existing) and product.default_code:
                        self._generate_product_qr_code(product)
                    elif not product.default_code:
                        _logger.warning(f"Product {product.name} has no internal reference, cannot generate QR code")

            # Product Variant
            elif self.product_var_ids:
                for product in self.product_var_ids:
                    if (not product.sh_qr_code or self.is_overwrite_existing) and product.default_code:
                        self._generate_product_qr_code(product)
                    elif not product.default_code:
                        _logger.warning(f"Product variant {product.name} has no internal reference, cannot generate QR code")
        else:
            raise UserError(_("You don't have rights to generate product QR Code"))

    def _generate_product_qr_code(self, product):
        if product.default_code:
            qr_code = product.default_code
            qr_code_image = self._create_qr_code_image(qr_code)
            product.write({
                'sh_qr_code': qr_code,
                'sh_qr_code_img': qr_code_image,
            })
        else:
            _logger.warning(f"Product {product.name} has no internal reference, cannot generate QR code")

    def _create_qr_code_image(self, qr_code):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_code)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        return qr_image
