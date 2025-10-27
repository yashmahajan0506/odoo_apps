from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Information'

    name = fields.Char(string='Name')
    roll_no = fields.Integer(string='Roll Number', required=True)
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
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
    image = fields.Binary(string='Photo')
    
    subject_ids=fields.Many2many('school.subject',string='Subjects')
    class_id = fields.Many2one('school.class', string="Class")

    _sql_constraints = [
        ('roll_no', 'unique(roll_no)', 'Roll Number must be unique!'),
        ]
    
    # @api.model
    # def create_default_student(self):
    #    return self.create({'name':'Iron man','email':'ironmana123@gmail.com'})
    
    @api.depends('name', 'roll_no')
    def _compute_full_detail(self):
        for rec in self:
            rec.full_detail = f"{rec.name} - {rec.roll_no}"
            
    
    def _calculate_age(self, dob):
        if not dob:
            return 0
        dob = fields.Date.from_string(dob) if isinstance(dob, str) else dob
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    
    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = self._calculate_age(rec.dob)

    @api.model
    def create(self, vals):
        if 'dob' in vals and self._calculate_age(vals['dob']) < 18:
            raise UserError("You cannot add a student with age less than 18!")
        return super().create(vals)

    def write(self, vals):
        if 'roll_no' in vals:
            for i in self:
                if i.roll_no:
                    raise UserError("You cannot change the roll no ")
        return super().write(vals)
          
        # if 'dob' in vals:
        #     for rec in self:
        #         if self._calculate_age(vals['dob']) < 18:
        #             raise UserError("You cannot set age less than 18!")
        # return super().write(vals) 
        
    def unlink(self):
        for rec in self:
            if rec.is_active:
                raise UserError("Cannot delete an active student!")
        return super().unlink()
      
class Schoolsubject(models.Model):
    _name='school.subject'
    _description="Subjects"

    name=fields.Char(string="Subject Name",required=True)
    code=fields.Char(string="Subject Code")
    

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = "School Classes"

    name = fields.Char(string="Class Name", required=True)
    class_teacher = fields.Char(string="Class Teacher")
    section = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ], string="Section")
    student_ids = fields.One2many('student.student', 'class_id', string="Students")