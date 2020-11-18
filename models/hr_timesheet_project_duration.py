# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.osv import osv


class project_duration_timesheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    projects_list = fields.Many2one('account.analytic.account', 'Projects List')
    timesheet_line = fields.Many2one('hr.analytic.timesheet', 'Timesheet line')
    project_duration_ids = fields.Many2one('project.duration', 'Project duration')

    def write(self, vals):
        res = super(project_duration_timesheet, self).write(vals)
        number = 0.0
        proj_duration_hours = 0.0
        emp_name = ''
        proj_duration_employee = ''

        for rec in self:
            # c_id = rec.search_read([('user_id', '=', self._uid)])
            # print("CURR", c_id)
            # print("T IDS", rec.timesheet_ids)

            for num in range(len(rec.timesheet_ids)):
                number += rec.timesheet_ids[num]['unit_amount']
                print("PROJECT", rec.timesheet_ids[num]['account_id']['name'])
                proj_name = rec.timesheet_ids[num]['account_id']['name']
                emp_name = rec.timesheet_ids[num]['user_id']['name']
                proj_duration_id = rec.project_duration_ids.search(['&', ('employee.user_id', '=', self._uid), ('proj_duration_id', '=', proj_name)])
                proj_duration_hours = proj_duration_id['hours_amount']
                proj_duration_employee = proj_duration_id['employee']['name']

            # print(emp_name, proj_duration_employee)
            # print(number, "<=", proj_duration_hours)
            if (emp_name == proj_duration_employee) and (number <= proj_duration_hours):

                return res

            else:
                raise osv.except_osv(('Warning!'),
                                     ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))


class project_duration_model(models.Model):
    _inherit = "account.analytic.account"

    project_duration_ids = fields.One2many('project.duration', 'proj_duration_id')


class project_duration(models.Model):
    _name = "project.duration"
    _description = "Project duration"

    employee = fields.Many2one('hr.employee', string='Employee', store=True)
    hours_amount = fields.Float(string='Number of hours', store=True)
    proj_duration_id = fields.Many2one('account.analytic.account', 'Model ID')
