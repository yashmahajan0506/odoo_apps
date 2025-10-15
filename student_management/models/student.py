from odoo import models, fields, api

from datetime import date
class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Information'
    name = fields.Char(string='Name', required=True)
    roll_no = fields.Integer(string='Roll Number', required=True)
    dob=fields.Date(string="Date of Birth",required=True)
    age = fields.Integer(string='Age',compute='_compute_age',store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone Number')
    admission_date = fields.Date(string='Admission Date', default=fields.Date.today())
    is_active = fields.Boolean(string='Active Student', default=True)
    notes = fields.Text(string='Notes')
    full_detail = fields.Char(string="Full Detail", compute="_compute_full_detail")
    image=fields.Binary(string='photo')


    _sql_constraints = [
        ('roll_no', 'unique(roll_no)', 'Roll Number must be unique!'),
    ]
    
    @api.depends('name', 'roll_no')
    def _compute_full_detail(self):
        for record in self:
            record.full_detail = f"{record.name} - {record.roll_no}"
    
    @api.depends('dob')
    def _compute_age(self):
        today=date.today()

        for i in self:
                if i.dob:
                      dob = i.dob
                      age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                      i.age = age
                else:
                   i.age = 0      