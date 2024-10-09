# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from collections import defaultdict
import logging

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

def _prepare_data(env, data):
    if data.get('active_model') == 'product.template':
        product_model = env['product.template'].with_context(display_default_code=False)
    elif data.get('active_model') == 'product.product':
        product_model = env['product.product'].with_context(display_default_code=False)
    else:
        raise UserError(_('Product model not defined, Please contact your administrator.'))

    total = 0
    qty_by_product_in = data.get('quantity_by_product')
    products = product_model.search([('id', 'in', [int(p) for p in qty_by_product_in.keys()])], order='name desc')
    quantity_by_product = defaultdict(list)
    
    for product in products:
        qty = qty_by_product_in[str(product.id)]
        quantity_by_product[product].append((0, qty))
        total += qty
        # 确保 QR 码数据已生成
        if product.default_code:
            product.sh_qr_code = product.default_code
            if not product.sh_qr_code_img:
                product.sh_qr_code_img = product._generate_qr_code_image(product.default_code)
        else:
            _logger.warning(f"Product {product.name} has no default_code for QR generation.")

    if data.get('custom_qr_codes'):
        for product, qr_codes_qtys in data.get('custom_qr_codes').items():
            quantity_by_product[product_model.browse(int(product))] += qr_codes_qtys
            total += sum(qty for _, qty in qr_codes_qtys)

    layout_wizard = env['sh.product.qrcode.generator.label.layout'].browse(data.get('layout_wizard'))
    if not layout_wizard:
        raise UserError(_('Label layout not found. Please configure the label layout before printing.'))

    _logger.info(f"Preparing label data for {len(products)} products with new QR code logic.")

    return {
        'quantity': quantity_by_product,
        'rows': layout_wizard.rows,
        'columns': layout_wizard.columns,
        'page_numbers': (total - 1) // (layout_wizard.rows * layout_wizard.columns) + 1,
        'price_included': data.get('price_included'),
        'extra_html': layout_wizard.extra_html,
        'use_default_code_for_qr': True,
    }

class ShReportProductTemplateLabel(models.AbstractModel):
    _name = 'report.sh_product_qrcode_generator.sh_report_product'
    _description = 'Product Label Report'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)

    def get_qr_code_data(self, product):
        return product.default_code if product.default_code else ''

class ShReportProductTemplateLabelDymo(models.AbstractModel):
    _name = 'report.sh_product_qrcode_generator.sh_report_product_dymo'
    _description = 'Product Label Report'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)

    def get_qr_code_data(self, product):
        return product.default_code if product.default_code else ''
