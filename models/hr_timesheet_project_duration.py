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

    @api.multi
    def write(self, vals):
        res = super(project_duration_timesheet, self).write(vals)
        number = 0.0
        proj_duration_hours = 0.0
        proj_duration_unsued_h = 0.0
        emp_name = ''
        proj_duration_employee = ''
        proj_duration_assistant = ''

        for rec in self:
            c_id = rec.search_read([('user_id', '=', self._uid)])
            # print("CURR", c_id)
            # print("T IDS", rec.timesheet_ids)
            # print(rec.project_duration_ids)

            for num in range(len(rec.timesheet_ids)):
                number += rec.timesheet_ids[num]['unit_amount']
                proj_name = rec.timesheet_ids[num]['account_id']['name']
                emp_name = rec.timesheet_ids[num]['user_id']['name']
                proj_id = rec.project_duration_ids.search(['&', '|', ('employee.user_id', '=', self._uid), ('assistant.user_id', '=', self._uid), ('proj_duration_id', '=', proj_name)])

                # print(proj_id)
                # if proj_id['assistant_exist']:

                proj_duration_hours = proj_id['hours_amount']
                proj_duration_unsued_h = proj_id['hours_unused']
                proj_duration_employee = proj_id['employee']['name']
                proj_duration_assistant = proj_id['assistant']['name']

                print(proj_duration_hours)
                print(proj_duration_unsued_h)

            if (((emp_name == proj_duration_employee) or (emp_name == proj_duration_assistant)) and ((number <= proj_duration_hours) or (number <= proj_duration_unsued_h)) or self.env.user.has_group('hr.group_hr_manager')):
                return res

            else:
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

    # @api.depends('hours_amount', 'assistant_exist')
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
            # if (employee_hours + assistant_houts) > rec.hours_amount:
            #     raise osv.except_osv(('Warning!'),
            #                          ('The number of hours of the team exceeds the number of allowed hours.'))
