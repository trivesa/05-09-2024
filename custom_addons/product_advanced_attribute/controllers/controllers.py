# -*- coding: utf-8 -*-
# Part of Atharva System. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_comparison.controllers.main import WebsiteSaleProductComparison
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import QueryURL
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools import lazy

class WebsiteSale(WebsiteSale):

    def _get_shop_domain(self, search, category, attrib_values, search_in_description=True):
        domain = request.website.sale_product_domain()
        attribute_values = []
        if search:
            product_attributes = request.env['product.attribute'].sudo().search([('use_in_search', '=', True)])
            if product_attributes:
                for attribute in product_attributes:
                    for srch in search.split(" "):
                        attr_values = request.env['product.attribute.value'].sudo().search([('attribute_id', '=', attribute.id),('name','ilike',srch)])
                        if attr_values:
                            for val in attr_values:
                                attribute_values.append(val.id)
                        attr_values = request.env['product.attribute_desc.lines'].sudo().search([('attribute_id','=',attribute.id),'|',('attribute_text','ilike',srch),('attribute_textarea','ilike',srch)])
                        if attr_values:
                            for val in attr_values:
                                attribute_values.append(val.attribute_id.id)

            for srch in search.split(" "):
                if len(attribute_values) > 0:
                    domain += [
                        '|', '|', '|', '|', '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                        ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch),
                        ('attribute_line_desc_ids.value_ids', 'in', attribute_values), ('attribute_line_ids.value_ids','in',attribute_values),
                        ('attribute_line_desc_ids.attribute_text', 'ilike', srch), ('attribute_line_desc_ids.attribute_textarea', 'ilike', srch)]
                else:
                    domain += [
                        '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                        ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]
        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += ['|',('attribute_line_ids.value_ids', 'in', ids),('attribute_line_desc_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += ['|',('attribute_line_ids.value_ids', 'in', ids),('attribute_line_desc_ids.value_ids', 'in',ids)]
        return domain

    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        res = super(WebsiteSale, self).shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post)
        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        ProductAttribute = request.env['product.attribute']
        filtered_attributes_ids = ProductAttribute.search([('id','in',list(attributes_ids))])

        domain = self._get_shop_domain(search, category, attrib_values)

        keep = QueryURL('/shop', **self._shop_get_query_url_kwargs(category and int(category), search, min_price, max_price, **post))

        pricelist_context = dict(request.env.context)

        if not pricelist_context.get('pricelist'):
            pricelist = request.website._get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.update_context(pricelist=pricelist.id, partner=request.env.user.partner_id)
        url = "/shop"
        if search:
            post["search"] = search
        if category:
            category = request.env['product.public.category'].browse(int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template']
        Category = request.env['product.public.category']
        if search:
            categories = Product.search(domain).mapped('public_categ_ids')
            categs = request.env['product.public.category'].filtered(lambda c: not c.parent_id)
        else:
            categs = Category.search([('parent_id', '=', False)] + request.website.website_domain())

        Product = request.env['product.template']
        parent_category_ids = []
        if category:
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            domain += [('sale_ok', '=', True), ('is_published', '=', True)]
            if min_price:
                min_price = float(min_price)
                domain += [('list_price', '>=', min_price)]
            if max_price:
                max_price = float(max_price)
                domain += [('list_price', '<=', max_price)]
        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))
        if products:
            attributes = ProductAttribute.search(['|',('attribute_line_ids.product_tmpl_id', 'in', products.ids),('attribute_line_desc_ids.product_tmpl_id', 'in', products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)
        attributes = ProductAttribute.search([('id','in',attributes.ids),('display_type','not in',['text','textarea'])])

        attr_value_dict, valid_attr_list = {}, []
        if attributes:
            for each_attr in attributes:
                for each_val in each_attr.value_ids:
                    attr_value_dict[each_val.id] = 0
            temp_prod_list = Product.search(domain, limit=False, order=self._get_search_order(post))
            if temp_prod_list:
                dom = [('product_tmpl_id','in',temp_prod_list.ids)]
                attrs_desc_line_rec = request.env['product.attribute_desc.lines'].search(dom)
                if attrs_desc_line_rec:
                    for each_attrs_desc_line_rec in attrs_desc_line_rec:
                        for each_vals_desc_line in each_attrs_desc_line_rec.value_ids:
                            if each_vals_desc_line.id in attr_value_dict:
                                attr_value_dict[each_vals_desc_line.id] += 1
                attrs_line_rec = request.env['product.template.attribute.line'].search(dom)
                if attrs_line_rec:
                    for each_attrs_line_rec in attrs_line_rec:
                        for each_vals_line in each_attrs_line_rec.value_ids:
                            if each_vals_line.id in attr_value_dict:
                                attr_value_dict[each_vals_line.id] += 1
            for each_attr in attributes:
                value_ids_count = 0
                for each_val in each_attr.value_ids:
                    if each_val.id in attr_value_dict and attr_value_dict[each_val.id] > 0:
                        value_ids_count += 1
                if value_ids_count > 0:
                    valid_attr_list.append(each_attr.id)
        attributes = ProductAttribute.search([('id','in',valid_attr_list)], order='category_id,sort_order')

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        fiscal_position_sudo = request.website.fiscal_position_id.sudo()
        products_prices = lazy(lambda: products._get_sales_prices(pricelist, fiscal_position_sudo))
        context_data = {
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'filtered_attributes': filtered_attributes_ids,
            'pager': pager,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'attr_value_prod_counts': attr_value_dict,
            'products_prices': products_prices,
            'get_product_prices': lambda product: lazy(lambda: products_prices[product.id]),
        }
        res.qcontext.update(context_data)
        return res
