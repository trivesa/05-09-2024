# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, _
from datetime import datetime
from odoo.exceptions import UserError
import csv
import base64
from odoo.tools import ustr
import logging

_logger = logging.getLogger(__name__)


class ImportTaskWizard(models.TransientModel):
    _name = "import.task.wizard"
    _description = "Import Task Wizard"

    project_id = fields.Many2one("project.project", string="Project")
    import_type = fields.Selection([
        ('csv', 'CSV File'),
        ('excel', 'Excel File')
    ], default="csv", string="Import File Type", required=True)
    file = fields.Binary(string="File")
    user_ids = fields.Many2many('res.users', string="Assigned to")
    # extension
    import_method = fields.Selection([
        ('default', 'By Default'),
        ('proj_user_wise', 'Project and user wise import')
    ], default="default", string="Import Method", required=True)

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
            name_relational_model = self.env['project.task'].fields_get()[
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
            name_relational_model = self.env['project.task'].fields_get()[
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
        selection_key_value_list = self.env['project.task'].sudo(
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

    def import_task_apply(self):

        project_task_obj = self.env['project.task']
        project_obj = self.env['project.project']
        user_obj = self.env['res.users']
        ir_model_fields_obj = self.env['ir.model.fields']
        # perform import task using by default method...
        if self and self.file:
            if self.import_method == 'default':
                for rec in self:
                    counter = 0
                    skipped_line_no = {}
                    row_field_dic = {}
                    row_field_error_dic = {}
                    try:
                        values = []
                        if self.import_type == 'csv':
                            # For CSV
                            file = str(
                                base64.decodebytes(self.file).decode('utf-8'))
                            values = csv.reader(file.splitlines())
                        elif self.import_type == 'excel':
                            # For EXCEL
                            values = self.read_xls_book()
                        skip_header = True

                        for row in values:
                            try:
                                if skip_header:
                                    skip_header = False

                                    for i in range(6, len(row)):
                                        name_field = row[i]
                                        name_m2o = False
                                        if '@' in row[i]:
                                            list_field_str = name_field.split(
                                                '@')
                                            name_field = list_field_str[0]
                                            name_m2o = list_field_str[1]
                                        search_field = ir_model_fields_obj.sudo().search([
                                            ("model", "=", "project.task"),
                                            ("name", "=", name_field),
                                            ("store", "=", True),
                                        ], limit=1)

                                        if search_field:
                                            field_dic = {
                                                'name': name_field,
                                                'ttype': search_field.ttype,
                                                'required': search_field.required,
                                                'name_m2o': name_m2o
                                            }
                                            row_field_dic.update(
                                                {i: field_dic})
                                        else:
                                            row_field_error_dic.update(
                                                {row[i]: " - field not found"})
                                    continue

                                if row_field_error_dic:
                                    res = self.show_success_msg(
                                        0, row_field_error_dic)
                                    return res

                                if row[2] != '':

                                    final_deadline_date = None
                                    if row[4] != '':
                                        cd = row[4]
                                        cd = str(datetime.strptime(
                                            cd, '%Y-%m-%d').date())
                                        final_deadline_date = cd

                                    search_project_id = False
                                    if row[0] != '':
                                        search_project = project_obj.search(
                                            [('name', '=', row[0])], limit=1)
                                        if search_project:
                                            search_project_id = search_project.id
                                        else:
                                            search_project_id = False
                                            skipped_line_no[str(
                                                counter + 2)] = " - Project not found. "
                                            counter = counter + 1
                                            continue

                                    search_user_id = False
                                    if row[1] != '':
                                        search_user = user_obj.search(
                                            [('name', '=', row[1])], limit=1)
                                        if search_user:
                                            search_user_id = search_user.id
                                        else:
                                            search_user_id = False

                                    vals = {
                                        'name': row[2],
                                        'date_deadline': final_deadline_date,
                                        'description': row[3],
                                        'project_id': search_project_id,
                                        'user_ids': [(6, 0, [search_user_id])],
                                        'allocated_hours': row[5],
                                    }

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

                                    project_task_obj.create(vals)
                                    counter = counter + 1
                                else:
                                    skipped_line_no[str(
                                        counter + 2)] = " - Task name is empty. "
                                    counter = counter + 1
                            except Exception as e:
                                skipped_line_no[str(
                                    counter)] = " - Value is not valid " + ustr(e)
                                counter = counter + 1
                                continue

                    except Exception:
                        raise UserError(
                            _("Sorry, Your csv file does not match with our format"))

                    if counter == 0:
                        raise UserError(_("Something went wrong"))
                    elif counter >= 1:
                        completed_task = counter - len(skipped_line_no)
                        res = rec.show_success_msg(
                            completed_task, skipped_line_no)
                        return res

            # project and user wise import.
            if self.import_method == 'proj_user_wise' and self.user_ids and self.project_id:
                for rec in self:
                    counter = 0
                    skipped_line_no = {}
                    row_field_dic = {}
                    row_field_error_dic = {}
                    try:
                        if self.import_type == 'csv':
                            # For CSV
                            file = str(
                                base64.decodebytes(self.file).decode('utf-8'))
                            values = csv.reader(file.splitlines())
                        elif self.import_type == 'excel':
                            # For EXCEL
                            values = self.read_xls_book()
                        skip_header = True

                        for row in values:
                            try:
                                if skip_header:
                                    skip_header = False

                                    for i in range(4, len(row)):
                                        name_field = row[i]
                                        name_m2o = False
                                        if '@' in row[i]:
                                            list_field_str = name_field.split(
                                                '@')
                                            name_field = list_field_str[0]
                                            name_m2o = list_field_str[1]
                                        search_field = ir_model_fields_obj.sudo().search([
                                            ("model", "=", "project.task"),
                                            ("name", "=", name_field),
                                            ("store", "=", True),
                                        ], limit=1)

                                        if search_field:
                                            field_dic = {
                                                'name': name_field,
                                                'ttype': search_field.ttype,
                                                'required': search_field.required,
                                                'name_m2o': name_m2o
                                            }
                                            row_field_dic.update(
                                                {i: field_dic})
                                        else:
                                            row_field_error_dic.update(
                                                {row[i]: " - field not found"})

                                    continue

                                if row_field_error_dic:
                                    res = self.show_success_msg(
                                        0, row_field_error_dic)
                                    return res

                                if row[0] != '':
                                    final_deadline_date = None
                                    if row[2] != '':
                                        cd = row[2]
                                        cd = str(datetime.strptime(
                                            cd, '%Y-%m-%d').date())
                                        final_deadline_date = cd
                                    vals = {
                                        'name': row[0],                                        
                                        'date_deadline': final_deadline_date,
                                        'description': row[3],
                                        'project_id': rec.project_id.id,
                                        'user_ids': [(6, 0, rec.user_ids.ids)],
                                        'allocated_hours': row[1],
                                    }

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

                                    project_task_obj.create(vals)
                                    counter = counter + 1
                                else:
                                    skipped_line_no[str(
                                        counter + 2)] = " - Task name is empty. "
                                    counter = counter + 1
                                    continue
                            except Exception as e:
                                skipped_line_no[str(
                                    counter)] = " - Value is not valid " + ustr(e)
                                counter = counter + 1
                                continue

                    except Exception:
                        raise UserError(
                            _("Sorry, Your file does not match with our format"))

                    if counter == 0:
                        raise UserError(_("Something went wrong"))
                    elif counter >= 1:
                        completed_task = counter - len(skipped_line_no)
                        res = rec.show_success_msg(
                            completed_task, skipped_line_no)
                        return res

        else:
            raise UserError(_('Please Attach The File !'))