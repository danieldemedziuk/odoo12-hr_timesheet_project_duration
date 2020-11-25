# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.osv import osv
from datetime import date

today = date.today().strftime('%Y-%m-%d')


class project_duration_timesheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    projects_list = fields.Many2one('account.analytic.account', 'Projects List')
    timesheet_line = fields.Many2one('hr.analytic.timesheet', 'Timesheet line')
    project_duration_ids = fields.Many2one('project.duration', 'Project duration')

    def write(self, vals):
        project_duration_timesheet.check_project_assistant(self)
        res = super(project_duration_timesheet, self).write(vals)

        return res

    def check_project_assistant(self):
        result = {}

        for c_timesheet in self.timesheet_ids.search([('user_id', '=', self._uid)]):
            curr_project = c_timesheet['account_id']['name']

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

                    assistant_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_assistant)]):
                        assistant_hours += timesheet['unit_amount']

                    result[curr_project][duration_assistant] = assistant_hours
                    sum_hours = employee_hours + assistant_hours

                    if sum_hours > duration_amount:
                        raise osv.except_osv(('Warning!'),
                                         ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))

                else:
                    employee_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_employee)]):
                        employee_hours += timesheet['unit_amount']

                    if employee_hours > duration_amount:
                        raise osv.except_osv(('Warning!'),
                                             ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))


class project_duration_model(models.Model):
    _inherit = "account.analytic.account"

    project_druation_sheet = fields.One2many('project.duration', 'proj_duration_id')
    date_start = fields.Date(string="Start date")
    date_stop = fields.Date(string="Stop date")
    notes = fields.Text(string="Notes")


class project_duration(models.Model):
    _name = "project.duration"
    _description = "Project duration account"

    employee = fields.Many2one('hr.employee', domain=([('x_production', '=', True)]), string='Employee', store=True)
    hours_amount = fields.Float(string='Number of hours', store=True)
    hours_unused = fields.Float(string='Hours unused', compute='check_hours_amount', readonly=True)
    assistant_exist = fields.Boolean(help='Is there an assistant for this employee')
    assistant = fields.Many2one('hr.employee', domain=([('x_production', '=', True)]), string='Assistant')
    proj_duration_id = fields.Many2one('account.analytic.account', 'Model ID')
    timesheet_sheet = fields.Many2one('hr_timesheet.sheet', 'Timesheet sheet')

    @api.one
    def check_hours_amount(self):
        employee_hours = 0.0
        assistant_houts = 0.0
        for rec in self:
            for timesheet_id in rec.timesheet_sheet.timesheet_ids.search_read([]):
                if (timesheet_id['employee_id'][1] == rec.employee['name']) and (timesheet_id['project_id'][1] == rec.proj_duration_id['name']):
                    employee_hours += timesheet_id['unit_amount']

                if rec.assistant_exist:
                    if (timesheet_id['employee_id'][1] == rec.assistant['name']) and (timesheet_id['project_id'][1] == rec.proj_duration_id['name']):
                        assistant_houts += timesheet_id['unit_amount']
                    rec.hours_unused = rec.hours_amount - (employee_hours + assistant_houts)
                else:
                    self.write({'assistant': False})
                    rec.hours_unused = rec.hours_amount - employee_hours
