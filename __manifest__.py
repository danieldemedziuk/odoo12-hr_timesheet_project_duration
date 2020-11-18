# -*- coding: utf-8 -*-

{
    'name': 'Timesheet Project Duration',
    'version': '1.0',
    'author': 'Daniel Demedziuk',
    'summary': 'timesheet, project',
    'sequence': 110,
    'complexity': 'normal',
    'description': """
Timesheet Project Duration
==================================
This is an addition to the hr_timesheet_sheet module, which extends the module's capabilities. The module adds a list of employees who can be assigned to the project and a certain number of hours.
With filled-in work cards, the number of hours assigned to an employee will decrease.

email: daniel.demedziuk@mjgroup.pl

""",
    'website': 'website',
    'category': 'Tool, Addon',
    'depends': ['account', 'hr_timesheet_sheet', 'mail', 'contacts'],
    'data': [
        'views/project_duration_view.xml',
        'security/hr_timesheet_project_duration_security.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
    },
}
