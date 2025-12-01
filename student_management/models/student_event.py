from odoo import models, fields, api

class StudentEvent(models.Model):
    _name = "student.event"
    _description = "Student Events"

    name = fields.Char(string="Event Name", required=True)
    date = fields.Date(string="Event Date", required=True)
    description = fields.Text(string="Description")
    student_ids = fields.Many2many(
        'student.student',
        string="Participating Students"
    )
    state = fields.Selection([
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='planned')


