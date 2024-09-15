# -*- coding: utf-8 -*-
# Part of Atharva System. See LICENSE file for full copyright and licensing details.

from odoo import models, tools, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.osv import expression

from collections import OrderedDict

class ProductAttributeSet(models.Model):
    _name = "product.attribute.set"
    _description = "Product Attribute Set"

    name = fields.Char(string='Attribute Set', required=True)
    active = fields.Boolean(default=True, help="When Inactive, it will not be selectable in product.")
    attribute_ids = fields.Many2many('product.attribute', string='Attributes')
    product_ids = fields.One2many('product.template','attribute_set_id',string='Products')

    _sql_constraints = [
        ('code_attribute_set', 'unique(name)', 'The name of the attribute set must be unique!')
    ]

class ProductTemplate(models.Model):
    _inherit = "product.template"

    attribute_set_id = fields.Many2one('product.attribute.set',string="Attribute Set")
    attribute_line_desc_ids = fields.One2many('product.attribute_desc.lines', 'product_tmpl_id', 'Product Attribute')

    @api.constrains('attribute_line_desc_ids')
    def _check_attribute_value_ids(self):
        for product in self:
            attributes = self.env['product.attribute']
            for value in product.attribute_line_desc_ids:
                if value.attribute_id in attributes:
                    raise ValidationError(_('Error! It is not allowed to choose more than one value for a given attribute.'))
                if value.attribute_id:
                    attributes |= value.attribute_id
        return True

    def get_variant_groups(self):
        categories = []
        for var in self.attribute_line_ids:
            category_id = var.attribute_id.category_id.id
            if category_id not in categories:
                categories.append(category_id)
        for var in self.attribute_line_desc_ids:
            category_id = var.attribute_id.category_id.id
            if category_id not in categories:
                categories.append(category_id)

        list_set = set(categories)
        categories = (list(list_set))
        res = OrderedDict()
        categories_list = self.env['product.attribute.category'].search([('id', 'in', categories)], order='sequence')
        for ca in categories_list:
            res.setdefault(ca, [])
        res.setdefault(self.env['product.attribute.category'], [])
        for var in self.attribute_line_ids:
            if var.attribute_id.use_in_product_attributes_table:
                res[var.attribute_id.category_id].append(var)
        for var in self.attribute_line_desc_ids:
            if var.attribute_id.use_in_product_attributes_table:
                res[var.attribute_id.category_id].append(var)
        return res

    def fill_attribute_set(self):
        old_attribute = []
        values = []
        for var in self:
            if var.attribute_set_id:
                if var.attribute_set_id:
                    for v in var.attribute_line_desc_ids:
                        old_attribute.append(v.attribute_id.id)
                    for attribute in var.attribute_set_id.attribute_ids:
                        values.append(attribute.id)
                        if attribute.id not in old_attribute:
                            self.env['product.attribute_desc.lines'].create({'product_tmpl_id' :var.id,'attribute_id' : attribute.id,'attribute_set_id' : var.attribute_set_id.id})
                    for i in range(len(old_attribute)):
                        if(old_attribute[i] not in values):
                            search_record = self.env['product.attribute_desc.lines'].search(['&',('product_tmpl_id','=',var.id),('attribute_id','=', old_attribute[i])])
                            if search_record:
                                search_record.unlink()
            else:
                var.attribute_line_desc_ids and var.attribute_line_desc_ids.unlink()


    def _search_get_detail(self, website, order, options):
        result = super()._search_get_detail(website, order, options)
        search_fields = result.setdefault('search_fields', [])
        mapping = result.setdefault('mapping', {})

        result['base_domain'] = result.get('base_domain', [])
        domains = [website.sale_product_domain()]

        new_search_field = ['attribute_line_ids.value_ids.name','attribute_line_desc_ids.value_ids.name','attribute_line_desc_ids.attribute_text','attribute_line_desc_ids.attribute_textarea']
        search_fields.extend(new_search_field)

        domains.append(['|',('attribute_line_desc_ids.value_ids.attribute_id.use_in_search','=',True),('attribute_line_ids.value_ids.attribute_id.use_in_search','=',True)])

        result['base_domain'].extend(domains)

        fields_to_add = [
            ('attribute_line_ids.value_ids.name', {'name': 'attribute_line_ids.value_ids.name', 'type': 'text', 'match': True}),
            ('attribute_line_desc_ids.value_ids.name', {'name': 'attribute_line_desc_ids.value_ids.name', 'type': 'text', 'match': True}),
            ('attribute_line_desc_ids.attribute_text', {'name': 'attribute_line_desc_ids.attribute_text', 'type': 'text', 'match': True}),
            ('attribute_line_desc_ids.attribute_textarea', {'name': 'attribute_line_desc_ids.attribute_textarea', 'type': 'text', 'match': True})
        ]

        for field, field_mapping in fields_to_add:
            search_fields.append(field)
            mapping[field] = field_mapping

        return result

class ProductAttribute(models.Model):
    _inherit="product.attribute"
    _order = "sort_order"

    display_type = fields.Selection(selection_add=[
        ('text', 'Textbox'),
        ('textarea','Text Area'),
        ('yes_no','Yes / No')
        ], ondelete={'text': 'set default', 'textarea': 'set default', 'yes_no': 'set default'})
    use_in_search = fields.Boolean(string='Use in Search', default=True)
    use_in_compare = fields.Boolean(string='Use in Compare', default=True)
    use_in_product_attributes_table = fields.Boolean(string='Use in Product Attributes Table', default=True)
    attribute_line_desc_ids = fields.One2many('product.attribute_desc.lines', 'attribute_id', 'Desc Lines')
    sort_order = fields.Integer(string='Priority Sequence', default=1)

    @api.depends('attribute_line_ids.active', 'attribute_line_ids.product_tmpl_id', 'attribute_line_desc_ids', 'attribute_line_desc_ids.product_tmpl_id')
    def _compute_products(self):
        for pa in self:
            product_list = []
            product_list.extend(pa.attribute_line_ids.product_tmpl_id.ids)
            product_list.extend(pa.attribute_line_desc_ids.product_tmpl_id.ids)
            pa.product_tmpl_ids = self.env['product.template'].browse(product_list)

    @api.model
    def create(self, values):
        res = super(ProductAttribute, self).create(values)
        if 'display_type' in values and values.get('display_type') == 'yes_no':
            self.env['product.attribute.value'].create({'name': 'Yes', 'attribute_id': res.id})
            self.env['product.attribute.value'].create({'name': 'No', 'attribute_id': res.id})
        return res

    def write(self, values):
        if('display_type' in values):
            if self.display_type != 'yes_no' and values.get('display_type') == 'yes_no':
                self.env['product.attribute.value'].search([('attribute_id','=',self.id)]).unlink()
                self.env['product.attribute.value'].create({'name': 'Yes', 'attribute_id': self.id})
                self.env['product.attribute.value'].create({'name': 'No', 'attribute_id': self.id})
            elif self.display_type == 'yes_no' and values.get('display_type') != 'yes_no':
                self.env['product.attribute.value'].search([('attribute_id','=',self.id)]).unlink()
        res = super(ProductAttribute, self).write(values)
        return res

class ProductAttributeValues(models.Model):
    _name = "product.attribute_desc.lines"
    _description = "Product Attribute Desc Lines"
    _rec_name = "attribute_id"
    _order = "sequence, id"

    @api.onchange('attribute_set_id')
    def _get_domains_x(self):
        result_ids = []
        record = self
        if  record and record.attribute_set_id and record.attribute_set_id.attribute_ids and record.attribute_set_id.attribute_ids.ids:
            result_ids = record.attribute_set_id.attribute_ids.ids
        return {'domain': {'attribute_id' : [('id','in',result_ids)]} }

    product_tmpl_id = fields.Many2one('product.template', 'Product Template', ondelete='cascade', required=True)
    attribute_id = fields.Many2one('product.attribute', 'Attribute', ondelete='restrict', required=True)
    sequence = fields.Integer(help="The sequence field is used to define order in which the tax lines are applied.",related="attribute_id.sort_order", store=True)
    attribute_set_id = fields.Many2one('product.attribute.set',string="Attribute Set")
    value_ids = fields.Many2many('product.attribute.value', string='Attribute Values')
    attribute_text = fields.Char("Text", translate=True)
    display_type = fields.Selection(related='attribute_id.display_type')
    attribute_textarea = fields.Html("TextArea", translate=True)

    @api.onchange('attribute_id','attribute_id.display_type')
    def reset_values(self):
        self.value_ids = False
        self.attribute_textarea = ''
        self.attribute_text = ''

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.onchange('module_website_sale_comparison')
    def module_comparison_warning(self):
        if not self.module_website_sale_comparison:
            raise UserError(_('Unchecking the Product Comparison Tool will uninstall the module "Product Advanced Attributes" and all the saved data of the specified module will be lost!'))

class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_compare_list(self):
        variant_attributes = self.product_tmpl_id.valid_product_template_attribute_line_ids._without_no_variant_attributes().attribute_id.sorted()
        no_variant_attributes = self.product_tmpl_id.attribute_line_desc_ids.attribute_id.sorted()
        attributes = variant_attributes + no_variant_attributes

        categories = OrderedDict([(cat, OrderedDict()) for cat in attributes.category_id.sorted()])
        if any(not pa.category_id for pa in attributes):
            # category_id is not required and the mapped does not return empty
            categories[self.env['product.attribute.category']] = OrderedDict()

        for pa in variant_attributes:
            if pa.use_in_compare:
                categories[pa.category_id][pa] = OrderedDict([(
                    product,
                    product.product_template_attribute_value_ids.filtered(lambda ptav: ptav.attribute_id == pa)
                ) for product in self])

        for pa in no_variant_attributes:
            if pa.use_in_compare:
                categories[pa.category_id][pa] = OrderedDict()
                for product in self:
                    categories[pa.category_id][pa].setdefault(product, [])
                    for line in product.attribute_line_desc_ids:
                        if line.attribute_id == pa:
                            if pa.display_type == 'text':
                                categories[pa.category_id][pa][product].append(line.attribute_text)
                            elif pa.display_type == 'textarea':
                                categories[pa.category_id][pa][product].append(line.attribute_textarea)
                            else:
                                categories[pa.category_id][pa][product].append(line.value_ids)
        return categories