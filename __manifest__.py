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
This is an addition to the hr_timesheet_sheet module, which extends the module's capabilities. The module adds a list of employees who can be assigned to the project and specifies the number of hours.
Thanks to filled in work cards, the number of hours assigned to an employee will decrease.
Each added employee may additionally have a helper who will be able to add this project to his work card. In case of an employee with a helper added, their number of hours will be added.

For more details please contact
email: daniel.demedziuk@gmail.com

Main Features
-------------
* Project team for the project
* Determining the number of hours for individual employees
* Checking the correctness of completed work cards
* Better project management
""",
    'website': 'website',
    'category': 'Tool, Addon',
    'depends': ['account', 'hr_timesheet_sheet', 'mail', 'contacts'],
    'data': [
        'views/project_duration_view.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
    },
}
