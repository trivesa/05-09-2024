#!/usr/bin/python3
{
    # App information
    'name': 'eBay Odoo Connector',
    'version': '17.0.0.3',
    'category': 'eCommerce',
    'license': 'OPL-1',
    'summary': 'Automate your vital business processes & eliminate the need for manual data entry at Odoo by bi-directional data exchange & integration between eBay & Odoo.Customers can manage their orders, can check the reporting, manage ebay fees & other operations as mentioned in the User documentation.Apart from Odoo Ebay Connector, we do have other ecommerce solutions or applications such as Woocommerce connector , Shopify connector , magento connector and also we have solutions for Marketplace Integration such as Odoo Amazon connector , Odoo Walmart Connector , Odoo Bol.com Connector.Aside from ecommerce integration and ecommerce marketplace integration, we also provide solutions for various operations, such as shipping , logistics , shipping labels , and shipping carrier management with our shipping integration , known as the Shipstation connector.For the customers who are into Dropship business, we do provide EDI Integration that can help them manage their Dropshipping business with our Dropshipping integration or Dropshipper integration It is listed as Dropshipping EDI integration and Dropshipper EDI integration.Emipro applications can be searched with different keywords like Amazon integration , Shopify integration , Woocommerce integration, Magento integration , Amazon vendor center module , Amazon seller center module , Inter company transfer , eBay integration , Bol.com integration , inventory management , warehouse transfer module , dropship and dropshipper integration and other Odoo integration application or module',
    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com/',
    # Dependencies
    'depends': ['common_connector_library'],
    # Views
    'data': [
        'view/product_template_view.xml',
        'view/product_product_view.xml',
        'security/res_groups.xml',
        'view/ebay_instance_ept_view.xml',
        'data/ir_cron_data.xml',
        'view/ebay_seller_ept_view.xml',
        'view/sale_workflow_config.xml',
        'view/sale_order.xml',
        'view/stock_picking.xml',
        'view/ebay_payment_options.xml',
        'wizard_views/res_config_ebay_seller.xml',
        'wizard_views/res_config_ebay_instance.xml',
        'wizard_views/res_config_settings.xml',
        'view/ebay_site_policy_ept.xml',
        'view/ebay_shipping_service.xml',
        'view/ebay_exclude_shipping_locations.xml',
        'view/ebay_shipping_locations.xml',
        'view/ebay_product_template_ept.xml',
        'view/ebay_product_product_ept.xml',
        'view/category.xml',
        'view/ebay_product_listing.xml',
        'view/duration_time.xml',
        'view/ebay_max_item_counts.xml',
        'view/ebay_feedback_score.xml',
        'view/ebay_unpaid_item_strike_count.xml',
        'view/ebay_unpaid_item_strike_duration.xml',
        'view/item_feedback_score.xml',
        'view/ebay_refund_options.xml',
        'view/ebay_restock_fee_options.xml',
        'view/ebay_refund_shipping_cost_options.xml',
        'view/ebay_return_days.xml',
        'wizard_views/ebay_process_import_export.xml',
        'wizard_views/ebay_credential_wizard.xml',
        'wizard_views/ebay_product_wizard_view.xml',
        'view/common_log_book_ept.xml',
        'view/common_log_lines_ept.xml',
        'wizard_views/ebay_cron_configuration.xml',
        'view/delivery_carrier.xml',
        'view/ebay_condition_ept.xml',
        'view/account_move.xml',
        'data/product_data.xml',
        'data/sequence.xml',
        'wizard_views/ebay_queue_process_wizard_view.xml',
        'view/ebay_import_product_queue.xml',
        'view/ebay_order_data_queue_ept.xml',
        'view/dashboard_operation_view.xml',
        'wizard_views/ebay_feedback_wizard.xml',
        'view/ebay_feedback_ept.xml',
        'view/ebay_res_partner_views.xml',
        'security/ir.model.access.csv',
        'view/product_data_queue_line_view.xml',
        'view/order_queue_line_view.xml',
    ],
    'images': ['static/description/eBay-Connector-Cover-Images.png'],
    'live_test_url': 'https://www.emiprotechnologies.com/r/vBX',
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'active': False,
    'price': 579.00,
    'currency': 'EUR',
    "cloc_exclude": [
        "ebaysdk/**/*",
        "**/*.xml",
    ],
    'assets': {
        'web.assets_backend': [

        ],
    },
}
