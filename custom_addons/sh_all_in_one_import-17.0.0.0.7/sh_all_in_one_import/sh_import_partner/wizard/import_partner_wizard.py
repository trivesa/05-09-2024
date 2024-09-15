# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from odoo.exceptions import UserError
import csv
import base64
import xlrd
from odoo.tools import ustr
import requests
import codecs
import logging
import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT



_logger = logging.getLogger(__name__)


class ImportPartnerWizard(models.TransientModel):
    _name = "import.partner.wizard"
    _description = "Import customer or supplier wizard"

    import_type = fields.Selection([
        ('csv', 'CSV File'),
        ('excel', 'Excel File')
    ], default="csv", string="Import File Type", required=True)
    file = fields.Binary(string="File")
    is_customer = fields.Boolean(string="Is a Customer", default=True)
    is_supplier = fields.Boolean(string="Is a Vendor")
    method = fields.Selection([
        ('create', 'Create Customer/Vendor'),
        ('write', 'Create or Update Customer/Vendor')
    ], default="create", string="Method", required=True)
    contact_update_by = fields.Selection([
        ('name', 'Name'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('mobile', 'Mobile'),
    ], default='name', string="Customer/Vendor Update By", required=True)

    def validate_field_value(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        """ Validate field value, depending on field type and given value """
        self.ensure_one()

        try:
            checker = getattr(self, 'validate_field_' + field_ttype)
        except AttributeError:
            _logger.warning(
                field_ttype + ": This type of field has no validation method")
            return {}
        else:
            return checker(field_name, field_ttype, field_value, field_required, field_name_m2o)

    def validate_field_many2many(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            name_relational_model = self.env['res.partner'].fields_get()[
                field_name]['relation']

            ids_list = []
            if field_value.strip() not in (None, ""):
                for x in field_value.split(','):
                    x = x.strip()
                    if x != '':
                        record = self.env[name_relational_model].sudo().search([
                            (field_name_m2o, '=', x)
                        ], limit=1)

                        if record:
                            ids_list.append(record.id)
                        else:
                            return {"error": " - " + x + " not found. "}
                            break

            return {field_name: [(6, 0, ids_list)]}

    def validate_field_many2one(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            name_relational_model = self.env['res.partner'].fields_get()[
                field_name]['relation']
            record = self.env[name_relational_model].sudo().search([
                (field_name_m2o, '=', field_value)
            ], limit=1)
            return {field_name: record.id if record else False}

    def validate_field_text(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_integer(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_float(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_char(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_boolean(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        boolean_field_value = False
        if field_value.strip() == 'TRUE':
            boolean_field_value = True

        return {field_name: boolean_field_value}

    def validate_field_selection(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}

        # get selection field key and value.
        selection_key_value_list = self.env['res.partner'].sudo(
        )._fields[field_name].selection
        if selection_key_value_list and field_value not in (None, ""):
            for tuple_item in selection_key_value_list:
                if tuple_item[1] == field_value:
                    return {field_name: tuple_item[0] or False}

            return {"error": " - " + field_name + " given value " + str(field_value) + " does not match for selection. "}

        # finaly return false
        if field_value in (None, ""):
            return {field_name: False}

        return {field_name: field_value or False}

    def show_success_msg(self, counter, skipped_line_no):
        # open the new success message box
        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        dic_msg = str(counter) + " Records imported successfully"
        if skipped_line_no:
            dic_msg = dic_msg + "\nNote:"
        for k, v in skipped_line_no.items():
            dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg

        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }
    
    def read_xls_book(self):
        book = xlrd.open_workbook(file_contents=base64.decodebytes(self.file))
        sheet = book.sheet_by_index(0)
        # emulate Sheet.get_rows for pre-0.9.4
        values_sheet = []
        for rowx, row in enumerate(map(sheet.row, range(sheet.nrows)), 1):
            values = []
            for colx, cell in enumerate(row, 1):
                if cell.ctype is xlrd.XL_CELL_NUMBER:
                    is_float = cell.value % 1 != 0.0
                    values.append(
                        str(cell.value) if is_float else str(int(cell.value)))
                elif cell.ctype is xlrd.XL_CELL_DATE:
                    is_datetime = cell.value % 1 != 0.0
                    # emulate xldate_as_datetime for pre-0.9.3
                    dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(
                        cell.value, book.datemode))
                    values.append(
                        dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT
                                    ) if is_datetime else dt.
                        strftime(DEFAULT_SERVER_DATE_FORMAT))
                elif cell.ctype is xlrd.XL_CELL_BOOLEAN:
                    values.append(u'True' if cell.value else u'False')
                elif cell.ctype is xlrd.XL_CELL_ERROR:
                    raise ValueError(
                        _("Invalid cell value at row %(row)s, column %(col)s: %(cell_value)s"
                          ) % {
                              'row':
                              rowx,
                              'col':
                              colx,
                              'cell_value':
                              xlrd.error_text_from_code.get(
                                  cell.value,
                                  _("unknown error code %s") % cell.value)
                          })
                else:
                    values.append(cell.value)
            values_sheet.append(values)
        return values_sheet

    def import_partner_apply(self):

        partner_obj = self.env['res.partner']
        ir_model_fields_obj = self.env['ir.model.fields']

        # perform import lead
        if self and self.file:
            # For CSV or For Excel
            if self.import_type == 'csv' or self.import_type == 'excel':
                counter = 1
                skipped_line_no = {}
                row_field_dic = {}
                row_field_error_dic = {}
                try:
                    if self.import_type == 'csv':
                        file = str(base64.decodebytes(
                                self.file).decode('utf-8'))
                        values = csv.reader(file.splitlines())

                    else:
                        values = self.read_xls_book()
                    skip_header = True

                    for row in values:
                        try:
                            if skip_header:
                                skip_header = False

                                for i in range(16, len(row)):
                                    name_field = row[i]
                                    name_m2o = False
                                    if '@' in row[i]:
                                        list_field_str = name_field.split('@')
                                        name_field = list_field_str[0]
                                        name_m2o = list_field_str[1]
                                    search_field = ir_model_fields_obj.sudo().search([
                                        ("model", "=", "res.partner"),
                                        ("name", "=", name_field),
                                    ], limit=1)

                                    if search_field:
                                        field_dic = {
                                            'name': name_field,
                                            'ttype': search_field.ttype,
                                            'required': search_field.required,
                                            'name_m2o': name_m2o
                                        }
                                        row_field_dic.update({i: field_dic})
                                    else:
                                        row_field_error_dic.update(
                                            {row[i]: " - field not found"})

                                counter = counter + 1
                                continue
                            # check if any error in dynamic field
                            if row_field_error_dic:
                                res = self.show_success_msg(
                                    0, row_field_error_dic)
                                return res

                            if row[1] != '':
                                vals = {}
                                if row[5] != '':
                                    search_state = self.env['res.country.state'].search(
                                        [('name', '=', row[5])], limit=1)
                                    if search_state:
                                        vals.update(
                                            {'state_id': search_state.id})
                                    else:
                                        skipped_line_no[str(
                                            counter)] = " - State not found. "
                                        counter = counter + 1
                                        continue

                                if row[7] != '':
                                    search_country = self.env["res.country"].search(
                                        [('name', '=', row[7])], limit=1)
                                    if search_country:
                                        vals.update(
                                            {'country_id': search_country.id})
                                    else:
                                        skipped_line_no[str(
                                            counter)] = " - Country not found. "
                                        counter = counter + 1
                                        continue

                                if row[13] != '' and row[0].strip() != 'Company':
                                    search_title = self.env["res.partner.title"].search(
                                        [('name', '=', row[13])], limit=1)
                                    if search_title:
                                        vals.update({'title': search_title.id})
                                    else:
                                        skipped_line_no[str(
                                            counter)] = " - Title not found. "
                                        counter = counter + 1
                                        continue
                                if row[8] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'function': row[8]
                                    })
                                vals.update({'company_type': 'person'})
                                if row[0].strip() == 'Company':
                                    vals.update({'company_type': 'company'})
                                    vals.pop('title', None)
                                    vals.pop('function', None)

                                if self.is_customer:
                                    vals.update({'customer_rank': 1})
                                else:
                                    vals.update({'customer_rank': 0})

                                if self.is_supplier:
                                    vals.update({'supplier_rank': 1})
                                else:
                                    vals.update({'supplier_rank': 0})

                                if row[15].strip() not in (None, ""):
                                    image_path = row[15].strip()
                                    if "http://" in image_path or "https://" in image_path:
                                        try:
                                            r = requests.get(image_path)
                                            if r and r.content:
                                                image_base64 = base64.encodebytes(
                                                    r.content)
                                                vals.update(
                                                    {'image_1920': image_base64})
                                            else:
                                                skipped_line_no[str(
                                                    counter)] = " - URL not correct or check your image size. "
                                                counter = counter + 1
                                                continue
                                        except Exception as e:
                                            skipped_line_no[str(
                                                counter)] = " - URL not correct or check your image size " + ustr(e)
                                            counter = counter + 1
                                            continue

                                    else:
                                        try:
                                            with open(image_path, 'rb') as image:
                                                image.seek(0)
                                                binary_data = image.read()
                                                image_base64 = codecs.encode(
                                                    binary_data, 'base64')
                                                if image_base64:
                                                    vals.update(
                                                        {'image_1920': image_base64})
                                                else:
                                                    skipped_line_no[str(
                                                        counter)] = " - Could not find the image or please make sure it is accessible to this user. "
                                                    counter = counter + 1
                                                    continue
                                        except Exception as e:
                                            skipped_line_no[str(
                                                counter)] = " - Could not find the image or please make sure it is accessible to this user " + ustr(e)
                                            counter = counter + 1
                                            continue
                                if row[2] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'street': row[2],
                                    })
                                if row[3] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'street2': row[3],
                                    })
                                if row[4] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'city': row[4],
                                    })
                                if row[6] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'zip': row[6],
                                    })
                                if row[9] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'phone': row[9],
                                    })
                                if row[10] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'mobile': row[10],
                                    })
                                if row[11] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'email': row[11],
                                    })
                                if row[12] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'website': row[12],
                                    })
                                if row[14] not in ("",False,None,0,0.0,'0','0.0'):
                                    vals.update({
                                        'comment': row[14],
                                    })
                                vals.update({
                                    'name': row[1],
                                })

                                # dynamic field logic start here
                                is_any_error_in_dynamic_field = False
                                for k_row_index, v_field_dic in row_field_dic.items():

                                    field_name = v_field_dic.get("name")
                                    field_ttype = v_field_dic.get("ttype")
                                    field_value = row[k_row_index]
                                    field_required = v_field_dic.get(
                                        "required")
                                    field_name_m2o = v_field_dic.get(
                                        "name_m2o")

                                    dic = self.validate_field_value(
                                        field_name, field_ttype, field_value, field_required, field_name_m2o)
                                    if dic.get("error", False):
                                        skipped_line_no[str(counter)] = dic.get(
                                            "error")
                                        is_any_error_in_dynamic_field = True
                                        break
                                    else:
                                        vals.update(dic)

                                if is_any_error_in_dynamic_field:
                                    counter = counter + 1
                                    continue
                                partner_domain = []
                                if self.contact_update_by == 'name':
                                    partner_domain = [
                                        ('name', '=', row[1]),
                                    ]
                                elif self.contact_update_by == 'email' and row[11] not in ['',None]:
                                    partner_domain = [
                                        ('email', '=', row[11]),
                                    ]
                                elif self.contact_update_by == 'phone' and row[9] not in ['',None]:
                                    partner_domain = [
                                        ('phone', '=', row[9]),
                                    ]
                                elif self.contact_update_by == 'mobile' and row[10] not in ['',None]:
                                    partner_domain = [
                                        ('mobile', '=', row[10]),
                                    ]
                                if self.method == 'create':
                                    partner_obj.sudo().create(vals)
                                    counter = counter + 1
                                elif self.method == 'write':
                                    partner_id = self.env['res.partner'].sudo().search(partner_domain,limit=1)
                                    if partner_id:
                                        partner_id.sudo().write(vals)
                                        counter = counter + 1
                                    elif not partner_id:
                                        partner_obj.sudo().create(vals)
                                        counter = counter + 1
                            else:
                                skipped_line_no[str(
                                    counter)] = " - Name is empty. "
                                counter = counter + 1
                        except Exception as e:
                            skipped_line_no[str(
                                counter)] = " - Value is not valid " + ustr(e)
                            counter = counter + 1
                            continue

                except Exception:
                    raise UserError(
                        _("Sorry, Your csv file does not match with our format"))

                if counter > 1:
                    completed_records = (counter - len(skipped_line_no)) - 2
                    res = self.show_success_msg(
                        completed_records, skipped_line_no)
                    return res

        else:
            raise UserError(_("Please Attach The File !"))