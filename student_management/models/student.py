from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
import  base64

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    roll_no = fields.Integer(string='Roll Number', required=True)
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        
        ('other', 'Other')
    ], string='Gender')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone Number')
    admission_date = fields.Date(string='Admission Date', default=fields.Date.context_today)
    is_active = fields.Boolean(string='Active Student', default=True)
    notes = fields.Text(string='Notes')
    full_detail = fields.Char(string="Full Detail", compute="_compute_full_detail", store=True)
    image = fields.Binary()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('alumni', 'Alumni'),
    ], string="Status", default='draft', tracking=True, readonly=True)
    assign_teacher=fields.Many2one('school.teacher',string="Assign Teacher",
        required=True)

    # subject_line_ids = fields.One2many('student.subject.line', 'student_id', string="Subjects & Marks")
    # class_id = fields.Many2one('school.class', string="Class")
    user_id = fields.Many2one('res.users', string="Related User", ondelete="cascade")
    # class_teacher_name = fields.Char(related='class_id.class_teacher', string='Class Teacher', store=True)

    # _sql_constraints = [
    #     ('roll_no_uniq', 'unique(roll_no)', 'Roll Number must be unique!'),
    # ]

    subject_count = fields.Integer(string="Subjects Count", compute="_compute_subject_count", store=False)

    
    # def action_send_mail_direct(self):
    #     self.ensure_one()
    
    #     # 1. Create attachment
    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'student_info.pdf',
    #         'datas': base64.b64encode(b'This is test PDF content'),
    #         'res_model': 'student.student',
    #         'res_id': self.id,
    #         'mimetype': 'application/pdf',
    #     })
    
        # 2. Create mail
        # mail = self.env['mail.mail'].create({
        #     'subject': 'Student Details',
        #     'body_html': '<p>Hello, this is a static mail with attachment.</p>',
        #     'email_to': 'test@example.com',
        #     'attachment_ids': [(4, attachment.id)],
        # })
    
        # 3. Send mail
    #    mail.send( )
    
    #     return True
    
    def action_send_report_mail(self):
         self.ensure_one()

         template = self.env.ref('student_management.email_template_student_report')

         
         template.send_mail(self.id, force_send=True)

         return True

    
    
    
    
    # @api.depends('subject_line_ids')
    # def _compute_subject_count(self):
    #     for rec in self:
    #         rec.subject_count = len(rec.subject_line_ids)

    # def action_open_subject_lines(self):
    #     self.ensure_one()
    #     domain = [('student_id', '=', self.id)]
    #     if self.subject_count == 1:
    #         subject = self.env['student.subject.line'].search(domain, limit=1)
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Subject Details',
    #             'res_model': 'student.subject.line',
    #             'view_mode': 'form',
    #             'res_id': subject.id,
    #             'target': 'current',
    #         }
    #     else:
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'All Subjects',
    #             'res_model': 'student.subject.line',
    #             'view_mode': 'list,form',
    #             'domain': domain,
    #             'context': {'default_student_id': self.id},
    #             'target': 'current',
    #         }

    def _cron_send_birthday_emails(self):
        today = date.today()
        students = self.search([])
        for student in students:
            if not student.dob or not student.email:
                continue
            if student.dob.month == today.month and student.dob.day == today.day:
                template = self.env.ref('student_management.email_template_student_birthday', raise_if_not_found=False)
                if template:
                    template.send_mail(student.id, force_send=True)
                    student.message_post(body=f"Birthday email sent to {student.email}")

    def _cron_update_student_state(self):
        today = fields.Date.today()
        for student in self.search([]):
            if student.admission_date:
                days = (today - student.admission_date).days
                if days >= 365 and student.state != 'alumni':
                    student.state = 'alumni'
                elif days >= 7 and student.state == 'draft':
                    student.state = 'confirmed'

    def change_state_to_alumni(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alumni Reason',
            'res_model': 'student.alumni.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_student_id': self.id},
        }

    @api.depends('name', 'roll_no')
    def _compute_full_detail(self):
        for rec in self:
            rec.full_detail = f"{rec.name or ''} - {rec.roll_no or ''}"

    def _calculate_age(self, dob):
        if not dob:
            return 0
        dob_date = fields.Date.from_string(dob) if isinstance(dob, str) else dob
        today = date.today()
        years = today.year - dob_date.year
        if (today.month, today.day) < (dob_date.month, dob_date.day):
            years -= 1
        return years

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = self._calculate_age(rec.dob)

    @api.model
    def create(self, vals):
        student = super(Student, self).create(vals)
        student.message_post(body="Student has been created successfully")
   
        if not student.user_id:
            if not student.email:
                raise UserError("Please enter an email for the student to create a login.")
            group_student = self.env.ref('student_management.group_student_user', raise_if_not_found=False)
            group_internal = self.env.ref('base.group_user', raise_if_not_found=False)
            groups = []
            if group_internal:
                groups.append(group_internal.id)
            if group_student:
                groups.append(group_student.id)
            user_vals = {
                'name': student.name,
                'login': student.email.lower(),
                'email': student.email.lower(),
                'password': '1234',
                'active': True,
                'groups_id': [(6, 0, groups)],
            }
            new_user = self.env['res.users'].sudo().create(user_vals)
            student.user_id = new_user.id
        return student

    def action_send_mail_to_student(self):
        template = self.env.ref('student_management.email_template_teacher_to_student', raise_if_not_found=False)
        if not template:
            raise UserError("Email template not found!")
        for record in self:
            if not record.email:
                raise UserError("Student email not found!")
            template.send_mail(record.id, force_send=True)
        return True

    def action_send_mail_to_teacher(self):
        template = self.env.ref('student_management.email_template_student_to_teacher', raise_if_not_found=False)
        if not template:
            raise UserError("Email template not found!")
        for record in self:
            if not record.class_id or not record.class_id.class_teacher:
                raise UserError("Teacher email not found!")
          
            template.send_mail(record.id, force_send=True)
        return True

    def action_send_email_with_attachment(self):
        res_ids = self.ids
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': self._name,
                'default_res_ids': res_ids,
                'default_composition_mode': 'comment',
            },
        }


# class Schoolsubject(models.Model):
#     _name = 'school.subject'
#     _description = "Subjects"

#     name = fields.Char(string="Subject Name")
#     code = fields.Char(string="Subject Code")


# class SchoolClass(models.Model):
#     _name = 'school.class'
#     _description = "School Classes"

#     name = fields.Char(string="Class Name")
#     class_teacher = fields.Char(string="Class Teacher")
#     section = fields.Selection([
#         ('a', 'A'),
#         ('b', 'B'),
#         ('c', 'C'),
#         ('d', 'D'),
#     ], string="Section")
#     student_ids = fields.One2many('student.student', 'class_id', string="Students")


# class StudentSubjectLine(models.Model):
#     _name = 'student.subject.line'
#     _description = 'Student Subject Marks'

#     student_id = fields.Many2one('student.student', string="Student", ondelete="cascade")
#     subject_id = fields.Many2one('school.subject', string="Subject", required=True)
#     subject_code = fields.Char(related='subject_id.code', string="Subject Code", store=True)
#     marks = fields.Float(string="Marks", default=0.0)
#     grade = fields.Char(string="Grade", compute='_compute_grade', store=True)

#     @api.depends('marks')
#     def _compute_grade(self):
#         for rec in self:
#             m = rec.marks
#             if m is None:
#                 rec.grade = False
#             elif m >= 90:
#                 rec.grade = "A"
#             elif m >= 75:
#                 rec.grade = "B"
#             elif m >= 60:
#                 rec.grade = "C"
#             elif m >= 40:
#                 rec.grade = "D"
#             else:
#                 rec.grade = "F"

    #all onetomany commands:-  
    
    #(0,0) : -  this is use for creating record :-  
    # def action_add_sub(self):
    #         self.write({'subject_line_ids':[
    #                 (0,0,{
    #                     'subject_id':1,
    #                     'marks':89,

    #                 })
    #         ]})
  