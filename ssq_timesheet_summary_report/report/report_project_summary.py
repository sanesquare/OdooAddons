from odoo import models, api
from datetime import datetime, timedelta

STYLES = {}


class TimesheetXlsx(models.AbstractModel):
    _name = "report.report_project_summary"
    _inherit = "report.report_xlsx.abstract"
    _description = "Project Summary Report"

    @api.model
    def _get_report_values(self, data=None):
        return {"report_data": data}

    def get_work_hours(self, date, employee, project):
        query = """
            SELECT SUM(unit_amount) FROM account_analytic_line
            WHERE project_id = %s AND employee_id = %s AND date = %s;
        """
        self.env.cr.execute(query, [project.id, employee.id, date])
        return self.env.cr.fetchall()[0][0] or 0

    def get_project_data(self, workbook, project, record):
        today = datetime.now().date()
        sheet = workbook.add_worksheet(project.name)
        sheet.set_column(0, 0, 15)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 15)
        sheet.set_row(3, 20)
        sheet.set_row(4, 20)

        sheet.merge_range("A1:B3", project.name, STYLES["project_head2"])
        sheet.write(0, 2, "EST HRS", STYLES["project_head1"])
        sheet.write(0, 3, "ACT HRS", STYLES["project_head1"])
        sheet.write(0, 4, "REM HRS", STYLES["project_head1"])
        sheet.write(0, 5, "DELIVERY", STYLES["project_head1"])

        allocated_hours = project.allocated_hours
        allocated_hours_string = (
            "{:02.0f}:{:02.0f}".format(*divmod(float(allocated_hours) * 60, 60)) if allocated_hours > 0 else "--:--"
        )
        sheet.merge_range(1, 2, 2, 2, allocated_hours_string, STYLES["project_head2"])
        date_string = datetime.strftime(project.date, "%d-%m-%Y") if project.date else ""
        sheet.merge_range(1, 5, 2, 5, date_string, STYLES["project_head2"])
        sheet.write(3, 0, "DATE", STYLES["col_head1"])

        col = 1
        actual_hours = 0

        if project.date_start:
            project_start_date = project.date_start
        else:
            project_start_date = project.create_date.date()

        employees = (
            record.employee_ids
            if record.employee_ids
            else self.env["account.analytic.line"]
            .search([("project_id", "=", project.id)], order="employee_id asc")
            .mapped("employee_id")
        )
        for employee in employees:
            sheet.set_column(col, col, 15)
            sheet.write(3, col, employee.name, STYLES["col_head1"])
            tot_hours = 0
            row = 5
            date = today
            while date >= project_start_date:
                if col == 1:
                    sheet.write(row, 0, datetime.strftime(date, "%d-%m-%Y"))
                work_hours = self.get_work_hours(date, employee, project)
                tot_hours += work_hours
                data_string = (
                    "{:02.0f}:{:02.0f}".format(*divmod(float(work_hours) * 60, 60)) if work_hours > 0 else "--:--"
                )
                sheet.write(row, col, data_string, STYLES["cell_data"])

                row += 1
                date -= timedelta(days=1)
            actual_hours += tot_hours
            data_string = "{:02.0f}:{:02.0f}".format(*divmod(float(tot_hours) * 60, 60)) if tot_hours > 0 else "--:--"
            sheet.write(4, col, data_string, STYLES["col_head2"])
            col += 1
        sheet.write(3, col, " ")
        if col > 6:
            sheet.merge_range(1, 6, 2, col - 1, " ", STYLES["project_head2"])

            if col == 7:
                sheet.write(0, 6, " ", STYLES["project_head1"])
            else:
                sheet.merge_range(0, 6, 0, col - 1, " ", STYLES["project_head1"])

        actual_hours_string = (
            "{:02.0f}:{:02.0f}".format(*divmod(float(actual_hours) * 60, 60)) if actual_hours > 0 else "--:--"
        )
        sheet.merge_range(1, 3, 2, 3, actual_hours_string, STYLES["project_head2"])

        rem_hours = allocated_hours - actual_hours
        color = "#30a04f" if rem_hours >= 0 else "red"
        project_head3 = workbook.add_format(
            {"bg_color": "#131f3a", "color": color, "align": "center", "valign": "vcenter", "bold": 1}
        )
        rem_hours_string = (
            "{:02.0f}:{:02.0f}".format(*divmod(float(abs(rem_hours)) * 60, 60)) if allocated_hours else "--:--"
        )
        rem_hours_string = "-" + rem_hours_string if rem_hours < 0 and allocated_hours else rem_hours_string
        sheet.merge_range(1, 4, 2, 4, rem_hours_string, project_head3)

        return {
            "name": project.name,
            "est_hours": allocated_hours_string,
            "act_hours": actual_hours_string,
            "rem_hours": rem_hours_string,
            "delivery": date_string,
            "color": color,
        }

    def generate_xlsx_report(self, workbook, data, record):
        sheet_dashboard = workbook.add_worksheet("Dashboard")

        STYLES["project_head2"] = workbook.add_format(
            {"bg_color": "#131f3a", "color": "white", "align": "center", "valign": "vcenter", "bold": 1}
        )
        STYLES["project_head1"] = workbook.add_format({"bg_color": "#ef9b10", "bold": 1})
        STYLES["col_head1"] = workbook.add_format({"color": "#131f3a", "bold": 1, "border": 1, "valign": "vcenter"})
        STYLES["col_head2"] = workbook.add_format({"bold": 1, "align": "center"})
        STYLES["cell_data"] = workbook.add_format({"align": "center"})

        projects_data_list = []
        DOMAIN = [("timesheet_ids", "!=", False)]
        if record.employee_ids:
            DOMAIN.append(("timesheet_ids.employee_id", "in", record.employee_ids.ids))
        projects = record.project_ids if record.project_ids else self.env["project.project"].search(DOMAIN)
        for project in projects:
            projects_data_list.append(self.get_project_data(workbook, project, record))

        COLOR = {0: "#3c7ee8", 1: "#30a04f", 2: "#efb205"}
        head = workbook.add_format(
            {
                "bold": 1,
                "align": "center",
                "valign": "vcenter",
                "color": "#dddddd",
                "bg_color": "#14405b",
                "border": 2,
                "border_color": "white",
            }
        )

        sheet_dashboard.set_column(0, 11, 10)
        sheet_dashboard.merge_range("A1:D2", "PROJECT", head)
        sheet_dashboard.merge_range("E1:F2", "ESTIMATED HOURS", head)
        sheet_dashboard.merge_range("G1:H2", "ACTUAL HOURS", head)
        sheet_dashboard.merge_range("I1:J2", "REMAINING HOURS", head)
        sheet_dashboard.merge_range("K1:L2", "DELIVERY", head)

        row = 2
        i = 0
        for project in projects_data_list:
            bg_color = COLOR[i % 3]
            sheet_dashboard.merge_range(
                row,
                0,
                row + 1,
                3,
                "  " + project["name"],
                workbook.add_format(
                    {
                        "bold": 1,
                        "valign": "vcenter",
                        "color": "#1c1c1c",
                        "bg_color": bg_color,
                        "border": 2,
                        "border_color": "#eeeeee",
                    }
                ),
            )
            sheet_dashboard.merge_range(
                row,
                4,
                row + 1,
                5,
                project["est_hours"],
                workbook.add_format(
                    {
                        "bold": 1,
                        "align": "center",
                        "valign": "vcenter",
                        "color": "#1c1c1c",
                        "bg_color": bg_color,
                        "border": 2,
                        "border_color": "#eeeeee",
                    }
                ),
            )
            sheet_dashboard.merge_range(
                row,
                6,
                row + 1,
                7,
                project["act_hours"],
                workbook.add_format(
                    {
                        "bold": 1,
                        "align": "center",
                        "valign": "vcenter",
                        "color": "#1c1c1c",
                        "bg_color": bg_color,
                        "border": 2,
                        "border_color": "#eeeeee",
                    }
                ),
            )
            sheet_dashboard.merge_range(
                row,
                8,
                row + 1,
                9,
                project["rem_hours"],
                workbook.add_format(
                    {
                        "bold": 1,
                        "align": "center",
                        "valign": "vcenter",
                        "color": project["color"],
                        "bg_color": "#cccccc",
                        "border": 2,
                        "border_color": "#eeeeee",
                    }
                ),
            )
            sheet_dashboard.merge_range(
                row,
                10,
                row + 1,
                11,
                project["delivery"],
                workbook.add_format(
                    {
                        "bold": 1,
                        "align": "center",
                        "valign": "vcenter",
                        "color": "#1c1c1c",
                        "bg_color": bg_color,
                        "border": 2,
                        "border_color": "#eeeeee",
                    }
                ),
            )
            i += 1
            row += 2
