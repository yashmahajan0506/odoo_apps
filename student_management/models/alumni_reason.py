from odoo import models, fields

class StudentAlumniReason(models.Model):
    _name = 'student.alumni.reason'
    _description = 'Student Alumni Reason'

    name = fields.Char(string="Reason", required=True)
    student_id = fields.Many2one('student.student', string="Student", ondelete='cascade')
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
