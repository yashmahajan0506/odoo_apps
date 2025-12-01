from odoo import models, fields

class SchoolSubject(models.Model):
        _name = "school.subject"
        _description = "Subjects offered in Departments"

        name = fields.Char("Subject Name", required=True)
        code = fields.Char("Subject Code")
        credits = fields.Integer("Credits")
        description = fields.Text("Description")

        department_id = fields.Many2one(
            "school.department",
            string="Department",
            required=True
        )
