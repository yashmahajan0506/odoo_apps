from odoo import models, fields, api

class StudentDashboard(models.Model):
            _name = "student.dashboard"
            _description = "Student Dashboard"


            total_students = fields.Integer(compute="_compute_data")
            active_students = fields.Integer(compute="_compute_data")
            # alumni_students = fields.Integer(compute="_compute_data")
            male_students = fields.Integer(compute="_compute_data")
            female_students = fields.Integer(compute="_compute_data")

            @api.model
            def search(self, args, limit=None, offset=0, order=None, count=False):
                if count:
                    return 1
                return [self.browse(1)]

            @api.depends()
            def _compute_data(self):
                Student = self.env["student.student"]
                for rec in self:
                    rec.total_students = Student.search_count([])
                    rec.active_students = Student.search_count([("is_active", "=", True)])
                    # rec.alumni_students = Student.search_count([("state", "=", "alumni")])
                    rec.male_students = Student.search_count([("gender", "=", "male")])
                    rec.female_students = Student.search_count([("gender", "=", "female")])

