   from odoo import models, fields, api

   class ProductTemplate(models.Model):
       _inherit = 'product.template'

       x_studio_item_code = fields.Char(string='商品编码')
   EOF

