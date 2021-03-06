#!/usr/bin/env python
# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.osv import osv
from datetime import date
from odoo.tools.translate import _

today = date.today().strftime('%Y-%m-%d')


class project_duration_timesheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    projects_list = fields.Many2one('account.analytic.account', 'Projects List')
    timesheet_line = fields.Many2one('hr.analytic.timesheet', 'Timesheet line')
    project_duration_ids = fields.Many2one('project.duration', 'Project duration')

    @api.multi
    def write(self, vals):
        depart_resutl = project_duration_timesheet.check_project_department(self)
        assis_result = project_duration_timesheet.check_project_assistant(self)
        curr_user = self['user_id']['name']
        res = super(project_duration_timesheet, self).write(vals)

        for c_timesheet in self.timesheet_ids.search([('user_id', '=', self._uid)]):
            curr_project = c_timesheet['account_id']['name']

            if (curr_user not in assis_result[curr_project]) and (curr_user not in depart_resutl[curr_project]):
                raise osv.except_osv(_('Warning!'),
                                     _('You are not on the list of employees assigned to the project. Contact the manager or administrator.'))

        return res

    def check_project_assistant(self):
        result = {}

        for c_timesheet in self.timesheet_ids.search([('user_id', '=', self._uid)]):
            curr_project = c_timesheet['account_id']['name']
            curr_user = c_timesheet['user_id']['name']

            result[curr_project] = {}

            for duration in self.project_duration_ids.search([('proj_duration_id', '=', curr_project)]):
                duration_employee = duration['employee']['name']
                duration_amount = duration['hours_amount']
                duration_assistant_exist = duration['assistant_exist']
                duration_assistant = duration['assistant']['name']

                if duration_assistant_exist:
                    employee_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_employee)]):
                        employee_hours += timesheet['unit_amount']

                    result[curr_project][duration_employee] = employee_hours

                    assistant_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_assistant)]):
                        assistant_hours += timesheet['unit_amount']

                    result[curr_project][duration_assistant] = assistant_hours
                    sum_hours = employee_hours + assistant_hours

                    if sum_hours > duration_amount:
                        raise osv.except_osv(_('Warning!'),
                                         _('Your number of hours per project is incorrect or has been exhausted. Check the correctness of the project and number of hours or contact the administrator.'))

                else:
                    employee_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_employee)]):
                        employee_hours += timesheet['unit_amount']

                    result[curr_project][duration_employee] = employee_hours

                    if employee_hours > duration_amount:
                        raise osv.except_osv(_('Warning!'),
                                         _('Your number of hours per project is incorrect or has been exhausted. Check the correctness of the project and number of hours or contact the administrator.'))

        return result

    def check_project_department(self):
        result = {}

        for c_timesheet in self.timesheet_ids.search([('user_id', '=', self._uid)]):
            curr_project = c_timesheet['account_id']['name']
            curr_user = c_timesheet['user_id']['name']

            result[curr_project] = {}

            for duration in self.project_duration_ids.search([('proj_duration_id', '=', curr_project)]):
                duration_amount = duration['hours_amount']
                duration_department_exist = duration['department_exist']
                duration_department = duration['department']['name']
                # result[curr_project] = {'duration_amount': duration_amount}

                if duration_department_exist:
                    sum_dep_hours = 0.0

                    for employee_id in self.env['hr.employee'].search([('department_id', '=', duration_department)]):
                        dep_emp_hours = 0.0

                        for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', employee_id['name'])]):
                            sum_dep_hours += timesheet['unit_amount']
                            dep_emp_hours += timesheet['unit_amount']

                        result[curr_project][employee_id['name']] = dep_emp_hours
                    # result[curr_project] = {'department_hours': sum_dep_hours}

                    if sum_dep_hours > duration_amount:
                        raise osv.except_osv(_('Warning!'),
                                         _('Your department has exceeded the number of hours allowed for the project or the number of hours is incorrect. Check the correctness of the project and number of hours or contact the administrator.'))

        return result


class project_duration_model(models.Model):
    _inherit = "account.analytic.account"

    project_druation_sheet = fields.One2many('project.duration', 'proj_duration_id')


class project_duration(models.Model):
    _name = "project.duration"
    _description = "Project duration account"

    employee = fields.Many2one('hr.employee', domain=([('x_production', '=', True)]), string='Employee', store=True)
    hours_amount = fields.Float(string='Number of hours', help='This is the total number of hours allocated to the employee for this project.', store=True)
    hours_unused = fields.Float(string='Hours unused', help='This is the amount of free hours left to be used by this employee.', compute='check_hours_amount', readonly=True)
    assistant_exist = fields.Boolean(help='Is there an assistant for this employee')
    assistant = fields.Many2one('hr.employee', domain=([('x_production', '=', True)]), string='Assistant')
    department_exist = fields.Boolean(help='Assign a department to this project team')
    department = fields.Many2one('hr.department', string='Department')
    proj_duration_id = fields.Many2one('account.analytic.account', 'Model ID')
    timesheet_sheet = fields.Many2one('hr_timesheet.sheet', 'Timesheet sheet')

    @api.one
    def check_hours_amount(self):
        employee_hours = 0.0
        assistant_hours = 0.0
        sum_dep_hours = 0.0
        print('0')
        for rec in self:
            print('0,1')
            print(rec.timesheet_sheet.timesheet_ids.search_read([]))
            for timesheet_id in rec.timesheet_sheet.timesheet_ids.search_read([]):
                print('1')
                if (rec.employee != "") and (timesheet_id['employee_id'][1] == rec.employee['name']) and (timesheet_id['project_id'][1] == rec.proj_duration_id['name']):
                    employee_hours += timesheet_id['unit_amount']
                    print('2')
                if rec.assistant_exist:
                    print('3')
                    if (timesheet_id['employee_id'][1] == rec.assistant['name']) and (timesheet_id['project_id'][1] == rec.proj_duration_id['name']):
                        assistant_hours += timesheet_id['unit_amount']
                        print('4')
                    rec.hours_unused = rec.hours_amount - (employee_hours + assistant_hours)

                else:
                    print('5')
                    rec.hours_unused = rec.hours_amount - employee_hours
                print('6')
                if rec.department_exist:
                    print('7')
                    for employee_id in self.env['hr.employee'].search([('department_id', '=', rec.department['id'])]):
                        if (timesheet_id['project_id'][1] == rec.proj_duration_id['name']) and (timesheet_id['employee_id'][1] == employee_id['name']):
                            sum_dep_hours += timesheet_id['unit_amount']
                            print('8')
                    rec.hours_unused = rec.hours_amount - sum_dep_hours

            if not rec.timesheet_sheet.timesheet_ids.search_read([]):
                rec.hours_unused = rec.hours_amount

    @api.onchange('assistant_exist', 'department_exist')
    def _default_value(self):
        for rec in self:
            if rec.assistant_exist == False:
                rec.write({'assistant': False})

            if rec.department_exist == False:
                rec.write({'department': False})
