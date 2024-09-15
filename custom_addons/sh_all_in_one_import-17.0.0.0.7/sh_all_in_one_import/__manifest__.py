# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    'name': 'All In One Import - Partner, Product, Sales, Purchase, Accounts, Inventory, BOM, CRM, Project | Import Product Template | Import Product Variant | Import Product Image | Import Sale Order Lines | Import Reordering Rules| Import Purchase Order Lines',
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    'support': 'support@softhealer.com',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Import Customers From Csv,Import Suppliers,Import Product image,Import Sale Order from excel,Import Stock,Import Inventory,import purchase order,Import Invoice,Import Bill of Material,Import Lead,Import Task,Import Vendor Detail,Import bank statement',
    'description': """This module is useful to import data from CSV/excel file.
 All In One Import - Sales, Purchase, Account, Inventory, BOM, CRM Odoo
 Import Partner From Csv, Import Partner From Excel, Import Partner From XLS, Import Partner From XLSX, Import Product From Csv, Import Product From Excel, Import Product From XLS, Import Product From XLSX,  Import Sales From Csv, Import Sale Order From Excel, Import Quotation From XLS, Import so From XLSX, Import Purchase From Csv, Import Purchase Order From Excel, Import Request For Quotation From XLS, Import RFQ From XLSX, Import Account From Csv, Import Invoice From Excel, Import Invoice From XLS, Import Account From XLSX, Import Inventory From Csv, Import Stock From Excel, Import Inventory From XLS, Import Stock From XLSX, Import BOM From Csv, Import Bill Of Material From Excel, Import BOM From XLS, Import Bill Of Material From XLSX, Import CRM From Csv, Import CRM From Excel, Import Lead From XLS, Import Lead From XLSX, Import Bill Of Material From XLSX, Import CRM From Csv, Import CRM From Excel, Import Lead From XLS, Import Lead From XLSX,  Import Project From XLSX, Import Project From Csv, Import Task From Excel, Import Reordering Rules From XLS, Import Lead From XLSX Odoo. 
 Import Partner From Csv, Import Product From Excel,  Import Sale Order From Csv ,Import Purchase Order From Excel Module,Import Account From Csv, Import Invoice From Excel,Import Inventory From Xls, Import Stock From Xlsx, Import Bill Of Material From CSV, Import CRM From Csv, Import Lead From XLS,Import Project From XLSX, Import Task From Excel, Import Reordering Rules From XLS Odoo. """,
    'version': '0.0.7',
    'depends': [
        'sh_message',
        'sale_management',
        'stock',
        'account',
        'purchase',
        'mrp',
        'project',
        'crm',
        'hr',
        'hr_attendance',
        'hr_timesheet',
        'hr_expense',
        'point_of_sale',
        'sh_product_multi_barcode',
        'website_sale',
        'sh_import_base',
    ],
    'application': True,
    'data': [
        'sh_import_ail/security/import_ail_security.xml',
        'sh_import_ail/security/ir.model.access.csv',
        'sh_import_ail/wizard/import_ail_wizard_views.xml',
        'sh_import_ail/views/account_move_views.xml',

        'sh_import_inv/security/import_inv_security.xml',
        'sh_import_inv/security/ir.model.access.csv',
        'sh_import_inv/wizard/import_inv_wizard_views.xml',
        'sh_import_inv/views/menus.xml',

        'sh_import_inventory_with_lot_serial/security/import_inventory_with_lot_serial_security.xml',
        'sh_import_inventory_with_lot_serial/security/ir.model.access.csv',
        'sh_import_inventory_with_lot_serial/wizard/import_inventory_with_lot_serial_wizard_views.xml',
        'sh_import_inventory_with_lot_serial/views/product_views.xml',
        'sh_import_inventory_with_lot_serial/views/stock_views.xml',

        'sh_import_inventory_without_lot_serial/security/import_inventory_without_lot_serial_security.xml',
        'sh_import_inventory_without_lot_serial/security/ir.model.access.csv',
        'sh_import_inventory_without_lot_serial/wizard/import_inventory_without_lot_serial_wizard_views.xml',
        'sh_import_inventory_without_lot_serial/views/stock_views.xml',

        'sh_import_lot_serial_picking/security/import_lot_security.xml',
        'sh_import_lot_serial_picking/security/ir.model.access.csv',
        'sh_import_lot_serial_picking/wizard/import_lot_wizard_views.xml',
        'sh_import_lot_serial_picking/views/stock_views.xml',

        'sh_import_partner/security/import_partner_security.xml',
        'sh_import_partner/security/ir.model.access.csv',
        'sh_import_partner/wizard/import_partner_wizard_views.xml',
        'sh_import_partner/views/sale_views.xml',

        'sh_import_po/security/import_po_security.xml',
        'sh_import_po/security/ir.model.access.csv',
        'sh_import_po/wizard/import_po_wizard_views.xml',
        'sh_import_po/views/purchase_views.xml',

        'sh_import_pol/security/import_pol_security.xml',
        'sh_import_pol/security/ir.model.access.csv',
        'sh_import_pol/wizard/import_pol_wizard_views.xml',
        'sh_import_pol/views/purchase_views.xml',

        'sh_import_product_tmpl/security/import_product_tmpl_security.xml',
        'sh_import_product_tmpl/security/ir.model.access.csv',
        'sh_import_product_tmpl/wizard/import_product_tmpl_wizard.xml',
        'sh_import_product_tmpl/views/sale_view.xml',

        'sh_import_product_tmpl_mb/security/import_product_tmpl_security.xml',
        'sh_import_product_tmpl_mb/security/ir.model.access.csv',
        'sh_import_product_tmpl_mb/wizard/import_product_tmpl_wizard.xml',
        'sh_import_product_tmpl_mb/views/sale_view.xml',

        "sh_import_product_var/security/import_product_var_security.xml",
        "sh_import_product_var/security/ir.model.access.csv",
        "sh_import_product_var/wizard/sh_import_product_var_wizard.xml",
        "sh_import_product_var/views/sale_view.xml",

        'sh_import_product_var_mb/security/import_product_var_security.xml',
        'sh_import_product_var_mb/security/ir.model.access.csv',
        'sh_import_product_var_mb/wizard/import_product_var_wizard_views.xml',
        'sh_import_product_var_mb/views/sale_order_import_product_var_mb_views.xml',

        'sh_import_so/security/import_so_security.xml',
        'sh_import_so/security/ir.model.access.csv',
        'sh_import_so/wizard/import_so_wizard_views.xml',
        'sh_import_so/views/sale_views.xml',

        "sh_import_sales_pricelist/security/import_pricelist_security.xml",
        "sh_import_sales_pricelist/security/ir.model.access.csv",
        "sh_import_sales_pricelist/wizard/import_pricelist_wizard_views.xml",

        'sh_import_sol/security/import_sol_security.xml',
        'sh_import_sol/security/ir.model.access.csv',
        'sh_import_sol/wizard/import_sol_wizard_views.xml',
        'sh_import_sol/views/sale_views.xml',

        'sh_import_supplier_info/security/import_supplier_info_security.xml',
        'sh_import_supplier_info/security/ir.model.access.csv',
        'sh_import_supplier_info/wizard/import_supplier_info_wizard_views.xml',
        'sh_import_supplier_info/views/purchase_views.xml',
        "sh_import_supplier_info/data/data.xml",
        "sh_import_supplier_info/views/inherit_import_base_supplier_info_views.xml",
        "sh_import_supplier_info/views/inherit_import_store_supplier_info_views.xml",

        "sh_import_reordering_rules/security/import_reordering_rule_security.xml",
        "sh_import_reordering_rules/security/ir.model.access.csv",
        "sh_import_reordering_rules/wizard/import_reordering_rules_wizard_views.xml",
        "sh_import_reordering_rules/views/stock_views.xml",

        "sh_import_bom/security/import_bom_security.xml",
        "sh_import_bom/security/ir.model.access.csv",
        "sh_import_bom/wizard/import_bom_wizard.xml",
        "sh_import_bom/views/mrp_view.xml",

        "sh_import_int_transfer/security/import_int_transfer_security.xml",
        "sh_import_int_transfer/security/ir.model.access.csv",
        "sh_import_int_transfer/wizard/import_int_transfer_wizard_views.xml",
        "sh_import_int_transfer/views/stock_views.xml",

        "sh_import_int_transfer_adv/security/import_int_transfer_security.xml",
        "sh_import_int_transfer_adv/security/ir.model.access.csv",
        "sh_import_int_transfer_adv/wizard/import_int_transfer_adv_wizard_views.xml",
        "sh_import_int_transfer_adv/views/stock_views.xml",

        "sh_import_lead/security/import_lead_security.xml",
        "sh_import_lead/security/ir.model.access.csv",
        "sh_import_lead/wizard/import_lead_wizard_views.xml",
        "sh_import_lead/views/crm_views.xml",

        "sh_import_product_img/security/import_product_img_security.xml",
        "sh_import_product_img/security/ir.model.access.csv",
        "sh_import_product_img/wizard/import_product_img_wizard.xml",
        "sh_import_product_img/views/sale_view.xml",
        "sh_import_product_img/data/data.xml",
        "sh_import_product_img/views/inherit_import_base.xml",
        "sh_import_product_img/views/inherit_import_store.xml",

        "sh_import_project_task/security/import_project_task_security.xml",
        "sh_import_project_task/security/ir.model.access.csv",
        "sh_import_project_task/wizard/import_task_wizard_views.xml",
        "sh_import_project_task/views/project_views.xml",

        "sh_import_emp_img/security/import_emp_img_security.xml",
        "sh_import_emp_img/security/ir.model.access.csv",
        "sh_import_emp_img/wizard/import_emp_img_wizard_views.xml",
        "sh_import_emp_img/views/hr_view.xml",

        "sh_import_emp_timesheet/security/import_emp_timesheet_security.xml",
        "sh_import_emp_timesheet/security/ir.model.access.csv",
        "sh_import_emp_timesheet/wizard/import_emp_timesheet_wizard.xml",
        "sh_import_emp_timesheet/views/timesheet_view.xml",

        "sh_import_partner_img/security/import_partner_img.xml",
        "sh_import_partner_img/security/ir.model.access.csv",
        "sh_import_partner_img/wizard/import_partner_img_wizard.xml",
        "sh_import_partner_img/views/sale_view.xml",

        "sh_import_attendance/security/import_attendance_security.xml",
        "sh_import_attendance/security/ir.model.access.csv",
        "sh_import_attendance/wizard/import_attendance_wizard_views.xml",

        "sh_import_img_zip/security/import_img_zip_security.xml",
        "sh_import_img_zip/security/ir.model.access.csv",
        "sh_import_img_zip/wizard/import_img_zip_wizard.xml",
        "sh_import_img_zip/views/sale_view.xml",

        'sh_import_pos/security/import_pos_groups.xml',
        'sh_import_pos/security/ir.model.access.csv',
        'sh_import_pos/wizard/import_pos_wizard_views.xml',
        'sh_import_pos/views/pos_views.xml',

        'sh_import_journal_item/security/import_journal_item_security.xml',
        'sh_import_journal_item/security/ir.model.access.csv',
        'sh_import_journal_item/wizard/import_journal_item_wizard_views.xml',
        'sh_import_journal_item/views/account_move_views.xml',

        "sh_import_journal_entry/security/import_journal_entry_security.xml",
        "sh_import_journal_entry/security/ir.model.access.csv",
        "sh_import_journal_entry/wizard/sh_import_journal_entry_views.xml",

        "sh_import_users/security/import_users_security.xml",
        "sh_import_users/security/ir.model.access.csv",
        "sh_import_users/wizard/import_user_wizard_views.xml",

        "sh_export_product_image_shop/security/ir.model.access.csv",
        "sh_export_product_image_shop/security/sh_export_product_image_shop_groups.xml",
        "sh_export_product_image_shop/data/product_template_data.xml",
        "sh_export_product_image_shop/data/product_varient_data.xml",
        "sh_export_product_image_shop/wizard/sh_export_product_image_shop_var_views.xml",
        "sh_export_product_image_shop/wizard/sh_export_product_image_shop_tmpl_views.xml",

        "sh_import_img_zip_shop/security/ir.model.access.csv",
        "sh_import_img_zip_shop/security/security.xml",
        "sh_import_img_zip_shop/wizard/import_img_zip_wizard_views.xml",
        "sh_import_img_zip_shop/views/sale_views.xml",

        'sh_import_chart_of_account/security/sh_import_coa_groups.xml',
        'sh_import_chart_of_account/security/ir.model.access.csv',
        'sh_import_chart_of_account/wizard/sh_import_coa_views.xml',
        'sh_import_chart_of_account/views/menus.xml',

        "sh_import_product_var_shop/security/ir.model.access.csv",
        "sh_import_product_var_shop/security/security.xml",
        "sh_import_product_var_shop/wizard/import_product_var_shop_wizard_views.xml",
        "sh_import_product_var_shop/views/sale_view.xml",

        'sh_import_inv_with_payment/security/import_inv_security.xml',
        'sh_import_inv_with_payment/security/ir.model.access.csv',
        'sh_import_inv_with_payment/wizard/sh_import_inv_with_payment_views.xml',
        'sh_import_inv_with_payment/views/account_views.xml',

        'sh_import_expense/security/security.xml',
        'sh_import_expense/security/ir.model.access.csv',
        'sh_import_expense/wizard/import_expense_wizard_views.xml',
        'sh_import_expense/views/expense_views.xml',

        'sh_all_in_one_import_advance/security/sh_all_in_one_import.xml',
        'sh_all_in_one_import_advance/security/ir.model.access.csv',
        'sh_all_in_one_import_advance/data/sh_all_in_one_import_kanban_data.xml',
        'sh_all_in_one_import_advance/views/sh_all_in_one_import_kanban_views.xml',

        'sh_import_payment/security/sh_import_payment_groups.xml',
        'sh_import_payment/security/ir.model.access.csv',
        'sh_import_payment/wizard/sh_import_payment_views.xml',
    ],
    'external_dependencies': {'python': ['xlrd']},
    'images': ['static/description/background.gif'],
    'auto_install': False,
    'installable': True,
    'price': 80,
    'currency': 'EUR',
}
