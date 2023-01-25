from odoo import models


class TimesheetXlsx(models.AbstractModel):
    _name = "report.ssq_timesheet_xlsx_report.report_timesheet_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Timesheet XLSX Report"

    def generate_xlsx_report(self, workbook, data, timesheets):
        sheet = workbook.add_worksheet("Timesheet")
        sheet.set_column(0, 0, 13)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 25)
        sheet.set_column(3, 3, 30)
        sheet.set_column(4, 4, 30)
        sheet.set_column(5, 5, 13)

        bold = workbook.add_format({"bold": True})
        footer = workbook.add_format({"bold": True, "align": "right"})
        content = workbook.add_format()
        content_right = workbook.add_format({"align": "right"})

        sheet.write(0, 0, "DATE", bold)
        sheet.write(0, 1, "EMPLOYEE", bold)
        sheet.write(0, 2, "PROJECT", bold)
        sheet.write(0, 3, "TASK", bold)
        sheet.write(0, 4, "DESCRIPTION", bold)
        sheet.write(0, 5, "HOURS SPENT", bold)

        i = 1
        total_work_hour = 0
        for timesheet in timesheets:
            sheet.write(i, 0, timesheet.date.strftime("%d-%m-%Y"), content)
            sheet.write(i, 1, timesheet.employee_id.name, content)
            sheet.write(i, 2, timesheet.project_id.name, content)
            sheet.write(i, 3, timesheet.task_id.name or "", content)
            sheet.write(i, 4, timesheet.name, content)
            sheet.write(i, 5, "{:02.0f}:{:02.0f}".format(*divmod(float(timesheet.unit_amount) * 60, 60)), content_right)
            i += 1
            total_work_hour += timesheet.unit_amount
        sheet.merge_range(i, 0, i, 4, "Total Work Hours", footer)
        sheet.write(i, 5, "{:02.0f}:{:02.0f}".format(*divmod(float(total_work_hour) * 60, 60)), footer)
