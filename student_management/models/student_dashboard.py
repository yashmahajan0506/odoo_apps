from odoo import models, fields, api
import base64
class StudentDashboard(models.Model):
            _name = "student.dashboard"
            _description = "Student Dashboard"
            
            total_students = fields.Integer(compute="_compute_data")
            active_students = fields.Integer(compute="_compute_data")
            male_students=fields.Integer(compute="_compute_data")
            female_students=fields.Integer(compute="_compute_data")
            department_count = fields.Integer(compute="_compute_data")
            subject_count = fields.Integer(compute="_compute_data")

            @api.model
            def search(self, args, limit=None, offset=0, order=None, count=False):
                if count:
                    return 1
                return [self.browse(1)]

            @api.depends()
            def _compute_data(self):
                Student = self.env["student.student"]
                Department = self.env["school.department"]
                Subject = self.env["school.subject"]

                for rec in self:
                    rec.total_students = Student.search_count([])
                    rec.active_students = Student.search_count([("is_active", "=", True)])
                    # rec.alumni_students = Student.search_count([("state", "=", "alumni")])
                    rec.male_students = Student.search_count([("gender", "=", "male")])
                    rec.female_students = Student.search_count([("gender", "=", "female")])
                    rec.department_count = Department.search_count([])
                    rec.subject_count = Subject.search_count([])

            @api.model
            def generate_pdf(self):
                Student = self.env["student.student"]
                Department = self.env["school.department"]
                Subject = self.env["school.subject"]
                
                data = {
                    "total_students": Student.search_count([]),
                    "active_students": Student.search_count([("is_active", "=", True)]),
                    "male_students" : Student.search_count([("gender", "=", "male")]),
                    "female_students" : Student.search_count([("gender", "=", "female")]),
                    "department_count": Department.search_count([]),
                    "subject_count": Subject.search_count([]),
                    
                }

                html = self.env["ir.qweb"]._render("student_management.student_dashboard_simple_pdf", data)

                pdf_content = self.env["ir.actions.report"]._run_wkhtmltopdf(
                    [html],
                    landscape=False,
                )

                return {
                    "pdf_base64": base64.b64encode(pdf_content).decode(),
                }
