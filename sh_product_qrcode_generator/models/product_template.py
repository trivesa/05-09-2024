# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

from io import BytesIO
import base64
import logging

try:
    import qrcode
except ImportError:
    qrcode = None

_logger = logging.getLogger(__name__)

class ShProductTemplate(models.Model):
    _inherit = "product.template"

    sh_qr_code = fields.Char(
        string="QR Code", related='product_variant_ids.sh_qr_code', readonly=False)
    sh_qr_code_img = fields.Binary(
        string="QR Code Image", readonly=False, compute='_compute_sh_qr_code_1')

    # ... 其他方法保持不变 ...

    def _generate_product_qr_code(self, product):
        """
        修改后的方法，使用内部参考生成二维码
        """
        if not product:
            return

        text = product.default_code

        if text and qrcode:
            qr_code = qrcode.QRCode(
                version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr_code.add_data(text)
            qr_code.make(fit=True)
            qr_img = qr_code.make_image()
            bytes_io = BytesIO()
            qr_img.save(bytes_io, format="PNG")
            qr_code_image = base64.b64encode(bytes_io.getvalue())

            product.sh_qr_code = text
            product.sh_qr_code_img = qr_code_image
        else:
            _logger.warning(_("Product %s has no internal reference, cannot generate QR code") % product.name)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ShProductTemplate, self).create(vals_list)
        is_create_qr_code = self.env['ir.config_parameter'].sudo().get_param(
            'sh_product_qrcode_generator.is_sh_product_qrcode_generator_when_create')
        if is_create_qr_code:
            for template in res:
                self._generate_product_qr_code(template)
        return res

    @api.depends('default_code')
    def _compute_sh_qr_code_1(self):
        for template in self:
            template.sh_qr_code_img = False
            if template.default_code:
                self._generate_product_qr_code(template)
