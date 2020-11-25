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
    #     emp_hr = 0.0
    #     assistant_hr = 0.0
    #     sum_hr = 0.0
    #     proj_duration_hours = 0.0
    #     # proj_duration_unused_h = 0.0
    #     proj_duration_employee = ''
    #     proj_duration_assistant = ''
    #     proj_dur_line = self.project_duration_ids
    #     curr_user = self.timesheet_ids
    #     c_id = self.search_read([])
    #     # print("CURR", c_id)
    #
    #     for num in range(len(self.timesheet_ids)):
    #         # print("T IDS", self.timesheet_ids)
    #         emp_hr += self.timesheet_ids[num]['unit_amount']
    #         proj_name = self.timesheet_ids[num]['account_id']['name']
    #         curr_user = self.timesheet_ids[num]['user_id']['name']
    #         proj_dur_line = self.project_duration_ids.search(['|', '&', ('employee.user_id', '=', self._uid), ('assistant.user_id', '=', self._uid), ('proj_duration_id', '=', proj_name)])
    #
    #     for x in range(len(proj_dur_line)):
    #         # print("PROJECT", proj_dur_line[x]['proj_duration_id']['name'])
    #         print("EXIST", proj_dur_line[x]['assistant_exist'])
    #         proj_duration_hours = proj_dur_line[x]['hours_amount']
    #         proj_duration_employee = proj_dur_line[x]['employee']['name']
    #
    #         if (not proj_dur_line[x]['assistant_exist']) and (curr_user == proj_duration_employee):
    #             print("CURR USER", curr_user)
    #             print("DURAT EMP", proj_duration_employee)
    #             print(emp_hr)
    #             print("HOURS", proj_duration_hours)
    #
    #             if ((curr_user == proj_duration_employee) and (emp_hr <= proj_duration_hours) or self.env.user.has_group('hr.group_hr_manager')):
    #                 return res
    #
    #             else:
    #                 raise osv.except_osv(('Warning!'),
    #                                      ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))
    #
    #         elif (curr_user == proj_duration_employee) or (curr_user == proj_dur_line[x]['assistant']['name']):
    #             proj_duration_assistant = proj_dur_line[x]['assistant']['name']
    #
    #
    #             for timesheet_id in c_id:
    #                 print('TIMESHEET ID', timesheet_id)
    #                 if timesheet_id.get('employee_id')[1] == proj_dur_line[x]['assistant']['name']:
    #                     print("DUR ASSIS", proj_dur_line[x]['assistant']['name'])
    #                     print("ASSISTANT", timesheet_id.get('employee_id')[1])
    #                     for timesheet_l in timesheet_id.get('timesheet_ids'):
    #                         ts = self.timesheet_ids
    #                         print('TS', ts)
    #
    #                         for t in ts:
    #                             print('TIMESHEET LINE', t)
    #                             assistant_hr += t['unit_amount']
    #                             print("ASSIS HR", assistant_hr)
    #                     # print("HR", assistant_hr)
    #                     sum_hr = emp_hr + assistant_hr
    #                 else:
    #                     continue
    #
    #
    #             print("CURR USER", curr_user)
    #             print("DURAT EMP", proj_duration_employee)
    #             print("DURAT ASSIS", proj_duration_assistant)
    #             print("SUM HR", sum_hr)
    #             print("DURAT HR", proj_duration_hours)
    #
    #
    #
    #
    #             if (((curr_user == proj_duration_employee) or (curr_user == proj_duration_assistant)) and (sum_hr <= proj_duration_hours) or self.env.user.has_group('hr.group_hr_manager')):
    #                 return res
    #
    #             else:
    #                 raise osv.except_osv(('Warning!'),
    #                                      ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))

        return res


    def check_project_assistant(self):
        # print("SELF SEARCH", self.search_read([]))
        # print("CURRENT TIMESHEET", self.timesheet_ids)
        # print("CURRENT TIMESHEET READ", self.timesheet_ids.search_read([]))

        sum_hours = 0.0
        result = {}

        for c_timesheet in self.timesheet_ids.search([('user_id', '=', self._uid)]):
            curr_project = c_timesheet['account_id']['name']
            print("CURR PROJECT", curr_project)
            # print("PROJECT DURATION", self.project_duration_ids.search([]))

            result[curr_project] = {}

            for duration in self.project_duration_ids.search([('proj_duration_id', '=', curr_project)]):
                print('DUR', duration)
                duration_employee = duration['employee']['name']
                print('DUR EMP', duration_employee)
                duration_amount = duration['hours_amount']
                print('DUR AMOUNT', duration_amount)
                duration_assistant_exist = duration['assistant_exist']
                print('DUR ASS EXIST', duration_assistant_exist)
                duration_assistant = duration['assistant']['name']
                print('DUR ASSISTANT', duration_assistant)

                if duration_assistant_exist:
                    employee_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_employee)]):
                        employee_hours += timesheet['unit_amount']
                        print("USER", timesheet['user_id']['name'])
                        print("PROJECT", timesheet['account_id']['name'])
                        print("AMOUNT", timesheet['unit_amount'])
                    print('EMPLOYEE HR', employee_hours)

                    assistant_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_assistant)]):
                        assistant_hours += timesheet['unit_amount']

                    print('PROJECT', curr_project)
                    print('ASSISTANT', duration_assistant)
                    print('ASSISTANT HR', assistant_hours)

                    result[curr_project][duration_assistant] = assistant_hours

                    sum_hours = employee_hours + assistant_hours
                    print("########", duration_employee, employee_hours, duration_assistant, assistant_hours, "SUM", sum_hours, "DUR AMOUNT", duration_amount)

                    if sum_hours > duration_amount:
                        raise osv.except_osv(('Warning!'),
                                         ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))

                else:
                    employee_hours = 0.0
                    for timesheet in self.timesheet_ids.search([('account_id', '=', curr_project), ('user_id', '=', duration_employee)]):
                        employee_hours += timesheet['unit_amount']
                        print("USER", timesheet['user_id']['name'])
                        print("PROJECT", timesheet['account_id']['name'])
                        print("AMOUNT", timesheet['unit_amount'])
                    print('EMPLOYEE HR', employee_hours)

                    if employee_hours > duration_amount:
                        raise osv.except_osv(('Warning!'),
                                             ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))


        print("ASSISTANTS RESULT", result)






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

            # if (employee_hours + assistant_houts) > rec.hours_amount:
            #     raise osv.except_osv(('Warning!'),
            #                          ('The number of hours of the team exceeds the number of allowed hours.'))
