from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Information'
    _inherit=['mail.thread','mail.activity.mixin']

    # _inherit = ['mail.thread', 'mail.activity.mixin']
 
    
    name = fields.Char(string='Name', tracking=True)
    roll_no = fields.Integer(string='Roll Number', required=True, default=False)
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
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('alumni', 'Alumni'),
    ], string="Status", default='draft', tracking=True,readonly=True)
    
    subject_line_ids = fields.One2many('student.subject.line', 'student_id', string="Subjects & Marks")
    class_id = fields.Many2one('school.class', string="Class")
#     user_id = fields.Many2one(
#     'res.users',
#     string='Related User',
#     help="Link student record to a specific Odoo user"
# )
    user_id = fields.Many2one('res.users', string="Related User", ondelete="cascade")

    _sql_constraints = [
        ('roll_no', 'unique(roll_no)', 'Roll Number must be unique!'),
        ]
    
    # @api.model
    # def create_default_student(self):
    #    return self.create({'name':'Iron man','email':'ironmana123@gmail.com'})
    
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_alumni(self):
        for rec in self:
            rec.state = 'alumni'

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'
    
    
    @api.constrains('image')
    def check_image(self):
        for rec in self:
            if not rec.image:
                raise UserError("You cannot add image empty") 
            
            
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
         student = super(Student, self).create(vals)
         
         
         student.message_post(
             body="Student Has Created successfully"
             #there are other type also :- like message_type,subject
             
         )
        
         if not student.user_id:
             if not student.email:
                 raise UserError(("Please enter an email for the student to create a login."))
    
             group_student = self.env.ref('student_management.group_student_user', raise_if_not_found=False)
             group_internal = self.env.ref('base.group_user', raise_if_not_found=False)
        
            
             user_vals = {
                 'name': student.name,
                 'login': student.email.lower(),
                 'email': student.email.lower(),
                 'password': '1234',
                 'active': True,
                 'groups_id': [(6, 0, [group_internal.id, group_student.id])],
             }
             new_user = self.env['res.users'].sudo().create(user_vals)
             student.user_id = new_user.id
        
         return student

    
    # @api.model
    # def create(self, vals):
    #     if 'dob' in vals and self._calculate_age(vals['dob']) < 18:
    #         raise UserError("You cannot add a student with age less than 18!")
    #     return super().create(vals)

    # def write(self, vals):
    #     if 'roll_no' in vals:
    #         for i in self:
    #             if i.roll_no:
    #                 raise UserError("You cannot change the roll no ")
    #     return super().write(vals)
          
    #     if 'dob' in vals:
    #         for rec in self:
    #             if self._calculate_age(vals['dob']) < 18:
    #                 raise UserError("You cannot set age less than 18!")
    #     return super().write(vals) 
        
    # def unlink(self):
    #     for rec in self:
    #         if rec.is_active:
    #             raise UserError("Cannot delete an active student!")
    #     return super().unlink()
      
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
    

class StudentSubjectLine(models.Model):
    _name = 'student.subject.line'
    _description = 'Student Subject Marks'

    student_id = fields.Many2one('student.student', string="Student", ondelete="cascade")
    subject_id = fields.Many2one('school.subject', string="Subject", required=True)
    subject_code = fields.Char(related='subject_id.code', string="Subject Code", store=True)
    marks = fields.Float(string="Marks",default=False)
    grade = fields.Char(string="Grade")

    @api.onchange('marks')
    def _onchange_marks(self):
        for rec in self:
            if rec.marks is None:
                rec.grade = False
            elif rec.marks >= 90:
                rec.grade = "A"
            elif rec.marks >= 75:
                rec.grade = "B"
            elif rec.marks >= 60:
                rec.grade = "C"
            elif rec.marks >= 40:
                rec.grade = "D"
            else:
                rec.grade = "F"
                