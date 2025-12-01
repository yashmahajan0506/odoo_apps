from odoo import models, fields

class Teacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher Information"

    name = fields.Char(string="Teacher Name", required=True)
    age = fields.Integer(string="Age")
    teacher_id = fields.Char(string="Teacher ID")

    department_id = fields.Many2one(
        "school.department",
        string="Department",
        help="Teacher's department"
    )

    expertise_subject = fields.Many2many(
        "school.subject",
        string="Expertise in Subject",
    )
