# Odoo12 Project duration module
## Table of contents
* [General info](#general-info)
* [Features](#features)
* [Technical](#technical)
* [Errors](#errors)

## General info
This is an addition to the hr_timesheet_sheet module, which extends the module's capabilities. The module adds a list of employees who can be assigned to the project and specifies the number of hours.
Thanks to filled in work cards, the number of hours assigned to an employee will decrease.
Each added employee may additionally have a helper who will be able to add this project to his work card.
In case of an employee with a helper added, their number of hours will be added.
Additionally, the table shows the number of hours that the team has been assigned to use.

<img src="https://i.ibb.co/3YxGNmz/1.png" alt="Timesheet Project Duration">

### Features:
- project team for the project
- determining the number of hours for individual employees
- checking the correctness of completed work cards
- better project management

For more details please contact the author:
<a href="mailto:daniel.demedziuk@gmail.com">daniel.demedziuk@gmail.com</a>

## Technical
### Depends:
- account
- hr
- hr_timesheet_sheet

<img src="https://i.ibb.co/wJsFGrc/2.png" alt="Analytical account table">

An additional table appears in the analytical account form at the bottom and shows in turn:
- <b>Employee</b> - downloaded from hr.employee,
- <b>Assistant Exist</b> - you can add a second employee as an assistant for the first,
- <b>Assistant</b> - first employee assistant downloaded from hr.employee
- <b>Hours unused</b> - result of the subtraction between the total number of hours and hours of employees,
- <b>Number of hours</b> - the total number of hours assigned by the manager to an employee to complete a project.
## Errors
When an employee who is not on the list tries to add a project to his work card and fill it in, he receives the following message.
<br/>
<img src="https://i.ibb.co/B6bHqqz/4.png" alt="#1 Error message">

When an employee who has been added to the list exceeds or incorrectly completes the number of hours per project, he will receive the following message.
<br/>
<img src="https://i.ibb.co/4YVZBLZ/3.png" alt="#2 Error message">
