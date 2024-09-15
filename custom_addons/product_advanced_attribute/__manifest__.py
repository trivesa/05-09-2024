# -*- coding: utf-8 -*-
# Part of Atharva System. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Advanced Attribute',
    'category' : 'Website',
    'summary': """
		Manage advanced product attributes""",
    'license' : 'OPL-1',
    'version': '1.0',
    'author': 'Atharva System',
    'website': 'https://www.atharvasystem.com',
    'support': 'support@atharvasystem.com',
    'description': """
       Manage advanced product attributes,
	   Advance Product Search,
	   Product attributes categorized,
	   Attribute set,
	   Website product filter,
	   Website Product Compare,
	   Custom website search,
	   Categorty Attributes, attribute groups , product feature , group features ,
	   Website Sale Category For Attribute ,Website Product Features , Product Filter ,
	   Product Attribute,
	   advanced Attribute,
	   advanced_product_attribute,
	   advanced product attribute,
	   Product geavanceerd kenmerk,Attribuut ingesteld, geavanceerde productkenmerken,atributos avanzados del producto
        سمات المنتج المتقدمة, مجموعة السمة
       Product geavanceerd kenmerk, Attribuut ingesteld, kenmerkgroepen
       Attribut avancé du produit , Ensemble d'attributs , groupes d'attributs
    """,
    'depends' : ['product','website_sale_comparison','website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/template.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            "product_advanced_attribute/static/src/css/adv_attrib_styles.css",
            "product_advanced_attribute/static/src/js/adv_attrib_js.js",
            "product_advanced_attribute/static/src/js/advanced_attrib_js.js"
        ],
    },
    'images': ['static/description/advance-product-att.png'],
	'price': 139.00,
    'currency': 'EUR',
    'installable': True,
    'application': True
}
